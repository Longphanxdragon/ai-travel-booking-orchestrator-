# ==============================================================================
# BỘ ĐIỀU PHỐI ĐA TÁC TỬ (MULTI-AGENT ORCHESTRATOR - STATEGRAPH ENGINE)
# ------------------------------------------------------------------------------
# Dành cho người mới (Beginner Guide):
# Multi-Agent StateGraph hoạt động giống hệt một Ban chỉ huy trong công ty:
# 1. Router Node (Giám đốc): Đọc tin nhắn, phân loại xem khách muốn hỏi Vé Xe,
#    Phòng Khách Sạn, Chính Sách hay Combo cả hai.
# 2. Bus Specialist Node (Trưởng phòng Xe): Chạy công cụ tra cứu tồn kho xe thực tế.
# 3. Hotel Specialist Node (Trưởng phòng Khách sạn): Chạy công cụ tra cứu phòng thực tế.
# 4. Policy Specialist Node (Trưởng phòng Pháp lý/Chính sách): Chạy Hybrid Search
#    (BM25 + Dense + RRF k=60) để đọc điều khoản hủy vé, nhận phòng sớm.
# 5. CSP Constraint Solver Node (Trưởng phòng Điều vận): So khớp giờ xe đến và giờ
#    nhận phòng. Nếu lệch > 3 tiếng, tự động đề xuất Early Check-in.
# 6. Response Synthesizer Node (Thư ký tổng hợp): Gom toàn bộ thông tin chuẩn xác
#    thành một câu trả lời tiếng Việt trôi chảy, kèm nút hành động chốt chỗ.
# ==============================================================================

import time
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from app.core.guardrails import token_budget_guard
from app.core.telemetry import telemetry
from app.models.schemas import (
    ActionDTO,
    BusSearchCriteria,
    ChatRequest,
    ChatResponse,
    CrossDomainMatchResult,
    HotelSearchCriteria,
    PolicyDocumentHit,
)
from app.services.rag.hybrid_search import hybrid_policy_engine
from app.services.tools.data_cleaner_pipeline import ConversationDataCleaner
from app.services.tools.travel_tools import (
    check_cross_domain_constraints,
    search_bus_trips_tool,
    search_hotel_rooms_tool,
)


# ==============================================================================
# KHÔNG GIAN TRẠNG THÁI CHUNG CỦA ĐỒ THỊ (SHARED STATE MODEL)
# ==============================================================================
class AgentExecutionState(BaseModel):
    """
    State Container của LangGraph: Chiếc 'ba-lô' truyền dữ liệu qua từng Node.
    """

    session_id: str
    raw_query: str
    cleaned_query: str
    trace_id: str
    intent: Literal["BUS_ONLY", "HOTEL_ONLY", "COMBO", "POLICY_QA", "GENERAL_CONSULTATION"] = (
        "GENERAL_CONSULTATION"
    )
    destination: str = "Đà Lạt"
    bus_criteria: Optional[BusSearchCriteria] = None
    hotel_criteria: Optional[HotelSearchCriteria] = None
    policy_query: Optional[str] = None

    bus_results: List[Dict[str, Any]] = Field(default_factory=list)
    hotel_results: List[Dict[str, Any]] = Field(default_factory=list)
    policy_hits: List[PolicyDocumentHit] = Field(default_factory=list)
    cross_domain_result: Optional[CrossDomainMatchResult] = None

    execution_path: List[str] = Field(default_factory=list)
    final_reply: str = ""
    actions: List[ActionDTO] = Field(default_factory=list)


class TravelMultiAgentOrchestrator:
    """
    Tác tử Điều phối Trung tâm (Star-Topology Multi-Agent StateGraph).
    Điều phối luồng thực thi phi chu trình tất định (Deterministic DAG Execution).
    """

    @classmethod
    async def process_chat(cls, request: ChatRequest) -> ChatResponse:
        start_time = time.monotonic()
        trace_id = telemetry.new_trace_id()

        # ----------------------------------------------------------------------
        # BƯỚC 0: HÀNG RÀO PHÒNG THỦ TOKEN & BẢO VỆ PII (SRE & PRIVACY GUARDRAILS)
        # ----------------------------------------------------------------------
        decision = token_budget_guard.inspect(request.session_id, request.message)
        if not decision.allowed:
            telemetry.increment("guardrail_blocks")
            elapsed = int((time.monotonic() - start_time) * 1000)
            return ChatResponse(
                session_id=request.session_id,
                reply=decision.safe_fallback_reply or "Yêu cầu không được phê duyệt bởi bộ lọc an toàn.",
                intent_detected="BLOCKED_BY_GUARDRAIL",
                actions=[ActionDTO(type="WARNING", payload={"reason": decision.reason})],
                latency_ms=elapsed,
                trace_id=trace_id,
                execution_path=["GUARDRAIL_INTERCEPTOR"],
            )

        telemetry.increment("tokens_processed", decision.estimated_tokens)

        # Che giấu PII (Số điện thoại / Email) ngay tại cửa ngõ vào
        cleaned_text = ConversationDataCleaner.anonymize_pii(request.message)

        # Khởi tạo Shared State
        state = AgentExecutionState(
            session_id=request.session_id,
            raw_query=request.message,
            cleaned_query=cleaned_text,
            trace_id=trace_id,
        )

        # ----------------------------------------------------------------------
        # BƯỚC 1: ROUTER NODE - PHÂN TÍCH Ý ĐỊNH & LẬP KẾ HOẠCH (INTENT CLASSIFIER)
        # ----------------------------------------------------------------------
        cls._node_router(state)

        # ----------------------------------------------------------------------
        # BƯỚC 2: CHUYÊN GIA THỰC THI (SPECIALIST AGENTS DISPATCH)
        # ----------------------------------------------------------------------
        if state.intent in ["BUS_ONLY", "COMBO"]:
            cls._node_bus_specialist(state)

        if state.intent in ["HOTEL_ONLY", "COMBO"]:
            cls._node_hotel_specialist(state)

        if state.intent in ["POLICY_QA", "COMBO"] or any(
            k in state.cleaned_query.lower() for k in ["chính sách", "hủy", "phụ thu", "quy định"]
        ):
            cls._node_policy_specialist(state)

        # ----------------------------------------------------------------------
        # BƯỚC 3: CONSTRAINT SOLVER NODE - GIẢI QUYẾT RÀNG BUỘC CHÉO CSP
        # ----------------------------------------------------------------------
        if state.bus_results and state.hotel_results:
            cls._node_cross_domain_solver(state)

        # ----------------------------------------------------------------------
        # BƯỚC 4: SYNTHESIZER NODE - TỔNG HỢP CÂU TRẢ LỜI CHUẨN XÁC, ZERO ẢO GIÁC
        # ----------------------------------------------------------------------
        cls._node_synthesizer(state)

        elapsed_ms = int((time.monotonic() - start_time) * 1000)
        telemetry.record_request(latency_ms=elapsed_ms, intent=state.intent)

        return ChatResponse(
            session_id=state.session_id,
            reply=state.final_reply,
            intent_detected=state.intent,
            actions=state.actions,
            latency_ms=elapsed_ms,
            trace_id=state.trace_id,
            execution_path=state.execution_path,
        )

    # ==========================================================================
    # CÁC NODE XỬ LÝ TRONG ĐỒ THỊ TRẠNG THÁI (STATEGRAPH NODES)
    # ==========================================================================
    @classmethod
    def _node_router(cls, state: AgentExecutionState) -> None:
        """Node 1: Phân rã ngữ nghĩa câu hỏi và nhận diện điểm đến."""
        state.execution_path.append("ROUTER_NODE")
        msg = state.cleaned_query.lower()

        # Nhận diện điểm đến
        if any(k in msg for k in ["nha trang", "nhatrang", "biển"]):
            state.destination = "Nha Trang"
        elif any(k in msg for k in ["vũng tàu", "vung tau", "bãi sau"]):
            state.destination = "Vũng Tàu"
        else:
            state.destination = "Đà Lạt"

        has_bus = any(k in msg for k in ["xe", "vé", "limousine", "giường nằm", "cabin", "futa", "điền linh", "hoa mai", "an anh"])
        has_hotel = any(k in msg for k in ["khách sạn", "homestay", "phòng", "ở", "nghỉ", "resort", "bungalow", "colline", "seaview"])
        has_policy = any(k in msg for k in ["chính sách", "hủy phòng", "hoàn tiền", "đổi vé", "phạt cọc", "quy định"])

        if has_bus and has_hotel:
            state.intent = "COMBO"
        elif has_bus:
            state.intent = "BUS_ONLY"
        elif has_hotel:
            state.intent = "HOTEL_ONLY"
        elif has_policy:
            state.intent = "POLICY_QA"
        else:
            state.intent = "GENERAL_CONSULTATION"

    @classmethod
    def _node_bus_specialist(cls, state: AgentExecutionState) -> None:
        """Node 2: Tác tử Xe Khách - Chuẩn hóa tham số và thực thi Tool truy vấn CSDL."""
        state.execution_path.append("BUS_SPECIALIST_NODE")
        msg = state.cleaned_query.lower()

        pref_type = None
        if any(k in msg for k in ["phòng đôi", "cabin đôi", "cabin"]):
            pref_type = "Phòng Đôi"
        elif any(k in msg for k in ["limousine", "vip"]):
            pref_type = "Limousine"

        criteria = BusSearchCriteria(
            origin="Sài Gòn",
            destination=state.destination,
            preferred_type=pref_type,
            passengers=2 if "phòng đôi" in msg else 1,
        )
        state.bus_criteria = criteria
        state.bus_results = search_bus_trips_tool(criteria)

    @classmethod
    def _node_hotel_specialist(cls, state: AgentExecutionState) -> None:
        """Node 3: Tác tử Khách Sạn - Chuẩn hóa tham số và thực thi Tool truy vấn CSDL."""
        state.execution_path.append("HOTEL_SPECIALIST_NODE")
        msg = state.cleaned_query.lower()

        pet_req = any(k in msg for k in ["thú cưng", "chó", "mèo", "cún", "pet", "vật nuôi"])
        pref_room = None
        if "deluxe" in msg:
            pref_room = "Deluxe"
        elif "bungalow" in msg:
            pref_room = "Bungalow"
        elif "suite" in msg:
            pref_room = "Suite"

        criteria = HotelSearchCriteria(
            destination=state.destination,
            room_type_preference=pref_room,
            pet_friendly_required=pet_req,
        )
        state.hotel_criteria = criteria
        state.hotel_results = search_hotel_rooms_tool(criteria)

    @classmethod
    def _node_policy_specialist(cls, state: AgentExecutionState) -> None:
        """Node 4: Tác tử Chính Sách - Gọi động cơ Hybrid Search (BM25 + Dense + RRF k=60)."""
        state.execution_path.append("POLICY_SPECIALIST_NODE")
        query_text = state.cleaned_query
        state.policy_query = query_text
        state.policy_hits = hybrid_policy_engine.search(query=query_text, top_k=2, mode="hybrid_rrf")

    @classmethod
    def _node_cross_domain_solver(cls, state: AgentExecutionState) -> None:
        """Node 5: Bộ giải quyết Ràng buộc chéo CSP giữa phương tiện và lưu trú."""
        state.execution_path.append("CSP_CONSTRAINT_SOLVER_NODE")
        bus = state.bus_results[0]
        hotel = state.hotel_results[0]
        state.cross_domain_result = check_cross_domain_constraints(bus, hotel)

    @classmethod
    def _node_synthesizer(cls, state: AgentExecutionState) -> None:
        """Node 6: Thư ký Tổng Hợp - Tạo câu trả lời có cấu trúc và nút tương tác."""
        state.execution_path.append("RESPONSE_SYNTHESIZER_NODE")
        sections: List[str] = []

        # 1. Đoạn thông tin Xe khách
        if state.bus_results:
            b = state.bus_results[0]
            sections.append(
                f"🚌 **Phương tiện ({state.destination}):** Nhà xe **{b['operator_name']}** ({b['bus_type']}) "
                f"khởi hành {b['departure_time']}, cập bến lúc {b['arrival_time']}. "
                f"Hiện còn đúng **{b['available_seats']} ghế/phòng trống** (Giá: {b['fare_vnd']:,}đ/vé). "
                f"Điểm đón: {b['pickup_point']}."
            )

        # 2. Đoạn thông tin Khách sạn
        if state.hotel_results:
            h = state.hotel_results[0]
            pet_badge = " (🐾 Cho phép mang thú cưng)" if h.get("pet_allowed") else ""
            sections.append(
                f"🏨 **Lưu trú ({state.destination}):** **{h['hotel_name']}** ({h['location']}) - Hạng phòng **{h['room_type']}**{pet_badge}. "
                f"Hiện còn **{h['available_rooms']} phòng trống** (Giá: {h['price_per_night']:,}đ/đêm). "
                f"Chính sách: {h['policy']}"
            )

        # 3. Đoạn lưu ý Ràng buộc chéo CSP (nếu có xung đột giờ)
        if state.cross_domain_result and state.cross_domain_result.is_time_conflict:
            sections.append(f"⚠️ **Lưu ý lịch trình & Early Check-in:** {state.cross_domain_result.recommendation}")

        # 4. Đoạn điều khoản chính sách từ Hybrid Search RRF (nếu có truy xuất)
        if state.policy_hits and (state.intent == "POLICY_QA" or any(k in state.cleaned_query.lower() for k in ["chính sách", "hủy", "phạt"])):
            top_hit = state.policy_hits[0]
            sections.append(
                f"📋 **Điều khoản áp dụng ({top_hit.title}):** {top_hit.content} "
                f"*(Truy xuất chính xác qua Hybrid Search BM25 Rank {top_hit.bm25_rank}, RRF Score: {top_hit.rrf_score})*"
            )

        # 5. Phản hồi chung khi câu hỏi quá ngắn
        if not sections:
            sections.append(
                "Dạ em là Trợ lý AI chuyên điều phối lịch trình du lịch thông minh. "
                "Em có thể giúp anh/chị tra cứu tồn kho xe Limousine và phòng khách sạn thời gian thực "
                "tại Đà Lạt, Nha Trang và Vũng Tàu, tự động xử lý lệch giờ check-in và chính sách hoàn hủy. "
                "Anh/chị dự định khởi hành đến đâu và vào ngày nào ạ?"
            )

        sections.append(
            "👉 *Thông tin trên được kiểm tra trực tiếp từ cơ sở dữ liệu thời gian thực. "
            "Anh/chị có thể liên hệ trực tiếp tổng đài nhà xe hoặc lễ tân khách sạn để chốt giữ chỗ nhé!*"
        )

        state.final_reply = "\n\n".join(sections)

        # Sinh Action DTO
        if state.bus_results and state.hotel_results:
            state.actions.append(
                ActionDTO(
                    type="HOLD_SUGGESTION",
                    payload={
                        "trip_id": state.bus_results[0]["trip_id"],
                        "room_id": state.hotel_results[0]["room_id"],
                        "destination": state.destination,
                    },
                )
            )
        elif state.bus_results:
            state.actions.append(
                ActionDTO(
                    type="REDIRECT_OPERATOR",
                    payload={"trip_id": state.bus_results[0]["trip_id"], "destination": state.destination},
                )
            )
        elif state.hotel_results:
            state.actions.append(
                ActionDTO(
                    type="REDIRECT_OPERATOR",
                    payload={"room_id": state.hotel_results[0]["room_id"], "destination": state.destination},
                )
            )
