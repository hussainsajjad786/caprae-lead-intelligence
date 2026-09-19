# Product and engineering notes

## What I built and why

A synthetic lead-qualification dashboard with two core capabilities: transparent fit scoring and a lead-quality layer. Search, filters, profile details, analytics and export make these capabilities usable end to end.

The user is a researcher or sales operator deciding which businesses to inspect first. The workflow reduces ambiguity about ranking and exposes unusable contact fields. It does not claim to discover real companies or measure conversion performance.

## Reference product analysis

Reviewed the public [SaaSquatch website](https://www.saasquatchleads.com/) on 18 September 2026. The public page advertises company filtering, contact enrichment, revenue estimates, scoring and exports. These support a discovery-to-outreach workflow. This review did not include a signed-in product trial, private screens, or a usability study.

Product hypothesis: users benefit when fit ranking is easy to audit and contact-format checks are clearly distinguished from external verification. This is an intentional focus for this MVP, not proof that SaaSquatch lacks either capability. No unsupported competitive comparison is made.

The copied prompt is a detailed engineering brief, while the handbook is the source for the interview deliverables. The handbook does not mandate React, FastAPI, or SQLite; those are chosen implementation decisions. Its rubric is Business Understanding 10, UX/UI 10, Technicality 10, Design 5, Other 5: 40 total.

## Why these two features

Ranking helps the user allocate attention. Quality checks help the user see whether the information is usable. Together they produce a reviewable shortlist, instead of encouraging indiscriminate collection. The demonstration is deliberately honest about synthetic data and unknown verification.

## UX choices

The overview answers “what do I have?” with four metrics. A clear call to action opens high-priority leads. Draft filters require Apply, so editing fields does not repeatedly change the dataset. A score badge communicates ranking, and the detail panel exposes the calculation. Native dialog behavior supports keyboard focus containment and Escape. Text accompanies status colors. The table scrolls horizontally on narrow screens; filters wrap, and navigation moves to the top.

Loading, empty, retry and export-error states are implemented. Analytics use global totals; the lead list and export use applied filters. The interface states this distinction in Analytics. An export is a synthetically qualified list, not a consented outreach list.

## Architecture and storage

React/Vite calls FastAPI REST endpoints. Pydantic constrains query inputs and response schemas. Service modules own scoring, validation, quality and deduplication. SQLAlchemy maps a Lead table and DuplicateReview table to SQLite.

SQLite keeps local startup simple. A unique normalized-domain index prevents duplicate canonical domains; a review log preserves rejected inputs. Scores/reasons and quality data are materialized on ingestion. Timestamps support future freshness tracking, although live enrichment is not implemented.

## Scoring, validation and deduplication

Six components sum to 100. Weights are readable constants. Industry and market assumptions are an illustrative ICP, not Caprae's verified investment criteria. Ranking rewards some larger companies; an acquisition search may need a different size preference.

Validation is syntax only and performs no network fetch. Completeness measures presence; quality requires syntactically usable email/website values. These differ intentionally: a fully populated record can still contain bad data.

Deduplication first compares normalized hostnames, then falls back to normalized name plus market when a domain is missing. It is not fuzzy entity resolution. Concurrent multi-worker imports need transaction-aware conflict handling and review queues; the current seed is single-process and serial. The service is reusable, but a public import endpoint is intentionally absent.

## Performance, security and hosting

Indexes support common equality filters and score ordering; offset pagination bounds response sizes. Query cancellation prevents stale frontend responses replacing newer ones. Reference data is fetched on mount/retry. No application cache is claimed. Small CSV results are buffered; large jobs would need chunked processing.

CORS is configured from environment variables, SQL values are bound, client strings are escaped by React, spreadsheet formula prefixes are neutralized, and real credentials/data are absent. With only synthetic data and read-only endpoints, the demo avoids the need for an account system.

The proposed hosting split is Vercel static frontend plus Render persistent FastAPI with a mounted SQLite disk. An Ubuntu VM alternative is documented. Neither has been deployed. Native Windows bundler restrictions required a portable esbuild WebAssembly alias during development.

## Five-hour scope

I intentionally focused the MVP on two high-impact workflows: lead prioritization and lead quality. Instead of attempting a large scraping platform, I optimized for a complete, demonstrable workflow.

No exact engineering duration is asserted. Track actual work and disclose AI assistance honestly. Suggested allocation within the handbook limit: 30 minutes research/design, 90 minutes backend/services, 90 minutes UI, 45 minutes tests/fixes, 45 minutes documentation/demo rehearsal. This is a planning budget, not a retrospective time report.

## Intentionally not built

Authentication, payments, live scraping, CAPTCHA/IP bypasses, external email verification, AI API calls, predictive ML, microservices, Kubernetes, CRM synchronization, and production ingestion. These would distract from the chosen workflow or require data, credentials and operational controls beyond this demo.

## Tradeoffs and next steps

Synthetic data makes the demo reproducible but does not prove extraction or real-world accuracy. Exact matching can miss subsidiaries and can flag unrelated same-name companies; preserved originals support manual review. B-tree indexes do not solve full-text search. SQLite serializes writes. No migration framework or multi-tenant authorization is included.

At scale, add PostgreSQL with tested migrations, keyset pagination/search indexes, ingestion workers, source provenance, a configurable ICP, Redis for expensive repeated queries and S3-compatible export storage. CRM integration should be opt-in, use stable IDs, and retain sync errors. Evaluate an ML ranker only after collecting appropriate outcome labels and comparing it against the rule-based baseline.
