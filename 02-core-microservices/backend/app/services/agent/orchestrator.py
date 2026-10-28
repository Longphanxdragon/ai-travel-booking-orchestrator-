# -------------------------------------------------------------------------
# LỜI NHẮN DÀNH CHO BẠN (Người mới bắt đầu):
# File này là nơi chứa "Bộ não Đa tác tử" (Multi-Agent).
# Hãy tưởng tượng Tác tử (Agent) là các nhân viên ảo trong một công ty:
# - Một anh nhân viên chuyên tìm vé xe (Bus Agent).
# - Một chị nhân viên chuyên tìm phòng (Hotel Agent).
# - Và một ông Giám đốc (Orchestrator) đứng ra chỉ đạo hai người kia.
# -------------------------------------------------------------------------

# BƯỚC THỰC HÀNH "VIBE CODING" CÙNG CURSOR:
# 1. Bạn mở phần mềm Cursor. Mở cái folder "backend" này lên.
# 2. Bạn mở chính file orchestrator.py này ra.
# 3. Bấm Ctrl + L để gọi khung AI của Cursor hiện lên.
# 4. Dán nguyên đoạn văn bản bên dưới vào và Enter:

"""
Mày hãy đóng vai một Senior Python Developer.
Tao muốn xây dựng một hệ thống Đa tác tử (Multi-Agent) bằng LangGraph trong file này.

1. Hãy đọc file app/models/schemas.py để hiểu các "khuôn dữ liệu" (VeXeKhach, PhongKhachSan).
2. Hãy dùng cú pháp @langgraph để tự đọc các file hướng dẫn trong thư mục _references của tao.
3. Code cho tao một luồng StateGraph đơn giản:
   - Có một biến SharedState để lưu lời khách hàng.
   - Một Node (Giám đốc) đọc lời khách.
   - Nếu khách hỏi xe, rẽ nhánh (Route) sang Node Bus Agent. Yêu cầu Bus Agent bắt buộc phải xuất ra dữ liệu tuân theo khuôn `VeXeKhach`.
   
Lưu ý: Viết thật nhiều comment tiếng Việt dễ hiểu vào code để người mới học cũng đọc được nhé.
"""
