# Phase 05 - LangGraph Workers and Response

## Context Links
- Parent plan: [plan.md](plan.md)
- Guide sections: `Guide.md` sections 10-11
- Main graph file: `src/app/graph.py`
- State: `src/app/state.py`
- Helpers: `src/app/utils.py`

## Overview
- Date: 2026-06-09
- Priority: P0
- Implementation status: pending
- Review status: pending
- Description: compile the LangGraph workflow and implement policy worker, data worker, and response synthesis.

## Key Insights
- `ShoppingState` already has required core fields.
- Existing utils support JSON extraction, timestamps, and LangChain message serialization.
- Worker 3 must produce one of three stable text formats.

## Requirements
- `ShoppingAssistant.__init__` loads chat model, data store, embeddings, policy store, tools, and graph.
- `build_graph()` creates `StateGraph(ShoppingState)` with supervisor, policy worker, data worker, response worker.
- Conditional routing sends to policy, data, both, or response for clarification.
- Worker 1 calls RAG search tool first.
- Worker 2 uses small data tools and reflects `not_found`.
- Worker 3 merges route, policy_result, data_result into final answer with evidence.
- Response worker must not invent facts outside worker outputs; if evidence is missing, return clarification or not_found instead of guessing.

## Architecture
- Use shared state keys from `ShoppingState`.
- Nodes are plain functions or closures bound to assistant dependencies.
- For mixed route, run policy and data before response. If parallel edges are complex, sequence data then policy or policy then data with trace; keep correctness over cleverness.
- Response worker returns user-facing string and trace.

## Related Code Files
- Modify: `src/app/graph.py`.
- Read: `src/app/data_access.py`, `src/rag/vector_store.py`, `src/app/prompts.py`, `src/provider/__init__.py`.

## Implementation Steps
1. Refactor graph construction to accept dependencies if needed.
2. Initialize dependencies in `ShoppingAssistant.__init__`.
3. Implement `ask()` initial state and graph invoke.
4. Implement policy tool wrapper and worker node.
5. Implement data worker with tool-bound model or deterministic tool selection assisted by LLM.
6. Implement response worker prompt invocation and fallback formatting.
7. Add conditional edge function.
8. Include trace entries for each node.
9. Add response fallback that formats from structured worker facts if the LLM response is malformed or omits required status/evidence headers.

## Todo List
- [ ] Load model/store/tool dependencies.
- [ ] Compile graph.
- [ ] Implement `ask()`.
- [ ] Implement supervisor, policy, data, response nodes.
- [ ] Save trace when requested.
- [ ] Smoke-test one policy, one data, one mixed, one clarification, one not_found question.

## Success Criteria
- End-to-end `ShoppingAssistant.ask()` returns `route`, worker results, `final_answer`, `trace`.
- Mixed route uses both policy and data evidence.
- Final answer follows required success, clarification, and not_found formats.
- No `NotImplementedError` remains in main runtime path.
- LLM output format drift cannot break CLI response shape.

## Risk Assessment
- LangGraph API changed across versions. Mitigation: use installed version and docs if needed.
- Tool-calling behavior varies by provider. Mitigation: keep deterministic fallback where route and IDs are obvious.
- `graph.py` may approach 200 lines. Mitigation: consider extracting helpers only if it clearly exceeds limit and improves clarity.

## Security Considerations
- Avoid storing raw API responses containing provider metadata in traces unless needed.
- Limit trace to route, tool calls, retrieved chunks, and final answer.

## Agent, Subagent, Skills
- Agent: `/ck:backend-development` plus `/ck:context-engineering`.
- Subagent: `fullstack_developer` owning `src/app/graph.py`.
- QA subagent: `tester` for smoke tests.
- Reviewer subagent: `code-reviewer` after tests pass.
- Skills: `/ck:docs-seeker`, `/ck:test`, `/ck:code-review`.

## Next Steps
- Proceed to Phase 06 after single-question flows work.

## Unresolved Questions
- None.
