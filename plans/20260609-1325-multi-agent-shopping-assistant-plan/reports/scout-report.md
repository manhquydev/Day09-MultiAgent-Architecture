# Scout Report

## Scope
- Read `README.md`, `Guide.md`, `Rubric.md`, `src/README.md`, `data/README.md`.
- Inspected current scaffold files in `src/app`, `src/rag`, `src/provider`.
- Checked `data/test.json`, policy heading structure, and mock data metadata.

## Relevant Files
- `README.md` - lab mission, required workers, RAG/data/tools, run commands.
- `Guide.md` - detailed implementation order and expected node/tool behavior.
- `Rubric.md` - score gates: supervisor, RAG, data tools, response, batch, trace.
- `src/app/graph.py` - main orchestration TODOs: assistant lifecycle, LangGraph nodes, routing, batch.
- `src/app/data_access.py` - mock data store and four required lookup tools.
- `src/app/prompts.py` - supervisor, policy, data, response prompt placeholders.
- `src/app/state.py` - minimal shared graph state already defined.
- `src/app/cli.py` - CLI entry point TODO for single question and batch.
- `src/rag/parser.py` - policy markdown chunking TODO.
- `src/rag/vector_store.py` - Chroma persistent index and search TODO.
- `src/rag/embeddings.py` - real `sentence-transformers/all-MiniLM-L6-v2` wrapper exists.
- `src/provider/__init__.py` and provider modules - model factory exists for gemini/openai/openrouter/ollama/custom.
- `data/policy_mock_vi.md` - policy KB with H2/H3 structure; return policy starts around section 5.
- `data/order_customer_mock_data.json` - 80 customers, 360 orders, 284 vouchers.
- `data/test.json` - 22 validation cases covering policy, data, mixed, clarification, not_found.

## Key Findings
- Source files are currently under 200 lines; no modularization needed before implementation.
- No local `CLAUDE.md` exists, so repository-level extra workflow rules are absent.
- `goal.md` is untracked and contains the plan-only objective.
- No source implementation should happen in this task; plan artifact only.
- Hosting is not a current requirement. Deliverable is a local CLI/library lab runnable with `PYTHONPATH=src python -m app.cli`.

## Unresolved Questions
- None.
