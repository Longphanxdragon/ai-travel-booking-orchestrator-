# 📊 TIÊU CHUẨN ĐÁNH GIÁ & KỊCH BẢN THỰC NGHIỆM
*(Tài liệu phục vụ Chương Đánh giá & Kết quả Thực nghiệm trong Đồ án tốt nghiệp)*

---

## 1. BỘ TIÊU CHUẨN ĐÁNH GIÁ (EVALUATION METRICS)

Để thuyết phục Hội đồng Khoa học Máy tính bằng số liệu định lượng (Quantitative Analysis), hệ thống áp dụng bộ tiêu chí đánh giá kép: **Hàn lâm (Ragas Framework)** và **Kỹ thuật phần mềm (System Performance)**.

### 1.1. Tiêu chí Đánh giá Chất lượng Sinh và Truy xuất (RAGAS Framework)
1. **Faithfulness (Độ trung thực - Không ảo giác):**
   Đo lường tỷ lệ các khẳng định trong câu trả lời của AI được suy ra trực tiếp từ Context (dữ liệu DB/chính sách trả về).
   $$Faithfulness = \frac{|V_c|}{|V|}$$
   *(Trong đó $|V_c|$ là số câu luận điểm được kiểm chứng bởi context, $|V|$ là tổng số câu luận điểm trong phản hồi).*
   - **Mục tiêu đạt được:** $\ge 0.95$ (Giảm thiểu tối đa tình trạng AI bịa ra thông tin phòng/vé).

2. **Answer Relevance (Độ liên quan của câu trả lời):**
   Đo mức độ câu trả lời giải quyết đúng trọng tâm yêu cầu của người dùng.
   - **Mục tiêu:** $\ge 0.90$.

3. **Context Recall & Precision (Độ chuẩn xác truy xuất Hybrid Search):**
   So sánh tài liệu tìm thấy giữa Naive Dense Search và Hybrid (BM25 + Dense + RRF) với tập ground-truth gồm 100 câu hỏi về mã phòng và điều khoản xe khách.

### 1.2. Tiêu chí Nghiệp vụ & Đa tác tử (Task-Oriented Metrics)
1. **Task Success Rate (TSR - Tỷ lệ hoàn thành tác vụ):**
   Tỷ lệ các phiên hội thoại kết thúc bằng một giao dịch giữ chỗ hợp lệ hoặc từ chối chính xác khi hết hàng.
2. **Turn Count Optimization (Số lượt hội thoại tối ưu):**
   Số câu hỏi qua lại trung bình để thu thập đủ biến số đặt combo (mục tiêu từ 3 đến 5 lượt hội thoại).
3. **Pessimistic Lock Collision Rate:**
   Tỷ lệ xung đột khi có 100 tác tử ảo cùng tranh chấp một ghế xe khách cuối cùng trong cùng 1 giây.

---

## 2. KỊCH BẢN THỬ NGHIỆM ĐỐI CHỨNG (BENCHMARK SCENARIOS)

Hệ thống được kiểm thử đối chứng giữa 3 kiến trúc:
- **Baseline A (Naive LLM):** GPT-4o-mini / Gemini Flash gọi trực tiếp không kèm RAG và Tool.
- **Baseline B (Standard RAG):** RAG truyền thống (chỉ dùng Dense Vector Embeddings + Prompt Injection danh sách giá).
- **Hệ thống đề xuất (Our System):** Multi-Agent LangGraph + Hybrid Search (BM25 + Qdrant) + Function Calling (ACID Postgres).

### Bảng kết quả thực nghiệm dự kiến (Benchmark Table)

| Tiêu chí đánh giá | Baseline A (Naive LLM) | Baseline B (Standard RAG) | Đề xuất (Our System) |
| :--- | :---: | :---: | :---: |
| **Độ chính xác tồn kho thực tế** | 12.0% (Ảo giác cao) | 48.5% (Do dữ liệu bị trễ) | **100% (SQL Real-time)** |
| **Bắt đúng mã phòng đặc thù** | 35.0% | 68.2% | **97.4% (BM25 + RRF)** |
| **Phát hiện xung đột giờ đón/nhận phòng** | 18.0% | 22.0% | **94.8% (CoT StateGraph)** |
| **Thời gian phản hồi trung bình (Latency)** | ~1.2s | ~2.1s | ~2.4s |
| **Độ trung thực (Faithfulness Score)** | 0.42 | 0.74 | **0.96** |
