# 🧠 PROJECT STATE SNAPSHOT & AI HANDOFF PROTOCOL
*(Cập nhật ngày: 31/10/2026 - Lưu trữ vĩnh viễn trên Repo GitHub)*

> **🚨 DÀNH CHO AI ASSISTANT TRONG MỌI CONVERSATION MỚI:**
> Khi người dùng mở một phiên trò chuyện mới, bạn **BẮT BUỘC** phải đọc file này đầu tiên để nắm toàn bộ bối cảnh dự án, kiến trúc đã thống nhất, và tiếp tục triển khai công việc mà KHÔNG ĐƯỢC hỏi lại những điều đã chốt!

---

## 📌 I. THÔNG TIN ĐỀ TÀI & ĐỊNH VỊ CỐT LÕI

1. **Tên Đề tài Đồ án Tốt nghiệp (Khoa học Máy tính - ĐH Bách Khoa TP.HCM):**
   > *"Ứng dụng Hybrid Search, Function Calling và Multi-Agent nhằm giải quyết bài toán ảo giác, sai lệch từ khóa và ràng buộc chéo trong tư vấn đặt xe khách và khách sạn."*
2. **Tác giả:** Phan Thành Long ([@Longphanxdragon](https://github.com/Longphanxdragon))
3. **Repository GitHub (Đã push & đồng bộ trực tiếp):**
   `https://github.com/Longphanxdragon/ai-travel-booking-orchestrator-.git`
4. **Chiến lược Kinh doanh & Vận hành (Business & ChatOps Strategy):**
   - **Tư vấn Đa kênh thần tốc (< 1.5s):** Chat qua Facebook Messenger, Zalo OA, Webchat.
   - **Mô hình Vận hành ChatOps (Không dùng Web App):** AI tự động tư vấn 24/7 $\rightarrow$ Bắn thông báo chốt đơn tức thì về Telegram/Zalo của Chủ doanh nghiệp $\rightarrow$ Chủ thao tác chốt hoặc gọi lại trực tiếp trên tin nhắn điện thoại.
   - **Không can thiệp Thanh toán:** Tránh toàn bộ rủi ro pháp lý, hoàn hủy, bồi thường. AI chỉ tư vấn, check chỗ, và điều hướng về nhà xe/khách sạn.
   - **Mục tiêu Vàng:** Sở hữu **Kho Dữ liệu Du lịch Độc quyền (Data Flywheel)** đã được lọc rác, ẩn danh PII để bán dữ liệu phân tích thị trường hoặc fine-tune AI riêng.

---

## 🛠️ II. HIỆN TRẠNG KỸ THUẬT ĐÃ HOÀN THÀNH (AS-IS)

1. **Cấu trúc Monorepo:** Đầy đủ `01-platform-nocode`, `02-core-microservices`, `03-shared-contracts`, `docs/`, `03-ai-orchestrator-report/`.
2. **Kiểm thử Tự động:**
   - Bộ test `pytest tests/test_core_system.py` đạt **100% PASSED (3/3 passed)**.
   - Đã benchmark 4 kịch bản thực tế (TC-01 đến TC-04): Tra cứu xe Nha Trang, phòng Đà Lạt thú cưng, combo lệch giờ 8 tiếng có PII.
3. **Báo cáo LaTeX Chuẩn BKU ([`03-ai-orchestrator-report/report/BaoCao_BKU/`](03-ai-orchestrator-report/report/BaoCao_BKU/)):**
   - **Chương 1: Tổng quan và Bối cảnh Đề tài** (✅ Đã xong)
   - **Chương 2: Cơ sở Lý thuyết & Công nghệ Nền tảng** (✅ Đã xong)
   - **Chương 3: Phân tích Yêu cầu Hệ thống** (✅ Đã xong - Toán học CSP $\langle X, D, C \rangle$, FR, NFR, 4 Bảng Trade-offs)
   - **Chương 4: Đặc tả Chi tiết các Ca Sử dụng** (✅ Đã xong - TikZ Use Case Diagram, 7 Ca sử dụng chuẩn IEEE/RUP, Quy trình ChatOps không Web App)
   - **Chương 5: Thiết kế Kiến trúc & Giải thuật** (✅ Đã xong - Phân tầng Microservices, StateGraph Star Topology, 3 Thuật toán lõi, Sơ đồ tuần tự ACID Locking, DDL CSDL, Data Flywheel)
   - **Đóng gói Overleaf Ready:** File [`03-ai-orchestrator-report/report/BaoCao_BKU_Ready.zip`](03-ai-orchestrator-report/report/BaoCao_BKU_Ready.zip) đã tạo sẵn (180 KB), nạp 1 click lên Overleaf.
4. **CI/CD GitHub Actions:**
   - `.github/workflows/ci.yml`: Tự động kiểm thử Pydantic v2 schemas, PII Cleaner và Core Test Suite.
   - `.github/workflows/compile-latex.yml`: Tự động biên dịch `main.tex` thành `BaoCao_LuanVan_BKU.pdf` khi push code.

---

## 📖 III. KẾ HOẠCH VIẾT TIẾP BÁO CÁO (CÁC CHƯƠNG CÒN LẠI)

- **Chương 6: Hiện thực Hệ thống (~20 trang)**
  *Mã nguồn lõi FastAPI (`app/main.py`); Adapter VeXeRe Playwright thực tế; Pipeline lọc rác và bảo mật PII (`data_cleaner_pipeline.py`); Logic giải quyết ràng buộc lệch giờ (`travel_tools.py`).*
- **Chương 7: Kiểm thử Thực nghiệm & Đánh giá RAGAS (~15 trang)**
  *Bộ 100 câu hỏi bẫy; Đánh giá Faithfulness, Answer Relevance; Benchmark đối chứng với bài báo ICML 2024 TravelPlanner.*
- **Chương 8: Triển khai & Khả năng Thương mại hóa (~10 trang)**
  *Đóng gói Docker Compose; Mô hình kinh doanh ChatOps cho Homestay/Nhà xe; Phân tích chi phí vận hành TCO.*
- **Chương 9: Kết luận & Hướng phát triển (~5 trang)**

---

## ⚡ IV. HƯỚNG DẪN KHI BẮT ĐẦU CONVERSATION MỚI (DÀNH CHO USER)

Khi mở cửa sổ chat mới, bạn chỉ cần gõ đúng một câu:
> **"Đọc file `PROJECT_STATE_SNAPSHOT.md` và tiếp tục viết tiếp Chương 6 (Hiện thực Hệ thống) Báo cáo LaTeX cho tôi."**

AI ở phiên mới sẽ đọc file này, hiểu ngay toàn bộ hiện trạng kỹ thuật và bắt tay vào viết tiếp Chương 6 mà không bị quên bất kỳ điều gì!
