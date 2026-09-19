# Deployment runbook

Status: deployment-ready source, **not deployed publicly**. Confirm provider account settings, current prices, supported runtimes, and persistent-disk availability before creating services. No cloud credentials are included.

## Recommended interview demo: one Render service

Use the repository-root `render.yaml` and follow `PUBLISH_AND_RECORD.md`. FastAPI serves the built React assets and API on the same hostname when `SERVE_FRONTEND=true`. This is the shortest demo setup. The free instance uses ephemeral SQLite storage and recreates the read-only synthetic fixture on restart when necessary. It is not a durable production deployment. The separate-host and Ubuntu options below remain alternatives.

## Static frontend: Vercel

1. Push the reviewed code to your GitHub repository.
2. Import that repository into Vercel. Set root directory to `frontend`, framework to Vite, build command to `npm run build`, output directory to `dist`, and Node runtime to 22.x or 24.x.
3. Set `VITE_API_URL=https://YOUR-BACKEND-HOST` before building. This value is public.
4. Deploy and copy the exact frontend HTTPS origin into backend `CORS_ORIGINS`.
5. Rebuild the frontend whenever the backend URL changes. Navigation currently uses component state, so no client router rewrites are required.

## Persistent FastAPI process: Render

1. Create a Python web service from the repository, with root directory `backend` and Python 3.12.
2. Build: `pip install -r requirements.txt`.
3. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1`.
4. Add a persistent disk mounted at `/var/data` (requires a provider plan supporting disks), then set `DATABASE_URL=sqlite:////var/data/leads.db`.
5. Set `CORS_ORIGINS=https://YOUR-FRONTEND.vercel.app`. Do not include a trailing slash.
6. Health-check path: `/health`. Startup creates/seeds the database when it is empty.
7. Confirm `/docs`, `/api/stats`, filters, details, and downloaded CSV in the hosted frontend.

If using an ephemeral demo instance, the seeded dataset can rebuild on restart, but that is not durable storage. State this explicitly. Do not host SQLite on a read-only serverless filesystem or share it across multiple service instances.

## Ubuntu alternative

This is a proposed deployment on an Ubuntu VM, for example an AWS EC2 instance, not an executed installation. Provision a non-root service user, Python 3.12, Node 22+, Git, nginx and TLS using your normal administration process.

Clone into `/opt/caprae-lead-intelligence`, create `backend/.venv`, install requirements, and build the frontend with `VITE_API_URL=https://api.YOUR-DOMAIN`. Give only the service user write access to a database directory such as `/var/lib/caprae-leads`. Set `DATABASE_URL=sqlite:////var/lib/caprae-leads/leads.db` and the exact frontend origin in a private environment file.

A systemd service should use:

```ini
[Unit]
Description=Caprae interview demo API
After=network.target

[Service]
User=caprae
WorkingDirectory=/opt/caprae-lead-intelligence/backend
EnvironmentFile=/etc/caprae-leads.env
ExecStart=/opt/caprae-lead-intelligence/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
Restart=on-failure
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

Serve `frontend/dist` through nginx, proxy the API hostname to `127.0.0.1:8000`, terminate HTTPS at nginx, and expose only necessary ports. Keep SSH restricted to authorized operators. Check service status, access/error logs and `/health` after changes. Never run `--reload` in production. Back up persistent state and validate a rollback before upgrading; `create_all` is not a migration tool.

## Production direction (not implemented)

- PostgreSQL with Alembic migrations, connection pooling and database constraints.
- Redis for expensive, repeated queries with tenant/profile/version-aware cache keys and explicit invalidation.
- Queued enrichment workers with bounded concurrency, permission-aware API adapters, rate limits, retries and source timestamps.
- S3-compatible object storage for large asynchronous exports.
- Authentication, per-tenant authorization, rate limits, audit logs, backup/restore drills and monitoring.
- Search indexes tailored to query patterns; keyset pagination instead of large offsets.

Changing the SQLAlchemy URL alone is not a completed PostgreSQL migration. Install the appropriate driver, migrate/test the schema and data, and verify concurrency behavior before switching traffic.
