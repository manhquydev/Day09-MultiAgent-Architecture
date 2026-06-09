# Phase 03 - Policy RAG Index

## Context Links
- Parent plan: [plan.md](plan.md)
- Guide sections: `Guide.md` section 7
- Policy file: `data/policy_mock_vi.md`
- Embedding helper: `src/rag/embeddings.py`
- RAG files: `src/rag/parser.py`, `src/rag/vector_store.py`

## Overview
- Date: 2026-06-09
- Priority: P0
- Implementation status: pending
- Review status: pending
- Description: implement H2/H3 policy chunking, persistent Chroma indexing, and search results with citations.

## Key Insights
- Required chunk structure: H2 heading, H3 heading, H3 content.
- Policy has important sections for shipping, returns, vouchers, support clarification.
- Embedding wrapper already uses normalized `sentence-transformers/all-MiniLM-L6-v2`.

## Requirements
- `parse_policy_markdown()` returns chunks with `section_h2`, `section_h3`, `citation`, `rendered_text`.
- Chunk only meaningful H3 sections under current H2.
- `ChromaPolicyStore` uses `chromadb.PersistentClient`.
- `ensure_index()` only rebuilds when collection empty.
- `rebuild()` clears/recreates collection and indexes all chunks.
- `search()` returns top-k hits with `citation`, `content`, `distance`.
- Search tool exposed to workers is named `search_policy` and counts toward the required tool inventory.

## Architecture
- Parser is pure and independent from Chroma.
- Vector store owns Chroma client, collection, embedding model.
- Policy worker later exposes `search_policy(query, top_k)` tool wrapping `ChromaPolicyStore.search`.

## Related Code Files
- Modify: `src/rag/parser.py`, `src/rag/vector_store.py`.
- Read: `src/rag/embeddings.py`, `src/app/config.py`, `data/policy_mock_vi.md`.

## Implementation Steps
1. Implement parser with line-based heading detection.
2. Ignore content before first H3 for chunks, unless a later need appears.
3. Build citation as `{section_h2} > {section_h3}`.
4. Initialize persistent Chroma collection.
5. Add deterministic IDs such as `policy-0001`.
6. Store metadata excluding large duplicate content except citation/headings.
7. Query with embedded user query and map Chroma results safely.
8. Add rebuild path for CLI `rebuild_index=True`.
9. Add smoke checks that return relevant citations for return window, delivery ETA, voucher restoration, and checking goods on delivery.

## Todo List
- [ ] Implement parser.
- [ ] Implement Chroma store init.
- [ ] Implement ensure/rebuild/search.
- [ ] Verify searches for return, delivery, voucher restoration, checking goods.

## Success Criteria
- Parser returns chunks for policy H3 sections.
- Chroma collection persists and can be rebuilt.
- Search returns citations and relevant policy text.
- RAG uses real embeddings, not keyword-only matching.
- Retrieval tests prove Chroma is populated from parsed H2/H3 chunks, not from whole-file embedding.

## Risk Assessment
- Chroma API differences can break collection reset. Mitigation: check installed `chromadb` docs if needed.
- Vietnamese semantic search may need direct query phrasing. Mitigation: use top_k 4 and citations.

## Security Considerations
- Chroma persists under project local `src/.chroma`; do not commit generated index.
- Policy text is mock data and safe for local traces.

## Agent, Subagent, Skills
- Agent: `/ck:context-engineering`.
- Subagent: `researcher-rag` if Chroma API uncertainty appears.
- Implementer subagent: `fullstack_developer` owning `src/rag/parser.py`, `src/rag/vector_store.py`.
- Skills: `/ck:docs-seeker` for current Chroma/LangChain docs, `/ck:test` for retrieval smoke checks.

## Next Steps
- Proceed to Phase 04 after search can retrieve useful citations.

## Unresolved Questions
- None.
