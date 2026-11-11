# ==============================================================================
# HỢP ĐỒNG DỮ LIỆU CHUẨN PYDANTIC V2 CHO TOÀN BỘ HỆ THỐNG (DATA CONTRACTS)
# Đảm bảo Type-safety, chống ảo giác 100% bằng cơ chế Function Calling Pydantic.
# Toàn bộ các class gốc (ChatRequest, ActionDTO, ChatResponse, BusSearchCriteria,
# HotelSearchCriteria, CrossDomainMatchResult) bảo toàn 100% tương thích ngược.
# ==============================================================================

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


# 1. KHUÔN TIN NHẮN TỔNG QUÁT TỪ FRONTEND / WEBHOOK ĐA KÊNH (IMMUTABLE CONTRACT)
class ChatRequest(BaseModel):
    session_id: str = Field(..., description="ID phiên làm việc duy nhất để theo vết StateGraph")
    message: str = Field(..., description="Tin nhắn của người dùng gửi từ Web/Zalo/FB")
    channel: str = Field("webchat", description="Kênh gửi tin nhắn: webchat, zalo, facebook")
    inbox_id: Optional[int] = Field(None, description="ID định danh doanh nghiệp Multi-tenant (nếu có)")


class ActionDTO(BaseModel):
    type: str = Field(
        ...,
        description="Loại hành động: REDIRECT_OPERATOR, SHOW_CARD, WARNING, CHATOPS_ALERT, HUMAN_HANDOVER, GUARDRAIL_BLOCK",
    )
    payload: Dict[str, Any] = Field(default_factory=dict, description="Dữ liệu chi tiết đính kèm hành động")


class ChatResponse(BaseModel):
    session_id: str
    reply: str = Field(..., description="Câu trả lời tự nhiên của AI sau khi đã đối khớp và lọc rác")
    intent_detected: Optional[str] = Field("CONSULTATION", description="Ý định phát hiện được")
    actions: List[ActionDTO] = Field(default_factory=list, description="Danh sách hành động gợi ý")
    latency_ms: Optional[int] = Field(0, description="Độ trễ xử lý phản hồi (mili-giây)")
    trace_id: Optional[str] = Field(None, description="Mã truy vết phân tán SRE (X-Trace-ID)")
    state_trace: Optional[List[str]] = Field(None, description="Chuỗi các Node trong StateGraph đã đi qua")
    execution_path: Optional[List[str]] = Field(None, description="Alias tương thích chuỗi Node thực thi")


# 2. KHUÔN CÔNG CỤ TRUY VẤN VÉ XE (FUNCTION CALLING TOOL SCHEMA)
class BusSearchCriteria(BaseModel):
    origin: str = Field("Sài Gòn", description="Điểm đi (Mặc định: Sài Gòn)")
    destination: str = Field(..., description="Điểm đến (Đà Lạt, Nha Trang, Vũng Tàu)")
    travel_date: Optional[str] = Field(None, description="Ngày khởi hành dạng YYYY-MM-DD")
    preferred_type: Optional[str] = Field(None, description="Ưu tiên loại xe: Limousine, Giường nằm, Phòng đôi")
    passengers: int = Field(1, ge=1, le=50, description="Số lượng vé cần tìm")


# 3. KHUÔN CÔNG CỤ TRUY VẤN PHÒNG KHÁCH SẠN (FUNCTION CALLING TOOL SCHEMA)
class HotelSearchCriteria(BaseModel):
    destination: str = Field(..., description="Thành phố hoặc khu vực muốn thuê phòng")
    room_type_preference: Optional[str] = Field(None, description="Hạng phòng ưu tiên (Deluxe, Standard, Bungalow)")
    max_price: Optional[int] = Field(None, description="Mức giá tối đa mỗi đêm (VND)")
    pet_friendly_required: bool = Field(False, description="Có yêu cầu cho phép mang thú cưng không")
    room_code: Optional[str] = Field(None, description="Mã hạng phòng chính xác (VD: DLX-OV-01)")
    rooms_needed: int = Field(1, ge=1, le=20, description="Số lượng phòng cần đặt")


# 4. KHUÔN KẾT QUẢ ĐỐI KHỚP RÀNG BUỘC CHÉO (CROSS-DOMAIN CSP MATCH RESULT)
class CrossDomainMatchResult(BaseModel):
    bus_operator: str
    bus_arrival_time: str
    hotel_name: str
    hotel_checkin_time: str
    time_gap_hours: float
    is_time_conflict: bool = Field(False, description="True nếu xe đến trước giờ check-in quá 3 tiếng")
    recommendation: Optional[str] = Field(None, description="Khuyến nghị: Nhận phòng sớm hoặc gửi đồ miễn phí")


# 5. KHUÔN TÌM KIẾM LAI CHÍNH SÁCH (HYBRID SEARCH: BM25 + DENSE + RRF k=60)
class PolicySearchRequest(BaseModel):
    query: str = Field(..., min_length=2, description="Câu truy vấn chính sách lưu trú / nhà xe / mã phòng")
    destination: Optional[str] = Field(None, description="Lọc theo điểm đến nếu có")
    top_k: int = Field(3, ge=1, le=10, description="Số lượng tài liệu trả về sau khi gộp hạng RRF")
    mode: Literal["hybrid_rrf", "bm25_only", "dense_only", "linear_fusion"] = Field(
        "hybrid_rrf", description="Chế độ truy xuất phục vụ vận hành và kiểm thử đối chứng Ablation"
    )


class PolicyDocumentHit(BaseModel):
    doc_id: str
    title: str
    entity_name: str = ""
    destination: str = ""
    category: str
    room_or_trip_code: str
    entity_code: Optional[str] = None
    content: str
    bm25_score: float = 0.0
    dense_score: float = 0.0
    bm25_rank: Optional[int] = None
    dense_rank: Optional[int] = None
    rrf_score: float = 0.0


class PolicySearchResponse(BaseModel):
    query: str
    mode: str
    rrf_k: int = 60
    results: List[PolicyDocumentHit]


# 6. KHUÔN GIAO DỊCH GIỮ CHỖ TẠM THỜI KHÓA BI QUAN ACID (15-MINUTE TTL HOLD)
class ReservationHoldRequest(BaseModel):
    session_id: str = Field(..., description="Phiên hội thoại yêu cầu giữ chỗ")
    trip_id: Optional[str] = Field(None, description="Mã chuyến xe cần giữ ghế")
    room_id: Optional[str] = Field(None, description="Mã phòng khách sạn cần giữ")
    seats_requested: int = Field(0, ge=0, le=50, description="Số ghế xe khách yêu cầu giữ")
    rooms_requested: int = Field(0, ge=0, le=20, description="Số phòng lưu trú yêu cầu giữ")
    customer_contact: Optional[str] = Field(None, description="Thông tin liên hệ thô (sẽ được lọc PII khi ghi log)")
    customer_contact_note: Optional[str] = Field(None, description="Alias ghi chú liên hệ tương thích")


class ReservationHoldResult(BaseModel):
    success: bool
    reservation_id: Optional[str] = None
    status: Literal["HOLD", "REJECTED_OUT_OF_STOCK", "OUT_OF_STOCK", "INVALID_REQUEST"]
    message: str
    expires_at: Optional[str] = None
    remaining_seats: Optional[int] = None
    remaining_rooms: Optional[int] = None
    ttl_seconds: int = 900
    chatops_alert_dispatched: bool = False
    sql_transaction_log: Optional[str] = None


# Alias tương thích tên kiểu
ReservationHoldResponse = ReservationHoldResult


# 7. KHUÔN THÔNG BÁO CHATOPS & CHUYỂN QUYỀN ĐIỀU KHIỂN (HUMAN TAKEOVER)
class ChatOpsNotificationPayload(BaseModel):
    alert_id: str
    session_id: str
    channel: str
    masked_customer_info: str
    itinerary_summary: str
    accommodation_summary: str
    hold_status: str
    quick_actions: List[str]
    formatted_message: str


class HumanTakeoverRequest(BaseModel):
    session_id: str = Field(..., description="ID phiên hội thoại chủ doanh nghiệp muốn tiếp quản")
    active: bool = Field(True, description="True để tạm dừng AI 30 phút, False để trao lại quyền cho AI")
    operator_name: str = Field("Chủ cơ sở / Lễ tân", description="Tên người tiếp quản")
    duration_minutes: int = Field(30, ge=1, le=240, description="Thời gian tạm ngắt AI tự động")


# 8. KHUÔN HỢP ĐỒNG WEBHOOK BẤT BIẾN CHATWOOT (03-shared-contracts/webhook-schemas.json)
class WebhookSenderDTO(BaseModel):
    id: str
    name: str
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None


class ChatwootIncomingWebhook(BaseModel):
    event: Literal["message_created", "conversation_status_changed"]
    inbox_id: int
    conversation_id: int
    message_type: Literal["incoming", "outgoing"] = "incoming"
    content: str
    sender: WebhookSenderDTO
    timestamp: Optional[str] = None


class ChatwootOutgoingReply(BaseModel):
    content: str
    message_type: str = "outgoing"
    private: bool = False
    content_type: Literal["text", "input_select", "cards", "form_link"] = "text"
    content_attributes: Dict[str, Any] = Field(default_factory=dict)
