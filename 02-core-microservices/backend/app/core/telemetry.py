# ==============================================================================
# HỆ THỐNG QUAN SÁT & ĐO LƯỜNG HIỆU NĂNG SRE (OBSERVABILITY & TELEMETRY)
# ------------------------------------------------------------------------------
# Dành cho người mới (Beginner Guide):
# Trong các công ty công nghệ lớn (Google, Meta, Uber), một hệ thống chạy được là
# chưa đủ — kỹ sư phải nhìn thấy "nhịp tim" của hệ thống theo thời gian thực:
# - Tốc độ phản hồi trung vị (p50) và trường hợp xấu (p95, p99) là bao nhiêu mili-giây?
# - Có bao nhiêu số điện thoại khách hàng đã được che giấu (PII Masked)?
# - Có bao nhiêu xung đột lệch giờ xe/khách sạn đã được AI cứu nguy kịp thời?
# ==============================================================================

import math
import uuid
from collections import Counter, deque
from datetime import datetime, timezone
from typing import Any, Deque, Dict, List


class TelemetryRegistry:
    """
     Trung tâm thu thập chỉ số vận hành thời gian thực (In-memory Prometheus-style Metrics).
    Lưu trữ tối đa 2.000 mẫu độ trễ gần nhất bằng cấu trúc Ring Buffer O(1) RAM.
    """

    def __init__(self, max_samples: int = 2000) -> None:
        self.started_at: str = datetime.now(timezone.utc).isoformat()
        self._latencies_ms: Deque[float] = deque(maxlen=max_samples)
        self._counters: Counter[str] = Counter()
        self._intent_distribution: Counter[str] = Counter()

    @staticmethod
    def new_trace_id() -> str:
        """Sinh mã định danh truy vết duy nhất cho mỗi Request (Distributed Tracing ID)."""
        return f"trc_{uuid.uuid4().hex[:12]}"

    def record_request(self, latency_ms: float, intent: str) -> None:
        """Ghi nhận một lượt xử lý hội thoại hoàn tất."""
        self._counters["total_requests"] += 1
        self._latencies_ms.append(float(latency_ms))
        self._intent_distribution[intent] += 1

    def increment(self, metric_name: str, amount: int = 1) -> None:
        """Tăng bộ đếm sự kiện bất kỳ (VD: pii_redactions, csp_conflicts_detected)."""
        self._counters[metric_name] += amount

    @staticmethod
    def _percentile(sorted_vals: List[float], pct: float) -> float:
        """Tính phân vị thứ pct (ví dụ p50, p95, p99) chính xác về mặt thống kê."""
        if not sorted_vals:
            return 0.0
        idx = min(len(sorted_vals) - 1, max(0, math.ceil((pct / 100.0) * len(sorted_vals)) - 1))
        return round(sorted_vals[idx], 2)

    def snapshot(self) -> Dict[str, Any]:
        """Xuất báo cáo toàn cảnh sức khỏe hệ thống phục vụ Dashboard / Giám sát."""
        samples = sorted(self._latencies_ms)
        avg_ms = round(sum(samples) / len(samples), 2) if samples else 0.0

        return {
            "service_started_at": self.started_at,
            "total_requests": self._counters["total_requests"],
            "latency_Stats_ms": {
                "sample_count": len(samples),
                "avg_ms": avg_ms,
                "p50_ms": self._percentile(samples, 50),
                "p95_ms": self._percentile(samples, 95),
                "p99_ms": self._percentile(samples, 99),
            },
            "guardrails_and_privacy": {
                "pii_messages_anonymized": self._counters["pii_anonymized"],
                "guardrail_blocks": self._counters["guardrail_blocks"],
                "rate_limit_blocks": self._counters["rate_limit_blocks"],
                "estimated_tokens_processed": self._counters["tokens_processed"],
            },
            "algorithmic_engines": {
                "hybrid_search_rrf_queries": self._counters["hybrid_search_queries"],
                "csp_time_conflicts_resolved": self._counters["csp_conflicts_detected"],
                "acid_holds_succeeded": self._counters["acid_holds_succeeded"],
                "acid_holds_rejected_out_of_stock": self._counters["acid_holds_rejected"],
                "chatops_alerts_dispatched": self._counters["chatops_alerts_sent"],
            },
            "intent_distribution": dict(self._intent_distribution),
        }

    def reset(self) -> None:
        """Đặt lại số liệu (dùng trong kiểm thử tự động)."""
        self._latencies_ms.clear()
        self._counters.clear()
        self._intent_distribution.clear()


telemetry = TelemetryRegistry()
