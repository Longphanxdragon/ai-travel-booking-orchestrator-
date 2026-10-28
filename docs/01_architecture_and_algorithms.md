# 🏛️ ĐẶC TẢ KIẾN TRÚC & THUẬT TOÁN HỆ THỐNG
*(Phục vụ Thuyết minh Đồ án Chuyên ngành & Luận văn Tốt nghiệp)*

---

## 1. TỔNG QUAN BÀI TOÁN KHOA HỌC MÁY TÍNH

Trong lĩnh vực xử lý ngôn ngữ tự nhiên (NLP) và hệ thống tác tử tự trị (Autonomous Agents), bài toán tư vấn và đặt chỗ (Booking) du lịch thường thất bại khi áp dụng các kỹ thuật Chatbot truyền thống hoặc RAG cơ bản (Naive RAG). Nguyên nhân cốt lõi bao gồm:

1. **Vấn đề Đóng băng Dữ liệu (Data Cutoff) & Ảo giác (Hallucination):** 
   - Mô hình LLM không có khả năng tự nhận biết sự thay đổi của các thực thể động (ghế trống xe khách, phòng trống khách sạn theo từng phút).
   - Khi được hỏi: *"Tối mai còn 2 vé xe Limousine đi Đà Lạt lúc 23h không?"*, mô hình LLM cơ bản có xu hướng tự tạo câu trả lời nghe có vẻ hợp lý nhưng hoàn toàn sai thực tế.
2. **Vấn đề Sai lệch Từ khóa Chuyên ngành (Keyword Mismatch):**
   - Không gian vector ngữ nghĩa (Dense Vector Embedding) có xu hướng ánh xạ các từ đồng nghĩa gần nhau. Tuy nhiên, trong đặt phòng khách sạn, các chuỗi ký tự như `Deluxe Ocean View` và `Standard Ocean View` chỉ khác nhau một từ nhưng là hai hạng phòng với mức giá và chính sách hoàn toàn khác nhau.
3. **Bài toán Thỏa mãn Ràng buộc Đa miền (Cross-Domain Constraint Satisfaction Problem - CSP):**
   - Chuyến xe xuất phát lúc 23:00 tối thứ Sáu từ TP.HCM sẽ đến Đà Lạt vào khoảng 06:00 sáng thứ Bảy. Khách sạn thường chỉ cho nhận phòng lúc 14:00.
   - Hệ thống phải có khả năng suy luận logic (Reasoning) để cảnh báo thời gian chờ 8 tiếng hoặc tự động đề xuất giải pháp nhận phòng sớm (Early Check-in).

---

## 2. THUẬT TOÁN CỐT LÕI (CORE ALGORITHMS)

### 2.1. Thuật toán Hybrid Search kết hợp Reciprocal Rank Fusion (RRF)
Để đảm bảo độ chính xác tuyệt đối khi tra cứu chính sách và tên hạng phòng, hệ thống triển khai tìm kiếm lai (Hybrid Search):

```
                        Câu truy vấn người dùng (q)
                                   │
                 ┌─────────────────┴─────────────────┐
                 ▼                                   ▼
          Sparse Retrieval                     Dense Retrieval
             (Thuật toán BM25)              (Cosine Similarity)
                 │                                   │
                 ▼                                   ▼
        Danh sách xếp hạng R_sparse         Danh sách xếp hạng R_dense
                 │                                   │
                 └─────────────────┬─────────────────┘
                                   ▼
                    Reciprocal Rank Fusion (RRF)
                                   │
                                   ▼
                     Tập kết quả đồng thuận (Fused Docs)
```

**Công thức RRF (Reciprocal Rank Fusion):**
$$RRF(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
Trong đó:
- $M$: Tập các bộ tìm kiếm ($M = \{BM25, Dense\}$).
- $r_m(d)$: Thứ hạng của văn bản $d$ trong bộ tìm kiếm $m$.
- $k$: Hằng số làm mịn (thông thường chọn $k = 60$).

### 2.2. Kỹ thuật Function Calling với Khóa Bi Quan (Pessimistic ACID Locking)
Khi tác tử quyết định thực hiện đặt chỗ hoặc giữ chỗ:
1. LLM phân tích ý định và trích xuất tham số theo schema JSON Pydantic:
   ```json
   {
     "trip_id": "BUS-SG-DL-2300",
     "seats_requested": 2,
     "customer_phone": "0901234567"
   }
   ```
2. Tác tử gọi hàm `hold_bus_seats` trong Backend. Hàm này mở một Transaction trên PostgreSQL:
   ```sql
   BEGIN TRANSACTION;
   SELECT available_seats FROM bus_trips 
   WHERE trip_id = 'BUS-SG-DL-2300' 
   FOR UPDATE; -- Khóa bi quan ngăn ngừa Race Condition

   -- Kiểm tra: Nếu available_seats >= 2:
   UPDATE bus_trips 
   SET available_seats = available_seats - 2 
   WHERE trip_id = 'BUS-SG-DL-2300';

   INSERT INTO bookings (booking_id, status, hold_expires_at) 
   VALUES (gen_random_uuid(), 'HOLD', NOW() + INTERVAL '15 minutes');

   COMMIT;
   ```

### 2.3. Đồ thị Trạng thái Đa Tác tử (Multi-Agent StateGraph)
Hệ thống sử dụng **LangGraph** để duy trì trạng thái phiên làm việc (`AgentState`):

```python
class AgentState(TypedDict):
    session_id: str
    messages: Annotated[list[BaseMessage], add_messages]
    bus_constraints: Optional[dict]       # Điểm đi, điểm đến, ngày giờ, số vé
    hotel_constraints: Optional[dict]     # Địa điểm, ngày nhận/trả, hạng phòng
    cross_check_status: Optional[str]     # MATCHED, TIME_CONFLICT, OUT_OF_STOCK
    pending_booking_id: Optional[str]
```

Luồng định tuyến (Routing Logic):
- **Node `orchestrator`**: Phân tích bối cảnh, xác định thông tin còn thiếu.
- **Node `bus_expert`**: Chuyên trách gọi tool tra cứu vé xe khách.
- **Node `hotel_expert`**: Chuyên trách gọi tool tra cứu phòng khách sạn.
- **Edge điều kiện `route_next_step`**: Nếu phát hiện xe đến trước giờ nhận phòng > 4 tiếng ➔ Kích hoạt thông báo cảnh báo khách hoặc gọi tool kiểm tra chính sách Early Check-in.
