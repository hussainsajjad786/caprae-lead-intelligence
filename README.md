# Caprae Lead Intelligence

**Find, qualify, verify, and prioritize the leads that matter.**

A focused interview MVP with two major features: transparent lead prioritization and an honest lead-quality layer. React + FastAPI + SQLAlchemy + SQLite. All records are fictional; “Format Valid” means syntax checks only.

## Problem and solution

A long prospect list is not a useful shortlist. Sales researchers need to see fit, missing information, and repeated companies before exporting leads into their workflow. This app takes a small synthetic dataset through search, qualification, quality review, deduplication, ranking, and filtered CSV export.

The intended benefit is less time sorting irrelevant or incomplete records and a cleaner handoff to sales. This demo has no measured conversion lift, time savings, or production performance results.

## Key features

1. **Intelligent lead scoring:** a deterministic 0–100 fit score with six visible contributions and High/Medium/Low priorities.
2. **Lead quality and verification layer:** format validation, completeness, quality flags, domain normalization, and duplicate prevention with a retained review log.

Filtering, the detail panel, deduplication, CSV export, and descriptive analytics support those two workflows. There is no live scraper, predictive ML, authentication, CRM connector, or external contact verification.

## Run locally

Use Python 3.12 and Node.js 22.12+ (Node 24 is also suitable). Commands below start in this repository's root. Python 3.14 is not the tested runtime for these pinned dependencies.

**Terminal 1 — backend (Windows PowerShell)**

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

If `py -3.12` is unavailable, install Python 3.12 or use the full path to a Python 3.12 executable. Activation is optional; calling the virtual environment's interpreter directly avoids PowerShell execution-policy changes.

**Terminal 2 — frontend**

```powershell
cd frontend
npm install
npm run dev
```

After the lockfile exists, `npm ci` is the reproducible installation command. If PowerShell blocks npm.ps1, use `npm.cmd` instead of `npm`.

**macOS/Linux backend**

```bash
cd backend
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend: **http://127.0.0.1:5173** · API: **http://127.0.0.1:8000** · OpenAPI: **http://127.0.0.1:8000/docs**

First startup creates `backend/leads.db`, seeds 32 canonical leads, and records 2 prevented duplicates from 34 synthetic source rows. Restarting does not reseed existing data. This is a single-process demo; start one backend worker.

## Demo flow

1. Inspect the overview: total leads, high priority, format validity, and average fit.
2. Click **Explore top leads**, or apply an industry/market/minimum-score filter.
3. Open **Aster Cloud** and explain how the six components sum to 100.
4. Open **Data Quality**: inspect a malformed record and a prevented duplicate.
5. Export CSV; it contains all results for the applied filters, including pages not currently visible.
6. Show Analytics and explain that its numbers describe the entire demo dataset.

## Architecture and tech stack

```text
User
  |
React 19 + Vite 6 + Lucide icons + CSS
  |  HTTP JSON / CSV
FastAPI + Pydantic
  |
Services
  +-- Scoring
  +-- Validation
  +-- Deduplication
  +-- Quality
  |
SQLAlchemy 2
  |
SQLite
```

The browser keeps draft filters separate from applied filters, cancels obsolete fetches, and loads reference lists once per mount/retry. The API owns filtering and derived data. Scoring and quality checks run during ingestion, never independently in the browser. Pytest validates service behavior and routes.

The frontend uses the esbuild WebAssembly package under the `esbuild` alias to avoid native executable filesystem restrictions on the development Windows host. It provides the same build API, with slower cold builds. This is a build-time portability tradeoff, not a browser dependency.

## Database design

`Lead` stores company/contact fields, normalized domain and name, nullable employees/revenue, fit score, priority, validation flags, completeness, quality score, JSON reasons, and timestamps. Revenue is an illustrative USD estimate. `normalized_domain` has a unique index; name, industry, market, score, and priority also have indexes. Nullable domains let incomplete companies enter review.

`DuplicateReview` retains each rejected incoming record, its matched lead ID, and the reason. Accepted leads are canonical; `is_duplicate` stays false. The review table makes duplicate detection visible without putting duplicate rows into exports. `create_all` is adequate for a disposable demo; production schema changes require migrations.

## Scoring logic

This is a transparent rule-based prioritization model created for the interview MVP, not a predictive ML model.

| Component | Maximum | Rules |
|---|---:|---|
| Company size | 25 | 200+: 25; 50–199: 20; 10–49: 12; 1–9: 5; missing/zero: 0 |
| Industry fit | 25 | Technology, SaaS, FinTech, Healthcare, AI, Cybersecurity: 25; another sector: 5; missing: 0 |
| Revenue fit | 20 | USD 10M+: 20; 5M+: 15; 1M+: 10; positive lower estimate: 5; missing/zero: 0 |
| Market fit | 10 | United States, Canada, United Kingdom: 10; another market: 3; missing: 0 |
| Format checks | 10 | Valid email syntax: 5; valid website syntax: 5 |
| Completeness | 10 | Rounded populated fraction of eight fields × 10 |

High is 75–100, Medium is 50–74, Low is 0–49. Constants live in `backend/app/services/scoring.py`. Python's built-in round uses ties-to-even. The size and industry preferences are an illustrative B2B profile, **not Caprae's investment mandate**. Larger does not universally mean better; a production customer needs a configurable ICP.

## Validation and deduplication

- URLs accept HTTP(S) or a bare hostname, reject userinfo, bad ports, spaces and malformed hostnames; normalize lowercase/IDNA, `www.`, and trailing hostname dots.
- Email validation is conservative syntax validation. It does not implement all RFC mailbox forms and does not check DNS, deliverability, ownership, or consent.
- Exact normalized domains identify duplicates. If either side lacks a domain, exact normalized company name **and market** trigger a review. Distinct valid domains are not merged solely on name.
- This is exact host matching, not public-suffix-aware entity resolution. Subdomains may represent different businesses. Name matching can produce false positives; the original record is retained for review.
- Completeness counts populated company, website, email, phone, industry, location, employees, and revenue. Quality uses the same eight fields but requires email/website formats to pass. High Quality is 85+, Medium is 60–84, Low is below 60.
- No live network requests run per lead. Zero records are externally verified.

## API documentation

Interactive schemas and examples are at `/docs`.

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | API identity and dataset notice |
| GET | `/health` | Process health |
| GET | `/api/leads` | Filtered, score-sorted list with pagination |
| GET | `/api/leads/{lead_id}` | Full profile, score reasons, quality flags |
| GET | `/api/leads/export` | CSV using the same filters |
| GET | `/api/stats` | Global counts, averages, industry/priority distributions |
| GET | `/api/industries` | Available industries |
| GET | `/api/locations` | Available markets |
| GET | `/api/quality/duplicates` | Prevented duplicate summaries |

List/export filters: `search`, `industry`, `location`, `min_score`, `max_score`, `priority`, `verification_status`. List pagination: `offset` (0+) and `limit` (1–100; default 50). Scores are bounded 0–100, minimum must not exceed maximum, invalid filters return 422, and missing IDs return 404. Search is case-insensitive and treats SQL wildcard characters literally. Export is registered before the numeric detail route.

```text
/api/leads?industry=SaaS&min_score=75&verification_status=Format%20Valid
```

## Performance and caching

SQLite is sufficient for 32 demo companies, and indexes support common exact filters and ranking. Substring search can still scan the table; indexes do not make arbitrary `%term%` searches fast. Paginated JSON avoids loading every lead into the table. Derived scores are persisted, and SQL aggregates compute statistics.

There is **no Redis, server response cache, or frontend query-cache library**. Reference data is held in React state after loading. The CSV implementation buffers the small result set in memory; the response wrapper does not make this a large-scale streaming pipeline. For large exports, use chunked reads and background jobs.

## Deployment

The simplest interview demo now uses one Render service: `render.yaml` builds React and serves it from FastAPI when `SERVE_FRONTEND=true`. Follow [PUBLISH_AND_RECORD.md](PUBLISH_AND_RECORD.md). UI and API share one origin; SQLite is rebuilt from the synthetic seed when the free instance's ephemeral files disappear. No public deployment has been performed.

See [DEPLOYMENT.md](DEPLOYMENT.md) for alternative Vercel + Render and Ubuntu instructions. The backend is a persistent FastAPI process, not a SQLite-backed serverless function.

The root `.env.example` documents backend settings. Copy it to `.env` to override defaults. `frontend/.env.example` documents `VITE_API_URL`; copy it to `frontend/.env` for a separate remote backend. Never put secrets in `VITE_*`: they are embedded in the client bundle. CORS accepts only listed origins, though CORS is not authentication.

## Security and ethical data collection

Demo data is synthetic and is included only to demonstrate the product workflow. Production ingestion would use permitted public/business data sources and appropriate terms of service.

No private data, third-party logins, aggressive scraping, CAPTCHA solving, or restriction bypassing is implemented. Hosts are subdomains of reserved `example.com`; phones use the fictional NANP 555-0100–0199 range. Never contact these demo records. SQLAlchemy binds query values, React escapes rendered text, CSV formula prefixes are neutralized, and no user-controlled outbound URL is fetched. No production write endpoint is exposed.

Public hosting is suitable only for this synthetic, read-only demo. Authentication, authorization, quotas, source permissions, privacy controls, and operational monitoring must precede real customer data.

## Tests and build

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```

Or `pytest` after activating the environment. Linux: `.venv/bin/python -m pytest -q`.

```powershell
cd frontend
npm run build
npm audit
```

See [SUBMISSION_AUDIT.md](SUBMISSION_AUDIT.md) for actual verification results and outstanding candidate actions. The repository contains tests for score boundaries, malformed inputs, normalization, idempotent seeding, duplicate retention, pagination, filter parity, health, and CSV protection.

## Five-hour scope and future improvements

I intentionally focused the MVP on two high-impact workflows: lead prioritization and lead quality. Instead of attempting a large scraping platform, I optimized for a complete, demonstrable workflow.

The handbook caps engineering at five hours. No exact authoring duration is claimed here; candidates should keep and disclose their own time log and AI assistance. Authentication, payments, microservices, production ingestion, and ML were deliberately excluded.

Future work: permitted source connectors, source provenance/freshness, configurable ICP, enrichment workers, CRM integrations with idempotent sync, PostgreSQL, Redis for expensive queries, object storage for exports, and learned ranking only after useful labeled outcomes exist. None is implemented.

## Submission materials

- [PROJECT_NOTES.md](PROJECT_NOTES.md): architecture, tradeoffs, reference-product analysis.
- Business-answer and resume drafts are provided separately in the local candidate package; they are excluded from the public repository.
- [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md): 90–120 second walkthrough.
- [INTERVIEW_PREP.md](INTERVIEW_PREP.md): 20 technical questions and answers.
- [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md): exact handoff steps and email draft.
- [PUBLISH_AND_RECORD.md](PUBLISH_AND_RECORD.md): step-by-step GitHub, Render and recording guide.

Do not upload the confidential handbook or personal employment answers to a public repository. This project is an independently prepared interview demo, not an official Caprae product.
