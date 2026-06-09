# Phase 02 - Data Lookup Tools

## Context Links
- Parent plan: [plan.md](plan.md)
- Data docs: `data/README.md`
- Guide sections: `Guide.md` sections 5-6
- Rubric: `Rubric.md` Worker 2 and small-tool penalty

## Overview
- Date: 2026-06-09
- Priority: P0
- Implementation status: pending
- Review status: pending
- Description: implement mock JSON loading, indexes, and four small LangChain tools.

## Key Insights
- Dataset metadata: 80 customers, 360 orders, 284 vouchers.
- Required examples: `C001`, `1971`, `2058`, missing `9999`.
- Rubric penalizes one generic lookup tool; use small focused tools.

## Requirements
- Load JSON once in `ShoppingDataStore.__init__`.
- Build `customer_by_id`, `order_by_id`, `orders_by_customer_id`, `vouchers_by_customer_id`.
- Implement methods with stable `status`: `ok`, `not_found`.
- Wrap methods as LangChain tools with clear descriptions.
- Preserve `only_active` voucher filtering.
- Define usable voucher filtering explicitly: include vouchers with `status` in `active` or `restored` and `remaining_uses > 0`; exclude `used`, `expired`, and `locked`.

## Architecture
- `ShoppingDataStore` owns normalized in-memory indexes.
- Data worker uses LangChain tools from `build_data_tools(store)`.
- Methods return serializable dicts only; no raw class instances.

## Related Code Files
- Modify: `src/app/data_access.py`.
- Read: `data/order_customer_mock_data.json`, `data/README.md`, `data/test.json`.
- Possible tests/scripts: lightweight direct calls from Python one-liners or later batch tests.

## Implementation Steps
1. Parse JSON with `json.loads(json_path.read_text(encoding="utf-8"))`.
2. Store metadata and source lists.
3. Build indexes during init.
4. Sort customer orders by `created_at` descending for list tool.
5. Return `not_found` when IDs missing, including queried ID.
6. Implement tools using `langchain_core.tools.tool`.
7. Keep tool names exactly descriptive: `get_customer_by_id`, `get_orders_by_customer_id`, `get_order_detail_by_order_id`, `get_vouchers_by_customer_id`.
8. Add direct assertions for known cases before graph integration: `C001` exists, `C999` not found, `1971` exists, `9999` not found, `C001` active voucher list excludes used voucher `PLAT-FS-0626-C001`.

## Todo List
- [ ] Implement data store init.
- [ ] Implement four lookup methods.
- [ ] Implement LangChain tool wrappers.
- [ ] Manually verify `C001`, `C014`, `1971`, `2058`, `9999`, `C999`.

## Success Criteria
- Each method returns `status`.
- Missing order/customer cases return `not_found`.
- Voucher active filter has deterministic, documented status rules.
- Four separate tools visible to data worker.

## Risk Assessment
- Large JSON output can be noisy. Mitigation: worker response should summarize relevant fields.
- Dates are strings. Mitigation: sort ISO-like strings directly unless format issue found.

## Security Considerations
- Mock data includes sample emails/phones. Keep traces local under `src/artifacts/traces`.
- Do not treat mock PII as production data.

## Agent, Subagent, Skills
- Agent: `/ck:backend-development`.
- Subagent: `fullstack_developer` owning `src/app/data_access.py`.
- QA subagent: `tester` for direct lookup checks.
- Skills: `/ck:databases` for indexing pattern, `/ck:test` for validation.

## Next Steps
- Proceed to Phase 03 after reliable lookup tools exist.

## Unresolved Questions
- None.
