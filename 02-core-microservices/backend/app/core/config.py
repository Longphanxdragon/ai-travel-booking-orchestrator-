# ==============================================================================
# TẦNG CẤU HÌNH TRUNG TÂM CHUẨN 12-FACTOR APP (CENTRALIZED CONFIGURATION)
# ------------------------------------------------------------------------------
# Dành cho người mới (Beginner Guide):
# Thay vì viết cứng (hardcode) mật khẩu, ngưỡng giờ, hay số lượng token rải rác
# trong hàng chục file code (rất dễ sai sót khi sửa), các công ty FAANG gom toàn
# bộ tham số vận hành vào MỘT file cấu hình duy nhất đọc từ Biến môi trường (ENV).
# ==============================================================================

import os
from pydantic import BaseModel, Field


class SystemSettings(BaseModel):
    """
    Bảng điều khiển thông số toàn hệ thống (Single Source of Truth).
    Tự động đọc từ biến môi trường (Environment Variables), nếu không có sẽ dùng
    giá trị mặc định an toàn để chạy Local / Unit Test ngay lập tức.
    """

    # 1. Định danh Dịch vụ (Service Identity)
    app_name: str = Field(
        default=os.getenv("APP_NAME", "AI Travel Booking Orchestrator API"),
        description="Tên hiển thị của Microservice trên Swagger UI",
    )
    app_version: str = Field(
        default=os.getenv("APP_VERSION", "2.0.0"),
        description="Phiên bản Semantic Versioning của dịch vụ",
    )
    environment: str = Field(
        default=os.getenv("APP_ENV", "production"),
        description="Môi trường chạy: development | staging | production",
    )

    # 2. Kết nối Cơ sở dữ liệu (Data Layer Endpoints)
    database_url: str = Field(
        default=os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres_secret_password@localhost:5432/chatwoot_production",
        ),
        description="Chuỗi kết nối PostgreSQL 16 phục vụ truy vấn tồn kho ACID",
    )
    qdrant_url: str = Field(
        default=os.getenv("QDRANT_URL", "http://localhost:6333"),
        description="Địa chỉ Qdrant Vector DB phục vụ Hybrid Search",
    )

    # 3. Siêu tham số Thuật toán Khoa học Máy tính (Algorithmic Hyperparameters)
    bm25_k1: float = Field(
        default=1.5,
        description="Hệ số bão hòa tần suất từ khóa trong công thức Okapi BM25",
    )
    bm25_b: float = Field(
        default=0.75,
        description="Hệ số chuẩn hóa độ dài tài liệu trong công thức Okapi BM25",
    )
    rrf_k: int = Field(
        default=60,
        description="Hằng số làm mịn k=60 theo chuẩn Cormack et al. cho Reciprocal Rank Fusion",
    )
    csp_time_conflict_threshold_hours: float = Field(
        default=3.0,
        description="Ngưỡng lệch giờ Delta T (tiếng) giữa giờ xe đến và giờ check-in khách sạn",
    )
    reservation_hold_ttl_minutes: int = Field(
        default=15,
        description="Thời gian giữ chỗ tạm thời (TTL = 15 phút) cho giao dịch khóa bi quan ACID",
    )

    # 4. Hàng rào Bảo vệ Chi phí & Chống Tấn công (SRE & FinOps Guardrails)
    max_input_tokens_per_turn: int = Field(
        default=int(os.getenv("MAX_INPUT_TOKENS", "512")),
        description="Ngưỡng Token tối đa cho 1 tin nhắn khách gửi (chống đốt tiền API LLM)",
    )
    max_session_tokens_budget: int = Field(
        default=int(os.getenv("MAX_SESSION_TOKENS", "4096")),
        description="Tổng ngân sách Token tối đa cho 1 phiên hội thoại",
    )
    rate_limit_requests_per_minute: int = Field(
        default=int(os.getenv("RATE_LIMIT_RPM", "120")),
        description="Số request tối đa mỗi phút trên một session_id (chống spam/DDoS)",
    )
    circuit_breaker_failure_threshold: int = Field(
        default=3,
        description="Số lần lỗi liên tiếp trước khi Cầu dao (Circuit Breaker) tự ngắt",
    )
    circuit_breaker_recovery_seconds: float = Field(
        default=30.0,
        description="Thời gian chờ (giây) trước khi Cầu dao thử đóng mạch trở lại (HALF_OPEN)",
    )

    # 5. Kênh Điều hành ChatOps (Telegram / Zalo Business Alert)
    telegram_bot_token: str = Field(
        default=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        description="Token Bot Telegram bắn thông báo chốt khách về điện thoại chủ nhà xe/khách sạn",
    )
    telegram_chat_id: str = Field(
        default=os.getenv("TELEGRAM_CHAT_ID", ""),
        description="Chat ID nhóm vận hành của chủ doanh nghiệp",
    )
    webhook_hmac_secret: str = Field(
        default=os.getenv("WEBHOOK_HMAC_SECRET", "bku_faang_enterprise_secret_2026"),
        description="Khóa bí mật kiểm tra chữ ký HMAC-SHA256 từ Webhook đa kênh",
    )


# Khởi tạo đối tượng Singleton dùng chung cho toàn bộ ứng dụng
settings = SystemSettings()
