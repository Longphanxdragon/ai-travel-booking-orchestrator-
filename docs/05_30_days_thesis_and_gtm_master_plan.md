# 🎯 KẾ HOẠCH TÁC CHIẾN 30 NGÀY: RA MẮT SẢN PHẨM & BÁO CÁO TỐT NGHIỆP 100+ TRANG

> **Mục tiêu kép tối thượng:**
> 1. **Về Học thuật:** Xuất bản cuốn Báo cáo Đồ án Tốt nghiệp hoàn chỉnh (chuẩn format ĐH Bách Khoa TP.HCM, quy mô 80–120+ trang LaTeX chất lượng cao).
> 2. **Về Thương mại:** Có sản phẩm chạy thực tế (Prototype / MVP) sẵn sàng mang đi demo và chào hàng các homestay, nhà xe, đại lý du lịch trong 30 ngày.

---

## 🤝 I. CƠ CHẾ LÀM VIỆC HIỆU QUẢ GIỮA BẠN VÀ TÔI (WORKFLOW PROTOCOL)

Để không bị hoang mang và lãng phí thời gian, chúng ta phân chia vai trò rõ ràng như hai nhà đồng sáng lập (Co-founders):

| Người thực hiện | Vai trò chính | Nhiệm vụ cụ thể |
| :--- | :--- | :--- |
| **BẠN (Product Owner / Kỹ sư trưởng)** | Định hướng & Thẩm định | 1. Ra lệnh theo từng chương/module cụ thể.<br>2. Cung cấp góp ý của Thầy hướng dẫn hoặc phản hồi từ doanh nghiệp.<br>3. Chạy thử nghiệm và mang sản phẩm đi gặp khách hàng. |
| **TÔI (Lead AI Engineer / Technical Writer)** | Thi công & Soạn thảo | 1. Viết mã nguồn hoàn chỉnh (FastAPI, LangGraph, Tools, CSDL).<br>2. Viết chi tiết từng chương báo cáo LaTeX học thuật (kèm công thức toán, biểu đồ, mã giả).<br>3. Tự động commit và đẩy (push) lên GitHub của bạn. |

### Cách giao việc cho tôi từng ngày:
Thay vì ra lệnh chung chung, bạn chỉ cần ra lệnh theo công thức:
- *"Hôm nay hãy viết chi tiết Mục 2.2 và 2.3 trong Chương 2 Báo cáo về thuật toán BM25 và Hybrid Search"*
- *"Hôm nay hãy code xong Tool tra cứu phòng khách sạn và đẩy lên GitHub"*

---

## 📅 II. LỘ TRÌNH TÁC CHIẾN 4 TUẦN (SPRINT ROADMAP)

```text
Tuần 1: Khung Báo Cáo & CSDL Tồn Kho Thật
   │  ├── Báo cáo: Hoàn thiện Chương 1 (Mở đầu) & Chương 2 (Cơ sở lý thuyết) (~30 trang)
   │  └── Code: Viết xong CSDL mẫu (Postgres) & API FastAPI cơ bản
   ▼
Tuần 2: Lõi AI Đa Tác Tử (Multi-Agent) & Phân Tích Thiết Kế
   │  ├── Báo cáo: Viết Chương 3 (Yêu cầu) & Chương 5 (Phân tích thiết kế) (~30 trang)
   │  └── Code: Hoàn thiện LangGraph Agent + Tool tra cứu xe khách & phòng
   ▼
Tuần 3: Adapter VeXeRe & Thử Nghiệm Đối Chứng (Benchmark)
   │  ├── Báo cáo: Viết Chương 6 (Hiện thực) & Chương 7 (Kiểm thử & RAGAS) (~25 trang)
   │  └── Code: Viết Adapter cắm VeXeRe/Mock API + Web UI Demo (Streamlit/Webchat)
   ▼
Tuần 4: Đóng Gói Demo Pitch Doanh Nghiệp & Hoàn Thiện Cuốn Báo Cáo
      ├── Báo cáo: Chương 8 (Triển khai), Chương 9 (Tổng kết), compile trọn bộ PDF (100+ trang)
      └── Thị trường: Cầm bản Demo web/Zalo đi chào 3 Homestay / Nhà xe để lấy thư xác nhận thử nghiệm
```

---

## 📖 III. CẤU TRÚC CUỐN BÁO CÁO TỐT NGHIỆP DỰ KIẾN (QUY MÔ 100+ TRANG)

Để đạt quy mô vài trăm trang (thường đồ án chuẩn Bách Khoa từ 80 đến 130 trang là độ dày lý tưởng nhất, không bị loãng), cuốn sách sẽ được chia thành 9 chương bài bản:

1. **CHƯƠNG 1: TỔNG QUAN VÀ BỐI CẢNH ĐỀ TÀI (~10 trang)**
   - Khó khăn thực tế trong chuyển đổi số ngành xe khách & lưu trú tại Việt Nam.
   - Giới hạn của Chatbot AI thế hệ cũ (Ảo giác, trễ dữ liệu).
   - Mục tiêu và phạm vi nghiên cứu của đề tài.

2. **CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÁC CÔNG NGHỆ NỀN TẢNG (~25 trang)**
   - Bản chất của Mô hình Ngôn ngữ Lớn (LLM) và cơ chế Attention.
   - Hạn chế của Naive RAG; Cơ sở toán học của thuật toán tìm kiếm thông tin BM25 và Dense Embeddings.
   - Thuật toán gộp hạng **Reciprocal Rank Fusion (RRF)**.
   - Lý thuyết về Tác tử Hướng tác vụ (Task-Oriented Agents) và cơ chế **Function Calling**.
   - Nguyên lý đồ thị trạng thái **LangGraph (StateGraph)** và suy luận **Chain-of-Thought (CoT)**.

3. **CHƯƠNG 3: PHÂN TÍCH YÊU CẦU HỆ THỐNG (~12 trang)**
   - Phân tích dữ liệu tĩnh (Chính sách hoàn hủy, điều khoản phụ thu trẻ em).
   - Phân tích dữ liệu động (Tồn kho ghế xe, phòng khách sạn).
   - Bài toán thỏa mãn ràng buộc chéo (Cross-domain CSP) giữa giờ xe đến và giờ check-in.
   - Yêu cầu phi chức năng: Độ trễ (< 3s), bảo đảm tính toàn vẹn dữ liệu (ACID).

4. **CHƯƠNG 4: ĐẶC TẢ CÁC TRƯỜNG HỢP SỬ DỤNG (USE CASE SPECIFICATION) (~12 trang)**
   - Use Case tổng quan hệ thống.
   - Chi tiết từng Use Case: Tra cứu xe khách, Tra cứu lưu trú, Giữ chỗ Combo tự động, Xử lý lệch giờ.

5. **CHƯƠNG 5: THIẾT KẾ KIẾN TRÚC VÀ GIẢI THUẬT (~25 trang)**
   - Kiến trúc Microservices tổng thể và Provider Adapter Pattern.
   - Thiết kế Cơ sở Dữ liệu Quan hệ (PostgreSQL) và Vector DB (Qdrant).
   - Thiết kế Đồ thị trạng thái Agent (LangGraph State Machine).
   - Thiết kế cơ chế khóa bi quan (Pessimistic Locking `SELECT ... FOR UPDATE`) chống bán trùng chỗ (Double Booking).

6. **CHƯƠNG 6: HIỆN THỰC HỆ THỐNG (~20 trang)**
   - Cấu trúc thư mục mã nguồn và chuẩn hóa Pydantic v2 Schemas.
   - Trích dẫn và giải thích các đoạn mã nguồn then chốt (Core Implementation snippets).
   - Hiện thực Adapter kết nối nền tảng đặt vé ngoại vi (VeXeRe API / OTA).

7. **CHƯƠNG 7: THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ (~15 trang)**
   - Xây dựng bộ dữ liệu kiểm thử (Evaluation Dataset) gồm 100 câu hỏi bẫy.
   - Đo lường định lượng theo khung **RAGAS Framework** (Faithfulness, Answer Relevance).
   - Bảng so sánh thực nghiệm đối chứng: Naive LLM vs Standard RAG vs Hệ thống đề xuất.
   - Đo lường hiệu năng chịu tải (Concurrent Stress Test).

8. **CHƯƠNG 8: MÔ HÌNH TRIỂN KHAI VÀ KHẢ NĂNG THƯƠNG MẠI HÓA (~10 trang)**
   - Đóng gói Docker Container & Docker Compose.
   - Mô hình cắm rút (Plug-and-Play) vào hệ sinh thái doanh nghiệp thực tế.
   - Phân tích bài toán kinh tế (TCO) và chi phí vận hành AI.

9. **CHƯƠNG 9: TỔNG KẾT VÀ HƯỚNG PHÁT TRIỂN (~5 trang)**
   - Các kết quả đã đạt được so với mục tiêu ban đầu.
   - Những mặt hạn chế còn tồn đọng.
   - Định hướng mở rộng trong tương lai.

---

## 🚀 IV. BƯỚC BẮT ĐẦU NGAY HÔM NAY:

Để đạt được mục tiêu cuốn báo cáo dày và chất lượng, **chúng ta sẽ tiến hành viết cuốn báo cáo từng chương một trực tiếp vào thư mục báo cáo LaTeX của bạn** (`03-ai-orchestrator-report/report/`).

Hôm nay, bạn có muốn tôi bắt tay ngay vào **viết chi tiết 100% nội dung Chương 1 (Mở đầu) và Chương 2 (Cơ sở lý thuyết - Toán học BM25, RRF, Function Calling)** với đầy đủ công thức toán học và hình vẽ để bạn có ngay 30 trang đầu tiên nộp cho Thầy không?
