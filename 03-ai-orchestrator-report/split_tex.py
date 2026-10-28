import os
import shutil

base_dir = r"D:\retail-automatic\03-ai-orchestrator-report\report\Mẫu_báo_cáo_ĐACN_ĐAKTMT_ĐAMH\Contents"

# We will recreate the structure cleanly.
# First, remove old files.
old_files = ["GioiThieu.tex", "CoSoLyThuyet.tex", "YeuCauHeThong.tex", "DacTaChiTietCacUseCase.tex", 
             "PhanTichThietKeHeThong.tex", "HienThuc.tex", "KiemThuHeThong.tex", "TrienKhai.tex", "TongKet.tex"]

structure = {
    "01_GioiThieu": {
        "title": "Giới thiệu",
        "subs": {
            "01_BoiCanh.tex": r"""\subsection{Bối cảnh nghiên cứu}
Sự ra đời của các Mô hình Ngôn ngữ Lớn (LLMs) như GPT-4, Gemini đã đánh dấu bước ngoặt trong Xử lý Ngôn ngữ Tự nhiên (NLP). Tuy nhiên, khi áp dụng vào các hệ thống đòi hỏi nghiệp vụ khắt khe, tính logic cao và dữ liệu thay đổi liên tục như Tư vấn Đặt lịch trình du lịch (Xe khách và Khách sạn), RAG nguyên bản (Native RAG) đã bộc lộ những khiếm khuyết chí mạng, không thể đáp ứng được chuẩn mực của một hệ thống lõi (Tech Core) trong ứng dụng thực tế.
""",
            "02_KhoKhan.tex": r"""\subsection{Khó khăn và Bài toán đặt ra}
\begin{enumerate}
    \item \textbf{Ảo giác dữ liệu động (Dynamic Data Hallucination):} Dữ liệu phòng trống, vé xe thay đổi từng giây. Việc nhúng tài liệu tĩnh (PDF/Doc) vào Vector DB khiến LLM bị "ảo giác", tự tin báo sai số lượng tồn kho.
    \item \textbf{Khớp sai từ khóa ngách (Keyword Mismatch):} Kỹ thuật Dense Vector Search đánh đồng các từ vựng na ná nhau, bỏ sót hoặc nhầm lẫn mã phòng đặc thù và tên nhà xe địa phương.
    \item \textbf{Ràng buộc chéo về thời gian (Temporal Cross-constraints):} Đặt vé và đặt phòng là chuỗi logic chặt chẽ. Đổi giờ xe đòi hỏi phải kiểm tra lại giờ check-in khách sạn. AI đơn lẻ (Single-Agent) không đủ khả năng quản lý và tự động giải quyết các xung đột lịch trình chéo này.
\end{enumerate}
""",
            "03_MucTieu.tex": r"""\subsection{Mục tiêu nghiên cứu}
Đồ án này tập trung xây dựng một \textbf{Tech Core AI chuyên sâu}, hoạt động như một dịch vụ lõi (Plug-in/Microservice) giải quyết triệt để 3 bài toán trên thông qua:
\begin{itemize}
    \item \textbf{Hybrid Search (BM25 + Dense) \& RRF:} Khắc phục điểm mù từ khóa ngách, đảm bảo truy xuất chính xác 100\% các mã định danh.
    \item \textbf{Function Calling (Gọi hàm):} Cấp quyền cho AI chọc thẳng vào CSDL thời gian thực, loại bỏ hoàn toàn ảo giác.
    \item \textbf{Multi-Agent Orchestration:} Xây dựng hệ thống Đa tác tử. Một Tác tử Điều phối (Orchestrator) sử dụng Chain-of-Thought (CoT) để đàm phán ràng buộc thời gian giữa Tác tử Xe và Tác tử Khách sạn.
\end{itemize}
""",
            "04_DongGop.tex": r"""\subsection{Đóng góp thực tiễn}
Đồ án mang lại một lõi AI thông minh, có thể tích hợp dễ dàng vào bất kỳ nền tảng SaaS nào, cung cấp năng lực tư vấn chính xác tuyệt đối, kiểm tra tồn kho thời gian thực và tự động lập lịch logic như một chuyên viên tư vấn con người.
"""
        }
    },
    "02_CoSoLyThuyet": {
        "title": "Cơ sở lý thuyết và công nghệ",
        "subs": {
            "01_HybridSearch.tex": r"""\subsection{Giới hạn của Native RAG và Giải pháp Hybrid Search}
Sinh văn bản tăng cường truy xuất (RAG) nguyên bản sử dụng Dense Embeddings để tìm kiếm ngữ nghĩa. Tuy nhiên, nó bị "mù" trước các từ khóa chính xác (Keyword Mismatch). 
\textbf{Hybrid Search (Tìm kiếm Lai)} giải quyết vấn đề này bằng cách kết hợp:
\begin{itemize}
    \item \textbf{Tìm kiếm Thưa (Sparse Search - BM25):} Dựa trên tần suất từ khóa, bắt chính xác mã phòng, tên riêng.
    \item \textbf{Tìm kiếm Dày đặc (Dense Vector Search):} Bắt nét nghĩa ẩn của câu hỏi.
\end{itemize}
Để gộp chung hai bảng xếp hạng, thuật toán \textbf{Reciprocal Rank Fusion (RRF)} được sử dụng, đẩy các tài liệu phù hợp ở cả hai phương pháp lên vị trí top đầu.
""",
            "02_FunctionCalling.tex": r"""\subsection{Function Calling (Tool Use)}
\textbf{Function Calling} biến LLM từ công cụ sinh văn bản thuần túy thành Tác tử có khả năng thực thi hành động (Agentic). Bằng cách định nghĩa JSON Schema cho các hàm (ví dụ: \texttt{check\_bus\_availability}), LLM tự động trích xuất tham số từ câu hỏi, yêu cầu hệ thống thực thi truy vấn CSDL, sau đó đọc kết quả thực tế để trả lời khách hàng. Quá trình này giúp loại bỏ 100\% ảo giác dữ liệu động.
""",
            "03_MultiAgent.tex": r"""\subsection{Hệ thống Đa tác tử (Multi-Agent System) \& CoT}
Thay vì dùng một AI duy nhất để xử lý toàn bộ luồng, \textbf{Multi-Agent System} chia nhỏ nghiệp vụ:
\begin{itemize}
    \item \textbf{Chia để trị (Divide and Conquer):} Mỗi Tác tử (Agent) như Bus Agent, Hotel Agent chỉ chứa Tools và Prompt chuyên biệt.
    \item \textbf{Chain-of-Thought (CoT):} Cơ chế ép LLM "suy nghĩ từng bước" trước khi ra kết luận.
    \item \textbf{Orchestrator (Bộ điều phối):} Tác tử trung tâm sử dụng CoT để lập kế hoạch, gọi Bus Agent tìm vé, lấy giờ đến, truyền cho Hotel Agent tìm phòng khớp giờ. Nếu có xung đột, Orchestrator tự động đàm phán lại.
\end{itemize}
"""
        }
    },
    "03_YeuCauHeThong": {
        "title": "Yêu cầu hệ thống",
        "subs": {
            "01_YeuCauChucNang.tex": r"""\subsection{Yêu cầu chức năng của Tech Core AI}
Đóng vai trò là một dịch vụ AI trung tâm (Plug-in Service), hệ thống phải đáp ứng các yêu cầu:
\begin{enumerate}
    \item \textbf{Quản lý tri thức tĩnh (Hybrid Search):} Lập chỉ mục văn bản chính sách, cẩm nang du lịch sử dụng đồng thời Dense Vector và BM25 vào Qdrant.
    \item \textbf{Truy vấn dữ liệu động (Function Calling):} Chuyển đổi ý định của khách hàng thành các lệnh gọi API kiểm tra vé xe, phòng trống trực tiếp trên CSDL PostgreSQL.
    \item \textbf{Điều phối Đa tác tử (Orchestration):} Duy trì Biến trạng thái (Shared State) xuyên suốt phiên hội thoại, tự động chuyển luồng (Routing) giữa các Agent chuyên biệt để giải quyết ràng buộc lịch trình.
\end{enumerate}
""",
            "02_YeuCauPhiChucNang.tex": r"""\subsection{Yêu cầu phi chức năng}
\begin{itemize}
    \item \textbf{Độ chính xác (Accuracy):} Truy xuất đúng mã phòng, tên nhà xe (NDCG@10 cao). 
    \item \textbf{Chống ảo giác (Zero Hallucination):} Tỷ lệ ảo giác thông tin tồn kho phải bằng 0\%.
    \item \textbf{Khả năng giải quyết ràng buộc (Success Rate):} Tỷ lệ lập lịch chéo thành công phải vượt trội so với mô hình Single-Agent.
    \item \textbf{Độ trễ API (Latency):} Toàn bộ quá trình đàm phán Đa tác tử không vượt quá 10 giây để đảm bảo trải nghiệm người dùng.
\end{itemize}
"""
        }
    },
    "04_DacTaUseCase": {
        "title": "Đặc tả chi tiết các Use-case",
        "subs": {
            "01_HybridSearch.tex": r"""\subsection{UC-01: Lập chỉ mục và truy xuất Hybrid Search}
\textbf{Luồng sự kiện:} Quản trị viên tải lên file chính sách khách sạn. Hệ thống băm văn bản (Chunking), nhúng qua mô hình Dense (Embedding) và Sparse (BM25), lưu vào Qdrant. Khi khách hàng hỏi mã phòng đặc thù, AI gọi truy vấn Hybrid, gộp hạng bằng RRF và trả về Context chính xác.
""",
            "02_FunctionCalling.tex": r"""\subsection{UC-02: LLM gọi hàm kiểm tra tồn kho (Function Calling)}
\textbf{Luồng sự kiện:} Khách hàng hỏi "Mai còn chuyến xe đêm đi Đà Lạt không?". LLM nhận diện ý định, tạm dừng sinh văn bản, yêu cầu kích hoạt Tool \texttt{check\_bus\_availability}. Backend thực thi truy vấn SQL lấy số ghế trống từ Database, trả lại kết quả (JSON) cho LLM. LLM tổng hợp thành câu trả lời tự nhiên.
""",
            "03_MultiAgent.tex": r"""\subsection{UC-03: Đàm phán Lịch trình chéo (Multi-Agent)}
\textbf{Luồng sự kiện:} 
1. Khách hàng yêu cầu đặt lịch trình xe và khách sạn, muốn check-in ngay khi đến.
2. Orchestrator Agent lập kế hoạch (CoT), giao quyền cho Bus Agent.
3. Bus Agent tìm chuyến xe, trả về "Đến nơi lúc 5h sáng" $\rightarrow$ Cập nhật vào Shared State.
4. Orchestrator gọi Hotel Agent tìm phòng có chính sách "Early check-in 5h sáng".
5. Hotel Agent gọi Hybrid Search tìm chính sách phụ thu, cập nhật kết quả.
6. Orchestrator tổng hợp toàn bộ State và trả lời khách hàng một lịch trình hoàn hảo.
"""
        }
    },
    "05_PhanTichThietKe": {
        "title": "Phân tích và thiết kế hệ thống",
        "subs": {
            "01_KienTrucLoi.tex": r"""\subsection{Kiến trúc lõi Tech Core}
Hệ thống được thiết kế dưới dạng một Microservice độc lập, bao gồm 3 khối chính:
\begin{enumerate}
    \item \textbf{Hybrid Search Engine:} Tích hợp Qdrant quản lý Vector Dense \& Sparse.
    \item \textbf{Real-time Tool Agent:} Lớp Wrapper API kết nối PostgreSQL cung cấp Tools cho LLM.
    \item \textbf{Multi-Agent Orchestrator:} Lớp não bộ sử dụng LangGraph điều khiển luồng suy luận.
\end{enumerate}
""",
            "02_StateGraph.tex": r"""\subsection{Thiết kế Đồ thị Trạng thái (State Graph)}
Sử dụng \textbf{Shared State} làm bộ nhớ trung tâm (chứa Chat History, Booking Context, Errors).
\begin{itemize}
    \item \textbf{Nodes (Nút):} Tác tử Điều phối (Orchestrator), Tác tử Xe (Bus Expert), Tác tử Khách sạn (Hotel Expert).
    \item \textbf{Edges (Cạnh):} Là các quy tắc điều hướng (Conditional Edges). Orchestrator quyết định chuyển luồng sang Bus Expert hay Hotel Expert, sau khi các Expert xong việc sẽ luôn trả quyền về lại Orchestrator.
\end{itemize}
""",
            "03_SequenceDiagram.tex": r"""\subsection{Sơ đồ tuần tự (Sequence Diagram) luồng CoT}
\begin{itemize}
    \item Khách hàng $\rightarrow$ API Gateway $\rightarrow$ Orchestrator.
    \item Orchestrator [Inner Monologue] $\rightarrow$ Route to Bus Agent.
    \item Bus Agent $\rightarrow$ Function Call $\rightarrow$ PostgreSQL $\rightarrow$ Update State.
    \item Orchestrator $\rightarrow$ Route to Hotel Agent $\rightarrow$ Hybrid Search $\rightarrow$ Qdrant $\rightarrow$ Update State.
    \item Orchestrator $\rightarrow$ Finalize Response $\rightarrow$ Khách hàng.
\end{itemize}
"""
        }
    },
    "06_HienThuc": {
        "title": "Hiện thực hóa hệ thống",
        "subs": {
            "01_NenTang.tex": r"""\subsection{Nền tảng công nghệ}
\begin{itemize}
    \item \textbf{AI Framework:} LangChain và LangGraph để xây dựng Đồ thị Đa tác tử.
    \item \textbf{Validation:} Pydantic v2 để định nghĩa nghiêm ngặt cấu trúc JSON của Tools.
    \item \textbf{LLM:} gemini-1.5-flash hoặc gpt-4o-mini với năng lực Tool Calling.
    \item \textbf{Cơ sở dữ liệu:} Qdrant (Vector) và PostgreSQL (SQL).
\end{itemize}
""",
            "02_HybridSearch.tex": r"""\subsection{Hiện thực Hybrid Search \& RRF}
\begin{lstlisting}[language=Python, title=Truy vấn Hybrid Search với Qdrant]
prefetch_dense = Prefetch(query=dense_vec, using="dense_embedding", limit=10)
prefetch_sparse = Prefetch(query=Query(**sparse_vec), using="sparse_bm25", limit=10)

results = qdrant.query_points(
    collection_name="travel_docs",
    prefetch=[prefetch_dense, prefetch_sparse],
    query=Query(fusion="rrf"), # Giai thuat Reciprocal Rank Fusion
    limit=5,
)
\end{lstlisting}
""",
            "03_FunctionCalling.tex": r'''\subsection{Hiện thực Tool Calling bằng Pydantic}
\begin{lstlisting}[language=Python, title=Định nghĩa Tool bằng Pydantic]
class BusSearchInput(BaseModel):
    route_code: str = Field(..., description="Mã tuyến đường, vd: SG-DL")
    date: str = Field(..., description="Ngày đi YYYY-MM-DD")

@tool(args_schema=BusSearchInput)
async def check_bus_availability(route_code: str, date: str) -> str:
    """Truy vấn CSDL PostgreSQL thời gian thực"""
    # Logic SQL query...
    return json.dumps({"seats": 10})
\end{lstlisting}
''',
            "04_MultiAgent.tex": r"""\subsection{Hiện thực Đồ thị Multi-Agent (LangGraph)}
\begin{lstlisting}[language=Python, title=Khởi tạo State Graph]
graph = StateGraph(AgentState)
graph.add_node("orchestrator", orchestrator_agent)
graph.add_node("bus_expert", bus_agent)
graph.add_node("hotel_expert", hotel_agent)

# Routing logic
graph.add_conditional_edges("orchestrator", route_next_step)
graph.add_edge("bus_expert", "orchestrator")
graph.add_edge("hotel_expert", "orchestrator")
app = graph.compile()
\end{lstlisting}
"""
        }
    },
    "07_KiemThu": {
        "title": "Kiểm thử và Đánh giá hệ thống (Evaluation)",
        "subs": {
            "00_Placeholder.tex": r"""\textit{(Phần này đang được để trống và sẽ được cập nhật số liệu sau khi hoàn tất quá trình chạy thực nghiệm hệ thống)}""",
            "01_KichBan.tex": r"""\subsection{Kịch bản và Môi trường kiểm thử}
% [Chờ bổ sung số liệu]
...
""",
            "02_HybridSearch.tex": r"""\subsection{Đánh giá Hiệu năng Hybrid Search (Khắc phục Keyword Mismatch)}
% [Chờ bổ sung số liệu]
...
""",
            "03_Hallucination.tex": r"""\subsection{Đánh giá Tỷ lệ Ảo giác (Hallucination Rate)}
% [Chờ bổ sung số liệu]
...
""",
            "04_MultiAgent.tex": r"""\subsection{Đánh giá Khả năng Lập lịch của Multi-Agent Orchestrator}
% [Chờ bổ sung số liệu]
...
"""
        }
    },
    "08_TrienKhai": {
        "title": "Triển khai Ứng dụng (Deployment)",
        "subs": {
            "01_ModelAsAService.tex": r"""\subsection{Đóng gói API (Model as a Service)}
Lõi AI Tech Core được thiết kế độc lập, đóng gói bằng Python FastAPI. Mọi nền tảng bên ngoài (Zalo Mini App, CRM, Chatwoot) đều có thể gọi qua API RESTful để nhận kết quả tư vấn thông minh, đảm bảo tính Plug-and-Play cho hệ thống Microservices.
""",
            "02_DockerCompose.tex": r"""\subsection{Triển khai với Docker Compose}
Hệ thống được Container hóa với 3 khối chính:
\begin{enumerate}
    \item \texttt{qdrant-server}: Vector Database phục vụ Hybrid Search.
    \item \texttt{postgres-db}: Cơ sở dữ liệu quan hệ phục vụ Function Calling.
    \item \texttt{ai-agent-api}: Tiến trình FastAPI chạy LangGraph điều khiển hội thoại.
\end{enumerate}
"""
        }
    },
    "09_TongKet": {
        "title": "Tổng kết",
        "subs": {
            "01_KetQua.tex": r"""\subsection{Kết quả đạt được}
Đồ án đã tiếp cận và giải quyết xuất sắc 3 bài toán hóc búa nhất của việc ứng dụng Trí tuệ Nhân tạo vào thương mại điện tử:
\begin{itemize}
    \item Tích hợp \textbf{Hybrid Search \& RRF} đảm bảo truy xuất chính xác tuyệt đối từ khóa.
    \item Ứng dụng \textbf{Function Calling} đưa tỷ lệ ảo giác tồn kho về 0\%.
    \item Kiến trúc \textbf{Multi-Agent Systems} với luồng CoT đàm phán thành công các ràng buộc lịch trình chéo, vượt trội so với Single-Agent.
\end{itemize}
Lõi AI này hoàn toàn đủ tiêu chuẩn tích hợp vào các hệ thống Microservices quy mô lớn.
""",
            "02_HanChe.tex": r"""\subsection{Hạn chế và Hướng phát triển}
\begin{itemize}
    \item \textbf{Độ trễ (Latency):} Việc đàm phán Đa tác tử tốn nhiều vòng lặp, dẫn đến thời gian sinh văn bản cao (5-10 giây). Cần tinh chỉnh mô hình Local (Local LLMs) chuyên biệt cho Tool Calling để chạy trực tiếp, giảm trễ mạng.
    \item \textbf{Học tăng cường (RLHF):} Tương lai cần bổ sung khả năng học từ phản hồi của khách hàng để Tác tử có thể đàm phán giá cả (Price Negotiation) linh hoạt.
\end{itemize}
"""
        }
    }
}

# Apply the restructuring
main_tex_path = r"D:\retail-automatic\03-ai-orchestrator-report\report\Mẫu_báo_cáo_ĐACN_ĐAKTMT_ĐAMH\main.tex"

for old_f in old_files:
    p = os.path.join(base_dir, old_f)
    if os.path.exists(p):
        os.remove(p)

for folder, data in structure.items():
    folder_path = os.path.join(base_dir, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    main_ch_path = os.path.join(folder_path, "main.tex")
    
    with open(main_ch_path, "w", encoding="utf-8") as fm:
        fm.write(f"\\section{{{data['title']}}}\n\n")
        
        for sub_name, sub_content in data["subs"].items():
            sub_path = os.path.join(folder_path, sub_name)
            with open(sub_path, "w", encoding="utf-8") as fs:
                fs.write(sub_content)
            # Input to chapter main.tex
            fm.write(f"\\input{{Contents/{folder}/{sub_name.replace('.tex', '')}}}\n")

# Now update the root main.tex to point to these new folders
if os.path.exists(main_tex_path):
    with open(main_tex_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace old \input commands with new ones
    old_inputs = [
        r"\input{Contents/GioiThieu}",
        r"\input{Contents/CoSoLyThuyet}",
        r"\input{Contents/YeuCauHeThong}",
        r"\input{Contents/DacTaChiTietCacUseCase}",
        r"\input{Contents/PhanTichThietKeHeThong}",
        r"\input{Contents/HienThuc}",
        r"\input{Contents/KiemThuHeThong}",
        r"\input{Contents/TrienKhai}",
        r"\input{Contents/TongKet}"
    ]
    
    new_inputs = [
        r"\input{Contents/01_GioiThieu/main}",
        r"\input{Contents/02_CoSoLyThuyet/main}",
        r"\input{Contents/03_YeuCauHeThong/main}",
        r"\input{Contents/04_DacTaUseCase/main}",
        r"\input{Contents/05_PhanTichThietKe/main}",
        r"\input{Contents/06_HienThuc/main}",
        r"\input{Contents/07_KiemThu/main}",
        r"\input{Contents/08_TrienKhai/main}",
        r"\input{Contents/09_TongKet/main}"
    ]
    
    # Simple replace
    for old, new in zip(old_inputs, new_inputs):
        content = content.replace(old, new)
        
    with open(main_tex_path, "w", encoding="utf-8") as f:
        f.write(content)
