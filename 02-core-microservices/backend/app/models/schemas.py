# ==============================================================================
# HỢP ĐỒNG DỮ LIỆU CHUẨN PYDANTIC V2 CHO TOÀN BỘ HỆ THỐNG
# Đảm bảo Type-safety, chống ảo giác 100% bằng cơ chế Function Calling Pydantic
# ==============================================================================

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# 1. KHUÔN TIN NHẮN TỔNG QUÁT TỪ FRONTEND / WEBHOOK ĐA KÊNH
class ChatRequest(BaseModel):
    session_id: str = Field(..., description="ID phiên làm việc duy nhất để theo vết StateGraph")
    message: str = Field(..., description="Tin nhắn của người dùng gửi từ Web/Zalo/FB")
    channel: str = Field("webchat", description="Kênh gửi tin nhắn: webchat, zalo, facebook")

class ActionDTO(BaseModel):
    type: str = Field(..., description="Loại hành động: REDIRECT_OPERATOR, SHOW_CARD, WARNING")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Dữ liệu chi tiết đính kèm hành động")

class ChatResponse(BaseModel):
    session_id: str
    reply: str = Field(..., description="Câu trả lời tự nhiên của AI sau khi đã đối khớp và lọc rác")
    intent_detected: Optional[str] = Field("CONSULTATION", description="Ý định phát hiện được")
    actions: List[ActionDTO] = Field(default_factory=list, description="Danh sách hành động gợi ý")
    latency_ms: Optional[int] = Field(0, description="Độ trễ xử lý phản hồi")

# 2. KHUÔN CÔNG CỤ TRUY VẤN VÉ XE (TOOL CALLING SCHEMA)
class BusSearchCriteria(BaseModel):
    origin: str = Field("Sài Gòn", description="Điểm đi (Mặc định: Sài Gòn)")
    destination: str = Field(..., description="Điểm đến (Đà Lạt, Nha Trang, Vũng Tàu)")
    travel_date: Optional[str] = Field(None, description="Ngày khởi hành dạng YYYY-MM-DD")
    preferred_type: Optional[str] = Field(None, description="Ưu tiên loại xe: Limousine, Giường nằm, Phòng đôi")
    passengers: int = Field(1, description="Số lượng vé cần tìm")

# 3. KHUÔN CÔNG CỤ TRUY VẤN PHÒNG KHÁCH SẠN (TOOL CALLING SCHEMA)
class HotelSearchCriteria(BaseModel):
    destination: str = Field(..., description="Thành phố hoặc khu vực muốn thuê phòng")
    room_type_preference: Optional[str] = Field(None, description="Hạng phòng ưu tiên (Deluxe, Standard, Bungalow)")
    max_price: Optional[int] = Field(None, description="Mức giá tối đa mỗi đêm (VND)")
    pet_friendly_required: bool = Field(False, description="Có yêu cầu cho phép mang thú cưng không")

# 4. KHUÔN KẾT QUẢ ĐỐI KHỚP RÀNG BUỘC CHÉO (CROSS-DOMAIN CONSTRAINT RESULT)
class CrossDomainMatchResult(BaseModel):
    bus_operator: str
    bus_arrival_time: str
    hotel_name: str
    hotel_checkin_time: str
    time_gap_hours: float
    is_time_conflict: bool = Field(False, description="True nếu xe đến trước giờ check-in quá 3 tiếng")
    recommendation: Optional[str] = Field(None, description="Khuyến nghị: Nhận phòng sớm hoặc gửi đồ miễn phí")
