import asyncio
import sys
import os

# Thiết lập đường dẫn để import chuẩn xác
sys.path.insert(0, os.path.abspath("."))

from app.models.schemas import ChatRequest
from app.services.agent.orchestrator import TravelMultiAgentOrchestrator

# Danh sách các câu hỏi test bẫy điển hình
TEST_CASES = [
    {
        "id": "TEST_CASE_1 (Ràng buộc chéo xe + khách sạn mang chó)",
        "query": "Tối mai có xe phòng đôi đi Đà Lạt và khách sạn ở Đà Lạt cho mang chó không em? SĐT a: 0901234567"
    },
    {
        "id": "TEST_CASE_2 (Chỉ hỏi xe khách Limousine Nha Trang)",
        "query": "Tìm giúp tôi 2 vé xe Limousine đi Nha Trang xuất phát từ Sài Gòn tối nay"
    },
    {
        "id": "TEST_CASE_3 (Chỉ hỏi khách sạn trung tâm)",
        "query": "Đà Lạt có khách sạn nào gần trung tâm chợ không shop?"
    }
]

async def run_interactive_demo():
    print("=" * 70)
    print("  🚀 DEMO KIỂM THỬ TÁC TỬ ĐA NHIỆM (AI TRAVEL ORCHESTRATOR)")
    print("=" * 70)

    # 1. Chạy tự động các test cases mẫu
    for tc in TEST_CASES:
        print(f"\n👉 [{tc['id']}]")
        print(f"👤 Khách hỏi: \"{tc['query']}\"")
        req = ChatRequest(session_id="demo_session", message=tc["query"])
        res = await TravelMultiAgentOrchestrator.process_chat(req)
        
        print("\n🤖 AI Trả lời:")
        print(res.reply)
        print(f"\n⏱️ Thời gian xử lý: {res.latency_ms} ms | Ý định: {res.intent_detected}")
        print("-" * 70)

    # 2. Chế độ gõ câu hỏi tự do trực tiếp
    print("\n" + "=" * 70)
    print("  💬 CHẾ ĐỘ CHAT TỰ DO TRỰC TIẾP (Gõ câu hỏi bất kỳ, gõ 'exit' để thoát)")
    print("=" * 70)
    
    while True:
        try:
            user_msg = input("\n👤 Bạn gõ câu hỏi: ")
            if user_msg.strip().lower() in ["exit", "quit", "thoat", "q"]:
                print("👋 Đã thoát phiên kiểm thử demo!")
                break
            if not user_msg.strip():
                continue

            req = ChatRequest(session_id="live_test", message=user_msg)
            res = await TravelMultiAgentOrchestrator.process_chat(req)
            print("\n🤖 AI Trả lời:")
            print(res.reply)
            print(f"\n⏱️ Độ trễ: {res.latency_ms} ms")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Đã thoát phiên kiểm thử demo!")
            break

if __name__ == "__main__":
    asyncio.run(run_interactive_demo())
