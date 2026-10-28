# 💎 CHIẾN LƯỢC KHO DỮ LIỆU ĐỘC QUYỀN (PROPRIETARY DATA FLYWHEEL)
*(Tài liệu Kiến trúc Bóc tách & Chuẩn hóa Dữ liệu Hội thoại Du lịch Đa kênh)*

---

## 1. TƯ DUY CHIẾN LƯỢC: DATA FLYWHEEL (BÁNH ĐÀ DỮ LIỆU)

> **"Không ôm rủi ro thanh toán - Chỉ ôm Dữ liệu hành vi và Ý định khách hàng."**

Doanh nghiệp lớn hoặc các quỹ đầu tư định giá một Startup AI không phải ở chỗ bạn tích hợp được bao nhiêu cổng thanh toán, mà ở **Bộ Dữ liệu Tinh khiết Độc quyền (Proprietary Cleaned Dataset)** mà thị trường không ai có:
1. Người dùng Việt Nam thường hỏi những câu gì khi đi du lịch? (Phụ thu trẻ em, mang thú cưng, say xe, giờ đón đêm).
2. Lộ trình nào đang "cháy vé" hoặc có nhu cầu cao mà nguồn cung không đủ?
3. Cặp ghép nối (Combo Pairs) xe nào + khách sạn nào có tỷ lệ khách gật đầu cao nhất?

```text
Khách chat (FB / Zalo)
         │
         ▼
[AI Tiếp nhận & Tư vấn thần tốc (< 1.5s)] ───► Trả lời khách hàng
         │
         ▼ (Bất đồng bộ - Background Task)
[Data ETL Pipeline: Lọc rác & Ẩn danh hóa PII]
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│             KHO DỮ LIỆU ĐỘC QUYỀN (GOLD DATA LAKE)          │
│                                                             │
│ 1. Travel Intent Data: Tuyến đường, ngân sách, thói quen    │
│ 2. Realtime Supply Log: Snapshot giá và ghế trống VeXeRe/KS │
│ 3. Conversion Pair: Combo xe + KS được chọn nhiều nhất      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. BÀI TOÁN TỐC ĐỘ: PHẢN HỒI THẦN TỐC (< 1.5 GIÂY) TRÊN ZALO / FACEBOOK

Nếu vừa chat với khách vừa chạy Playwright cào VeXeRe thì mất 3–5 giây (khách sẽ rời đi). 

**Giải pháp kỹ thuật chuẩn công nghiệp:**
1. **Cache ấm (Warm Cache / Redis Snapshot):** Adapter quét và lưu sẵn snapshot các tuyến đường hot (Sài Gòn - Đà Lạt, Nha Trang, Vũng Tàu) định kỳ 15 phút một lần vào bộ nhớ tạm.
2. **Streaming & Non-blocking I/O:** AI phản hồi ngay câu chào và dữ liệu cache trong 800ms.
3. **Decoupled Data Logging:** Quá trình lưu và làm sạch dữ liệu được đẩy vào tiến trình chạy ngầm (`BackgroundTasks` của FastAPI), không làm nghẽn luồng chat của khách dù chỉ 1 mili-giây.

---

## 3. CƠ CHẾ LỌC RÁC & CẤU TRÚC KHO DỮ LIỆU ĐỘC QUYỀN

### 3.1. Loại bỏ dữ liệu rác (Noise Filtering) & Bảo mật (Privacy First)
- **Loại bỏ:** Lời chào cụt lủn ("alo", "hi"), icon vô nghĩa, các đoạn spam quảng cáo.
- **Ẩn danh hóa (PII Anonymization):** Tự động che số điện thoại (`090****567`), tên riêng thật của khách để tuân thủ Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân.

### 3.2. Cấu trúc CSDL Kho Dữ liệu Độc quyền (`proprietary_data_lake`)
Mỗi phiên chat được bóc tách thành 3 bảng giá trị cao:

#### Bảng 1: `customer_intents` (Hành vi & Nhu cầu tiềm ẩn)
- `session_id`: Mã phiên ẩn danh.
- `origin` & `destination`: Tuyến đường (VD: Sài Gòn ➔ Đà Lạt).
- `travel_date_range`: Khoảng ngày đi (Cuối tuần, dịp lễ).
- `group_type`: Đi 1 mình, Cặp đôi, hay Gia đình có trẻ nhỏ.
- `budget_tier`: Tiết kiệm, Tiêu chuẩn, hay Cao cấp (Limousine phòng đôi).
- `special_requests`: Cần xe trung chuyển, say xe cần ngồi đầu, mang thú cưng.

#### Bảng 2: `market_supply_snapshots` (Dữ liệu thị trường thời gian thực)
- Lưu lại thời điểm nào các hãng xe (Phương Trang, Điền Linh) hết vé hoặc tăng giá vé để phân tích biến động thị trường du lịch.

#### Bảng 3: `ai_conversion_traces` (Dữ liệu huấn luyện AI độc quyền)
- Lưu cặp câu hỏi - câu trả lời chất lượng cao (High-quality Dialog Pairs).
- Đây là **tài sản vàng** để sau này Fine-tune mô hình AI riêng (Domain-Specific SLM) hoặc bán trọn gói cho các tập đoàn du lịch lớn!
