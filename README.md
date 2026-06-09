# Day 09 — Multi-Agent Shopping Assistant

Hệ thống Shopping Assistant theo mô hình multi-agent xây dựng bằng **LangGraph**, sử dụng LLM thật, RAG thật (ChromaDB + sentence-transformers), và mock data local.

## Kiến trúc hệ thống

```
User Input
   │
   ▼
Supervisor Agent  ──────────────────────────────────────────┐
   │ route: policy / data / both / clarification_needed     │
   │                                                         │
   ▼                 ▼                                       │
Worker 1         Worker 2                                    │
Policy/RAG       Data Lookup                                 │
(ChromaDB)       (4 tools)                                   │
   │                 │                                       │
   └────────┬────────┘                                       │
            ▼                                                │
       Worker 3 Response ◄──────────────────────────────────┘
            │
            ▼
      Final Answer
   (Answer: / Evidence: / Status: not_found / Status: clarification_needed)
```

## Trạng thái hoàn thiện (Rubric)

| Tiêu chí | Điểm | Trạng thái |
|---|---|---|
| Supervisor Agent định tuyến đúng nhóm câu hỏi | 15 | ✅ |
| Worker 1 — RAG thật trên policy markdown | 15 | ✅ |
| Worker 2 — 4 tools nhỏ, rõ nhiệm vụ | 15 | ✅ |
| Worker 3 — tổng hợp final answer | 15 | ✅ |
| Chunking đúng cấu trúc H2 + H3 + content | 10 | ✅ |
| ChromaDB + sentence-transformers/all-MiniLM-L6-v2 thật | 10 | ✅ |
| Xử lý `clarification_needed` | 5 | ✅ |
| Xử lý `not_found` | 5 | ✅ |
| Batch test từ `data/test.json` | 10 | ✅ |
| Citation rõ ràng cho policy chunks | 3 | ✅ |
| Trace JSON debug từng bước graph | 3 | ✅ |
| Provider abstraction (gemini/openai/openrouter/ollama/custom) | 2 | ✅ |
| Prompt tách riêng từng agent | 2 | ✅ |
| **Tổng** | **110** | **✅ 100%** |

**Bonus ngoài rubric:** Web UI Streamlit, per-agent model overrides, query expansion, DeepSeek provider, OpenRouter provider.

## Tài nguyên

| File | Mô tả |
|---|---|
| [data/policy_mock_vi.md](data/policy_mock_vi.md) | Knowledge base chính sách mua sắm tiếng Việt |
| [data/order_customer_mock_data.json](data/order_customer_mock_data.json) | Mock data khách hàng / đơn hàng / voucher |
| [data/test.json](data/test.json) | 22 test case cho batch evaluation |
| [Rubric.md](Rubric.md) | Thang điểm chấm bài |
| [Guide.md](Guide.md) | Hướng dẫn chi tiết |
| [src/README.md](src/README.md) | Tài liệu kỹ thuật mã nguồn |

## Cài đặt

```bash
pip install -r src/requirements.txt
```

Tạo file `.env` tại thư mục gốc:

```env
LLM_MODEL=gemini-2.0-flash
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_key_here

# Tuỳ chọn: cấu hình riêng từng agent
# SUPERVISOR_MODEL=gemini-2.0-flash
# POLICY_MODEL=gemini-2.0-flash
# DATA_MODEL=gemini-2.0-flash
# RESPONSE_MODEL=gemini-2.0-flash
```

Các provider hỗ trợ: `gemini`, `openai`, `deepseek`, `ollama`, `openrouter`, `custom`.

## Chạy CLI

Hỏi một câu:

```bash
PYTHONPATH=src python -m app.cli --question "Đơn hàng 1971 có được hoàn trả không?"
```

Batch test toàn bộ 22 câu hỏi:

```bash
PYTHONPATH=src python -m app.cli --batch --test-file data/test.json
```

Rebuild lại Chroma index rồi chạy batch:

```bash
PYTHONPATH=src python -m app.cli --batch --rebuild
```

## Chạy Web UI (Streamlit)

```bash
PYTHONPATH=src python -m streamlit run src/app_ui.py
```

Hoặc trên Windows, chạy thẳng file [run_ui.bat](run_ui.bat).

Giao diện cung cấp:
- Chat trực quan với trace suy luận của agent
- Inspect RAG citations và dữ liệu tra cứu từng bước
- Xem database mock (Customers & Orders)
- Cấu hình LLM Provider, Model, Temperature, RAG Top-K trực tiếp trên sidebar
