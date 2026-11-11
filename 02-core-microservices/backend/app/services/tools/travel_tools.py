# ==============================================================================
# HỆ THỐNG CÔNG CỤ THỰC THI (AGENTIC TOOLS) & GIAO DỊCH KHÓA BI QUAN ACID
# ------------------------------------------------------------------------------
# Dành cho người mới (Beginner Guide):
# Tại sao gọi là "Khóa bi quan" (Pessimistic Locking)?
# - Trong ngành khách sạn và xe khách, nếu 2 khách hàng cùng bấm "Giữ phòng"
#   vào đúng mili-giây thứ 50, mà hệ thống không khóa dòng dữ liệu lại
#   (SELECT ... FOR UPDATE), cả 2 khách sẽ đều tưởng mình đã đặt thành công!
#   Đến ngày đi thì 1 người bị đuổi vì hết phòng (Bán khống - Overbooking).
# - "Khóa bi quan" nghĩa là: Cứ hễ có ai chạm vào phòng đó để kiểm tra/giữ chỗ,
#   hệ thống lập tức "khóa cửa" dòng dữ liệu đó lại, bắt người thứ 2 phải xếp hàng
#   chờ giao dịch của người thứ 1 hoàn tất. Đảm bảo đúng 100% không bao giờ bán trùng!
# ==============================================================================

import asyncio
import copy
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from app.core.config import settings
from app.core.guardrails import chatops_circuit_breaker
from app.core.telemetry import telemetry
from app.models.schemas import (
    BusSearchCriteria,
    CrossDomainMatchResult,
    HotelSearchCriteria,
    ReservationHoldRequest,
    ReservationHoldResponse,
)


# ==============================================================================
# CƠ SỞ DỮ LIỆU TỒN KHO THỜI GIAN THỰC (GROUND-TRUTH SQL DATABASE)
# Khớp 100% DDL trong 03-shared-contracts/database-init.sql
# ==============================================================================
INITIAL_BUS_DATABASE: List[Dict[str, Any]] = [
    {
        "trip_id": "BUS-SG-DL-2230",
        "operator_name": "Phương Trang (FUTA)",
        "origin": "Sài Gòn",
        "destination": "Đà Lạt",
        "bus_type": "Limousine Giường Nằm 34 Chỗ",
        "departure_time": "22:30",
        "arrival_time": "05:30",
        "fare_vnd": 320000,
        "available_seats": 6,
        "pickup_point": "Bến xe Miền Tây / Lê Hồng Phong Q5",
    },
    {
        "trip_id": "BUS-SG-DL-2300",
        "operator_name": "Điền Linh Limousine",
        "origin": "Sài Gòn",
        "destination": "Đà Lạt",
        "bus_type": "Limousine 24 Phòng Đôi",
        "departure_time": "23:00",
        "arrival_time": "06:15",
        "fare_vnd": 450000,
        "available_seats": 4,
        "pickup_point": "VP Hàng Xanh Bình Thạnh",
    },
    {
        "trip_id": "BUS-SG-NT-2100",
        "operator_name": "An Anh Limousine",
        "origin": "Sài Gòn",
        "destination": "Nha Trang",
        "bus_type": "Limousine 34 Phòng VIP",
        "departure_time": "21:00",
        "arrival_time": "05:00",
        "fare_vnd": 380000,
        "available_seats": 8,
        "pickup_point": "Bến xe Miền Đông mới",
    },
    {
        "trip_id": "BUS-SG-VT-0800",
        "operator_name": "Hoa Mai Limousine",
        "origin": "Sài Gòn",
        "destination": "Vũng Tàu",
        "bus_type": "Limousine 9 Chỗ VIP",
        "departure_time": "08:00",
        "arrival_time": "10:15",
        "fare_vnd": 190000,
        "available_seats": 5,
        "pickup_point": "44 Nguyễn Thái Bình, Quận 1",
    },
]

INITIAL_HOTEL_DATABASE: List[Dict[str, Any]] = [
    {
        "room_id": "HOTEL-DL-01",
        "hotel_name": "Khách sạn Colline Đà Lạt",
        "location": "Trung tâm (gần Chợ Đà Lạt)",
        "room_type": "Deluxe Double",
        "price_per_night": 950000,
        "available_rooms": 3,
        "checkin_standard": "14:00",
        "early_checkin_fee": 250000,
        "pet_allowed": False,
        "policy": "Miễn phí hủy phòng trước 48 giờ.",
    },
    {
        "room_id": "HOTEL-DL-02",
        "hotel_name": "Homestay Thung Lũng Mây",
        "location": "Cách trung tâm 3km (View thung lũng săn mây)",
        "room_type": "Phòng Đôi Bungalow",
        "price_per_night": 550000,
        "available_rooms": 2,
        "checkin_standard": "14:00",
        "early_checkin_fee": 150000,
        "pet_allowed": True,
        "policy": "Cho phép mang chó mèo dưới 5kg. Hủy trước 24 giờ mất 50%.",
    },
    {
        "room_id": "HOTEL-NT-01",
        "hotel_name": "SeaView Nha Trang Hotel",
        "location": "Đường Trần Phú (Cách biển 50m)",
        "room_type": "Deluxe Ocean View",
        "price_per_night": 750000,
        "available_rooms": 5,
        "checkin_standard": "14:00",
        "early_checkin_fee": 200000,
        "pet_allowed": False,
        "policy": "Miễn phí hủy phòng trước 72 giờ. View ngắm bình minh biển.",
    },
    {
        "room_id": "HOTEL-VT-01",
        "hotel_name": "Malibu Beach Hotel Vũng Tàu",
        "location": "Bãi Sau Vũng Tàu",
        "room_type": "Executive Suite",
        "price_per_night": 1200000,
        "available_rooms": 4,
        "checkin_standard": "14:00",
        "early_checkin_fee": 350000,
        "pet_allowed": False,
        "policy": "Bao gồm buffet sáng 2 người lớn, hủy trước 48h miễn phí.",
    },
]


class InventoryDatabaseEngine:
    """
    Động cơ Quản lý Tồn kho & Giao dịch Khóa Bi quan ACID (Thread-safe Async Mutex).
    Mô phỏng đầy đủ hành vi `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED; ... FOR UPDATE`.
    """

    def __init__(self) -> None:
        self._bus_trips: Dict[str, Dict[str, Any]] = {
            t["trip_id"]: copy.deepcopy(t) for t in INITIAL_BUS_DATABASE
        }
        self._hotel_rooms: Dict[str, Dict[str, Any]] = {
            h["room_id"]: copy.deepcopy(h) for h in INITIAL_HOTEL_DATABASE
        }
        self._reservations: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    def query_bus(self, criteria: BusSearchCriteria) -> List[Dict[str, Any]]:
        """Truy vấn chính xác chuyến xe khách còn vé trống theo thời gian thực (Zero Hallucination)."""
        results = []
        dest_query = criteria.destination.strip().lower()

        for trip in self._bus_trips.values():
            if trip["available_seats"] < criteria.passengers:
                continue

            # Đối khớp điểm đến
            if dest_query in trip["destination"].lower() or trip["destination"].lower() in dest_query:
                # Kiểm tra lọc loại xe (Limousine, Giường nằm, Phòng đôi)
                if criteria.preferred_type:
                    pref = criteria.preferred_type.lower()
                    if pref not in trip["bus_type"].lower():
                        continue
                results.append(copy.deepcopy(trip))

        # Sắp xếp ưu tiên: Còn nhiều ghế hơn và giá tốt hơn
        results.sort(key=lambda x: (x["fare_vnd"], -x["available_seats"]))
        return results

    def query_hotels(self, criteria: HotelSearchCriteria) -> List[Dict[str, Any]]:
        """Truy vấn phòng khách sạn thực tế còn trống theo địa điểm, giá và chính sách thú cưng."""
        results = []
        dest_query = criteria.destination.strip().lower()

        for room in self._hotel_rooms.values():
            if room["available_rooms"] < criteria.rooms_needed:
                continue

            loc_full = f"{room['hotel_name']} {room['location']}".lower()
            matched = False

            if "đà lạt" in dest_query or "da lat" in dest_query:
                matched = any(k in loc_full for k in ["đà lạt", "chợ đà lạt", "thung lũng", "colline"])
            elif "nha trang" in dest_query or "nhatrang" in dest_query:
                matched = any(k in loc_full for k in ["nha trang", "trần phú", "biển", "seaview"])
            elif "vũng tàu" in dest_query or "vung tau" in dest_query:
                matched = any(k in loc_full for k in ["vũng tàu", "bãi sau", "malibu"])
            else:
                matched = dest_query in loc_full

            if not matched:
                continue

            # Lọc chính sách thú cưng
            if criteria.pet_friendly_required and not room["pet_allowed"]:
                continue

            # Lọc ngân sách tối đa
            if criteria.max_price and room["price_per_night"] > criteria.max_price:
                continue

            # Lọc loại phòng ưu tiên
            if criteria.room_type_preference:
                pref = criteria.room_type_preference.lower()
                if pref not in room["room_type"].lower():
                    continue

            results.append(copy.deepcopy(room))

        results.sort(key=lambda x: x["price_per_night"])
        return results

    async def execute_pessimistic_hold(
        self, request: ReservationHoldRequest
    ) -> ReservationHoldResponse:
        """
        Thực thi giao dịch Khóa Bi quan (Pessimistic Hold Transaction) nguyên tử (Atomic).
        Bảo đảm tính chất ACID:
        - Atomic: Giữ cả xe và phòng cùng lúc, nếu 1 trong 2 hết thì Rollback cả 2.
        - Consistent: Không bao giờ tồn tại ghế âm (available_seats < 0).
        - Isolated: Sử dụng Mutex Lock khóa tài nguyên trong suốt giao dịch.
        - Durable: Sinh mã UUID và thời hạn TTL 15 phút lưu vào bảng reservations.
        """
        async with self._lock:
            # 1. Kiểm tra tồn kho xe
            bus_target = self._bus_trips.get(request.trip_id) if request.trip_id else None
            if request.trip_id and not bus_target:
                return ReservationHoldResponse(
                    success=False,
                    status="INVALID_REQUEST",
                    message=f"Không tìm thấy mã chuyến xe '{request.trip_id}' trong hệ thống.",
                )

            # 2. Kiểm tra tồn kho phòng
            hotel_target = self._hotel_rooms.get(request.room_id) if request.room_id else None
            if request.room_id and not hotel_target:
                return ReservationHoldResponse(
                    success=False,
                    status="INVALID_REQUEST",
                    message=f"Không tìm thấy mã phòng khách sạn '{request.room_id}' trong hệ thống.",
                )

            # 3. Kiểm tra điều kiện tồn kho thực tế (SELECT ... FOR UPDATE)
            if bus_target and bus_target["available_seats"] < request.seats_requested:
                telemetry.increment("acid_holds_rejected")
                return ReservationHoldResponse(
                    success=False,
                    status="OUT_OF_STOCK",
                    message=(
                        f"Chuyến xe {bus_target['operator_name']} chỉ còn {bus_target['available_seats']} chỗ trống, "
                        f"không đủ {request.seats_requested} chỗ quý khách yêu cầu."
                    ),
                    remaining_seats=bus_target["available_seats"],
                )

            if hotel_target and hotel_target["available_rooms"] < request.rooms_requested:
                telemetry.increment("acid_holds_rejected")
                return ReservationHoldResponse(
                    success=False,
                    status="OUT_OF_STOCK",
                    message=(
                        f"Khách sạn {hotel_target['hotel_name']} chỉ còn {hotel_target['available_rooms']} phòng trống, "
                        f"không đủ {request.rooms_requested} phòng quý khách yêu cầu."
                    ),
                    remaining_rooms=hotel_target["available_rooms"],
                )

            # 4. CẬP NHẬT TRỪ TỒN KHO NGUYÊN TỬ (COMMIT TRANSACTION)
            if bus_target and request.seats_requested > 0:
                bus_target["available_seats"] -= request.seats_requested

            if hotel_target and request.rooms_requested > 0:
                hotel_target["available_rooms"] -= request.rooms_requested

            # 5. Tạo bản ghi giữ chỗ tạm thời (TTL 15 phút)
            res_id = f"RES-{uuid.uuid4().hex[:8].upper()}"
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.reservation_hold_ttl_minutes)

            self._reservations[res_id] = {
                "reservation_id": res_id,
                "session_id": request.session_id,
                "trip_id": request.trip_id,
                "room_id": request.room_id,
                "seats_held": request.seats_requested,
                "rooms_held": request.rooms_requested,
                "status": "HOLD",
                "expires_at": expires_at.isoformat(),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "customer_note": request.customer_contact_note,
            }

            telemetry.increment("acid_holds_succeeded")

            # 6. Gửi cảnh báo ChatOps về Telegram chủ doanh nghiệp (bảo vệ bằng Circuit Breaker)
            chatops_sent = False
            if chatops_circuit_breaker.can_execute():
                try:
                    chatops_sent = await self._dispatch_chatops_alert(self._reservations[res_id])
                    chatops_circuit_breaker.record_success()
                except Exception:
                    chatops_circuit_breaker.record_failure()

            return ReservationHoldResponse(
                success=True,
                reservation_id=res_id,
                status="HOLD",
                message=(
                    f"Giữ chỗ thành công! Mã giữ chỗ: {res_id}. "
                    f"Hệ thống đã khóa chỗ tạm thời trong {settings.reservation_hold_ttl_minutes} phút. "
                    "Chủ nhà xe/khách sạn đã nhận được thông tin để liên hệ xác nhận với quý khách."
                ),
                expires_at=expires_at.isoformat(),
                remaining_seats=bus_target["available_seats"] if bus_target else None,
                remaining_rooms=hotel_target["available_rooms"] if hotel_target else None,
                chatops_alert_dispatched=chatops_sent,
            )

    async def _dispatch_chatops_alert(self, res_data: Dict[str, Any]) -> bool:
        """Mô phỏng phát thông báo ChatOps tức thì về điện thoại Telegram của Chủ nhà xe / Khách sạn."""
        telemetry.increment("chatops_alerts_sent")
        # Giả lập I/O mạng 10ms
        await asyncio.sleep(0.01)
        return True

    def reset(self) -> None:
        """Khôi phục dữ liệu gốc phục vụ chạy Unit Test."""
        self._bus_trips = {t["trip_id"]: copy.deepcopy(t) for t in INITIAL_BUS_DATABASE}
        self._hotel_rooms = {h["room_id"]: copy.deepcopy(h) for h in INITIAL_HOTEL_DATABASE}
        self._reservations.clear()


# Khởi tạo Singleton Database Engine
db_engine = InventoryDatabaseEngine()


# ==============================================================================
# HÀM CÔNG CỤ (TOOL FUNCTIONS) CẮM VÀO LANGGRAPH / FUNCTION CALLING
# ==============================================================================
def search_bus_trips_tool(criteria: BusSearchCriteria) -> List[Dict[str, Any]]:
    """Công cụ truy vấn danh sách chuyến xe khách thực tế từ CSDL."""
    return db_engine.query_bus(criteria)


def search_hotel_rooms_tool(criteria: HotelSearchCriteria) -> List[Dict[str, Any]]:
    """Công cụ truy vấn danh sách phòng khách sạn thực tế từ CSDL."""
    return db_engine.query_hotels(criteria)


def check_cross_domain_constraints(
    bus_trip: Dict[str, Any], hotel_room: Dict[str, Any]
) -> CrossDomainMatchResult:
    """
    Module Giải Quyết Bài Toán Thỏa Mãn Ràng Buộc Chéo (Cross-domain CSP Solver).
    Tính toán độ lệch thời gian Delta T giữa giờ xe đến (T_arr) và giờ check-in khách sạn (T_checkin):
    - Nếu Delta T > 3.0 giờ -> Kích hoạt xung đột (is_time_conflict = True), tự động đưa ra
      phương án giải quyết: Phụ thu nhận phòng sớm (Early Check-in) hoặc Gửi hành lý miễn phí.
    """
    telemetry.increment("csp_conflicts_detected")

    arr_str = bus_trip.get("arrival_time", "06:00")
    chk_str = hotel_room.get("checkin_standard", "14:00")

    arr_hour = int(arr_str.split(":")[0])
    chk_hour = int(chk_str.split(":")[0])

    # Giả định xe chạy đêm đến sáng hôm sau (ví dụ đi 22:30 đến 05:30)
    gap = chk_hour - arr_hour
    if gap < 0:
        gap += 24

    is_conflict = gap > settings.csp_time_conflict_threshold_hours
    recommendation: Optional[str] = None

    if is_conflict:
        fee_vnd = hotel_room.get("early_checkin_fee", 200000)
        recommendation = (
            f"Xe {bus_trip.get('operator_name')} cập bến lúc {arr_str} sáng, nhưng giờ nhận phòng tiêu chuẩn "
            f"của {hotel_room.get('hotel_name')} là {chk_str} (Khoảng chờ {gap} tiếng). "
            f"Khách sạn có chính sách hỗ trợ nhận phòng sớm phụ thu {fee_vnd:,}đ "
            "hoặc quý khách có thể gửi hành lý hoàn toàn miễn phí tại quầy lễ tân để đi dạo/ăn sáng trước."
        )

    return CrossDomainMatchResult(
        bus_operator=bus_trip.get("operator_name", ""),
        bus_arrival_time=arr_str,
        hotel_name=hotel_room.get("hotel_name", ""),
        hotel_checkin_time=chk_str,
        time_gap_hours=float(gap),
        is_time_conflict=is_conflict,
        recommendation=recommendation,
    )
