-- HỢP ĐỒNG CƠ SỞ DỮ LIỆU DÙNG CHUNG (ACID POSTGRESQL SCHEMA)
-- Sử dụng cho cả Plan A (n8n query) và Plan B (FastAPI Microservices query)

CREATE TABLE IF NOT EXISTS tenants (
    inbox_id INTEGER PRIMARY KEY,           -- ID Hộp thư Chatwoot tương ứng với Quán ăn
    name VARCHAR(255) NOT NULL,             -- Tên Quán ăn / Nhà hàng
    status VARCHAR(50) DEFAULT 'ACTIVE',    -- Trạng thái: ACTIVE, LOCKED, MAINTENANCE
    balance_vnd BIGINT DEFAULT 0,           -- Số dư VND (Nút Khóa kiểm tra cột này)
    price_per_order BIGINT DEFAULT 1000,    -- Phí SaaS trên mỗi đơn hàng (mặc định 1.000đ)
    hotline VARCHAR(50),                    -- Số điện thoại Hotline báo khi bảo trì
    telegram_chat_id VARCHAR(100),          -- ID Nhóm Telegram báo đơn cho bếp
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_logs (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    inbox_id INTEGER REFERENCES tenants(inbox_id),
    customer_name VARCHAR(255),
    customer_phone VARCHAR(50),
    total_amount BIGINT,
    fee_deducted BIGINT DEFAULT 1000,
    status VARCHAR(50) DEFAULT 'COMPLETED', -- COMPLETED, FAILED, REFUNDED
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tạo chỉ mục (Index) tăng tốc độ query cho Nút Khóa
CREATE INDEX IF NOT EXISTS idx_tenants_status_balance ON tenants(inbox_id, status, balance_vnd);
