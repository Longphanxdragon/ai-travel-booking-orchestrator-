# ❓ BỘ 4 CÂU HỎI CHIẾN LƯỢC HỎI THẦY HÙNG TRONG BUỔI BÁO CÁO NGHIỆM THU ĐACN
*(Mục đích: Định hình tiêu chuẩn chấm điểm ĐATN & Thể hiện tư duy nghiên cứu đỉnh cao)*

---

### CÂU HỎI 1: VỀ PHƯƠNG PHÁP ĐÁNH GIÁ KHOA HỌC (EVALUATION FRAMEWORK)
> **Bạn hỏi:**
> *"Thưa Thầy, để đánh giá định lượng hiện tượng Ảo giác (Hallucination) và độ liên quan của câu trả lời, em dự kiến áp dụng khung đo lường **RAGAS** với 2 chỉ số cốt lõi là **Faithfulness** và **Answer Relevance**, kết hợp đo đạc **Task Success Rate (TSR)** khi giải bài toán ràng buộc thời gian. Thầy thấy bộ chỉ số này đối với một Luận văn tốt nghiệp ngành Khoa học Máy tính đã đủ chặt chẽ chưa, hay em nên bổ sung thêm các độ đo về chi phí truy xuất và độ trễ (Latency/Token Cost) ạ?"*

* **Ý nghĩa học thuật:** Chứng minh cho Thầy thấy bạn hiểu sâu về các tiêu chuẩn đo lường AI quốc tế (không đo đạc cảm tính bằng mắt thường).

---

### CÂU HỎI 2: VỀ THIẾT KẾ BỘ DỮ LIỆU KIỂM THỬ ĐỐI CHỨNG (BENCHMARK DATASET)
> **Bạn hỏi:**
> *"Trong Sprint tới, em sẽ xây dựng một bộ **100 câu hỏi kiểm nghiệm chuẩn (Benchmark Dataset)** gồm 3 cụm bẫy: (1) bẫy tồn kho động, (2) bẫy sai lệch mã phòng, và (3) bẫy xung đột giờ đón/nhận phòng. Theo kinh nghiệm hướng dẫn của Thầy, em nên xây dựng Ground Truth hoàn toàn thủ công (Human-annotated) hay có thể dùng kỹ thuật kết hợp LLM-as-a-Judge (ví dụ GPT-4o chấm điểm đối chứng) để kết quả thực nghiệm có sức thuyết phục cao nhất trước Hội đồng chấm thi ạ?"*

* **Ý nghĩa học thuật:** Đưa Thầy vào vai trò chuyên gia phương pháp luận nghiên cứu (Research Methodology). Thầy sẽ đánh giá bạn rất cao vì bạn đang chuẩn bị thực nghiệm một cách bài bản.

---

### CÂU HỎI 3: VỀ GIẢI THUẬT GỘP HẠNG LAI (HYBRID SEARCH - BM25 & RRF)
> **Bạn hỏi:**
> *"Đối với bài toán tìm kiếm lai kết hợp giữa BM25 và Dense Vector, em đang dùng giải thuật **Reciprocal Rank Fusion (RRF)** với hằng số làm mịn $k = 60$. Thầy có gợi ý em nên thử nghiệm thêm thuật toán học gộp hạng có trọng số (Weighted Linear Combination) và tối ưu hóa trọng số $\alpha$ bằng phương pháp Grid Search trên tập ngữ liệu du lịch tiếng Việt không ạ?"*

* **Ý nghĩa học thuật:** Khoe khéo với Thầy là bạn đã nắm chắc công thức toán học và giải thuật RRF, đồng thời mở đường cho một hướng nghiên cứu mở rộng rất "hàn lâm" trong Chương 5 và Chương 7 của Luận văn.

---

### CÂU HỎI 4: VỀ BÀI TOÁN THỎA MÃN RÀNG BUỘC (CSP) TRONG LANGGRAPH
> **Bạn hỏi:**
> *"Hiện tại ở bài toán ràng buộc thời gian giữa xe và phòng khách sạn, em đang giải quyết bằng đồ thị trạng thái có điều kiện (Conditional StateGraph). Để tăng hàm lượng thuật toán cho Luận văn ĐATN, em có nên mô hình hóa bài toán này thành một bài toán quy hoạch động (Dynamic Constraint Programming) hoặc sử dụng thuật toán ReAct với cơ chế Backtracking khi xảy ra xung đột không ạ?"*

* **Ý nghĩa học thuật:** Chạm đúng "gu" của các thầy chuyên ngành Thuật toán và Khoa học Máy tính Bách Khoa.
