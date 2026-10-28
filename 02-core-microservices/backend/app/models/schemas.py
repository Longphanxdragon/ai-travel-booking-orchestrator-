# Pydantic là một thư viện giúp kiểm tra tính hợp lệ của dữ liệu.
# BaseModel giống như một cái "Khuôn đúc bánh". Nếu bột đổ vào không đúng khuôn, nó sẽ báo lỗi ngay.
from pydantic import BaseModel, Field
from typing import Optional

# 1. Khuôn dành cho tin nhắn mà Khách hàng gửi lên
class ChatRequest(BaseModel):
    # Field(...) có nghĩa là thông tin này BẮT BUỘC phải có, không được thiếu.
    # description="" là lời giải thích bí mật dành riêng cho con AI hiểu biến này dùng để làm gì.
    session_id: str = Field(..., description="Mã số của phiên chat, dùng để máy chủ nhớ lịch sử nói chuyện.")
    message: str = Field(..., description="Câu hỏi mà khách hàng gõ vào.")

# 2. Khuôn dành cho câu trả lời mà AI trả về cho Khách hàng
class ChatResponse(BaseModel):
    reply: str = Field(..., description="Câu trả lời cuối cùng của AI sau khi đã suy nghĩ xong.")

# 3. Khuôn trói buộc AI - KHÔNG CHO AI ẢO GIÁC KHI TÌM VÉ XE
# Khi AI muốn tìm vé xe, ta ép nó phải điền đúng 3 ô thông tin này. Nó không được tự bịa ra thông tin khác.
class VeXeKhach(BaseModel):
    route: str = Field(..., description="Tuyến đường cần đi (Ví dụ: SG-NhaTrang)")
    date: str = Field(..., description="Ngày xuất phát, bắt buộc viết theo chuẩn YYYY-MM-DD")
    
    # Optional[str] nghĩa là thông tin này CÓ THỂ BỎ QUA nếu khách chưa cung cấp.
    time: Optional[str] = Field(None, description="Thời gian đi mong muốn (Sáng/Chiều/Tối).")

# 4. Khuôn trói buộc AI - KHI TÌM PHÒNG KHÁCH SẠN
class PhongKhachSan(BaseModel):
    location: str = Field(..., description="Khu vực khách sạn (Ví dụ: Gần biển, Trung tâm)")
    check_in: str = Field(..., description="Ngày khách muốn nhận phòng")
    check_out: str = Field(..., description="Ngày khách muốn trả phòng")
    
    # bool có nghĩa là giá trị này chỉ được phép là Đúng (True) hoặc Sai (False)
    early_checkin_required: bool = Field(False, description="Khách có cần nhận phòng sớm không? (Mặc định là Sai)")
