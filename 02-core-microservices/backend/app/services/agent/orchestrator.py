# ==============================================================================
# BỘ ĐIỀU PHỐI ĐA TÁC TỬ (MULTI-AGENT ORCHESTRATOR - STATEGRAPH ENGINE)
# Lõi Khoa học Máy tính: Giải quyết Ràng buộc chéo (Cross-domain CSP) & Anti-Hallucination
# ==============================================================================

import time
from typing import Dict, Any, List
from app.models.schemas import ChatRequest, ChatResponse, ActionDTO, BusSearchCriteria, HotelSearchCriteria
from app.services.tools.travel_tools import search_bus_trips_tool, search_hotel_rooms_tool, check_cross_domain_constraints
from app.services.tools.data_cleaner_pipeline import ConversationDataCleaner

class TravelMultiAgentOrchestrator:
    """
    Tác tử điều phối trung tâm.
    Phân rã ý định ➔ Gọi Bus Agent ➔ Gọi Hotel Agent ➔ Đối khớp Ràng buộc chéo ➔ Trả lời thần tốc.
    """

    @classmethod
    async def process_chat(cls, request: ChatRequest) -> ChatResponse:
        start_time = time.time()
        msg_clean = ConversationDataCleaner.anonymize_pii(request.message)

        # 1. Nhận diện Ý định (Intent Recognition)
        msg_lower = msg_clean.lower()
        has_bus = any(k in msg_lower for k in ["xe", "vé", "limousine", "giường nằm"])
        has_hotel = any(k in msg_lower for k in ["khách sạn", "homestay", "phòng", "ở", "nghỉ"])

        dest = "Đà Lạt"
        if "nha trang" in msg_lower:
            dest = "Nha Trang"

        bus_results: List[Dict[str, Any]] = []
        hotel_results: List[Dict[str, Any]] = []
        cross_check = None
        actions = []

        # 2. Điều phối tác tử Bus Agent
        if has_bus:
            bus_pref = "Phòng Đôi" if ("phòng đôi" in msg_lower or "cabin" in msg_lower) else None
            criteria = BusSearchCriteria(destination=dest, preferred_type=bus_pref)
            bus_results = search_bus_trips_tool(criteria)

        # 3. Điều phối tác tử Hotel Agent
        if has_hotel:
            pet_req = any(k in msg_lower for k in ["thú cưng", "chó", "mèo", "pet"])
            criteria = HotelSearchCriteria(destination="Đà Lạt" if "đà lạt" in msg_lower else dest, pet_friendly_required=pet_req)
            hotel_results = search_hotel_rooms_tool(criteria)

        # 4. Giải quyết Ràng buộc chéo (Cross-domain Constraint Reasoning)
        if bus_results and hotel_results:
            cross_check = check_cross_domain_constraints(bus_results[0], hotel_results[0])

        # 5. Sinh phản hồi tự nhiên, chuẩn xác, không ảo giác
        reply_lines = []
        if bus_results:
            b = bus_results[0]
            reply_lines.append(f"🚌 **Phương tiện:** Nhà xe {b['operator_name']} ({b['bus_type']}) khởi hành {b['departure_time']}, đến nơi lúc {b['arrival_time']}. Còn đúng {b['available_seats']} chỗ (Giá: {b['fare_vnd']:,}đ/vé). Điểm đón: {b['pickup_point']}.")

        if hotel_results:
            h = hotel_results[0]
            reply_lines.append(f"🏨 **Lưu trú:** {h['hotel_name']} ({h['location']}) - Hạng {h['room_type']}. Còn {h['available_rooms']} phòng (Giá: {h['price_per_night']:,}đ/đêm). Chính sách: {h['policy']}")

        if cross_check and cross_check.is_time_conflict:
            reply_lines.append(f"\n⚠️ **Lưu ý lịch trình:** {cross_check.recommendation}")

        if not reply_lines:
            reply_lines.append("Dạ em có thể hỗ trợ anh/chị tra cứu lịch trình xe Limousine và phòng khách sạn tại Đà Lạt, Nha Trang theo thời gian thực ạ. Anh/chị dự định đi vào ngày nào ạ?")

        reply_lines.append("\n👉 *Để đảm bảo quyền lợi, anh/chị có thể liên hệ trực tiếp tổng đài nhà xe hoặc lễ tân khách sạn để xác nhận chỗ nhé!*")
        actions.append(ActionDTO(type="REDIRECT_OPERATOR", payload={"destination": dest}))

        elapsed_ms = int((time.time() - start_time) * 1000)
        return ChatResponse(
            session_id=request.session_id,
            reply="\n\n".join(reply_lines),
            intent_detected="COMBO_INQUIRY" if (has_bus and has_hotel) else "SINGLE_INQUIRY",
            actions=actions,
            latency_ms=elapsed_ms
        )
