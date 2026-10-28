# IMPORT là hành động "mượn" đồ nghề từ các thư viện người khác đã viết sẵn.
from fastapi import FastAPI
from app.models.schemas import ChatRequest, ChatResponse

# Khởi tạo ứng dụng FastAPI. 
# Bạn hãy tưởng tượng 'app' giống như một cô tiếp tân của nhà hàng. 
# Cô ấy sẽ đứng ở cửa để nhận yêu cầu từ khách (Frontend/Người dùng).
app = FastAPI(title="AI Booking Orchestrator API")

# @app.post("/chat") giống như việc tạo ra một cái quầy có biển hiệu "/chat".
# Chỉ những khách hàng mang yêu cầu đúng chuẩn (POST) mới được phục vụ.
# response_model=ChatResponse: Bắt buộc cô tiếp tân phải trả đồ ra đúng định dạng ChatResponse.
@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    # 'request' chính là gói hàng khách gửi tới (chứa session_id và message).
    
    # ---------------------------------------------------------
    # TẠI ĐÂY LÀ NƠI PHÉP THUẬT XẢY RA
    # Sau này, Cursor sẽ viết code để gọi con AI (LangGraph) ở đây.
    # AI sẽ đọc request.message, suy nghĩ, tìm vé, tìm phòng...
    # ---------------------------------------------------------
    
    # Tạm thời khi chưa có AI, chúng ta cứ trả về một câu chào mặc định.
    # Dữ liệu trả về bắt buộc phải tuân theo khuôn ChatResponse.
    return ChatResponse(reply="Đây là API gốc, AI đang đi vắng, vui lòng đợi...")
