# 🛍️ Retail Automatic Workspace

Hệ thống tự động hóa chăm sóc khách hàng và bán lẻ toàn diện, kết hợp sức mạnh giữa Chatbot tự động (**Typebot**) và nền tảng quản lý hỗ trợ khách hàng đa kênh (**Chatwoot**).

---

## 📁 Cấu trúc thư mục (Workspace Structure)

```text
d:\retail-automatic/
├── typebot.io-main/   # 🤖 Typebot: Trình tạo và vận hành Chatbot tự động (Workflow automation)
├── chatwoot/          # 💬 Chatwoot: Nền tảng Live Chat & Quản lý quan hệ khách hàng (Omnichannel CRM)
└── README.md          # 📖 Tài liệu hướng dẫn tổng quan hệ thống
```

---

## 🔗 Sự kết hợp giữa Typebot & Chatwoot trong Bán lẻ tự động

1. **Tiếp nhận & Sàng lọc tự động (Typebot)**:
   - Khách hàng truy cập Website, Facebook Messenger, Zalo, hoặc WhatsApp sẽ lập tức được tiếp cận bởi kịch bản tự động từ **Typebot**.
   - Trả lời các câu hỏi thường gặp (FAQ), tư vấn sản phẩm, thu thập thông tin đơn hàng 24/7 không cần nhân sự trực.

2. **Chuyển giao tư vấn viên (Chatwoot Hand-off)**:
   - Khi khách hàng có yêu cầu đặc biệt, khiếu nại, hoặc cần tư vấn sâu, kịch bản Typebot tự động kích hoạt block **Chatwoot Hand-off**.
   - Toàn bộ lịch sử trò chuyện được chuyển tiếp liền mạch vào hộp thư (Inbox) của **Chatwoot** để nhân viên chăm sóc khách hàng tiếp nhận và xử lý.

---

## 🚀 Hướng dẫn khởi chạy nhanh (Quick Start)

### 1. Khởi chạy Typebot
Di chuyển vào thư mục `typebot.io-main` và sử dụng Docker Compose hoặc Bun/Node:
```bash
cd typebot.io-main
# Sử dụng Docker Compose cho môi trường phát triển
docker compose -f docker-compose.dev.yml up -d
```

### 2. Khởi chạy Chatwoot
Di chuyển vào thư mục `chatwoot` và làm theo hướng dẫn thiết lập môi trường:
```bash
cd chatwoot
# Sao chép file cấu hình mẫu
cp .env.example .env
# Khởi chạy bằng Docker Compose (nếu sử dụng Docker)
docker compose up -d
```

---

## 💡 Khuyến nghị tối ưu
- Bạn có thể đổi tên thư mục `typebot.io-main` thành `typebot` để cấu trúc tên thư mục đồng bộ và ngắn gọn hơn (`typebot` và `chatwoot`).
- Cấu hình Webhook giữa Chatwoot và Typebot trong trang quản trị API của từng dịch vụ để liên kết dữ liệu thời gian thực.
