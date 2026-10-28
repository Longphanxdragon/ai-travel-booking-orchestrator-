# 🧠 PROJECT STATE SNAPSHOT & AI HANDOFF PROTOCOL
*(Cập nhật ngày: 28/10/2026 - Lưu trữ vĩnh viễn trên Repo GitHub)*

> **🚨 DÀNH CHO AI ASSISTANT TRONG MỌI CONVERSATION MỚI:**
> Khi người dùng mở một phiên trò chuyện mới, bạn **BẮT BUỘC** phải đọc file này đầu tiên để nắm toàn bộ bối cảnh dự án, kiến trúc đã thống nhất, và tiếp tục triển khai công việc mà KHÔNG ĐƯỢC hỏi lại những điều đã chốt!

---

## 📌 I. THÔNG TIN ĐỀ TÀI & ĐỊNH VỊ CỐT LÕI

1. **Tên Đề tài Đồ án Tốt nghiệp (Khoa học Máy tính - ĐH Bách Khoa TP.HCM):**
   > *"Ứng dụng Hybrid Search, Function Calling và Multi-Agent nhằm giải quyết bài toán ảo giác, sai lệch từ khóa và ràng buộc chéo trong tư vấn đặt xe khách và khách sạn."*
2. **Tác giả:** Phan Thành Long ([@Longphanxdragon](https://github.com/Longphanxdragon))
3. **Repository GitHub (Đã push & đồng bộ trực tiếp):**
   `https://github.com/Longphanxdragon/ai-travel-booking-orchestrator-.git`
4. **Chiến lược Kinh doanh (Business Strategy):**
   - **Tư vấn Đa kênh thần tốc (< 1.5s):** Chat qua Facebook, Zalo, Webchat.
   - **Không can thiệp Thanh toán:** Tránh toàn bộ rủi ro pháp lý, hoàn hủy, bồi thường. AI chỉ tư vấn, check chỗ, và điều hướng về nhà xe/khách sạn.
   - **Mục tiêu Vàng:** Sở hữu **Kho Dữ liệu Du lịch Độc quyền (Data Flywheel)** đã được lọc rác, ẩn danh PII để bán dữ liệu phân tích thị trường hoặc fine-tune AI riêng.

---

## 🛠️ II. HIỆN TRẠNG KỸ THUẬT ĐÃ HOÀN THÀNH (AS-IS)

1. **Cấu trúc Monorepo:** Đầy đủ `01-platform-nocode`, `02-core-microservices`, `03-shared-contracts`, `docs/`, `03-ai-orchestrator-report/`.
2. **Bộ Tài liệu Chuẩn GitHub (docs/):**
   - `docs/01_architecture_and_algorithms.md`: Toán học BM25, RRF, Function Calling, LangGraph.
   - `docs/02_evaluation_metrics.md`: Chuẩn đánh giá RAGAS (Faithfulness, Relevance, Context Recall).
   - `docs/03_api_contracts_and_plugins.md`: Chuẩn API Plug-and-Play (`POST /api/v1/chat`).
   - `docs/04_vexere_and_ota_plugin_adapter.md`: Mẫu thiết kế Adapter cắm VeXeRe/Traveloka.
   - `docs/05_30_days_thesis_and_gtm_master_plan.md`: Lộ trình 30 ngày song hành Báo cáo & MVP.
   - `docs/06_proprietary_data_flywheel_strategy.md`: Đường ống ETL lọc rác và tạo kho dữ liệu độc quyền.
3. **Mã nguồn đã kiểm thử thực tế:**
   - `02-core-microservices/backend/app/services/tools/vexere_realtime_adapter.py`: Đã test cào trực tiếp thành công 4 hãng xe lớn (Phương Trang, Điền Linh, Phong Phú, An Anh) từ VeXeRe.
   - `02-core-microservices/backend/app/services/tools/data_cleaner_pipeline.py`: Pipeline lọc rác và ẩn danh PII.
4. **Báo cáo LaTeX:**
   - Template chuẩn ĐH Bách Khoa TP.HCM nằm trong `03-ai-orchestrator-report/report/`.
   - File tổng hợp `03-ai-orchestrator-report/build_tex.py` đã sửa lỗi và chạy hoàn hảo.

---

## 📖 III. KẾ HOẠCH VIẾT CUỐN BÁO CÁO ĐỒ ÁN (QUY MÔ 100+ TRANG)

Cuốn báo cáo sẽ được viết trực tiếp vào thư mục LaTeX `03-ai-orchestrator-report/report/Contents/` theo 9 chương chuẩn mực:

- **Chương 1: Tổng quan và Bối cảnh Đề tài (~10 trang)**
  *Thách thức ngành xe khách & lưu trú; Điểm yếu của Chatbot cũ; Mục tiêu và đóng góp của đề tài.*
- **Chương 2: Cơ sở Lý thuyết & Công nghệ Nền tảng (~25 trang)**
  *Bản chất LLM; Hạn chế Naive RAG; Toán học BM25 & Dense Vector; Thuật toán RRF; Function Calling; Multi-Agent StateGraph.*
- **Chương 3: Phân tích Yêu cầu Hệ thống (~12 trang)**
  *Phân tích dữ liệu tĩnh và động; Bài toán thỏa mãn ràng buộc chéo (Cross-domain CSP); Yêu cầu phi chức năng (Latency < 1.5s).*
- **Chương 4: Đặc tả Ca sử dụng (Use Cases) (~12 trang)**
  *Use Case Diagram; Kịch bản tra cứu xe, tra cứu phòng, xử lý lệch giờ.*
- **Chương 5: Thiết kế Kiến trúc & Giải thuật (~25 trang)**
  *Kiến trúc Microservices; Provider Adapter Pattern; Data Flywheel Pipeline; Thiết kế CSDL PostgreSQL & Qdrant.*
- **Chương 6: Hiện thực Hệ thống (~20 trang)**
  *Mã nguồn lõi FastAPI; Adapter VeXeRe thực tế; Pipeline lọc rác hội thoại PII Cleaner.*
- **Chương 7: Kiểm thử Thực nghiệm & Đánh giá RAGAS (~15 trang)**
  *Bộ 100 câu hỏi bẫy; Đánh giá Faithfulness, Answer Relevance; Benchmark với Naive LLM và Standard RAG.*
- **Chương 8: Triển khai & Khả năng Thương mại hóa (~10 trang)**
  *Đóng gói Docker; Chiến lược kinh doanh Data Flywheel; Phân tích chi phí vận hành TCO.*
- **Chương 9: Kết luận & Hướng phát triển (~5 trang)**

---

## ⚡ IV. HƯỚNG DẪN KHI BẮT ĐẦU CONVERSATION MỚI (DÀNH CHO USER)

Khi cuộc trò chuyện này quá dài hoặc bạn mở cửa sổ chat mới, bạn chỉ cần gõ đúng một câu:
> **"Đọc file `PROJECT_STATE_SNAPSHOT.md` và tiếp tục viết tiếp Chương [X] Báo cáo LaTeX cho tôi."**

AI ở phiên mới sẽ đọc file này, hiểu ngay toàn bộ câu chuyện và bắt tay vào viết tiếp mà không bị quên bất kỳ điều gì!
