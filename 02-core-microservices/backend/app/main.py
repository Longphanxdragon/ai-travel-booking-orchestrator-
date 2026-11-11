# ==============================================================================
# FASTAPI APPLICATION ENTRYPOINT - AI TRAVEL BOOKING ORCHESTRATOR
# ------------------------------------------------------------------------------
# Dành cho người mới (Beginner Guide):
# File main.py là "Cổng chính" của toàn bộ hệ thống Microservice:
# 1. /health: Bác sĩ khám sức khỏe (Kubernetes Liveness / Readiness Probe).
# 2. /metrics: Phòng điều khiển hiển thị tốc độ phản hồi p50, p95, số vụ PII đã che.
# 3. /api/v1/chat: Cửa nhận khách chính — AI trò chuyện, đối khớp vé xe và khách sạn.
# 4. /api/v1/policy/search: Cửa tra cứu chính sách bằng Hybrid Search BM25 + Dense + RRF.
# 5. /api/v1/reservations/hold: Cửa giao dịch khóa bi quan ACID giữ chỗ 15 phút.
# 6. /api/v1/webhook/chatwoot: Cửa kết nối trực tiếp với Facebook Messenger / Zalo OA.
# ==============================================================================

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.guardrails import rate_limiter
from app.core.telemetry import telemetry
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    ChatwootIncomingWebhook,
    ChatwootOutgoingReply,
    PolicySearchRequest,
    PolicySearchResponse,
    ReservationHoldRequest,
    ReservationHoldResponse,
)
from app.services.agent.orchestrator import TravelMultiAgentOrchestrator
from app.services.rag.hybrid_search import hybrid_policy_engine
from app.services.tools.data_cleaner_pipeline import ConversationDataCleaner, data_flywheel_store
from app.services.tools.travel_tools import db_engine

app = FastAPI(
    title=settings.app_name,
    description=(
        "Microservice Trí tuệ Nhân tạo Đa nhiệm giải quyết triệt để 3 bài toán nan giải: "
        "Ảo giác dữ liệu động (Function Calling ACID), Sai lệch từ khóa (Hybrid Search BM25 + RRF), "
        "và Ràng buộc chéo di chuyển & lưu trú (Multi-Agent StateGraph CSP)."
    ),
    version=settings.app_version,
)

# Cấu hình CORS mở để cắm vào Webchat, React Native App, Chatwoot, hoặc Zalo Mini App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# 1. ENDPOINTS HẠ TẦNG & SỨC KHỎE HỆ THỐNG (SRE & OBSERVABILITY)
# ==============================================================================
@app.get("/health", tags=["Infrastructure"])
async def health_check():
    """Kiểm tra nhịp tim của dịch vụ (Kubernetes Liveness Probe)."""
    return {
        "status": "healthy",
        "service": "ai-travel-booking-orchestrator",
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.get("/metrics", tags=["Infrastructure"])
async def get_system_metrics():
    """Báo cáo chỉ số vận hành SRE: Độ trễ p50, p95, p99, PII che giấu, RRF queries."""
    return telemetry.snapshot()


@app.get("/api/v1/analytics/data-flywheel", tags=["Analytics"])
async def get_data_flywheel_insights():
    """Báo cáo thị trường tự động bóc tách từ Hồ Dữ Liệu Ý Định (Data Flywheel Lake)."""
    return data_flywheel_store.analytics_summary()


# ==============================================================================
# 2. ENDPOINT CHÍNH: HỘI THOẠI ĐA TÁC TỬ (MULTI-AGENT CORE)
# ==============================================================================
@app.post("/api/v1/chat", response_model=ChatResponse, tags=["AI Core"])
async def chat_endpoint(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    x_forwarded_for: str = Header(None),
):
    """
    Điểm chạm duy nhất tiếp nhận câu hỏi của khách hàng:
    - Áp dụng Rate Limiter chống spam.
    - Chạy Multi-Agent StateGraph điều phối giải quyết ràng buộc chéo CSP.
    - Đẩy tác vụ làm sạch PII và bóc tách dữ liệu độc quyền ra chạy ngầm (Background Task).
    """
    # Kiểm tra Rate Limiting
    client_key = request.session_id or x_forwarded_for or "anonymous_client"
    allowed, remaining = rate_limiter.allow_request(client_key)
    if not allowed:
        telemetry.increment("rate_limit_blocks")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Bạn đang gửi tin nhắn quá nhanh. Vui lòng chờ 30 giây trước khi tiếp tục.",
        )

    # 1. Tác tử Multi-Agent phân rã và xử lý câu hỏi
    response = await TravelMultiAgentOrchestrator.process_chat(request)

    # 2. Chạy ngầm (Background Task) đường ống Data Flywheel (0ms ảnh hưởng tốc độ khách)
    def background_data_flywheel_task(sess_id: str, raw_msg: str):
        ConversationDataCleaner.extract_intent(
            session_id=sess_id,
            raw_messages=[{"content": raw_msg}],
        )

    background_tasks.add_task(background_data_flywheel_task, request.session_id, request.message)

    return response


# ==============================================================================
# 3. ENDPOINT TÌM KIẾM LAI CHÍNH SÁCH (HYBRID SEARCH: BM25 + DENSE + RRF k=60)
# ==============================================================================
@app.post("/api/v1/policy/search", response_model=PolicySearchResponse, tags=["Retrieval Engine"])
async def search_policy_endpoint(req: PolicySearchRequest):
    """
    Tra cứu điều khoản khách sạn, nhà xe bằng thuật toán Hybrid Search:
    Kết hợp BM25 (chính xác từ vựng) và Dense Vector (ngữ nghĩa) qua Reciprocal Rank Fusion k=60.
    """
    hits = hybrid_policy_engine.search(query=req.query, top_k=req.top_k, mode=req.mode)
    return PolicySearchResponse(
        query=req.query,
        mode=req.mode,
        rrf_k=settings.rrf_k,
        results=hits,
    )


# ==============================================================================
# 4. ENDPOINT GIAO DỊCH KHÓA BI QUAN ACID & BẮN CHATOPS (TRANSACTION ENGINE)
# ==============================================================================
@app.post("/api/v1/reservations/hold", response_model=ReservationHoldResponse, tags=["Transactions"])
async def create_reservation_hold(req: ReservationHoldRequest):
    """
    Thực thi giao dịch Khóa Bi quan (Pessimistic Hold) tồn kho xe khách và phòng khách sạn.
    Chống hiện tượng Bán khống (Overbooking) 100% bằng cơ chế khóa nguyên tử ACID (TTL = 15 phút),
    đồng thời phát cảnh báo ChatOps về điện thoại Telegram của chủ doanh nghiệp.
    """
    res = await db_engine.execute_pessimistic_hold(req)
    return res


# ==============================================================================
# 5. ADAPTER TÍCH HỢP CHATWOOT WEBHOOK ĐA KÊNH (IMMUTABLE CONTRACT COMPLIANCE)
# Khớp 100% tệp 03-shared-contracts/webhook-schemas.json
# ==============================================================================
@app.post("/api/v1/webhook/chatwoot", response_model=ChatwootOutgoingReply, tags=["Integrations"])
async def chatwoot_webhook_adapter(payload: ChatwootIncomingWebhook, background_tasks: BackgroundTasks):
    """
    Cổng cắm rút tương thích ngược với Chatwoot Omnichannel CRM (Facebook, Zalo, WhatsApp).
    Nhận tin nhắn khách gửi -> Chuyển vào Lõi AI Multi-Agent -> Trả về JSON đúng hợp đồng Chatwoot.
    """
    # Chỉ xử lý tin nhắn mới từ khách hàng (bỏ qua tin nhắn outgoing của chính bot)
    if payload.event != "message_created" or payload.message_type != "incoming":
        return ChatwootOutgoingReply(content="OK", private=True)

    session_id = f"cw_{payload.inbox_id}_{payload.conversation_id}"
    req = ChatRequest(
        session_id=session_id,
        message=payload.content,
        channel="chatwoot_omnichannel",
        inbox_id=payload.inbox_id,
    )

    ai_res = await TravelMultiAgentOrchestrator.process_chat(req)

    # Chạy ngầm đường ống Data Flywheel
    background_tasks.add_task(
        ConversationDataCleaner.extract_intent,
        session_id,
        [{"content": payload.content}],
    )

    return ChatwootOutgoingReply(
        content=ai_res.reply,
        message_type="outgoing",
        content_type="text",
        content_attributes={
            "intent": ai_res.intent_detected,
            "latency_ms": ai_res.latency_ms,
            "actions": [a.model_dump() for a in ai_res.actions],
        },
    )
