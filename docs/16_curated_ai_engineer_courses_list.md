# 🎓 LỘ TRÌNH CÁC KHÓA HỌC TINH GỌN ĐỂ TRỞ THÀNH KỸ SƯ AI CHUYÊN NGHIỆP
*(Chắt lọc đúng những gì dự án này dùng - Học nhanh, thực chiến, không lan man)*

---

## 📌 NGUYÊN TẮC: KHÔNG HỌC TRÀN LAN
Bạn không cần đi học lại toán đại số tuyến tính từ đầu hay ngồi luyện thi các chứng chỉ lý thuyết dài 6 tháng. Để làm chủ dự án này và đi làm kỹ sư AI, bạn chỉ cần học **5 khóa học ngắn hạn (mỗi khóa chỉ mất 1-3 ngày, hầu hết đều MIỄN PHÍ và được dạy bởi chính những người tạo ra công nghệ)**.

---

## 1. KHÓA 1: NỀN TẢNG PYTHON ASYNC & KIỂM SOÁT DỮ LIỆU BẰNG PYDANTIC
*Mục tiêu: Hiểu cách code không bị lỗi cú pháp, hiểu cách Pydantic trói buộc dữ liệu AI.*

- **Khóa học đề xuất:** **Pydantic V2 Essentials & FastAPI Path** (trên trang chủ FastAPI hoặc YouTube của Tiangolo).
- **Link học:** [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/) (Đọc từ phần First Steps đến Pydantic Models).
- **Thời lượng:** ~4 đến 6 tiếng.
- **Những gì bạn cần nắm sau khóa:**
  - `BaseModel` là gì? Tại sao đặt kiểu `str`, `int` thì dữ liệu sai nó tự văng lỗi?
  - `async/await` trong Python là gì? Tại sao gọi API thì phải dùng `async` để không bị đơ ứng dụng?

---

## 2. KHÓA 2: FUNCTION CALLING & KIẾN TRÚC TÁC TỬ (AGENTIC AI)
*Mục tiêu: Hiểu bản chất con AI gọi hàm thế nào để không bao giờ bị ảo giác.*

- **Khóa học đề xuất:** **Functions, Tools and Agents with LangChain** (Dạy bởi Harrison Chase - CEO LangChain trên DeepLearning.AI).
- **Nền tảng:** [DeepLearning.AI](https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/) *(MIỄN PHÍ 100%)*.
- **Thời lượng:** ~2 tiếng.
- **Những gì bạn cần nắm sau khóa:**
  - Sự khác nhau giữa việc "hỏi AI một câu tự do" và "bảo AI trích xuất tham số JSON để gọi hàm".
  - Cách thiết lập danh sách công cụ (Tools) và truyền kết quả từ Database ngược lại cho AI.

---

## 3. KHÓA 3: ĐA TÁC TỬ VỚI ĐỒ THỊ TRẠNG THÁI (LANGGRAPH)
*Mục tiêu: Hiểu cách điều khiển bầy Agent phối hợp, giải bài toán lệch giờ xe và khách sạn (CSP).*

- **Khóa học đề xuất:** **AI Agents in LangGraph** (Dạy bởi chính đội ngũ phát triển LangGraph trên DeepLearning.AI).
- **Nền tảng:** [DeepLearning.AI](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/) *(MIỄN PHÍ 100%)*.
- **Thời lượng:** ~2 đến 3 tiếng.
- **Những gì bạn cần nắm sau khóa:**
  - `StateGraph` là gì? `Node` (Agent) và `Edge` (Đường nối rẽ nhánh có điều kiện) hoạt động ra sao?
  - `SharedState`: Cách các Agent chuyền tay nhau một bảng thông tin chung (State) mà không làm mất lịch sử hội thoại.

---

## 4. KHÓA 4: RAG NÂNG CAO & TÌM KIẾM LAI (HYBRID SEARCH - BM25 & VECTOR)
*Mục tiêu: Hiểu sâu toán học BM25, Cosine Similarity và thuật toán gộp hạng RRF để chém gió tự tin trước Hội đồng Bách Khoa.*

- **Khóa học đề xuất:** **Advanced Retrieval for AI with Chroma/Qdrant** & **Building Hybrid Search Systems**.
- **Nền tảng:** [DeepLearning.AI - Advanced Retrieval](https://www.deeplearning.ai/short-courses/advanced-retrieval-for-ai/) *(MIỄN PHÍ 100%)*.
- **Thời lượng:** ~2 tiếng.
- **Những gì bạn cần nắm sau khóa:**
  - Dense Vector (Ý nghĩa ngữ nghĩa) vs Sparse Vector (BM25 - Từ khóa chính xác).
  - Thuật toán gộp hạng **Reciprocal Rank Fusion (RRF)**: Tại sao phải xếp hạng 1, 2, 3 rồi mới gộp thay vì cộng điểm trực tiếp?

---

## 5. KHÓA 5: THƯỚC ĐO CHẤT LƯỢNG AI BẰNG RAGAS (EVALUATION)
*Mục tiêu: Biết cách đưa số liệu khoa học vào Luận văn để lấy điểm 10.*

- **Khóa học đề xuất:** **Evaluating and Debugging Generative AI Models** (trên DeepLearning.AI) hoặc đọc tài liệu chính thức của **Ragas Framework**.
- **Link học:** [Ragas Documentation Tutorial](https://docs.ragas.io/en/stable/getstarted/index.html).
- **Thời lượng:** ~2 tiếng.
- **Những gì bạn cần nắm sau khóa:**
  - Đo lường độ trung thực (**Faithfulness**): Đếm số câu có bằng chứng trong Database thật.
  - Đo lường độ liên quan (**Answer Relevance**).

---

## 🗓️ KẾ HOẠCH HỌC TRONG 5 NGÀY (MỖI NGÀY 2 TIẾNG):

| Ngày | Khóa cần học | Mục tiêu thực tế |
| :---: | :--- | :--- |
| **Ngày 1** | Khóa 1 (FastAPI & Pydantic) | Mở file `schemas.py` trong dự án lên, đọc hiểu từng dòng code định nghĩa dữ liệu. |
| **Ngày 2** | Khóa 2 (Function Calling) | Mở file `travel_tools.py` lên, hiểu cách hàm tra cứu vé xe chọc vào dữ liệu thật. |
| **Ngày 3** | Khóa 3 (LangGraph Agents) | Mở file `orchestrator.py` lên, hiểu cách con AI tự so sánh lệch giờ và rẽ nhánh. |
| **Ngày 4** | Khóa 4 (Hybrid Search & RRF) | Đọc lại công thức BM25 và RRF trong file `docs/01_architecture_and_algorithms.md`. |
| **Ngày 5** | Khóa 5 (Ragas Metrics) | Hiểu cách tạo bảng 100 câu hỏi bẫy để đo tỷ lệ ảo giác cho Luận văn. |

---

> 💡 **Lời khuyên chân thành:** Tất cả các khóa trên DeepLearning.AI đều được thiết kế theo dạng video ngắn 5-10 phút, có sẵn khung chạy code thực hành ngay trên trình duyệt, không cần cài đặt gì phức tạp. Bạn xem qua một lượt là bạn sẽ thấy **mọi thứ tôi làm trong dự án này đều nằm trọn vẹn trong các khóa học đó!**
