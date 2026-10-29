-- ==============================================================================
-- SCHEMA CƠ SỞ DỮ LIỆU ĐỘC LẬP: DỊCH VỤ DU LỊCH & ĐẶT VÉ (POSTGRESQL 16 ACID)
-- Dùng chung cho Core Microservices, LangGraph Function Calling & Mock Testing
-- ==============================================================================

-- 1. BẢNG KHÁCH SẠN / LƯU TRÚ (HOTEL_ROOMS)
CREATE TABLE IF NOT EXISTS hotel_rooms (
    room_id VARCHAR(50) PRIMARY KEY,
    hotel_name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,         -- Vị trí: Gần biển, Trung tâm, v.v.
    room_type VARCHAR(100) NOT NULL,        -- Deluxe Ocean View, Standard Double
    price_per_night BIGINT NOT NULL,        -- Giá niêm yết theo đêm (VND)
    available_rooms INTEGER DEFAULT 0,      -- Số phòng trống thực tế
    early_checkin_fee BIGINT DEFAULT 200000,-- Phí nhận phòng sớm trước 14:00
    pet_allowed BOOLEAN DEFAULT FALSE,      -- Cho phép mang thú cưng hay không
    cancellation_policy TEXT,               -- Chính sách hủy phòng
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. BẢNG CHUYẾN XE KHÁCH (BUS_TRIPS)
CREATE TABLE IF NOT EXISTS bus_trips (
    trip_id VARCHAR(50) PRIMARY KEY,
    operator_name VARCHAR(100) NOT NULL,    -- Phương Trang, Điền Linh, Phong Phú
    origin VARCHAR(100) NOT NULL,           -- Điểm đi: Sài Gòn
    destination VARCHAR(100) NOT NULL,      -- Điểm đến: Đà Lạt, Nha Trang
    bus_type VARCHAR(100) NOT NULL,         -- Limousine 24 Phòng Đôi, Giường nằm 34 chỗ
    departure_time TIMESTAMP WITH TIME ZONE NOT NULL,
    arrival_time TIMESTAMP WITH TIME ZONE NOT NULL,
    pickup_point VARCHAR(255) NOT NULL,     -- Điểm đón cụ thể (Bến xe, Văn phòng)
    fare_vnd BIGINT NOT NULL,               -- Giá vé (VND)
    available_seats INTEGER DEFAULT 0,      -- Số ghế trống thực tế
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. BẢNG LƯU VẾT Ý ĐỊNH & KHO DỮ LIỆU ĐỘC QUYỀN (PROPRIETARY TRAVEL INTENTS)
CREATE TABLE IF NOT EXISTS travel_intents_lake (
    intent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(100) NOT NULL,
    origin VARCHAR(100),
    destination VARCHAR(100),
    preferred_bus_type VARCHAR(100),
    group_size INTEGER DEFAULT 1,
    special_requirements JSONB DEFAULT '[]'::jsonb,
    cleaned_query TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. BẢNG GIỮ CHỖ TẠM THỜI (ACID RESERVATIONS)
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(100) NOT NULL,
    trip_id VARCHAR(50) REFERENCES bus_trips(trip_id),
    room_id VARCHAR(50) REFERENCES hotel_rooms(room_id),
    seats_held INTEGER DEFAULT 0,
    rooms_held INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'HOLD',      -- HOLD, EXPIRED, CANCELLED
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- DỮ LIỆU MẪU CHUẨN THỰC CHIẾN ĐỂ DEMO NGAY
INSERT INTO hotel_rooms (room_id, hotel_name, location, room_type, price_per_night, available_rooms, early_checkin_fee, pet_allowed, cancellation_policy)
VALUES 
('HOTEL-DL-01', 'Khách sạn Colline Đà Lạt', 'Trung tâm (gần Chợ Đà Lạt)', 'Deluxe Double', 950000, 3, 250000, FALSE, 'Miễn phí hủy trước 48h'),
('HOTEL-DL-02', 'Homestay Thung Lũng Mây', 'Cách trung tâm 3km (View thung lũng)', 'Phòng Đôi Bungalow', 550000, 2, 150000, TRUE, 'Hủy trước 24h mất 50%'),
('HOTEL-NT-01', 'SeaView Nha Trang Hotel', 'Đường Trần Phú (Cách biển 50m)', 'Deluxe Ocean View', 750000, 5, 200000, FALSE, 'Miễn phí hủy trước 72h')
ON CONFLICT (room_id) DO NOTHING;

INSERT INTO bus_trips (trip_id, operator_name, origin, destination, bus_type, departure_time, arrival_time, pickup_point, fare_vnd, available_seats)
VALUES
('BUS-SG-DL-2230', 'Phương Trang (FUTA)', 'Sài Gòn', 'Đà Lạt', 'Limousine Giường Nằm 34 Chỗ', NOW() + INTERVAL '1 day 22 hours', NOW() + INTERVAL '2 days 5 hours', 'Bến xe Miền Tây / Lê Hồng Phong Q5', 320000, 6),
('BUS-SG-DL-2300', 'Điền Linh Limousine', 'Sài Gòn', 'Đà Lạt', 'Limousine 24 Phòng Đôi', NOW() + INTERVAL '1 day 23 hours', NOW() + INTERVAL '2 days 6 hours', 'VP Hàng Xanh Bình Thạnh', 450000, 4),
('BUS-SG-NT-2100', 'An Anh Limousine', 'Sài Gòn', 'Nha Trang', 'Limousine 34 Phòng VIP', NOW() + INTERVAL '1 day 21 hours', NOW() + INTERVAL '2 days 5 hours 30 minutes', 'Bến xe Miền Đông mới', 380000, 8)
ON CONFLICT (trip_id) DO NOTHING;
