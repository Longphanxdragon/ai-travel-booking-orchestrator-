# 🔌 KIẾN TRÚC ADAPTER PLUG-IN VÀO VEXERE & CÁC NỀN TẢNG OTA
*(Tài liệu thiết kế kỹ thuật - Technical Architecture for External Provider Integrations)*

---

## 1. NGUYÊN LÝ CỐT LÕI: MẪU THIẾT KẾ ADAPTER (ADAPTER PATTERN)

Để Lõi AI Orchestrator có thể "cắm" (plug-in) vào VeXeRe, Traveloka, Agoda hoặc bất kỳ PMS/ERP của nhà xe nào mà **không làm thay đổi 1 dòng code trong Bộ não AI (LangGraph Brain)**, chúng ta áp dụng mẫu thiết kế **Provider Adapter Pattern (Interface Segregation)**.

```text
                      ┌──────────────────────────────────────┐
                      │    LÕI AI ORCHESTRATOR (LangGraph)   │
                      │                                      │
                      │  Công cụ trừu tượng (Abstract Tool): │
                      │  `check_bus_schedule(route, date)`   │
                      └──────────────────┬───────────────────┘
                                         │
                         Hợp đồng trừu tượng (BaseBusProvider)
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│  MockLocalAdapter    │      │    VexereAdapter     │      │   GenericOTAAdapter  │
│  (DB Postgres nội bộ)│      │  (Public/Partner API)│      │ (Traveloka / Booking)│
└──────────────────────┘      └──────────────────────┘      └──────────────────────┘
```

> **Điểm ăn tiền với Hội đồng Đồ án:**
> Khẳng định tính độc lập tuyệt đối của Microservice: AI chỉ giao tiếp qua một **Interface trừu tượng**. Việc dữ liệu lấy từ SQLite nội bộ, hay gọi API thật của VeXeRe chỉ là việc **thay đổi cấu hình (Plug-and-Play)** mà không sửa logic suy luận của AI.

---

## 2. BA PHƯƠNG ÁN KẾT NỐI VÀO VEXERE THỰC TẾ

Tùy vào mức độ hợp tác hoặc giai đoạn làm đồ án, bạn có 3 cách thực tế để cắm vào VeXeRe:

### Phương án A: Đối tác B2B (Official Partner API) - *Chuẩn công nghiệp nhất*
- **Bản chất:** VeXeRe cung cấp hệ thống API dành cho đại lý và đối tác (B2B Affiliate/Agent API).
- **Cách tích hợp:**
  - Đăng ký tài khoản Partner / Affiliate với VeXeRe.
  - Lấy `API_KEY` và `PARTNER_ID`.
  - Adapter gửi HTTP GET/POST trực tiếp tới Endpoint của VeXeRe để lấy danh sách chuyến xe và trạng thái ghế trống thời gian thực.
- **Ưu điểm:** Tốc độ phản hồi cực nhanh (< 300ms), dữ liệu chính xác 100%, có cơ chế giữ chỗ và xuất vé chính thức.

### Phương án B: Reverse Engineering / Session Hooking - *Dành cho Prototype/Demo đồ án*
- **Bản chất:** Bắt các endpoint Public Search mà giao diện web/app của VeXeRe sử dụng khi người dùng tìm kiếm chuyến đi.
- **Endpoint ví dụ:** `https://api.vexere.com/v1/trips?from=TP-Ho-Chi-Minh&to=Da-Lat&date=2026-11-01`
- **Cơ chế triển khai:**
  - Viết một Python Adapter sử dụng `httpx` hoặc `aiohttp` giả lập Header trình duyệt.
  - Phân tích JSON trả về từ VeXeRe và map (ánh xạ) về khuôn dữ liệu `VeXeKhach` của chúng ta.
- **Ưu điểm:** Không cần ký hợp đồng B2B, có dữ liệu thật 100% của hàng trăm nhà xe đang chạy trên đường để demo trước Hội đồng.

### Phương án C: Headless Browser Driver (Playwright / Puppeteer Micro-service)
- **Bản chất:** Nếu VeXeRe chặn bot bằng Cloudflare/WAF, ta dựng một Microservice chạy trình duyệt ẩn danh (Headless Chromium).
- **Cơ chế:** Khi khách hỏi xe, Agent gửi lệnh tới Microservice này ➔ Playwright tự gõ tìm kiếm trên Vexere.com ➔ trích xuất dữ liệu trả về cho AI trong 2-3 giây.

---

## 3. THIẾT KẾ MÃ NGUỒN PLUG-IN CHUẨN (PYTHON FASTAPI)

### 3.1. Định nghĩa Interface trừu tượng (`base_provider.py`)
```python
from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel

class BusTripDTO(BaseModel):
    trip_id: str
    operator_name: str          # Tên nhà xe (Phương Trang, Thành Bưởi...)
    bus_type: str               # Giường nằm, Limousine
    departure_time: str         # 22:30 2026-11-01
    arrival_time: str           # 05:30 2026-11-02
    available_seats: int        # Số ghế trống
    fare_vnd: int               # Giá vé

class BaseBusProvider(ABC):
    @abstractmethod
    async def search_trips(self, from_loc: str, to_loc: str, travel_date: str) -> List[BusTripDTO]:
        """Phương thức bắt buộc mọi nhà cung cấp (VeXeRe, DB nội bộ) phải hiện thực."""
        pass
```

### 3.2. Cài đặt VeXeRe Adapter (`vexere_adapter.py`)
```python
import httpx
from typing import List
from .base_provider import BaseBusProvider, BusTripDTO

class VexereAdapter(BaseBusProvider):
    def __init__(self, api_key: str = None, base_url: str = "https://api.vexere.com"):
        self.api_key = api_key
        self.base_url = base_url

    async def search_trips(self, from_loc: str, to_loc: str, travel_date: str) -> List[BusTripDTO]:
        headers = {"User-Agent": "Mozilla/5.0"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # Gọi API VeXeRe (hoặc endpoint đối tác)
        async with httpx.AsyncClient() as client:
            # Tham số tra cứu thực tế
            response = await client.get(
                f"{self.base_url}/v1/trips",
                params={"from": from_loc, "to": to_loc, "date": travel_date},
                headers=headers,
                timeout=5.0
            )
            data = response.json()

        # Ánh xạ (Mapping) từ dữ liệu VeXeRe sang chuẩn DTO của Lõi AI
        trips = []
        for item in data.get("trips", []):
            trips.append(BusTripDTO(
                trip_id=str(item.get("id")),
                operator_name=item.get("comp_name", "Nhà xe đối tác"),
                bus_type=item.get("bus_type", "Giường nằm"),
                departure_time=item.get("dep_time"),
                arrival_time=item.get("arr_time"),
                available_seats=int(item.get("empty_seats", 0)),
                fare_vnd=int(item.get("fare", 0))
            ))
        return trips
```

### 3.3. Cắm rút động qua biến môi trường (`ENV`)
Trong file cấu hình hệ thống:
```bash
# Chọn Adapter muốn cắm vào hệ thống:
BUS_PROVIDER=vexere      # Hoặc: internal_db, traveloka
VEXERE_API_KEY=your_partner_api_key_here
```

Và trong Agent Factory:
```python
def get_bus_provider() -> BaseBusProvider:
    provider = os.getenv("BUS_PROVIDER", "internal_db")
    if provider == "vexere":
        return VexereAdapter()
    return InternalDatabaseAdapter() # Cắm CSDL Postgres nội bộ
```

---

## 4. GIÁ TRỊ THƯƠNG MẠI VÀ ĐỒ ÁN
1. **Khả năng thương mại (Plug & Play B2B):** Khi đi pitching với các công ty du lịch hoặc nhà xe tư nhân, bạn chỉ cần cắm Adapter tương ứng của họ vào là hệ thống chạy ngay lập tức.
2. **Khả năng mở rộng (Scalability):** Hôm nay là VeXeRe, ngày mai có thể cắm thêm Bamboo Airways, Vietnam Airlines, hoặc Booking.com mà không cần viết lại con AI.
