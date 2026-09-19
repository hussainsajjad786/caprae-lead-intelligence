# Interview preparation

Use these as explanations to understand, not answers to memorize. Open the corresponding module and trace one request before recording.

1. **Why React?** Components keep the table, filters and detail panel understandable. React state separates draft filters from applied filters and updates the UI after API responses. The app does not need a large global state library.

2. **Why FastAPI?** It provides typed request validation, straightforward route definitions and generated OpenAPI docs. It is a good fit for a small Python service. Synchronous SQLAlchemy routes are ordinary `def` functions; async syntax would not automatically make database work faster.

3. **Why SQLite?** The small, single-process demo needs reproducibility more than concurrent writes. SQLite is a local file with no separate database service. It is not a claim that SQLite is right for a multi-tenant production workload.

4. **Why SQLAlchemy?** It separates Python models and query construction from SQL details, binds query values, and eases a future database transition. It does not replace schema migrations or database knowledge.

5. **How does scoring work?** Size 25, industry 25, revenue 20, market 10, format checks 10, completeness 10. The same inputs produce the same score. Each component and maximum is returned in the detail response.

6. **Why rules instead of ML?** No labeled outcome dataset exists. Rules are transparent and easy to challenge. An ML system should earn its complexity through evaluated ranking quality, not a label on the UI.

7. **How does deduplication work?** Normalize the domain, match it against a unique indexed column, then use normalized name plus market as a fallback if a domain is absent. Preserve rejected inputs in DuplicateReview. Do not merge distinct valid domains solely because names match.

8. **How does validation work?** Parse HTTP(S) URLs, normalize hostnames and validate email syntax. No DNS requests or emails are sent. A syntactically valid address can still be fictional, unreachable or unauthorized for outreach.

9. **How would this scale to a million leads?** Measure query plans, migrate to PostgreSQL, add appropriate search indexes and keyset pagination, move ingestion/export into bounded workers, and implement source/tenant limits. The current `.all()` export must become batched or asynchronous; do not load a million rows into memory.

10. **How would you use PostgreSQL?** Use a supported driver, explicit Alembic migrations, uniqueness constraints, pool limits and staging tests. Choose indexes from actual filters and ordering, and consider pg_trgm/full-text search for text lookup.

11. **Where would Redis help?** Expensive repeated analytics or search results, with cache keys containing the query, tenant, profile and dataset version. Set TTLs and invalidate after updates. The current dataset is too small to justify a Redis service.

12. **Changing websites?** Prefer documented APIs. For permitted parsing, isolate each adapter, validate schemas, test saved fixtures and monitor missing-field rates. Stop and inspect structural changes rather than silently importing garbage.

13. **CAPTCHA?** Stop automation and use an authorized API, permission-based workflow or human review where allowed. Do not bypass the protection or promise stealth scraping.

14. **IP restrictions?** Respect rate limits and blocks, back off on 429 responses, honor Retry-After and contact the provider. Rotating identities to evade a restriction is not part of this design.

15. **Ethical scraping?** Use permitted sources, review terms and applicable privacy obligations, minimize collected fields, preserve provenance and retention rules, and respect technical protections. Public accessibility alone is not permission for every use.

16. **CRM integration?** Map canonical lead fields to the CRM schema, let the user approve a preview, store stable external IDs, use idempotent upserts and retry with limits. Track failures and duplicate conflicts rather than claiming every row synced.

17. **Replacing SQLite?** Database URL is only one step. Add the PostgreSQL driver, migrations, backup/export, import checks, transaction tests and rollback. Validate row counts, null handling and uniqueness before switching traffic.

18. **How would you deploy?** Build static React assets on Vercel, run FastAPI as a persistent process with HTTPS and configured CORS, and give SQLite a persistent disk for the demo. In production, use PostgreSQL. On Ubuntu, use a non-root systemd service behind nginx, monitor logs and health, and keep secrets outside Git.

19. **Most important product decision?** Making fit and quality visible separately. A high fit score does not certify a contact; the researcher can inspect missing or invalid data before export.

20. **What next?** A configurable customer profile and one permitted connector with source/freshness metadata. Those changes would test whether the workflow improves actual research before adding more infrastructure or ML.

## Ten things to explain without reading

1. The exact researcher problem and the two chosen workflows.
2. One request from React through FastAPI, services and SQLite.
3. The 100-point calculation and 75/50 priority boundaries.
4. Why format validity is different from external verification.
5. Why populated fields and usable fields produce different percentages.
6. Exact domain matching, name fallback and retained duplicate inputs.
7. Why export and table filters must match, and how CSV formula protection works.
8. Why SQLite fits the demo and what a real PostgreSQL migration requires.
9. What is implemented, what is proposed, and what remains untested in production.
10. Your actual contribution, AI assistance, lessons learned and one tradeoff you would revisit.

## Practice exercises

Calculate Aster Cloud's score from the rules. Then remove its email and recalculate completeness, quality and fit. Explain why a strong fit can still need review. Run a search containing `%` and explain why it is treated literally. Find the route-ordering decision that keeps `/export` from being interpreted as a lead ID. Describe how the unique domain constraint and service-level review complement each other.
