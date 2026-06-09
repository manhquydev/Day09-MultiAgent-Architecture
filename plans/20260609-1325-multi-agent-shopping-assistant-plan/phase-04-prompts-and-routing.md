# Phase 04 - Prompts and Routing

## Context Links
- Parent plan: [plan.md](plan.md)
- Prompt file: `src/app/prompts.py`
- Graph TODOs: `src/app/graph.py`
- Test cases: `data/test.json`
- Guide sections: `Guide.md` sections 8-9

## Overview
- Date: 2026-06-09
- Priority: P0
- Implementation status: pending
- Review status: pending
- Description: replace placeholder prompts and implement robust supervisor classification for policy, data, mixed, clarification, and not_found flows.

## Key Insights
- `data/test.json` defines explicit expected routes for 22 cases.
- Clarification cases have no usable customer/order ID.
- Mixed cases ask data-specific question requiring policy interpretation.
- Supervisor should output parseable JSON.

## Requirements
- Prompts must be concise, Vietnamese-compatible, and JSON-oriented where needed.
- Supervisor output fields: `status`, `needs_policy`, `needs_data`, `clarification_question`, optional extracted IDs.
- Routing should handle:
  - policy only
  - data only
  - data + policy
  - clarification_needed
- Keep deterministic fallback for malformed LLM JSON using `extract_json_payload`.
- Route normalization must match `data/test.json`: `policy`, `data`, `data+policy`, or `[]` for clarification.

## Architecture
- `prompts.py` contains only prompt templates.
- `supervisor_node` invokes LLM and parses JSON.
- Conditional edge function uses route booleans/status, not ad hoc question text after supervisor.
- Trace includes supervisor raw/parsed output.

## Related Code Files
- Modify: `src/app/prompts.py`, `src/app/graph.py`.
- Read: `src/app/utils.py`, `src/app/state.py`, `data/test.json`.

## Implementation Steps
1. Write strict supervisor prompt with examples for route classes.
2. Write policy/data/response prompts with required output format.
3. Implement supervisor node with LLM call and JSON parse.
4. Add conservative heuristic fallback for IDs and route if LLM JSON invalid.
5. Ensure missing "của tôi" voucher/order questions route to clarification.
6. Trace route decision with timestamp and parsed route.
7. Build a route check table from `data/test.json`: Q01-Q05/Q20 policy, Q06-Q10/Q17-Q19/Q21 data, Q11-Q14/Q22 mixed, Q15-Q16 clarification.

## Todo List
- [ ] Replace prompt placeholders.
- [ ] Implement supervisor JSON parsing.
- [ ] Implement route fallback.
- [ ] Verify expected routes for all 22 test questions without calling workers where possible.

## Success Criteria
- Expected route matches `data/test.json` for policy/data/mixed/clarification cases.
- Clarification output contains a clear question asking for `order_id` or `customer_id`.
- Supervisor does not hard-code final answers.
- Malformed supervisor JSON cannot crash the graph; fallback returns a traceable route decision.

## Risk Assessment
- LLM routing can vary. Mitigation: strict JSON prompt plus deterministic fallback.
- Too much heuristic can become hard-coded flow. Mitigation: use heuristics only for classification and ID extraction.

## Security Considerations
- Do not include API keys or environment content in prompts/traces.
- Keep user question only as trace input.

## Agent, Subagent, Skills
- Agent: `/ck:context-engineering`.
- Subagent: `researcher-langgraph` for current LangGraph conditional edge patterns if needed.
- Implementer subagent: `fullstack_developer` owning `src/app/prompts.py` and supervisor parts of `src/app/graph.py`.
- Skills: `/ck:docs-seeker`, `/ck:backend-development`, `/ck:test`.

## Next Steps
- Proceed to Phase 05 after route decisions are stable.

## Unresolved Questions
- None.
