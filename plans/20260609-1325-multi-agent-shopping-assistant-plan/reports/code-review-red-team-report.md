# Code Review Red-team Report

## Scope
- Reviewed plan quality, phase count, execution readiness, and red-team failure modes before implementation.
- Target files: `plan.md`, `phase-01` through `phase-06`, `reports/scout-report.md`.
- Spec sources: `goal.md`, `README.md`, `Guide.md`, `Rubric.md`, `data/test.json`.

## Findings

### Accepted Finding 1 - Medium - Contract Ambiguity
- Location: `plan.md`
- Problem: Overview listed phases and validation commands but did not pin tool inventory, route/status contract, evidence contract, or artifact boundaries.
- Impact: Implementer could build "passing-looking" code with wrong tool count, inconsistent route shape, or traces that omit useful debugging evidence.
- Fix applied: Added `Contracts` section and stricter batch validation gate.

### Accepted Finding 2 - Medium - Voucher Usability Ambiguous
- Location: `phase-02-data-lookup-tools.md`
- Problem: `only_active` filtering was underspecified.
- Impact: Q08 could include used/locked/expired vouchers or exclude restored-but-usable vouchers inconsistently.
- Fix applied: Defined usable vouchers as `active` or `restored` with `remaining_uses > 0`, and added known-case assertions.

### Accepted Finding 3 - Medium - Batch Gate Too Weak
- Location: `phase-06-cli-batch-trace-verification.md`
- Problem: Original success criteria allowed route/status failures to be merely documented.
- Impact: Team could hand off a known-failing lab while claiming validation completed.
- Fix applied: Required all 22 route/status checks to pass, plus expected_contains checks where defined.

### Accepted Finding 4 - Low - LLM Format Drift Not Contained
- Location: `phase-05-langgraph-workers-and-response.md`
- Problem: Plan relied on prompts but did not require fallback formatting when LLM omits required headers/status.
- Impact: CLI could break stable output format despite correct worker facts.
- Fix applied: Added structured fallback response requirement.

## Phase Count Review
- Verdict: keep 6 phases.
- Reason: Existing split follows dependency order and maps to real files. Adding a separate "contracts" phase would add overhead; contracts now live in overview and phase acceptance criteria.

## Red-team Verdict
- Before patch: not ready to implement cleanly; too much was implicit.
- After patch: ready for implementation with clear contracts and stronger validation gates.

## Unresolved Questions
- None.
