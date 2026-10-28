# 📜 SAAS_RULES.md — BỘ QUY TẮC & KIẾN TRÚC THƯ MỤC KÉP (MODULAR MONOREPO)

> **🚨 GIAO THỨC BẮT BUỘC CHO AI AGENT (PRE-PHASE REREAD PROTOCOL):**
> 1. Trước khi bắt đầu bất kỳ Giai đoạn (Phase) mới nào hoặc khi bắt đầu một phiên làm việc mới, AI **BẮT BUỘC** phải dùng công cụ `view_file` để đọc lại toàn bộ file `SAAS_RULES.md` này. Không được suy đoán hoặc bỏ qua các nguyên tắc bất di bất dịch dưới đây!
> 2. **Tự động cập nhật tiến độ (Realtime Progress Tracking)**: Khi hoàn thành xong bất kỳ mục nào trong Lộ trình (Ví dụ: 1.1), AI **BẮT BUỘC** phải mở file `SAAS_RULES.md` này ra, sửa dấu `[ ]` thành `[x]`, và ghi chú ngắn gọn (1 câu) thời gian hoàn thành bên cạnh. Điều này giúp theo dõi tiến độ dự án realtime.

---

## 🏗️ I. CẤU TRÚC THƯ MỤC KÉP & CHIẾN THUẬT DOCKER PROFILES

Dự án được tổ chức theo mô hình **Modular Monorepo (Strangler Fig Pattern)**:
```text
d:\retail-automatic/
├── 📁 01-platform-nocode/      # [PLAN A - KIẾM TIỀN NHANH]: Gói "Mì ăn liền" cho khách hàng MVP
│   ├── chatwoot/               # Live-Chat Omnichannel CRM
│   ├── typebot.io-main/        # Form chọn món động
│   └── n8n-workflows/          # Các file JSON workflow cấu hình kéo thả
│
├── 📁 02-core-microservices/   # [PLAN B - ĐỒ ÁN 10 ĐIỂM]: Gói "Hàn lâm Kỹ sư" tự code 100%
│   ├── ai-rag-service/         # Service Python/FastAPI xử lý RAG Vector DB & Circuit Breaker
│   ├── tenant-auth-service/    # Service quản lý Quán, ACID Postgres & Nút Khóa 1.000đ
│   ├── message-consumer/       # Worker xử lý RabbitMQ / Kafka khi tải nặng 1.000 đơn/phút
│   └── billing-webhook/        # Service nhận webhook VietQR ngân hàng tự động mở khóa
│
├── 📁 03-shared-contracts/     # [CẦU NỐI KHÔNG GIÁN ĐOẠN]: Chuẩn hóa giao tiếp API & Schemas
│   ├── webhook-schemas.json    # HỢP ĐỒNG BẤT KHẢ XÂM PHẠM (Immutable API Contract)
│   └── database-init.sql       # Schema PostgreSQL dùng chung cho cả Plan A và Plan B
│
├── 🐳 docker-compose.yml       # Trạm điều phối tổng với Docker Profiles (nocode vs microservices)
└── 📜 SAAS_RULES.md            # Bộ quy tắc tối thượng của toàn bộ dự án
```

### 🔥 Chiến thuật Khởi chạy Docker Profiles (Tối ưu RAM cho VPS):
- File `docker-compose.yml` ở root sử dụng tính năng **Docker Profiles**.
- Chạy `docker compose --profile nocode up -d`: Chỉ bật Chatwoot, n8n, Typebot (Phục vụ Plan A kiếm tiền ngay).
- Chạy `docker compose --profile microservices up -d`: Chỉ bật FastAPI, RabbitMQ, Postgres (Phục vụ Plan B chịu tải & bảo vệ Đồ án).
- *(Ghi chú: Cách này giúp VPS 150k/tháng không bị sập vì bật cả 2 hệ thống cùng lúc khi chưa cần thiết).*

---

## 💎 II. CÁC NGUYÊN TẮC BẤT DI BẤT DỊCH (CORE INVARIANTS)

1. **Khóa cứng Hợp đồng API (API Contracts Invariance)**:
   - Tuyệt đối **KHÔNG ĐƯỢC** thay đổi file `webhook-schemas.json` trong thư mục `03-shared-contracts` nếu chưa được sự đồng ý của Human (Sếp/CTO).
   - Mọi Microservices viết sau này phải tuân theo 100% cấu trúc JSON đã được định nghĩa ở đây. Dù luồng bên trong là n8n hay FastAPI, đầu vào/ra phải giống hệt nhau để lật công tắc không gián đoạn dịch vụ.
2. **Chi phí AI luôn bằng 0đ (Zero-Cost AI Strategy)**:
   - Luôn áp dụng thuật toán **Round-Robin** (ở Plan A) hoặc **Circuit Breaker / Load Balancer** (ở Plan B) với danh sách API Keys Free Tier (Gemini 2.5 Flash, Gemini 3.1 Pro).
3. **Quyền lực của "Nút Khóa" (The 1.000đ Billing Lock)**:
   - Trước mỗi lần gọi AI hoặc xử lý đơn hàng, hệ thống **BẮT BUỘC** phải tra cứu trạng thái Quán (`status == ACTIVE` và `balance >= 1000`).
   - Nếu vi phạm điều kiện số dư ➔ Ngay lập tức ngắt luồng AI và trả lời tin nhắn tự động bảo trì.
4. **Cô lập dữ liệu Multi-tenant (Tenant Isolation)**:
   - Mỗi Quán ăn/Nhà hàng phải là một **Account/Inbox riêng biệt** trong Chatwoot.
   - Luôn lấy `inbox_id` làm khóa chính (Primary Key) để định tuyến dữ liệu.

---

## 🗺️ III. LỘ TRÌNH TRIỂN KHAI & THEO DÕI GIAI ĐOẠN (PHASES CHECKLIST)

### 📌 GIAI ĐOẠN 1 (PHASE 1): HẠ TẦNG DOCKER & DÒNG CHẢY MVP (Plan A)
*Mục tiêu: Dựng hạ tầng 1 lần luôn & chạy thông luồng cơ bản cho 1 quán mẫu để bán hàng ngay.*
- [x] **1.1. Tổ chức thư mục**: Sắp xếp lại workspace theo đúng mô hình Modular Monorepo (tạo `01-platform-nocode`, `02-core-microservices`, `03-shared-contracts`). *(Hoàn thành lúc 2026-07-27 09:10:00+07:00)*
- [x] **1.2. Hạ tầng Docker Compose**: Viết file `docker-compose.yml` tại root kết nối Chatwoot, Typebot, và n8n sử dụng Docker Profiles (`nocode`). *(Hoàn thành lúc 2026-07-27 09:10:00+07:00)*
- [ ] **1.3. Luồng logic cơ bản (n8n)**: Webhook nhận tin nhắn Chatwoot ➔ Gọi Gemini tư vấn ➔ Gửi Link Typebot ➔ Báo đơn về Telegram bếp.
- 🎯 *Tiêu chí hoàn thành Phase 1*: Bot AI tự động trò chuyện chốt món thành công trên 1 kênh thực tế, sẵn sàng kinh doanh.

---

### 📌 GIAI ĐOẠN 2 (PHASE 2): THƯƠNG MẠI HÓA & NÚT KHÓA 1.000Đ/ĐƠN
*Mục tiêu: Kiểm soát chi phí AI 0đ và thu phí tự động VietQR.*
- [ ] **2.1. Cơ sở dữ liệu Quán**: Thiết lập bảng `Tenants` với các cột `inbox_id`, `name`, `status`, `balance`, `hotline`.
- [ ] **2.2. Nút Khóa 1.000đ**: Cấu hình logic ngắt luồng AI khi số dư `< 1.000đ`.
- [ ] **2.3. Webhook VietQR Top-up**: Khách chuyển khoản `PAY INBOX_ID` ➔ Tự động cộng tiền và mở khóa dịch vụ.
- 🎯 *Tiêu chí hoàn thành Phase 2*: Hệ thống SaaS tự động khóa khi hết tiền và tự động mở khóa khi chủ quán nạp tiền VietQR.

---

### 📌 GIAI ĐOẠN 3 (PHASE 3): XÂY DỰNG LÕI MICROSERVICES (Plan B - Đồ án 10 Điểm)
*Mục tiêu: Tự code 100% Backend thay thế n8n/Chatwoot để bảo vệ Đồ án và chịu tải lớn.*
- [ ] **3.1. Hàng đợi RabbitMQ & Tenant Service**: Viết service Python/FastAPI tiếp nhận webhook và quản lý ACID PostgreSQL.
- [ ] **3.2. AI RAG Service & Circuit Breaker**: Viết service xử lý tìm kiếm ngữ nghĩa menu trong Vector DB (`pgvector`/`Qdrant`) và tự động Failover API Key khi gặp lỗi 429.
- [ ] **3.3. Cơ chế chuyển mạch (Strangler Switch)**: Thử nghiệm chuyển hướng Webhook URL từ n8n sang FastAPI mà không làm rớt tin nhắn của khách hàng.
- 🎯 *Tiêu chí hoàn thành Phase 3*: Có sẵn bộ code chuẩn Kỹ sư A+ để nộp cho thầy chấm đồ án, đồng thời có thể áp dụng cho các quán ăn có lượng traffic cực lớn!
