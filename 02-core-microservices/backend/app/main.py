# ==============================================================================
# FASTAPI APPLICATION ENTRYPOINT - AI TRAVEL BOOKING ORCHESTRATOR
# Plug-and-Play Microservice Architecture
# ==============================================================================

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import ChatRequest, ChatResponse
from app.services.agent.orchestrator import TravelMultiAgentOrchestrator
from app.services.tools.data_cleaner_pipeline import ConversationDataCleaner

app = FastAPI(
    title="AI Travel Booking Orchestrator API",
    description="Microservice giải quyết triệt để 3 bài toán: Ảo giác dữ liệu động, Ràng buộc chéo (Multi-Agent CSP) và Sai lệch từ khóa.",
    version="1.0.0"
)

# Cấu hình CORS để cắm vào bất kỳ Web / App / Chatwoot / Zalo nào
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Kiểm tra sức khỏe dịch vụ."""
    return {"status": "healthy", "service": "ai-travel-booking-orchestrator", "version": "1.0.0"}

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, background_tasks: BackgroundTasks):
    """
    Điểm chạm (Endpoint) duy nhất tiếp nhận hội thoại từ người dùng đa kênh.
    Xử lý phản hồi thần tốc (< 500ms) và đẩy việc lưu trữ dữ liệu độc quyền ra chạy ngầm.
    """
    # 1. Tác tử Multi-Agent phân rã và xử lý câu hỏi
    response = await TravelMultiAgentOrchestrator.process_chat(request)

    # 2. Chạy ngầm (Background Task) đường ống bóc tách dữ liệu độc quyền không làm chậm phản hồi
    def background_etl():
        # Lọc rác và bảo mật PII
        anonymized = ConversationDataCleaner.anonymize_pii(request.message)
        # Bóc tách ý định để làm giàu kho dữ liệu du lịch độc quyền (Data Flywheel)
        intent = ConversationDataCleaner.extract_intent(request.session_id, [{"content": anonymized}])
        # Sau này sẽ ghi trực tiếp vào PostgreSQL bảng travel_intents_lake

    background_tasks.add_task(background_etl)

    return response
