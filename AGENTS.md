# 🤖 AI AGENT EXECUTION RULES & SAFETY PROTOCOL
*(Áp dụng cho mọi AI Assistant: Cursor, Claude, Antigravity, GitHub Copilot)*

> **🚨 QUY TẮC TỐI THƯỢNG (PRIME DIRECTIVE):**
> Bạn đang làm việc trên một **Dự án Luận văn Tốt nghiệp Ngành Khoa học Máy tính (ĐH Bách Khoa TP.HCM)** kết hợp **Hệ thống SaaS Khởi nghiệp B2B**. 
> Bất kỳ hành động sửa đổi code nào gây ra lỗi (Broken Tests / Syntax Error / Broken Schemas) đều bị nghiêm cấm tuyệt đối. Trước khi viết bất kỳ dòng code nào, bạn BẮT BUỘC phải đọc và tuân thủ các nguyên tắc dưới đây.

---

## 1. BẢN ĐỒ DỰ ÁN (PROJECT SITEMAP - ĐỌC ĐẦU TIÊN)
Trước khi làm việc, bạn phải đọc 2 file mỏ neo để nắm 100% bối cảnh:
1. [`PROJECT_STATE_SNAPSHOT.md`](PROJECT_STATE_SNAPSHOT.md): Tình trạng tiến độ, kiến trúc và quyết định kỹ thuật đã chốt.
2. [`docs/01_architecture_and_algorithms.md`](docs/01_architecture_and_algorithms.md): Bản đặc tả toán học chi tiết về 3 bài toán:
   - **Bài toán 1:** Ảo giác dữ liệu động $\rightarrow$ Dùng Function Calling Pydantic + Khóa bi quan PostgreSQL ACID (`database-init.sql`).
   - **Bài toán 2:** Sai lệch từ khóa $\rightarrow$ Dùng Hybrid Search (BM25 + Dense Qdrant + RRF với $k=60$).
   - **Bài toán 3:** Ràng buộc chéo di chuyển & lưu trú $\rightarrow$ Dùng LangGraph StateGraph (Orchestrator).

---

## 2. QUY TẮC BẤT DI BẤT DỊCH VỀ DỮ LIỆU & CODE (NON-NEGOTIABLE INVARIANTS)

1. **Khóa cứng Hợp đồng Pydantic Schemas (`app/models/schemas.py`):**
   - Không được tùy tiện xóa hoặc đổi tên các trường trong `ChatRequest`, `ChatResponse`, `BusSearchCriteria`, `HotelSearchCriteria`.
   - Mọi thay đổi về Schema phải tương thích ngược (Backward Compatible) và phải được cập nhật tương ứng trong Unit Tests.
2. **Không ảo giác dữ liệu (Zero Hardcoded Hallucination):**
   - Tuyệt đối không để AI tự bịa ra giờ xe chạy hay phòng trống trong Prompt text tự do.
   - Dữ liệu tồn kho BẮT BUỘC phải được gọi thông qua các hàm trong `app/services/tools/travel_tools.py` hoặc adapter `vexere_realtime_adapter.py`.
3. **Bảo mật PII Bắt buộc (Privacy First):**
   - Mọi câu hỏi người dùng trước khi ghi vào log hoặc lưu trữ BẮT BUỘC phải đi qua `ConversationDataCleaner.anonymize_pii()` để che SĐT (`090****567`) và Email.

---

## 3. QUY TRÌNH PHÁT TRIỂN 4 BƯỚC (ZERO-ERROR PIPELINE)
Mọi AI Agent khi nhận lệnh code một tính năng mới phải tuân thủ nghiêm ngặt 4 bước:

1. **Bước 1 - Khảo sát:** Đọc kỹ tài liệu đặc tả tương ứng trong thư mục `docs/`.
2. **Bước 2 - Viết code theo chuẩn Type-hints & Async:** Luôn khai báo kiểu dữ liệu rõ ràng (Type Hints) và sử dụng `async/await` cho các tác vụ I/O.
3. **Bước 3 - BẮT BUỘC CHẠY KIỂM THỬ TRƯỚC KHI BÁO HOÀN THÀNH:**
   Mở terminal chạy lệnh:
   ```bash
   cd 02-core-microservices/backend
   pytest tests/test_core_system.py
   ```
   *Nếu bài test FAIL $\rightarrow$ Không được phép commit code lên git. Phải tự sửa lỗi cho tới khi kết quả hiển thị 100% PASSED!*
4. **Bước 4 - Commit có ý nghĩa (Conventional Commits):**
   Ghi commit message rõ ràng: `feat:`, `fix:`, `docs:`, `test:`.

---

## 4. PHÂN CHIA TRÁCH NHIỆM FILE (DON'T TOUCH ZONES)
- **Khu vực Học thuật & Báo cáo:** Chỉ sửa trong `03-ai-orchestrator-report/report/BaoCao_BKU/`.
- **Khu vực Tài liệu Đặc tả:** Chỉ sửa trong `docs/`.
- **Khu vực Lõi Microservice:** Code trong `02-core-microservices/backend/app/`.
