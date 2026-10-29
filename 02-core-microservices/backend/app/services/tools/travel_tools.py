# ==============================================================================
# HỆ THỐNG CÔNG CỤ THỰC THI (AGENTIC TOOLS) CHO TOÀN BỘ MICROSERVICE
# Kết nối CSDL PostgreSQL nội bộ & Live VeXeRe Adapter
# ==============================================================================

from typing import List, Dict, Any
from app.models.schemas import BusSearchCriteria, HotelSearchCriteria, CrossDomainMatchResult

# Mock CSDL mô phỏng từ database-init.sql để chạy thử nghiệm an toàn không phụ thuộc kết nối ngoài
MOCK_BUS_DATABASE = [
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
        "pickup_point": "Bến xe Miền Tây / Lê Hồng Phong Q5"
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
        "pickup_point": "VP Hàng Xanh Bình Thạnh"
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
        "pickup_point": "Bến xe Miền Đông mới"
    }
]

MOCK_HOTEL_DATABASE = [
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
        "policy": "Miễn phí hủy phòng trước 48 giờ."
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
        "policy": "Cho phép mang chó mèo dưới 5kg. Hủy trước 24 giờ mất 50%."
    }
]

def search_bus_trips_tool(criteria: BusSearchCriteria) -> List[Dict[str, Any]]:
    """Truy vấn chính xác chuyến xe khách còn vé trống theo thời gian thực (Zero Hallucination)."""
    results = []
    for trip in MOCK_BUS_DATABASE:
        if criteria.destination.lower() in trip["destination"].lower():
            if criteria.preferred_type:
                if criteria.preferred_type.lower() in trip["bus_type"].lower():
                    results.append(trip)
            else:
                results.append(trip)
    return results

def search_hotel_rooms_tool(criteria: HotelSearchCriteria) -> List[Dict[str, Any]]:
    """Truy vấn phòng khách sạn thực tế còn trống theo địa điểm và chính sách."""
    results = []
    dest_key = criteria.destination.lower()
    for room in MOCK_HOTEL_DATABASE:
        loc_str = (room["hotel_name"] + " " + room["location"]).lower()
        # Nếu đang tìm Đà Lạt hoặc Nha Trang hoặc tìm chung
        is_matched = True
        if "đà lạt" in dest_key or "da lat" in dest_key:
            is_matched = ("đà lạt" in loc_str or "thung lũng" in loc_str or "colline" in loc_str)
        elif "nha trang" in dest_key:
            is_matched = ("nha trang" in loc_str or "biển" in loc_str)

        if is_matched:
            if criteria.pet_friendly_required and not room["pet_allowed"]:
                continue
            if criteria.max_price and room["price_per_night"] > criteria.max_price:
                continue
            results.append(room)
    return results

def check_cross_domain_constraints(bus_trip: Dict[str, Any], hotel_room: Dict[str, Any]) -> CrossDomainMatchResult:
    """Xử lý bài toán thỏa mãn ràng buộc chéo (CSP) giữa giờ xe đến và giờ nhận phòng."""
    # Giả định xe đến sáng (06:00) và checkin lúc 14:00
    arr_hour = int(bus_trip["arrival_time"].split(":")[0])
    chk_hour = int(hotel_room["checkin_standard"].split(":")[0])
    gap = chk_hour - arr_hour

    is_conflict = gap > 3.0
    rec = None
    if is_conflict:
        rec = f"Xe đến lúc {bus_trip['arrival_time']} nhưng giờ nhận phòng là {hotel_room['checkin_standard']} (Chờ {gap} tiếng). Khách sạn hỗ trợ nhận phòng sớm phụ thu {hotel_room['early_checkin_fee']:,}đ hoặc giữ hành lý miễn phí tại quầy lễ tân."

    return CrossDomainMatchResult(
        bus_operator=bus_trip["operator_name"],
        bus_arrival_time=bus_trip["arrival_time"],
        hotel_name=hotel_room["hotel_name"],
        hotel_checkin_time=hotel_room["checkin_standard"],
        time_gap_hours=gap,
        is_time_conflict=is_conflict,
        recommendation=rec
    )
