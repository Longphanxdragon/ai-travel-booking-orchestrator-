# ==============================================================================
# DỊCH VỤ ĐIỀU PHỐI THÔNG BÁO CHATOPS & HUMAN TAKEOVER (UC-06 SPECIFICATION)
# Chuyển giao khách đặt chỗ tức thời về Telegram/Zalo chủ doanh nghiệp mà không
# cần mở Web Dashboard cồng kềnh; tuân thủ nghiêm ngặt bảo mật PII khi ghi log.
# ==============================================================================

import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
import httpx

from app.models.schemas import ChatOpsNotificationPayload, HumanTakeoverRequest
from app.services.tools.data_cleaner_pipeline import ConversationDataCleaner


class HumanTakeoverRegistry:
    """
    Quản lý trạng thái Chuyển quyền Điều khiển (Handover Protocol).
    Khi chủ nhà xe / homestay bấm '[Vào chat trực tiếp]', AI tạm dừng trả lời tự động
    trên session_id đó trong 30 phút để người thật tư vấn chốt cọc.
    """

    _active_sessions: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def activate_takeover(cls, req: HumanTakeoverRequest) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        if not req.active:
            cls._active_sessions.pop(req.session_id, None)
            return {
                "session_id": req.session_id,
                "takeover_active": False,
                "message": "Đã trao lại quyền tư vấn tự động 24/7 cho AI Orchestrator.",
            }

        expires_at = now + timedelta(minutes=req.duration_minutes)
        record = {
            "session_id": req.session_id,
            "operator_name": req.operator_name,
            "expires_at": expires_at,
            "takeover_active": True,
        }
        cls._active_sessions[req.session_id] = record
        return {
            "session_id": req.session_id,
            "takeover_active": True,
            "operator_name": req.operator_name,
            "expires_at": expires_at.isoformat(),
            "message": f"AI đã tạm ngắt tự động {req.duration_minutes} phút để {req.operator_name} chat trực tiếp.",
        }

    @classmethod
    def is_human_active(cls, session_id: str) -> bool:
        record = cls._active_sessions.get(session_id)
        if not record:
            return False
        if datetime.now(timezone.utc) >= record["expires_at"]:
            cls._active_sessions.pop(session_id, None)
            return False
        return True

    @classmethod
    def clear_all(cls) -> None:
        cls._active_sessions.clear()


class ChatOpsNotifier:
    """
    Định dạng và gửi thông báo đơn giữ chỗ / yêu cầu tư vấn sâu về Telegram / Zalo
    của chủ cơ sở lưu trú hoặc điều hành nhà xe theo chuẩn Chat-to-Chat (ChatOps).
    """

    # Hàng đợi lưu vết phục vụ kiểm toán & Unit Test không cần mạng ngoài
    _audit_outbox: List[ChatOpsNotificationPayload] = []

    @classmethod
    def build_lead_alert(
        cls,
        session_id: str,
        channel: str,
        raw_customer_message: str,
        bus_trip: Optional[Dict[str, Any]] = None,
        hotel_room: Optional[Dict[str, Any]] = None,
        reservation_id: Optional[str] = None,
        ttl_minutes: int = 15,
    ) -> ChatOpsNotificationPayload:
        # BẮT BUỘC ẩn danh hóa PII trước khi lưu trữ vào log kiểm toán hệ thống
        masked_info = ConversationDataCleaner.anonymize_pii(raw_customer_message)

        itinerary_text = "Chưa chọn chuyến xe cụ thể"
        if bus_trip:
            itinerary_text = (
                f"Nhà xe {bus_trip['operator_name']} ({bus_trip['bus_type']}), "
                f"khởi hành {bus_trip['departure_time']} -> đến {bus_trip['arrival_time']} "
                f"(Giá {bus_trip['fare_vnd']:,}đ/vé)"
            )

        hotel_text = "Chưa chọn phòng lưu trú cụ thể"
        if hotel_room:
            hotel_text = (
                f"{hotel_room['hotel_name']} - Hạng {hotel_room['room_type']} "
                f"(Giá {hotel_room['price_per_night']:,}đ/đêm)"
            )

        hold_status = (
            f"Đã khóa giữ chỗ ACID (Mã: {reservation_id}, TTL còn {ttl_minutes}:00 phút)"
            if reservation_id
            else "Khách đang quan tâm lịch trình tiềm năng (Hot Lead)"
        )

        quick_actions = [
            "CALL_CUSTOMER: Bấm gọi khách ngay",
            "CONFIRM_DEPOSIT: Xác nhận giữ chỗ / cọc",
            "HUMAN_TAKEOVER: Vào chat trực tiếp (Tạm ngắt AI 30p)",
        ]

        formatted = (
            f"[ĐƠN TƯ VẤN MỚI TỪ {channel.upper()}]\n"
            f"- Phiên khách hàng: {session_id}\n"
            f"- Yêu cầu (đã bảo mật PII): {masked_info}\n"
            f"- Lịch trình xe: {itinerary_text}\n"
            f"- Lưu trú: {hotel_text}\n"
            f"- Trạng thái: {hold_status}\n"
            f"- Thao tác nhanh: [Bấm gọi khách ngay] | [Xác nhận cọc] | [Vào chat trực tiếp]"
        )

        return ChatOpsNotificationPayload(
            alert_id=f"ALERT-{uuid.uuid4().hex[:8].upper()}",
            session_id=session_id,
            channel=channel,
            masked_customer_info=masked_info,
            itinerary_summary=itinerary_text,
            accommodation_summary=hotel_text,
            hold_status=hold_status,
            quick_actions=quick_actions,
            formatted_message=formatted,
        )

    @classmethod
    async def dispatch_alert(cls, payload: ChatOpsNotificationPayload) -> bool:
        """
        Bắn bất đồng bộ (Non-blocking Async I/O) sang Telegram/Zalo Webhook nếu được cấu hình,
        đồng thời ghi vào hộp thư kiểm toán nội bộ.
        """
        cls._audit_outbox.append(payload)
        webhook_url = os.getenv("CHATOPS_WEBHOOK_URL")
        if not webhook_url:
            return True

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.post(
                    webhook_url,
                    json={"text": payload.formatted_message, "metadata": payload.model_dump()},
                )
                return resp.status_code < 400
        except Exception:
            return False

    @classmethod
    def get_outbox(cls) -> List[ChatOpsNotificationPayload]:
        return list(cls._audit_outbox)

    @classmethod
    def clear_outbox(cls) -> None:
        cls._audit_outbox.clear()
