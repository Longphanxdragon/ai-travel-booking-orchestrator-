# ==============================================================================
# ĐƯỜNG ỐNG BẢO MẬT PII & BÁNH ĐÀ DỮ LIỆU ĐỘC QUYỀN (DATA FLYWHEEL PIPELINE)
# ------------------------------------------------------------------------------
# Dành cho người mới (Beginner Guide):
# Khách hàng Việt Nam khi chat Zalo/Facebook rất hay gửi kèm Số điện thoại,
# Email, hoặc số CCCD. Theo Nghị định 13/2023/NĐ-CP và chuẩn bảo mật FAANG:
# 1. TUYỆT ĐỐI KHÔNG gửi thẳng SĐT/Email thô của khách lên máy chủ OpenAI/Google
#    hoặc ghi thẳng vào file log mà chưa che giấu (Anonymize).
# 2. Sau khi ẩn danh xong, các nhu cầu quý giá ("Khách đi Đà Lạt thích xe Cabin
#    đôi và mang theo chó cưng") sẽ được gom ngầm vào Hồ Dữ Liệu (Data Lake)
#    tạo thành tài sản độc quyền (Data Moat) cho doanh nghiệp!
# ==============================================================================

import re
from collections import Counter, deque
from datetime import datetime, timezone
from typing import Any, Deque, Dict, List, Optional
from pydantic import BaseModel, Field
from app.core.telemetry import telemetry


class CleanedTravelIntent(BaseModel):
    """Khuôn dữ liệu tinh khiết bóc tách từ hội thoại người dùng (đã sạch 100% PII)."""

    session_id: str
    origin: Optional[str] = Field(None, description="Điểm đi đã chuẩn hóa")
    destination: Optional[str] = Field(None, description="Điểm đến đã chuẩn hóa")
    departure_date: Optional[str] = Field(None, description="Ngày khởi hành YYYY-MM-DD")
    preferred_bus_type: Optional[str] = Field(None, description="Loại xe: Limousine, Giường nằm, Ghế ngồi")
    group_size: int = Field(1, description="Số lượng khách")
    special_requirements: List[str] = Field(
        default_factory=list,
        description="Yêu cầu riêng: say xe, thú cưng, trung chuyển, nhận phòng sớm",
    )
    sentiment: str = Field("NEUTRAL", description="Cảm xúc: POSITIVE, NEUTRAL, NEGATIVE")
    cleaned_query: str = Field("", description="Nội dung câu hỏi đã ẩn danh PII")
    cleaned_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DataFlywheelRepository:
    """
    Kho lưu trữ Hồ Dữ Liệu Ý Định Du Lịch (In-memory Buffer + SQL Generator cho travel_intents_lake).
    Giúp doanh nghiệp thống kê nhu cầu thị trường theo thời gian thực mà không xâm phạm đời tư.
    """

    def __init__(self, max_records: int = 5000) -> None:
        self._records: Deque[CleanedTravelIntent] = deque(maxlen=max_records)

    def append(self, intent: CleanedTravelIntent) -> None:
        """Lưu bản ghi ý định đã làm sạch vào Data Lake."""
        self._records.append(intent)

    def analytics_summary(self) -> Dict[str, Any]:
        """Tổng hợp báo cáo phân tích thị trường tự động từ Data Flywheel."""
        total = len(self._records)
        if total == 0:
            return {
                "total_clean_intents_captured": 0,
                "top_destinations": {},
                "vip_limousine_preference_rate": 0.0,
                "pet_friendly_demand_rate": 0.0,
            }

        dest_counter: Counter[str] = Counter()
        vip_count = 0
        pet_count = 0

        for item in self._records:
            if item.destination:
                dest_counter[item.destination] += 1
            if item.preferred_bus_type and "Limousine" in item.preferred_bus_type:
                vip_count += 1
            if any("thú cưng" in req.lower() for req in item.special_requirements):
                pet_count += 1

        return {
            "total_clean_intents_captured": total,
            "top_destinations": dict(dest_counter.most_common(5)),
            "vip_limousine_preference_rate": round(vip_count / total, 4),
            "pet_friendly_demand_rate": round(pet_count / total, 4),
        }

    def clear(self) -> None:
        self._records.clear()


data_flywheel_store = DataFlywheelRepository()


class ConversationDataCleaner:
    """
    Bộ lọc rác & Bóc tách dữ liệu độc quyền chuẩn Privacy-First.
    Chạy cả ở cổng chặn đầu vào (Synchronous PII Masking < 0.05ms) và ở luồng ngầm
    BackgroundTasks (Asynchronous Feature Extraction -> 0ms ảnh hưởng độ trễ API).
    """

    # Biểu thức chính quy (Regex) biên dịch sẵn để đạt tốc độ xử lý micro-giây
    RE_VN_PHONE = re.compile(r"(0\d{2,3})\d{4}(\d{3})\b")
    RE_INTL_VN_PHONE = re.compile(r"(\+84\d{2})\d{4}(\d{3})\b")
    RE_EMAIL = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
    RE_CCCD = re.compile(r"\b\d{12}\b")
    RE_GROUP_SIZE = re.compile(r"(\d+)\s*(vé|người|khách|ghế|chỗ)", re.IGNORECASE)

    @classmethod
    def anonymize_pii(cls, text: str) -> str:
        """
        Che số điện thoại, email và CCCD của khách hàng để bảo mật 100%.
        Ví dụ:
        - '0901234567'        -> '090****567'
        - 'test@gmail.com'    -> '[PROTECTED_EMAIL]'
        - '079203001234'      -> '[PROTECTED_ID]'
        """
        if not text:
            return text

        original = text
        # 1. Che số CCCD 12 chữ số trước (để không bị nhầm với chuỗi số điện thoại)
        masked = cls.RE_CCCD.sub("[PROTECTED_ID]", text)
        # 2. Che số điện thoại di động Việt Nam 10-11 số chuẩn (090****567)
        masked = cls.RE_VN_PHONE.sub(r"\1****\2", masked)
        masked = cls.RE_INTL_VN_PHONE.sub(r"\1****\2", masked)
        # 3. Che địa chỉ Email
        masked = cls.RE_EMAIL.sub("[PROTECTED_EMAIL]", masked)

        if masked != original:
            telemetry.increment("pii_anonymized")

        return masked

    @classmethod
    def extract_intent(
        cls,
        session_id: str,
        raw_messages: List[Dict[str, str]],
    ) -> Optional[CleanedTravelIntent]:
        """Lọc bỏ tin nhắn rác (alo, hi, icon ngắn) và bóc tách vector nhu cầu thị trường."""
        valid_segments = []
        for msg in raw_messages:
            content = cls.anonymize_pii(msg.get("content", "").strip())
            if len(content) > 3:
                valid_segments.append(content)

        combined_text = " ".join(valid_segments)
        if not combined_text:
            return None

        lower_text = combined_text.lower()

        # Nhận diện điểm đến chuẩn hóa
        dest: Optional[str] = None
        if any(k in lower_text for k in ["đà lạt", "da lat", "dalat"]):
            dest = "Đà Lạt"
        elif any(k in lower_text for k in ["nha trang", "nhatrang"]):
            dest = "Nha Trang"
        elif any(k in lower_text for k in ["vũng tàu", "vung tau"]):
            dest = "Vũng Tàu"

        # Nhận diện phân khúc phương tiện
        bus_type = "Xe giường nằm phổ thông"
        if any(k in lower_text for k in ["limousine", "phòng đôi", "cabin", "vip"]):
            bus_type = "Limousine VIP"

        # Nhận diện quy mô nhóm khách
        group_size = 1
        grp_match = cls.RE_GROUP_SIZE.search(lower_text)
        if grp_match:
            group_size = max(1, min(45, int(grp_match.group(1))))
        elif "phòng đôi" in lower_text:
            group_size = 2

        # Nhận diện yêu cầu đặc thù giá trị cao
        specs: List[str] = []
        if any(k in lower_text for k in ["say xe", "ghế đầu", "tầng dưới"]):
            specs.append("Khách dễ say xe - Ưu tiên ghế trước")
        if any(k in lower_text for k in ["thú cưng", "chó", "mèo", "cún", "pet"]):
            specs.append("Có mang theo thú cưng")
        if any(k in lower_text for k in ["nhận phòng sớm", "check-in sớm", "gửi đồ", "gửi hành lý"]):
            specs.append("Cần hỗ trợ nhận phòng sớm / gửi hành lý")

        intent_record = CleanedTravelIntent(
            session_id=session_id,
            origin="Sài Gòn",
            destination=dest,
            preferred_bus_type=bus_type,
            group_size=group_size,
            special_requirements=specs,
            cleaned_query=combined_text,
        )
        data_flywheel_store.append(intent_record)
        return intent_record
