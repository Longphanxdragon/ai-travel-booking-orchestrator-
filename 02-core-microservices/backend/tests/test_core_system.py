import pytest
import asyncio
from app.models.schemas import ChatRequest, ChatResponse
from app.services.agent.orchestrator import TravelMultiAgentOrchestrator
from app.services.tools.data_cleaner_pipeline import ConversationDataCleaner

def test_pydantic_schemas():
    """Kiểm tra tính hợp lệ của khuôn mẫu Pydantic v2."""
    req = ChatRequest(session_id="s1", message="Tìm xe", channel="webchat")
    assert req.session_id == "s1"
    assert req.channel == "webchat"

def test_pii_cleaner():
    """Kiểm tra chức năng che số điện thoại và email bảo mật."""
    raw = "Số điện thoại của tôi là 0901234567, email: test@gmail.com"
    clean = ConversationDataCleaner.anonymize_pii(raw)
    assert "090****567" in clean
    assert "[PROTECTED_EMAIL]" in clean

def test_orchestrator_cross_domain_reasoning():
    """Kiểm tra khả năng suy luận ràng buộc chéo và chống ảo giác."""
    req = ChatRequest(
        session_id="test_suite_01",
        message="Tối mai có xe phòng đôi đi Đà Lạt và khách sạn cho mang chó không em?"
    )
    res: ChatResponse = asyncio.run(TravelMultiAgentOrchestrator.process_chat(req))
    
    assert res.session_id == "test_suite_01"
    assert "Điền Linh Limousine" in res.reply
    assert "Homestay Thung Lũng Mây" in res.reply
    assert "Lưu ý lịch trình" in res.reply # Đã phát hiện lệch giờ 8 tiếng!
    assert res.latency_ms is not None
