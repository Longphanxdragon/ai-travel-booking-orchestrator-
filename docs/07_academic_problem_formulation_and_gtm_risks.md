# 🔬 BẢN THẨM ĐỊNH KỸ THUẬT & CHIẾN LƯỢC KHOA HỌC MÁY TÍNH
*(Tài liệu định hướng cốt lõi cho Báo cáo Đồ án Tốt nghiệp & Chiến lược Thâm nhập Thị trường)*

---

## 1. BẢN CHẤT CỦA 3 BÀI TOÁN KHOA HỌC: MỐI QUAN HỆ HỮU CƠ
3 bài toán bạn nêu không hề tách rời ngẫu nhiên, mà là **3 mắt xích liên hoàn** tạo nên một hệ thống Tác tử AI đáng tin cậy:

```text
Khách hỏi câu phức tạp 
       │
       ▼
[BÀI TOÁN 2: MULTI-AGENT LANGGRAPH] ── Lập kế hoạch (Planning) & Phân rã bài toán
       │
       ├─────────────────────────────────┬─────────────────────────────────┐
       ▼                                 ▼                                 ▼
Tra cứu Dữ liệu Tĩnh               Tra cứu Dữ liệu Động              Kiểm tra Ràng buộc Chéo
(Chính sách, hoàn hủy)             (Vé xe, phòng trống)              (Giờ xe đến vs Check-in)
       │                                 │                                 │
       ▼                                 ▼                                 │
[BÀI TOÁN 3: HYBRID RAG]           [BÀI TOÁN 1: FUNCTION CALLING]          │
Chống sai lệch từ khóa             Chống dữ liệu cũ & Ảo giác              │
(BM25 + Dense Qdrant)              (Tra cứu thời gian thực)                │
       │                                 │                                 │
       └─────────────────────────────────┴─────────────────────────────────┘
                                         │
                                         ▼
                   [TRIỆT TIÊU HOÀN TOÀN ẢO GIÁC (ZERO HALLUCINATION)]
                                         │
                                         ▼
                     Sinh phản hồi chuẩn xác cho Khách hàng
```

### Chi tiết độ khó & Dữ liệu đặc thù của từng bài toán:
1. **Bài toán 1: Xử lý Dữ liệu Động (Zero Outdated Data & Anti-Hallucination)**
   - *Bản chất:* LLM bị giới hạn bởi thời điểm đóng băng tri thức (Knowledge Cutoff). Nếu nhét giá vé vào Prompt, AI sẽ bị ảo giác khi vé đã bán hết 5 phút trước.
   - *Giải pháp:* Dùng **Function Calling** để AI biến ý định thành truy vấn API/SQL trực tiếp vào CSDL thật.
   - *Độ khó:* Trung bình - Khá. Khó ở khâu định dạng Schema chuẩn xác và xử lý khi API bên ngoài bị timeout/lỗi mạng (Circuit Breaker).
   - *Dữ liệu đặc thù:* Dữ liệu có cấu trúc (Structured Data) biến động theo từng giây: Bảng chuyến xe (giờ chạy, số ghế trống, giá vé theo ngày) và Tồn kho phòng.

2. **Bài toán 2: Đa tác tử LangGraph xử lý Ràng buộc chéo (Cross-domain CSP)**
   - *Bản chất:* Giải quyết mâu thuẫn thời gian giữa hai thực thể độc lập. Xe giường nằm đến lúc 5h sáng, nhưng khách sạn chỉ cho nhận phòng lúc 14h chiều.
   - *Giải pháp:* Dùng **LangGraph StateGraph** với cơ chế Chain-of-Thought (CoT). Agent điều phối tự động đối chiếu: $T_{checkin} - T_{arrival} > 4h \rightarrow$ Tự động kích hoạt hành động đề xuất Early Check-in hoặc giữ hành lý.
   - *Độ khó:* Khó. Đòi hỏi thiết kế State Machine chặt chẽ, kiểm soát vòng lặp hội thoại không bị vô tận (Infinite Loop).
   - *Dữ liệu đặc thù:* Ma trận quy tắc nghiệp vụ (Business Rules Matrix) và lịch sử trạng thái hội thoại nhiều lượt (Multi-turn Conversation State).

3. **Bài toán 3: Chống sai lệch từ khóa phòng/xe (Hybrid Search RAG)**
   - *Bản chất:* Khách hỏi *"Phòng Deluxe Double Sea View"* hoặc xe *"Limousine 34 phòng"*. Vector DB thông thường tìm theo ngữ nghĩa sẽ dễ lấy nhầm phòng *Standard* hoặc xe ghế ngồi.
   - *Giải pháp:* Kết hợp **BM25 (so khớp ký tự chính xác)** và **Dense Embedding (hiểu ngữ nghĩa)**, gộp điểm bằng **Reciprocal Rank Fusion (RRF)**.
   - *Độ khó:* Trung bình. Khó ở việc tinh chỉnh siêu tham số $k$ trong công thức RRF và bộ lọc tiếng Việt.
   - *Dữ liệu đặc thù:* Dữ liệu phi cấu trúc (Unstructured Data): File PDF/Text chính sách hoàn hủy, cẩm nang dịch vụ, mô tả chi tiết tiện nghi khách sạn.

---

## 2. DỰ ĐỊNH RA MẮT BẢN PLUG-IN SỚM ĐỂ THU THẬP DỮ LIỆU: CÓ HỢP LÝ KHÔNG?

**CÂU TRẢ LỜI: CỰC KỲ HỢP LÝ VÀ CHUẨN MỰC NGHIEP VỤ (VIBE CỦA SILICON VALLEY).**
Trong Khoa học Máy tính hiện đại, nghiên cứu mà dùng dữ liệu tự bịa (Synthetic Data) thì hội đồng chỉ chấm ở mức Khá. Nhưng nếu bạn có **Tập dữ liệu thực tế (Real-world Benchmark Dataset)** được thu thập từ người dùng thật qua bản demo, bạn nắm chắc điểm 10 trong tay!

### Những KHÓ KHĂN THỰC TẾ bạn sẽ đối mặt khi ra mắt sớm:
1. **Khó khăn 1: "Cold Start" (Người dùng chat những câu không lường trước được)**
   - Khách Việt Nam gõ teencode, sai chính tả, nói lóng (*"ê shop có xe đêm đi ĐL k, fix giá t đi"*).
   - *Giải pháp:* Dùng các mô hình LLM nhỏ có khả năng hiểu tiếng Việt tốt (Gemini Flash) kết hợp Prompt chuẩn hóa câu trước khi đẩy vào StateGraph.
2. **Khó khăn 2: Tốc độ phản hồi (Latency Trap)**
   - Nếu cào dữ liệu sống quá lâu (> 4 giây), khách trên Fanpage/Zalo sẽ bỏ đi ngay.
   - *Giải pháp:* Bắt buộc dùng cơ chế **Warm Cache** (quét sẵn dữ liệu tuyến hot lưu vào bộ nhớ) và phản hồi theo dạng Streaming.
3. **Khó khăn 3: Bảo vệ dữ liệu cá nhân (Pháp lý PII)**
   - Khách có thể vô tình gửi SĐT, thông tin nhạy cảm vào khung chat.
   - *Giải pháp:* Phải kích hoạt module `ConversationDataCleaner` che SĐT/Email ngay lập tức trước khi lưu vào kho dữ liệu độc quyền.

---

## 3. PHẦN PHẦN MỀM (SOFTWARE ENGINEERING) CÓ NÊN ĐƯA VÀO ĐỒ ÁN KHÔNG?

**BẮT BUỘC ĐƯA VÀO, NHƯNG PHẢI ĐẶT ĐÚNG VỊ TRÍ!**
Lời khuyên của Thầy bạn là hoàn toàn chuẩn xác:
- **Hội đồng Khoa học Máy tính:** Chấm điểm dựa trên **Bài toán, Thuật toán, Đồ thị, Công thức Toán học, Chỉ số đo lường RAGAS**. (Đây là 70% điểm số - Phần Core).
- **Phần mềm (Microservices, Docker, FastAPI, Chatwoot, Zalo Plugin):** Đóng vai trò là **"Hệ thống Thực nghiệm & Môi trường Hiện thực hóa" (Experimental System & Validation Platform)**. (Chiếm 30% điểm số còn lại - Phần Phụ trợ nhưng là điểm cộng tuyệt đối).

> **Cách đặt tiêu đề thông minh trong Báo cáo:**
> Thay vì ghi: *"Chương 8: Viết web app bán vé"*, bạn hãy ghi:
> **"Chương 8: Thiết kế Môi trường Thực nghiệm và Hiện thực hóa Hệ thống dưới dạng Kiến trúc Microservices Hướng Tác tử (Task-Oriented Microservices Architecture)."** 
> ➔ Thầy cô Khoa học Máy tính sẽ thấy bạn có tư duy kỹ thuật đỉnh cao, vừa giỏi thuật toán vừa làm được hệ thống chạy thật!
