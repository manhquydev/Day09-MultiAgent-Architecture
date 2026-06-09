# Phase 06 - CLI, Batch, Trace, Verification

## Context Links
- Parent plan: [plan.md](plan.md)
- CLI: `src/app/cli.py`
- Batch tests: `data/test.json`
- Rubric: `Rubric.md`
- Guide sections: `Guide.md` sections 12-15

## Overview
- Date: 2026-06-09
- Priority: P0
- Implementation status: pending
- Review status: pending
- Description: finish CLI entry point, batch runner, trace files, summary output, and final verification loop.

## Key Insights
- Rubric awards 10 points for batch test and 3 for trace JSON.
- Test cases include expected route/status and partial expected contains.
- No hosted deployment needed; hand-off is reproducible local CLI commands.

## Requirements
- CLI supports `--question`, `--trace-file`, `--batch`, `--test-file`.
- `run_batch()` saves per-case trace JSON and `summary.json`.
- Summary includes case ID, question, expected/actual route, expected/actual status, pass flags, and trace path.
- Validation must not fake LLM/RAG/data results.
- Run compile, smoke tests, and batch.
- Batch is not accepted with known route/status failures; fix implementation or document external blocker before hand-off.

## Architecture
- `app.cli` parses args and calls `ShoppingAssistant`.
- `ShoppingAssistant.run_batch()` owns batch loop and output directory creation.
- Trace filenames use test IDs when available.
- Summary JSON lives under a clear artifact dir such as `src/artifacts/traces/batch-YYYYMMDD-HHMM/summary.json`.

## Related Code Files
- Modify: `src/app/cli.py`, `src/app/graph.py`.
- Read: `data/test.json`, `src/app/utils.py`.
- Generated: `src/artifacts/traces/**`, `src/.chroma/**`.

## Implementation Steps
1. Finish CLI single-question path and print final answer.
2. Finish CLI batch path and print summary location/counts.
3. Implement batch output dir creation.
4. Add simple evaluator for expected route/status/contains.
5. Run syntax compile.
6. Run targeted single questions:
   - `Chính sách hoàn trả hàng ra sao?`
   - `Đơn hàng 1971 bao giờ được giao?`
   - `Đơn hàng 1971 có được hoàn trả không?`
   - `Voucher của tôi còn dùng được không?`
   - `Kiểm tra đơn hàng 9999 giúp tôi`
7. Run full batch with `data/test.json`.
8. Fix failures without weakening tests.
9. Inspect at least one trace each for policy, data, mixed, clarification, and not_found to confirm the trace contract.

## Todo List
- [ ] Implement CLI single and batch.
- [ ] Implement batch summary and evaluator.
- [ ] Run compile.
- [ ] Run smoke tests.
- [ ] Run full batch.
- [ ] Run code review.
- [ ] Update project docs/changelog only if required by final implementation scope.

## Success Criteria
- `python -m py_compile src/app/*.py src/provider/*.py src/rag/*.py` passes.
- Single question CLI works.
- Batch generates trace JSON files and `summary.json`.
- Expected route/status pass for all 22 cases; expected_contains pass for Q01 and Q11.
- Summary records failures explicitly with error messages, not silent omissions.
- Code review findings addressed before hand-off.

## Risk Assessment
- Live LLM can make outputs nondeterministic. Mitigation: deterministic route/status evaluator checks structured state, not prose only.
- Batch can be slow due to LLM calls. Mitigation: run smoke tests first; rebuild index once.

## Security Considerations
- Ensure traces do not include secrets.
- Keep generated artifacts uncommitted unless explicitly requested.

## Agent, Subagent, Skills
- Agent: `/ck:test` for validation.
- Subagent: `tester` owns test execution and failure report.
- Subagent: `code-reviewer` reviews final changed code.
- Subagent: `docs-manager` updates docs if implementation changes user-facing commands.
- Skills: `/ck:backend-development`, `/ck:test`, `/ck:code-review`, `/ck:docs`.

## Next Steps
- Mark plan implementation complete only after validation evidence exists.

## Unresolved Questions
- None.
