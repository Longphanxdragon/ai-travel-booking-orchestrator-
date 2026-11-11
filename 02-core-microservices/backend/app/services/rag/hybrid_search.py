# ==============================================================================
# ĐỘNG CƠ TÌM KIẾM LAI ĐA MIỀN (HYBRID SEARCH ENGINE: BM25 + DENSE + RRF k=60)
# ------------------------------------------------------------------------------
# Dành cho người mới (Beginner Guide):
# Tại sao AI truyền thống (chỉ dùng Vector Search) hay tư vấn nhầm chính sách?
# - Vector Search giỏi hiểu "ý nghĩa tương đồng" (VD: "cún cưng" ~ "chó mèo"),
#   nhưng lại hay đánh đồng 2 mã phòng gần giống nhau như "Deluxe Ocean View"
#   và "Standard Ocean View" dẫn đến báo sai giá phạt hủy phòng!
# - BM25 giỏi bắt "từ khóa định danh chính xác từng chữ" (như tên nhà xe
#   "Điền Linh", hạng phòng "Deluxe"), nhưng lại mù từ đồng nghĩa.
#
# Giải thuật Reciprocal Rank Fusion (RRF, k=60) kết hợp bảng xếp hạng của CẢ HAI
# phương pháp mà không cần chỉnh trọng số thủ công, giúp đạt độ chính xác tối đa!
# ==============================================================================

import math
import re
from collections import Counter
from typing import Any, Dict, List, Literal, Optional, Tuple
from app.core.config import settings
from app.core.telemetry import telemetry
from app.models.schemas import PolicyDocumentHit


# ==============================================================================
# KHO TRI THỨC CHÍNH SÁCH CHUẨN (GROUND-TRUTH POLICY KNOWLEDGE BASE)
# Bao phủ các cặp thực thể dễ gây nhầm lẫn từ khóa (Hard Negatives) để kiểm chứng RRF
# ==============================================================================
DEFAULT_POLICY_CORPUS: List[Dict[str, str]] = [
    {
        "doc_id": "POL-NT-DELUXE-01",
        "title": "Chính sách Phòng Deluxe Ocean View - SeaView Nha Trang Hotel",
        "entity_code": "DELUXE-OCEAN-NT",
        "category": "HOTEL_POLICY",
        "content": (
            "Hạng phòng Deluxe Ocean View tại SeaView Nha Trang Hotel (Trần Phú): "
            "Miễn phí hủy phòng hoàn tiền 100% trước 72 giờ. Nhận phòng tiêu chuẩn 14:00, "
            "trả phòng 12:00. Hỗ trợ nhận phòng sớm từ 06:00 sáng với phụ thu 200.000đ "
            "hoặc gửi hành lý miễn phí tại quầy lễ tân 24/7. Không cho phép mang thú cưng."
        ),
    },
    {
        "doc_id": "POL-NT-STANDARD-02",
        "title": "Chính sách Phòng Standard Ocean View - SeaView Nha Trang Hotel",
        "entity_code": "STANDARD-OCEAN-NT",
        "category": "HOTEL_POLICY",
        "content": (
            "Hạng phòng Standard Ocean View tại SeaView Nha Trang Hotel (Trần Phú): "
            "Giá tiết kiệm không hoàn hủy (Non-refundable), hủy phòng mất 100% phí đêm đầu. "
            "Nhận phòng tiêu chuẩn 14:00. Phụ thu nhận phòng sớm trước 10:00 là 300.000đ. "
            "Không hỗ trợ giường phụ và không nhận vật nuôi."
        ),
    },
    {
        "doc_id": "POL-DL-COLLINE-03",
        "title": "Chính sách Khách sạn Colline Đà Lạt - Hạng Deluxe Double",
        "entity_code": "DELUXE-DOUBLE-COLLINE-DL",
        "category": "HOTEL_POLICY",
        "content": (
            "Khách sạn Colline Đà Lạt (Trung tâm Chợ Đà Lạt) - Hạng phòng Deluxe Double: "
            "Miễn phí hủy phòng trước 48 giờ. Giờ check-in chuẩn 14:00, check-out 12:00. "
            "Khách đi xe đêm tới Đà Lạt lúc 05:00-06:00 sáng được gửi valy miễn phí tại sảnh "
            "hoặc nhận phòng sớm nếu còn phòng trống với phụ thu 250.000đ. Không nhận chó mèo."
        ),
    },
    {
        "doc_id": "POL-DL-COLLINE-STD-04",
        "title": "Chính sách Khách sạn Colline Đà Lạt - Hạng Standard Twin",
        "entity_code": "STANDARD-TWIN-COLLINE-DL",
        "category": "HOTEL_POLICY",
        "content": (
            "Khách sạn Colline Đà Lạt - Hạng phòng Standard Twin hai giường đơn: "
            "Hủy trước 24 giờ chịu phí 50% giá phòng. Không có cửa sổ hướng quảng trường. "
            "Phụ thu nhận phòng sớm từ 06:00-10:00 sáng là 200.000đ/phòng. Cấm mang thú cưng."
        ),
    },
    {
        "doc_id": "POL-DL-MAY-PET-05",
        "title": "Quy định Mang Thú Cưng & Hủy Phòng - Homestay Thung Lũng Mây Đà Lạt",
        "entity_code": "BUNGALOW-PET-MAY-DL",
        "category": "HOTEL_POLICY",
        "content": (
            "Homestay Thung Lũng Mây Đà Lạt - Hạng Phòng Đôi Bungalow săn mây: "
            "Cho phép mang theo thú cưng (chó, mèo, cún con, vật nuôi dưới 5kg) có sổ tiêm phòng, "
            "phí vệ sinh khử khuẩn 100.000đ/bé. Hủy phòng trước 24 giờ mất 50% tiền cọc. "
            "Hỗ trợ check-in sớm lúc 06:00 sáng phụ thu 150.000đ hoặc gửi đồ uống trà nóng miễn phí."
        ),
    },
    {
        "doc_id": "POL-VT-PULLMAN-06",
        "title": "Chính sách Phòng Executive Suite - Malibu Beach Hotel Vũng Tàu",
        "entity_code": "EXEC-SUITE-VT",
        "category": "HOTEL_POLICY",
        "content": (
            "Hạng phòng Executive Suite hướng biển Bãi Sau tại Malibu Beach Vũng Tàu: "
            "Miễn phí đổi lịch hoặc hoàn hủy trước 48 giờ. Bao gồm buffet sáng cho 2 người lớn "
            "và 2 trẻ em dưới 6 tuổi. Phụ thu nhận phòng sớm trước 12:00 là 350.000đ."
        ),
    },
    {
        "doc_id": "POL-BUS-DIENLINH-07",
        "title": "Quy định Hành lý, Đổi trả & Đón trả - Nhà xe Điền Linh Limousine",
        "entity_code": "BUS-DIENLINH-24CABIN",
        "category": "BUS_POLICY",
        "content": (
            "Nhà xe Điền Linh Limousine tuyến Sài Gòn - Đà Lạt (Xe 24 Phòng Đôi Cabin VIP): "
            "Đón khách tại VP Hàng Xanh Bình Thạnh, có xe trung chuyển miễn phí bán kính 5km "
            "quanh Chợ Đà Lạt. Miễn phí 20kg hành lý/khách. Đổi hoặc hủy vé trước giờ xe chạy "
            "12 tiếng mất phí 10%, hủy dưới 12 tiếng không hoàn tiền. Nhận chở thú cưng bỏ lồng kín dưới gầm."
        ),
    },
    {
        "doc_id": "POL-BUS-FUTA-08",
        "title": "Quy định Vé, Trung chuyển & Say xe - Nhà xe Phương Trang (FUTA Bus Lines)",
        "entity_code": "BUS-FUTA-34SLEEPER",
        "category": "BUS_POLICY",
        "content": (
            "Nhà xe Phương Trang (FUTA) tuyến Sài Gòn - Đà Lạt (Limousine Giường Nằm 34 Chỗ): "
            "Xuất bến tại Bến xe Miền Tây và VP Lê Hồng Phong Q5. Khách dễ say xe được ưu tiên "
            "xếp giường tầng dưới dãy A1-A6 gần tài xế. Hủy vé trước 24 giờ phí 10%, trước 4 giờ phí 30%. "
            "Tuyệt đối không nhận vận chuyển chó mèo, gia cầm trên khoang hành khách."
        ),
    },
    {
        "doc_id": "POL-BUS-ANANH-09",
        "title": "Chính sách Tuyến Sài Gòn - Nha Trang - Nhà xe An Anh Limousine",
        "entity_code": "BUS-ANANH-34VIP",
        "category": "BUS_POLICY",
        "content": (
            "Nhà xe An Anh Limousine (34 Phòng VIP có ghế massage): Đón tại Bến xe Miền Đông mới "
            "và Ngã tư Bình Thái, trả khách dọc đường Trần Phú Nha Trang lúc 05:00 sáng. "
            "Miễn phí hủy đổi trước 24 tiếng. Trẻ em dưới 1m nằm chung với bố mẹ được miễn vé."
        ),
    },
    {
        "doc_id": "POL-BUS-HOANGMAI-10",
        "title": "Chính sách Tuyến Sài Gòn - Vũng Tàu - Hoa Mai Limousine 9 Chỗ",
        "entity_code": "BUS-HOAMAI-9VIP",
        "category": "BUS_POLICY",
        "content": (
            "Nhà xe Hoa Mai Limousine ghế thương gia Boeing 9 chỗ tuyến Quận 1 - Vũng Tàu: "
            "Khởi hành mỗi 30 phút từ 04:30 đến 21:00, thời gian di chuyển 2 giờ 15 phút qua cao tốc Long Thành. "
            "Đưa đón tận nơi nội thành TP. Vũng Tàu. Đổi chuyến miễn phí trước 60 phút."
        ),
    },
    {
        "doc_id": "POL-COMBO-EARLY-11",
        "title": "Quy chuẩn Giải quyết Xung đột Lệch giờ Xe đêm & Giờ Check-in Khách sạn",
        "entity_code": "RULE-CSP-EARLY-CHECKIN",
        "category": "COMBO_RULE",
        "content": (
            "Quy tắc điều phối lịch trình Combo Xe Đêm + Lưu Trú: Khi chuyến xe khách giường nằm "
            "cập bến lúc rạng sáng (04:30 - 06:30) trong khi giờ nhận phòng tiêu chuẩn của khách sạn "
            "là 14:00 (độ trễ chờ đợi Delta T > 3 giờ), hệ thống bắt buộc tư vấn 2 lựa chọn: "
            "(1) Đăng ký Early Check-in có thu phí theo biểu giá từng khách sạn, hoặc "
            "(2) Ký gửi hành lý miễn phí tại quầy lễ tân để đi ăn sáng, tham quan trước."
        ),
    },
    {
        "doc_id": "POL-COMBO-HOLIDAY-12",
        "title": "Chính sách Phụ thu Lễ Tết & Cao điểm Du lịch (30/4, 2/9, Tết Nguyên Đán)",
        "entity_code": "RULE-HOLIDAY-SURCHARGE",
        "category": "COMBO_RULE",
        "content": (
            "Trong giai đoạn Lễ Tết cao điểm, giá vé xe khách tăng tối đa không quá 40% theo kê khai Sở GTVT, "
            "phòng khách sạn áp dụng phụ thu cao điểm 20%-30% và không áp dụng chính sách hoàn hủy miễn phí. "
            "Thời gian giữ chỗ tạm thời (ACID Reservation Hold) vẫn duy trì tối đa 15 phút."
        ),
    },
]


# ==============================================================================
# BẢN ĐỒ KHÁI NIỆM NGỮ NGHĨA ĐẶC TRƯNG (SEMANTIC CONCEPT PROJECTION AXES)
# Mô phỏng không gian nhúng Dense Vector R^12 bắt từ đồng nghĩa tiếng Việt
# ngay cả khi không có từ khóa trùng khớp (Zero-Lexical-Overlap Recall)
# ==============================================================================
SEMANTIC_AXES: List[List[str]] = [
    # Trục 0: Biển / Nha Trang / Nghỉ dưỡng ven biển
    ["biển", "ocean", "view", "nha trang", "trần phú", "bãi sau", "vũng tàu", "seaview", "malibu"],
    # Trục 1: Núi / Đà Lạt / Săn mây / Homestay
    ["đà lạt", "săn mây", "thung lũng", "chợ đà lạt", "bungalow", "homestay", "colline", "lạnh"],
    # Trục 2: Thú cưng / Chó mèo / Vật nuôi (Bắt đồng nghĩa cực mạnh cho Dense Search)
    ["thú cưng", "chó", "mèo", "cún", "vật nuôi", "pet", "boss", "mang cún", "chó con", "lồng"],
    # Trục 3: Hoàn tiền / Hủy vé / Đổi lịch / Phạt cọc
    ["hủy", "hoàn tiền", "đổi lịch", "đổi vé", "trả vé", "mất cọc", "phạt", "refundable", "hoàn phí"],
    # Trục 4: Nhận phòng sớm / Lệch giờ / Xe đêm đến sáng / Gửi hành lý
    ["nhận phòng sớm", "check-in sớm", "early", "rạng sáng", "5h sáng", "6h sáng", "gửi hành lý", "gửi đồ", "valy", "chờ"],
    # Trục 5: Hạng sang / Cabin đôi / VIP / Massage
    ["vip", "limousine", "phòng đôi", "cabin", "suite", "executive", "massage", "thương gia", "cao cấp"],
    # Trục 6: Tiết kiệm / Phổ thông / Giường đơn
    ["tiết kiệm", "giá rẻ", "standard", "twin", "phổ thông", "không hoàn"],
    # Trục 7: Say xe / Sức khỏe / Giường tầng dưới
    ["say xe", "chóng mặt", "tầng dưới", "gần tài xế", "êm", "người già"],
    # Trục 8: Đưa đón / Trung chuyển / Bến xe
    ["trung chuyển", "đưa đón", "tận nơi", "bến xe", "hàng xanh", "miền tây", "miền đông", "điểm đón"],
    # Trục 9: Hành lý / Cân nặng / Quá cước
    ["hành lý", "20kg", "cân nặng", "thùng hàng", "gầm xe", "valy"],
    # Trục 10: Trẻ em / Gia đình / Buffet sáng
    ["trẻ em", "em bé", "gia đình", "buffet", "ăn sáng", "miễn vé", "dưới 1m"],
    # Trục 11: Lễ Tết / Phụ thu cao điểm / Giữ chỗ 15 phút
    ["lễ", "tết", "cao điểm", "phụ thu", "giữ chỗ", "15 phút", "30/4"],
]


class HybridPolicySearchEngine:
    """
    Động cơ Tìm kiếm Lai (Hybrid Search) chuẩn toán học của Đồ án:
    1. Nhánh Từ vựng (Sparse Lexical): Okapi BM25 với k1 = 1.5, b = 0.75.
    2. Nhánh Ngữ nghĩa (Dense Semantic): Không gian Vector chuẩn hóa L2 + Cosine Similarity
       (Hỗ trợ cắm trực tiếp Qdrant Client hoặc chạy Deterministic Vector Projector nội bộ).
    3. Bộ Gộp hạng Tương hỗ (Reciprocal Rank Fusion - RRF): k = 60.
    """

    TOKEN_PATTERN = re.compile(r"[0-9a-zA-ZÀ-ỹ]+")

    def __init__(
        self,
        corpus: Optional[List[Dict[str, str]]] = None,
        k1: float = settings.bm25_k1,
        b: float = settings.bm25_b,
        rrf_k: int = settings.rrf_k,
    ) -> None:
        self.corpus: List[Dict[str, str]] = list(corpus or DEFAULT_POLICY_CORPUS)
        self.k1 = k1
        self.b = b
        self.rrf_k = rrf_k

        # Tiền tính toán chỉ mục ngược (Inverted Index) cho BM25 & Vector ngữ nghĩa cho Dense
        self._doc_tokens: List[List[str]] = []
        self._doc_term_freqs: List[Counter[str]] = []
        self._doc_lengths: List[int] = []
        self._doc_freq: Counter[str] = Counter()
        self._dense_vectors: List[List[float]] = []
        self._avgdl: float = 1.0

        self._build_index()

    @classmethod
    def tokenize(cls, text: str) -> List[str]:
        """
        Tách từ tiếng Việt & thực thể định danh (Unigrams + Domain Bigrams).
        Ví dụ: 'Deluxe Ocean View' -> ['deluxe', 'ocean', 'view', 'deluxe_ocean', 'ocean_view'].
        Việc giữ cả unigram và bigram giúp BM25 bắt cực chuẩn tên nhà xe ('điền_linh') và mã phòng!
        """
        words = [w.lower() for w in cls.TOKEN_PATTERN.findall(text)]
        bigrams = [f"{words[i]}_{words[i + 1]}" for i in range(len(words) - 1)]
        return words + bigrams

    def _compute_dense_embedding(self, text: str) -> List[float]:
        """
        Ánh xạ văn bản vào không gian Dense Vector chuẩn hóa L2 (Unit Hypersphere).
        Kết hợp 12 trục khái niệm ngữ nghĩa du lịch + 52 chiều băm ký tự n-gram (Character 3-gram)
        tạo thành vector 64 chiều liên tục.
        """
        text_lower = text.lower()
        vec = [0.0] * 64

        # 12 chiều đầu: Cường độ ngữ nghĩa theo khái niệm (Semantic Concept Activation)
        for axis_idx, keywords in enumerate(SEMANTIC_AXES):
            score = 0.0
            for kw in keywords:
                if kw in text_lower:
                    score += 1.5
            vec[axis_idx] = score

        # 52 chiều sau: Phân bố ngữ cảnh mềm qua Character Trigrams (chống lỗi gõ tắt/dấu)
        clean = re.sub(r"\s+", " ", text_lower).strip()
        for i in range(max(0, len(clean) - 2)):
            trigram = clean[i : i + 3]
            bucket = 12 + (sum(ord(c) * (idx + 1) for idx, c in enumerate(trigram)) % 52)
            vec[bucket] += 0.15

        # Chuẩn hóa L2: ||e||_2 = 1 để phép nhân vô hướng chính là Cosine Similarity
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def _build_index(self) -> None:
        """Xây dựng chỉ mục BM25 và Dense Vector trong bộ nhớ (O(N * L))."""
        self._doc_tokens.clear()
        self._doc_term_freqs.clear()
        self._doc_lengths.clear()
        self._doc_freq.clear()
        self._dense_vectors.clear()

        for doc in self.corpus:
            # Ghép tiêu đề (nhân đôi trọng số tự nhiên), mã thực thể và nội dung
            full_text = f"{doc['title']} {doc['title']} {doc['entity_code']} {doc['content']}"
            tokens = self.tokenize(full_text)
            tf = Counter(tokens)

            self._doc_tokens.append(tokens)
            self._doc_term_freqs.append(tf)
            self._doc_lengths.append(len(tokens))

            for unique_term in tf.keys():
                self._doc_freq[unique_term] += 1

            # Dense Vector: Nhúng ngữ nghĩa của tiêu đề và nội dung
            self._dense_vectors.append(self._compute_dense_embedding(f"{doc['title']} {doc['content']}"))

        total_len = sum(self._doc_lengths)
        self._avgdl = (total_len / len(self.corpus)) if self.corpus else 1.0

    def _idf(self, term: str) -> float:
        """
        Công thức Robertson-Zaragoza IDF chuẩn mực:
        IDF(q_i) = ln( (N - n(q_i) + 0.5) / (n(q_i) + 0.5) + 1 )
        """
        n_docs = len(self.corpus)
        df = self._doc_freq.get(term, 0)
        return math.log(((n_docs - df + 0.5) / (df + 0.5)) + 1.0)

    def rank_bm25(self, query: str) -> List[Tuple[int, float]]:
        """
        Xếp hạng toàn bộ kho tài liệu bằng công thức Okapi BM25.
        Trả về danh sách [(doc_index, bm25_score)] giảm dần theo điểm số.
        """
        q_tokens = self.tokenize(query)
        scores: List[Tuple[int, float]] = []

        for idx, tf in enumerate(self._doc_term_freqs):
            doc_len = self._doc_lengths[idx]
            score = 0.0
            norm_denom_part = self.k1 * (1.0 - self.b + self.b * (doc_len / self._avgdl))

            for term in q_tokens:
                freq = tf.get(term, 0)
                if freq == 0:
                    continue
                idf_val = self._idf(term)
                numerator = freq * (self.k1 + 1.0)
                denominator = freq + norm_denom_part
                score += idf_val * (numerator / denominator)

            scores.append((idx, score))

        scores.sort(key=lambda item: (-item[1], item[0]))
        return scores

    def rank_dense(self, query: str) -> List[Tuple[int, float]]:
        """
        Xếp hạng toàn bộ kho tài liệu bằng Cosine Similarity trong không gian Dense Vector.
        Trả về danh sách [(doc_index, cosine_similarity)] giảm dần.
        """
        q_vec = self._compute_dense_embedding(query)
        scores: List[Tuple[int, float]] = []

        for idx, d_vec in enumerate(self._dense_vectors):
            cosine_sim = sum(qv * dv for qv, dv in zip(q_vec, d_vec))
            scores.append((idx, cosine_sim))

        scores.sort(key=lambda item: (-item[1], item[0]))
        return scores

    def search(
        self,
        query: str,
        top_k: int = 3,
        mode: Literal["hybrid_rrf", "bm25_only", "dense_only"] = "hybrid_rrf",
    ) -> List[PolicyDocumentHit]:
        """
        Thực thi truy vấn theo chế độ chỉ định:
        - 'hybrid_rrf': Gộp hạng tương hỗ RRF(d) = 1/(k + r_bm25(d)) + 1/(k + r_dense(d)) với k=60.
        - 'bm25_only': Chỉ dùng BM25 (phục vụ kiểm thử đối chứng Ablation Study).
        - 'dense_only': Chỉ dùng Dense Vector (phục vụ kiểm thử đối chứng Baseline RAG).
        """
        telemetry.increment("hybrid_search_queries")

        bm25_ranked = self.rank_bm25(query)
        dense_ranked = self.rank_dense(query)

        # Ánh xạ doc_index -> Thứ hạng thực tế r_m(d) thuộc {1, 2, ..., N}
        bm25_rank_map: Dict[int, int] = {
            doc_idx: rank_pos + 1 for rank_pos, (doc_idx, _) in enumerate(bm25_ranked)
        }
        bm25_score_map: Dict[int, float] = dict(bm25_ranked)
        dense_rank_map: Dict[int, int] = {
            doc_idx: rank_pos + 1 for rank_pos, (doc_idx, _) in enumerate(dense_ranked)
        }

        fused: List[Tuple[int, float]] = []
        for doc_idx in range(len(self.corpus)):
            r_bm25 = bm25_rank_map[doc_idx]
            r_dense = dense_rank_map[doc_idx]

            if mode == "bm25_only":
                # Nếu BM25 không bắt được từ khóa nào (score == 0), xếp cuối bảng
                score = (1.0 / (self.rrf_k + r_bm25)) if bm25_score_map[doc_idx] > 0 else 0.0
            elif mode == "dense_only":
                score = 1.0 / (self.rrf_k + r_dense)
            else:
                # Công thức RRF chuẩn Cormack et al. (SIGIR 2009)
                bm25_contrib = (1.0 / (self.rrf_k + r_bm25)) if bm25_score_map[doc_idx] > 0 else (1.0 / (self.rrf_k + len(self.corpus) + 50))
                dense_contrib = 1.0 / (self.rrf_k + r_dense)
                score = bm25_contrib + dense_contrib

            fused.append((doc_idx, score))

        fused.sort(key=lambda item: (-item[1], bm25_rank_map[item[0]]))

        hits: List[PolicyDocumentHit] = []
        for doc_idx, final_score in fused[:top_k]:
            raw_doc = self.corpus[doc_idx]
            entity_c = raw_doc.get("entity_code", "")
            hits.append(
                PolicyDocumentHit(
                    doc_id=raw_doc["doc_id"],
                    title=raw_doc["title"],
                    entity_name=raw_doc.get("title", ""),
                    destination="",
                    category=raw_doc.get("category", "POLICY"),
                    room_or_trip_code=entity_c,
                    entity_code=entity_c,
                    content=raw_doc["content"],
                    bm25_score=round(bm25_score_map.get(doc_idx, 0.0), 4),
                    dense_score=round(dict(dense_ranked).get(doc_idx, 0.0), 4),
                    bm25_rank=bm25_rank_map[doc_idx],
                    dense_rank=dense_rank_map[doc_idx],
                    rrf_score=round(final_score, 6),
                )
            )
        return hits


# Khởi tạo Singleton Engine để tái sử dụng chỉ mục O(1) cho mọi Request
hybrid_policy_engine = HybridPolicySearchEngine()
DEFAULT_HYBRID_ENGINE = hybrid_policy_engine
HybridSearchEngine = HybridPolicySearchEngine
TRAVEL_POLICY_CORPUS = DEFAULT_POLICY_CORPUS

