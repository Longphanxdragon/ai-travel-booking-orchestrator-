# 🎓 CẨM NANG TIÊU CHÍ CHẤM ĐỒ ÁN TỐT NGHIỆP: KHOA HỌC MÁY TÍNH VS CÔNG NGHỆ PHẦN MỀM
*(Áp dụng cho Trường ĐH Bách Khoa TP.HCM - HCMUT, ĐHQG-HCM và các trường kỹ thuật hàng đầu)*

---

## 1. BÁO CÁO 100 TRANG CÓ ĐỦ KHÔNG?

**CÂU TRẢ LỜI NGẮN GỌN: 100 TRANG LÀ "ĐỘ DÀY HOÀNG KIM" (SWEET SPOT).**

- **Dưới 60 trang:** Hội đồng sẽ đánh giá là *sơ sài, thiếu cơ sở lý thuyết hoặc thiếu thực nghiệm định lượng*. Rất khó đạt điểm 9-10.
- **Từ 90 đến 130 trang:** **CHUẨN MỰC TỐI ƯU CỦA ĐỒ ÁN XUẤT SẮC (A/A+)**. Đủ dung lượng để trình bày sâu về công thức toán, kiến trúc thuật toán, mã nguồn cốt lõi và các biểu đồ phân tích thực nghiệm mà không bị đánh giá là "bôi chữ".
- **Trên 180 trang:** Thường bị phản tác dụng vì hội đồng không có thời gian đọc hết, dễ bị bắt bẻ những phần copy tài liệu chung chung hoặc nội dung bị loãng.

---

## 2. PHÂN BIỆT 2 HƯỚNG CHẤM: KHOA HỌC MÁY TÍNH (CS) VS CÔNG NGHỆ PHẦN MỀM (SE)

Thầy giáo của bạn nói chuẩn xác 100%. Hai hội đồng này nhìn đồ án bằng hai "cặp kính" hoàn toàn khác nhau:

| Tiêu chí so sánh | Hướng CÔNG NGHỆ PHẦN MỀM (SE) | Hướng KHOA HỌC MÁY TÍNH (CS) - *HƯỚNG CỦA ĐỒ ÁN NÀY* |
| :--- | :--- | :--- |
| **Câu hỏi Hội đồng hỏi bạn** | *"Hệ thống có chạy mượt không? Quản lý phiên bản thế nào? Sơ đồ Class, Use Case có đúng chuẩn UML không?"* | *"Tại sao dùng thuật toán này mà không dùng thuật toán kia? Độ phức tạp thuật toán là bao nhiêu? Đo lường ảo giác bằng công thức nào?"* |
| **Trọng tâm đánh giá** | Quy trình phát triển phần mềm (Agile/Scrum), Thiết kế kiến trúc (Clean Architecture), CI/CD, Kiểm thử tự động (Unit Test, Integration Test). | **Mô hình giải thuật (Algorithms), Cơ sở toán học (Mathematical Foundations), Tối ưu hóa suy luận, Thực nghiệm đối chứng có số liệu (Empirical Benchmarks).** |
| **Sản phẩm bàn giao** | Một ứng dụng hoàn chỉnh, giao diện đẹp, ít lỗi, chịu tải tốt. | **Một giải pháp giải quyết bài toán khó (Vấn đề Ảo giác, Dữ liệu động, Ràng buộc chéo) được chứng minh bằng số liệu khoa học.** |

---

## 3. ĐỒ ÁN NÀY ĐÍCH THỰC LÀ HƯỚNG KHOA HỌC MÁY TÍNH (CS)!

Đề tài của bạn: *"Ứng dụng Hybrid Search, Function Calling và Multi-Agent nhằm giải quyết bài toán ảo giác, sai lệch từ khóa và ràng buộc chéo trong tư vấn đặt xe khách và khách sạn"* là một đề tài **chuẩn Khoa học Máy tính 100%**:
1. **Bài toán khoa học rõ ràng:** Bài toán Thỏa mãn ràng buộc đa miền (Cross-domain CSP) và Bài toán Giảm thiểu ảo giác thông tin động (Dynamic Hallucination Mitigation).
2. **Có giải thuật & Toán học cụ thể:** 
   - Thuật toán xếp hạng lai **BM25 + Cosine Similarity**.
   - Thuật toán gộp hạng **Reciprocal Rank Fusion (RRF)**: $RRF(d) = \sum \frac{1}{k + r_i(d)}$.
   - Đồ thị trạng thái tác tử **LangGraph StateGraph**.
3. **Phần mềm (Microservices, Docker, VeXeRe Adapter) đóng vai trò gì?**
   Nó đóng vai trò là **"Hệ thống Thực nghiệm" (Validation Testbed)** để chứng minh thuật toán của bạn chạy được ngoài đời thực, chứ không phải một bài báo lý thuyết suông.

---

## 4. BẢNG TIÊU CHÍ CHẤM ĐIỂM CHI TIẾT (RUBRIC ĐIỂM 10 CỦA HỘI ĐỒNG KHMT)

Một hội đồng Khoa học Máy tính Bách Khoa thường chấm dựa trên thang điểm sau:

### 1. Cơ sở Lý thuyết & Tổng quan bài toán (20% - 2.0 điểm)
- Có chỉ ra được tại sao các giải pháp hiện nay (Naive RAG, Prompt thông thường) thất bại không?
- Các công thức toán học (BM25, RRF, Embedding Cosine) có được giải thích mạch lạc, chính xác không?

### 2. Thiết kế Giải thuật & Đề xuất Mô hình (30% - 3.0 điểm) - *QUAN TRỌNG NHẤT*
- Thiết kế Đa tác tử (Multi-Agent StateGraph) có chặt chẽ không?
- Cơ chế Function Calling có ép buộc được Schema dữ liệu Pydantic để triệt tiêu ảo giác 100% không?
- Cơ chế xử lý ràng buộc thời gian giữa giờ xe đến và giờ nhận phòng được mô hình hóa bằng logic gì?

### 3. Thực nghiệm & Đánh giá Khoa học (30% - 3.0 điểm) - *ĐIỂM ĂN TIỀN TUYỆT ĐỐI*
- Có xây dựng được bộ dữ liệu kiểm thử (Evaluation Dataset) gồm các câu hỏi khó/bẫy không?
- **Có bảng số liệu so sánh đối chứng (Benchmark) rõ ràng không?** (Ví dụ: So sánh mô hình đề xuất vs Naive RAG vs GPT thông thường dựa trên khung đánh giá **RAGAS: Faithfulness, Answer Relevance**).
- Tỷ lệ giảm ảo giác là bao nhiêu %? Tốc độ truy xuất cải thiện bao nhiêu ms?

### 4. Báo cáo & Kỹ năng Trình bày (20% - 2.0 điểm)
- Định dạng LaTeX chuẩn Bách Khoa (canh lề, tài liệu tham khảo BibTeX, hình vẽ vector sắc nét, bảng biểu rõ ràng).
- Trình bày lưu loát, tự tin, trả lời phản biện gãy gọn trước các câu hỏi xoáy của Thầy phản biện.
