# 🔬 02-core-microservices (Plan B - Đồ án Tốt nghiệp 10 Điểm)

Thư mục này chứa mã nguồn Backend tự viết 100% bằng Python/FastAPI, RabbitMQ, và Vector DB (pgvector/Qdrant) theo mô hình Microservices.

---

## 📂 Danh sách các Microservices:
- `ai-rag-service/`: Xử lý RAG menu quán ăn & Circuit Breaker xoay tua API Key LLM.
- `tenant-auth-service/`: Quản lý Quán ăn, kiểm tra ACID PostgreSQL cho Nút Khóa 1.000đ.
- `message-consumer/`: Worker tiêu thụ tin nhắn từ RabbitMQ khi tải nặng > 1.000 đơn/phút.
- `billing-webhook/`: Xử lý Webhook VietQR ngân hàng tự động mở khóa.

---

## 🎓 Sử dụng khi Bảo vệ Đồ án:
Khi đi nộp báo cáo tốt nghiệp, bạn chỉ cần nộp toàn bộ thư mục `02-core-microservices/` và `03-shared-contracts/`.
