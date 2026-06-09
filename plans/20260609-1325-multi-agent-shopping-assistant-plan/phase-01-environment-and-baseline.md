# Phase 01 - Environment and Baseline

## Context Links
- Parent plan: [plan.md](plan.md)
- Scout report: [reports/scout-report.md](reports/scout-report.md)
- Setup docs: `README.md`, `Guide.md`, `src/requirements.txt`
- Config: `src/app/config.py`, `src/provider/*`

## Overview
- Date: 2026-06-09
- Priority: P0
- Implementation status: pending
- Review status: pending
- Description: prepare local environment, select one real LLM provider, install dependencies, and capture scaffold baseline.

## Key Insights
- `Settings.load()` already supports provider selection through `.env`.
- Default model is `gemini-3.1-flash-lite`; Gemini needs `GOOGLE_API_KEY`.
- Chroma data persists under `src/.chroma`; traces under `src/artifacts/traces`.
- No app hosting target exists. This is local CLI execution.

## Requirements
- Create `.env` locally, never commit secrets.
- Install `src/requirements.txt` in a Python virtualenv.
- Confirm scaffold compiles before implementation.
- Keep build/run commands Windows-friendly, but preserve README `PYTHONPATH=src` intent.

## Architecture
- CLI calls `ShoppingAssistant`.
- `ShoppingAssistant` loads settings, provider chat model, data store, RAG store, and compiled graph.
- Provider modules remain the only LLM factory surface.

## Related Code Files
- Modify: none expected in this phase, except optional `.env` local file ignored by git.
- Read: `src/app/config.py`, `src/provider/__init__.py`, provider modules.

## Implementation Steps
1. Create venv: `python -m venv .venv`.
2. Install deps: `.venv\Scripts\python.exe -m pip install -r src\requirements.txt`.
3. Create `.env` with one provider, e.g. Gemini: `LLM_PROVIDER=gemini`, `LLM_MODEL=gemini-3.1-flash-lite`, `GOOGLE_API_KEY=...`.
4. Run baseline syntax check: `.venv\Scripts\python.exe -m py_compile src\app\*.py src\provider\*.py src\rag\*.py`.
5. Record any dependency/API errors before code work.

## Todo List
- [ ] Pick provider and configure `.env`.
- [ ] Install dependencies.
- [ ] Run baseline `py_compile`.
- [ ] Verify no secrets are tracked.

## Success Criteria
- Dependencies install.
- Provider factory can instantiate selected model when API key exists.
- Baseline compile result known.

## Risk Assessment
- `gemini-3.1-flash-lite` availability may vary. Mitigation: use provider abstraction to switch model/provider.
- `sentence-transformers` download can be slow. Mitigation: plan first run time into RAG phase.

## Security Considerations
- `.env` must remain untracked.
- Do not print API keys in logs or traces.

## Agent, Subagent, Skills
- Agent: lead controller.
- Subagent: `researcher-testing` only if dependency install fails.
- Skills: `/ck:devops` for environment issues, `/ck:test` for compile gate.

## Next Steps
- Proceed to Phase 02 after environment and baseline status are clear.

## Unresolved Questions
- None.
