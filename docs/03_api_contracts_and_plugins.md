# 🔌 HỢP ĐỒNG API & KIẾN TRÚC PLUG-AND-PLAY
*(Tài liệu dành cho Kỹ sư & Đối tác tích hợp Lõi AI vào hệ thống khác)*

---

## 1. NGUYÊN TẮC THIẾT KẾ PLUG-AND-PLAY (CẮM RÚT ĐỘC LẬP)

Lõi AI Orchestrator được thiết kế như một **Headless AI Microservice**. Nó không phụ thuộc vào giao diện hiển thị (UI agnostic) và có thể cắm vào bất kỳ hệ thống kinh doanh nào thông qua chuẩn RESTful API và Webhook.

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Booking   │    │  Mobile App     │    │   Zalo / FB     │
│   (React/Vue)   │    │ (Flutter/React) │    │  (Chatwoot OA)  │
└────────┬────────┘    └────────┬────────┘    └────────┬────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                ▼ HTTP POST JSON
               ┌─────────────────────────────────┐
               │  AI Booking Orchestrator API    │
               │  Endpoint: /api/v1/chat         │
               └────────────────┬────────────────┘
                                │
               ┌────────────────┴────────────────┐
               ▼                                 ▼
      ┌─────────────────┐               ┌─────────────────┐
      │ Qdrant Vector   │               │ PostgreSQL PMS  │
      │ (Chính sách/PDF)│               │ (Xe & Phòng)    │
      └─────────────────┘               └─────────────────┘
```

---

## 2. ĐẶC TẢ API GIAO TIẾP (API SPECIFICATION)

### 2.1. Endpoint Tiếp nhận Hội thoại
- **URL:** `POST /api/v1/chat`
- **Content-Type:** `application/json`

#### Request Body
```json
{
  "session_id": "usr_9988a1b2",
  "inbox_id": 101,
  "message": "Tôi muốn đặt 2 vé xe giường nằm đi Nha Trang tối thứ 6 tuần này và 1 phòng đôi gần biển.",
  "channel": "webchat"
}
```

#### Response Body (Thành công - 200 OK)
```json
{
  "session_id": "usr_9988a1b2",
  "reply": "Dạ em đã kiểm tra chuyến xe và phòng cho anh/chị:\n1. 🚌 Xe giường nằm Limousine (Hãng Phương Trang) xuất phát 22:30 Thứ Sáu, còn đúng 4 ghế tầng dưới (Giá: 320.000đ/vé).\n2. 🏨 Khách sạn SeaView Nha Trang (cách biển 50m) còn phòng Deluxe Double nhận sáng Thứ Bảy (Giá: 750.000đ/đêm).\n\n⚠️ Lưu ý: Xe tới bến lúc 05:30 sáng, giờ nhận phòng chuẩn là 14:00. Khách sạn hỗ trợ giữ hành lý miễn phí hoặc phụ thu 200.000đ để nhận phòng sớm lúc 06:00.\n\nAnh/chị có muốn giữ chỗ ngay trong 15 phút không ạ?",
  "intent_detected": "COMBO_BOOKING",
  "actions": [
    {
      "type": "SHOW_HOLD_BUTTON",
      "hold_payload": {
        "trip_id": "BUS-NT-2230",
        "room_id": "HOTEL-SV-01",
        "seats": 2,
        "nights": 1
      }
    }
  ],
  "latency_ms": 1820
}
```

---

## 3. CÁCH NHÚNG LÕI NÀY VÀO DỰ ÁN KHÁC TRONG 3 BƯỚC

Nếu một doanh nghiệp hoặc đồ án khác muốn mượn Lõi AI này:
1. **Bước 1:** Kéo Docker Image hoặc clone folder `02-core-microservices/backend`.
2. **Bước 2:** Cung cấp thông tin kết nối CSDL hiện có qua biến môi trường (`DATABASE_URL`, `QDRANT_URL`).
3. **Bước 3:** Gửi tin nhắn từ bất kỳ kênh nào vào `POST /api/v1/chat`, hệ thống sẽ tự lo toàn bộ phần logic suy luận, tìm kiếm và trả về câu trả lời chuẩn xác.
