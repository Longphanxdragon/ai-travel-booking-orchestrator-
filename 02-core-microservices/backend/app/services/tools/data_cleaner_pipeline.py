import re
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class CleanedTravelIntent(BaseModel):
    """Khuôn dữ liệu tinh khiết bóc tách từ hội thoại người dùng."""
    session_id: str
    origin: Optional[str] = Field(None, description="Điểm đi đã chuẩn hóa")
    destination: Optional[str] = Field(None, description="Điểm đến đã chuẩn hóa")
    departure_date: Optional[str] = Field(None, description="Ngày khởi hành YYYY-MM-DD")
    preferred_bus_type: Optional[str] = Field(None, description="Loại xe: Limousine, Giường nằm, Ghế ngồi")
    group_size: int = Field(1, description="Số lượng khách")
    special_requirements: list[str] = Field(default_factory=list, description="Yêu cầu riêng: say xe, thú cưng, trung chuyển")
    sentiment: str = Field("NEUTRAL", description="Cảm xúc: POSITIVE, NEUTRAL, NEGATIVE")
    cleaned_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class ConversationDataCleaner:
    """
    Bộ lọc rác & Bóc tách dữ liệu độc quyền.
    Chạy ngầm (Background Task) để không ảnh hưởng đến tốc độ phản hồi trên Zalo/Facebook.
    """
    
    @staticmethod
    def anonymize_pii(text: str) -> str:
        """Che số điện thoại và email của khách hàng để bảo mật."""
        # Che số điện thoại Việt Nam (10 số)
        text = re.sub(r'(0\d{2,3})\d{4}(\d{3})', r'\1****\2', text)
        # Che email
        text = re.sub(r'[\w\.-]+@[\w\.-]+', r'[PROTECTED_EMAIL]', text)
        return text

    @staticmethod
    def extract_intent(session_id: str, raw_messages: list[Dict[str, str]]) -> Optional[CleanedTravelIntent]:
        """Lọc bỏ tin nhắn rác (alo, hi, icon) và gom cụm tri thức giá trị."""
        combined_text = " ".join([m.get("content", "") for m in raw_messages if len(m.get("content", "").strip()) > 3])
        if not combined_text:
            return None

        # Trích xuất sơ bộ các thực thể cốt lõi (Sau này dùng LLM Function Calling để bóc sâu)
        dest = None
        if any(k in combined_text.lower() for k in ["đà lạt", "da lat", "dalat"]):
            dest = "Đà Lạt"
        elif any(k in combined_text.lower() for k in ["nha trang", "nhatrang"]):
            dest = "Nha Trang"

        bus_type = "Xe giường nằm phổ thông"
        if "limousine" in combined_text.lower() or "phòng đôi" in combined_text.lower() or "cabin" in combined_text.lower():
            bus_type = "Limousine VIP"

        specs = []
        if "say xe" in combined_text.lower() or "ghế đầu" in combined_text.lower():
            specs.append("Khách dễ say xe - Ưu tiên ghế trước")
        if "thú cưng" in combined_text.lower() or "chó" in combined_text.lower() or "mèo" in combined_text.lower():
            specs.append("Có mang theo thú cưng")

        return CleanedTravelIntent(
            session_id=session_id,
            origin="Sài Gòn",
            destination=dest,
            preferred_bus_type=bus_type,
            special_requirements=specs
        )
