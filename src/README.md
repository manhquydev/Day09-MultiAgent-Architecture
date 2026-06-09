# VinShop Shopping Assistant — Tài liệu Mã nguồn (`src/`)

Thư mục `src/` chứa toàn bộ mã nguồn hệ thống Shopping Assistant Multi-Agent. Tất cả các yêu cầu kỹ thuật trong Rubric đã được triển khai đầy đủ.

## Cấu trúc thư mục

```
src/
├── app/
│   ├── graph.py          # LangGraph orchestration — 4 nodes, conditional routing
│   ├── data_access.py    # ShoppingDataStore + 4 LangChain tools
│   ├── prompts.py        # System prompts tách riêng cho từng agent
│   ├── config.py         # Settings dataclass + .env loader
│   ├── state.py          # TypedDict ShoppingState
│   ├── utils.py          # JSON helpers, retry, timestamp
│   └── cli.py            # CLI: --question / --batch / --rebuild
├── rag/
│   ├── parser.py         # Markdown chunker (H2 / H3 / content)
│   ├── vector_store.py   # ChromaPolicyStore (Chroma persistent)
│   └── embeddings.py     # SentenceTransformerEmbeddings wrapper
├── provider/
│   ├── __init__.py       # get_chat_model() router động
│   ├── gemini.py         # Google Gemini API
│   ├── openai.py         # OpenAI GPT models
│   ├── deepseek.py       # DeepSeek API
│   ├── ollama.py         # Ollama local models
│   ├── openrouter.py     # OpenRouter API
│   └── custom.py         # Custom OpenAI-compatible endpoint
├── app_ui.py             # Streamlit Web UI (bonus)
├── requirements.txt
└── artifacts/            # Trace JSON và batch output
```

## Các module chính

### `src/rag/` — RAG Engine

| File | Chức năng |
|---|---|
| `parser.py` | Parse policy markdown thành chunks theo cấu trúc `## H2 / ### H3 / content`. Hỗ trợ cả trường hợp H2 không có H3 con. Mỗi chunk có field `citation` dạng `"H2 > H3"`. |
| `vector_store.py` | Quản lý ChromaDB persistent collection. Hỗ trợ `ensure_index()` (lazy build) và `rebuild()` (force rebuild). Search trả về danh sách hits kèm `citation`, `content`, `distance`. |
| `embeddings.py` | Wrapper `SentenceTransformerEmbeddings` dùng model `sentence-transformers/all-MiniLM-L6-v2`. |

### `src/provider/` — LLM Provider Abstraction

`get_chat_model(settings, provider, model)` tự động khởi tạo đúng provider. Hỗ trợ:

| Provider | Model ví dụ |
|---|---|
| `gemini` | `gemini-2.0-flash`, `gemini-2.5-flash` |
| `openai` | `gpt-4o`, `gpt-4o-mini` |
| `deepseek` | `deepseek-chat`, `deepseek-reasoner` |
| `ollama` | `llama3.2`, `mistral` (local) |
| `openrouter` | bất kỳ model trên openrouter.ai |
| `custom` | bất kỳ endpoint tương thích OpenAI |

Có thể cấu hình riêng từng agent qua biến môi trường `SUPERVISOR_MODEL`, `POLICY_MODEL`, `DATA_MODEL`, `RESPONSE_MODEL`.

### `src/app/graph.py` — LangGraph Orchestration

**Supervisor Node** — định tuyến dựa trên LLM kết hợp regex:
- `policy` → chỉ cần tra chính sách
- `data` → chỉ cần tra dữ liệu (có ID cụ thể)
- `policy + data` → câu hỏi kết hợp
- `clarification_needed` → câu hỏi có "tôi" nhưng thiếu ID

**Worker 1 (Policy RAG)** — tìm kiếm Chroma với query expansion cho các từ khoá đổi trả / hoàn tiền.

**Worker 2 (Data Lookup)** — gọi 4 tools, tổng hợp facts từ customer, orders, vouchers.

**Worker 3 (Response)** — tổng hợp `Answer:` + `Evidence:`, hoặc trả `Status: clarification_needed` / `Status: not_found`.

**Trace** — mỗi node đẩy một entry vào `state["trace"]` với timestamp UTC, input, output, raw_response LLM.

### `src/app/data_access.py` — 4 LangChain Tools

| Tool | Mô tả |
|---|---|
| `get_customer_by_id` | Tra thông tin khách hàng theo `customer_id` (ví dụ `C001`) |
| `get_orders_by_customer_id` | Danh sách đơn hàng gần đây của khách hàng |
| `get_order_detail_by_order_id` | Chi tiết một đơn hàng theo `order_id` (ví dụ `1971`) |
| `get_vouchers_by_customer_id` | Danh sách voucher; hỗ trợ `only_active=True` lọc voucher còn dùng được |

Tất cả ID đều được ép kiểu `str` trước khi lookup để tránh lỗi type mismatch.

### `src/app/prompts.py` — System Prompts

Prompts tách riêng cho từng agent: `SUPERVISOR_PROMPT`, `POLICY_WORKER_PROMPT`, `DATA_WORKER_PROMPT`, `RESPONSE_WORKER_PROMPT`.

### `src/app_ui.py` — Streamlit Web UI (Bonus)

- Chat interface với trace suy luận từng agent
- Inspect RAG citations, dữ liệu tra cứu thực tế từng bước
- Xem mock database (Customers & Orders tab)
- Sidebar cấu hình trực tiếp: Provider, Model, Temperature, RAG Top-K
- Hỗ trợ Dark/Light mode

## Chạy thử nghiệm

### CLI

```bash
# Một câu hỏi
PYTHONPATH=src python -m app.cli --question "Đơn hàng 1971 có được hoàn trả không?"

# Batch 22 test cases
PYTHONPATH=src python -m app.cli --batch --test-file data/test.json

# Rebuild Chroma index rồi chạy batch
PYTHONPATH=src python -m app.cli --batch --rebuild
```

Kết quả batch lưu tại `src/artifacts/`: `summary.json` và trace JSON từng case.

### Streamlit Web UI

```bash
PYTHONPATH=src python -m streamlit run src/app_ui.py
```

Trên Windows: chạy file `run_ui.bat` ở thư mục gốc.

## Cấu hình `.env`

```env
LLM_MODEL=gemini-2.0-flash
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_key_here

# Tuỳ chọn: per-agent model override
# SUPERVISOR_PROVIDER=gemini
# SUPERVISOR_MODEL=gemini-2.0-flash
# POLICY_PROVIDER=gemini
# POLICY_MODEL=gemini-2.0-flash
# DATA_PROVIDER=gemini
# DATA_MODEL=gemini-2.0-flash
# RESPONSE_PROVIDER=gemini
# RESPONSE_MODEL=gemini-2.0-flash

# RAG
# EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
# RAG_TOP_K=6
```
