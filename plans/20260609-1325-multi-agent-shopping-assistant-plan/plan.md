---
title: "Multi-agent shopping assistant plan"
description: "Phase plan to finish the LangGraph shopping assistant lab with real LLM, RAG, data tools, traces, and batch validation."
status: pending
priority: P2
effort: 9h
branch: main
tags: [langgraph, rag, multi-agent, shopping-assistant]
created: 2026-06-09
---

# Multi-agent Shopping Assistant Plan

## Goal
Complete the local CLI shopping assistant lab in `src/` using LangGraph, real LLM provider, Chroma, `sentence-transformers/all-MiniLM-L6-v2`, mock JSON data, trace output, and `data/test.json` batch validation.

## Current Evidence
- Mission and technical requirements: `README.md`, `Guide.md`, `Rubric.md`.
- Scaffold TODOs: `src/app/graph.py`, `src/app/data_access.py`, `src/app/prompts.py`, `src/rag/parser.py`, `src/rag/vector_store.py`, `src/app/cli.py`.
- Existing helpers: `src/app/config.py`, `src/app/state.py`, `src/app/utils.py`, `src/rag/embeddings.py`, `src/provider/*`.
- Scout report: [reports/scout-report.md](reports/scout-report.md).

## Phases
1. [Environment and baseline](phase-01-environment-and-baseline.md) - pending, 0%.
2. [Data lookup tools](phase-02-data-lookup-tools.md) - pending, 0%.
3. [Policy RAG index](phase-03-policy-rag-index.md) - pending, 0%.
4. [Prompts and routing](phase-04-prompts-and-routing.md) - pending, 0%.
5. [LangGraph workers and response](phase-05-langgraph-workers-and-response.md) - pending, 0%.
6. [CLI, batch, trace, verification](phase-06-cli-batch-trace-verification.md) - pending, 0%.

## Contracts
- Required tools: `search_policy`, `get_customer_by_id`, `get_orders_by_customer_id`, `get_order_detail_by_order_id`, `get_vouchers_by_customer_id`.
- Route contract: normalize final route to a list containing only `policy` and/or `data`; clarification route is `[]`.
- Status contract: every run resolves to `ok`, `clarification_needed`, or `not_found`.
- Evidence contract: success answers include policy evidence when route has `policy`, and data evidence when route has `data`.
- Trace contract: trace captures supervisor decision, worker tool calls, retrieved policy citations, lookup statuses, final status, and final answer.
- Artifact contract: generated `.env`, `src/.chroma/**`, and `src/artifacts/traces/**` stay out of git unless explicitly requested.

## Agent Map
- Lead/controller: Codex main agent, keep scope, integrate results.
- Planner: `/ck:plan` plus `planning`, maintain phase files.
- Researchers: `researcher-langgraph`, `researcher-rag`, `researcher-testing` if docs/API uncertainty appears.
- Implementers: `/ck:backend-development`, `/ck:context-engineering`, `/ck:databases` as phase skills.
- QA: `tester` subagent with `/ck:test`; then `code-reviewer` subagent with `/ck:code-review`.
- Docs: `docs-manager` subagent with `/ck:docs` only if implementation changes public docs.

## Validation Gates
- Syntax: `python -m py_compile src/app/*.py src/provider/*.py src/rag/*.py`.
- Single runs: `PYTHONPATH=src python -m app.cli --question "..."`
- Batch: `PYTHONPATH=src python -m app.cli --batch --test-file data/test.json`.
- Evidence: all 22 test cases pass route/status checks, expected_contains checks pass where defined, traces saved per case, summary JSON generated.

## Non-goals
- No hosted web deployment unless requirements change.
- No new provider package unless chosen provider cannot satisfy lab.
- No broad refactor before TODOs pass.

## Unresolved Questions
- None.
