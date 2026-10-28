# 🚀 AI BOOKING ORCHESTRATOR - MASTER PLAN (PLAN C)

*Tài liệu này được tạo ra để lưu trữ toàn bộ bối cảnh (Context), Kiến trúc lõi và Sprint Plan của dự án. Bất kỳ AI Assistant nào trong các luồng hội thoại mới đều PHẢI đọc file này trước khi bắt đầu viết code để đảm bảo tính nhất quán của hệ thống.*

---

## 1. TỔNG QUAN DỰ ÁN (PROJECT OVERVIEW)
- **Tên dự án:** Nghiên cứu ứng dụng Hybrid Search, Function Calling và Multi-Agent nhằm giải quyết ảo giác và ràng buộc chéo trong tư vấn đặt chỗ du lịch.
- **Tác giả:** Phan Thành Long
- **Mục tiêu kép:** 
  1. Hoàn thành Đồ án Chuyên ngành (Khoa học Máy tính) với các chỉ số đo lường AI chuẩn mực.
  2. Tạo bản Prototype B2B SaaS (AI Employee) đi chốt sale các Homestay/Phòng vé thực tế.

## 2. KIẾN TRÚC LÕI (CORE ARCHITECTURE)
Dự án được phân rã thành 3 khối công nghệ lõi độc lập, tuân thủ nguyên tắc Microservices:

1. **Khối 1: Hybrid Search Engine (Qdrant)**
   - **Nhiệm vụ:** Giải quyết bài toán *Keyword Mismatch* (sai lệch mã phòng, tên nhà xe).
   - **Công nghệ:** Kết hợp Sparse Vector (BM25) và Dense Vector (Embedding). Gộp hạng bằng Reciprocal Rank Fusion (RRF).

2. **Khối 2: Real-time Tool Agent (Function Calling)**
   - **Nhiệm vụ:** Giải quyết bài toán *Ảo giác dữ liệu động (Hallucination)*.
   - **Công nghệ:** Cấp quyền cho LLM (Pydantic schemas) chọc thẳng vào SQLite/PostgreSQL để tra cứu vé xe, phòng trống theo thời gian thực (Real-time).

3. **Khối 3: Microservices-based Multi-Agent Orchestrator (LangGraph)**
   - **Nhiệm vụ:** Giải quyết bài toán *Ràng buộc chéo (Cross-constraints)* giữa giờ xe đến và giờ check-in khách sạn.
   - **Công nghệ:** Sử dụng LangGraph StateGraph.
   - **Các Agents:** 
     - *Orchestrator Agent:* Nhạc trưởng lập kế hoạch bằng Chain-of-Thought (CoT).
     - *Bus Agent:* Chuyên gia gọi API xe khách.
     - *Hotel Agent:* Chuyên gia gọi API khách sạn.

## 3. LỘ TRÌNH AGILE (SPRINT PLAN - 6 TUẦN)

### 🎯 TUẦN 1-2: ĐỊNH HÌNH BÀI TOÁN & THU THẬP DATA
- **Crawler:** Dùng BeautifulSoup cào 500 mô tả khách sạn (Agoda/Booking), lưu thành `hotels_data.csv` để làm data tĩnh (Hybrid Search).
- **Mock DB:** Tạo `mock_database.sqlite` (bảng `bus_seats` và `hotel_rooms`) làm data động (Function Calling).
- **Nghiên cứu:** LangGraph, Qdrant, BM25+RRF.
- **Thử nghiệm:** Ném data cào được lên Coze.com tạo 1 con bot nháp để test giọng điệu (Prompt Engineering).

### 🎯 TUẦN 3-4: THIẾT KẾ KIẾN TRÚC & BUILD BASELINE (NAIVE RAG)
- **Kiến trúc:** Vẽ sơ đồ luồng dữ liệu (Webhook -> FastAPI -> LangGraph -> Qdrant & SQL).
- **Code Baseline:** Viết `baseline_rag.py`. Nhét CSV vào Vector DB, truy vấn bằng RAG truyền thống (chỉ Dense Vector, không có Agent) để chứng minh sự "ngu ngốc" của RAG truyền thống.
- **Đánh giá (Metrics):** Cài đặt kịch bản đo độ chính xác (NDCG) và Tỷ lệ ảo giác (Hallucination rate).

### 🎯 TUẦN 5-6: PROTOTYPE LÕI (MULTI-AGENT) & ĐO LƯỜNG
- **Code AI Core:** 
  - Tích hợp Qdrant (Hybrid Search).
  - Viết hàm `check_bus_ticket` và `check_hotel_room` chọc vào SQLite. Ép LLM dùng Function Calling.
  - Viết file `multi_agent.py` dùng LangGraph.
- **Giao diện:** Viết Web UI chat cực gọn bằng Streamlit (~50 dòng code) để Demo.
- **Thực nghiệm:** Chạy 20 câu hỏi bẫy vào cả `baseline_rag.py` và `multi_agent.py`. Trích xuất log ra Excel so sánh để đưa vào Báo cáo ĐACN.

---

## 4. GHI CHÚ CHO AI ASSISTANT ĐỜI SAU (AI HANDOFF INSTRUCTIONS)
*Xin chào, nếu bạn là một AI đang đọc file này trong một luồng hội thoại mới:*
1. User đang ở giai đoạn code thực thi. Hãy hỏi User xem họ đang ở **Sprint số mấy** trong lộ trình trên.
2. Code Python phải sử dụng **LangGraph** (cho Multi-Agent), **Qdrant** (cho Vector DB), và **Pydantic** (cho Function Calling Schema).
3. Đừng viết mã giả (pseudo-code), hãy viết mã thực thi được và tuân thủ các best-practices của kiến trúc Microservices.
