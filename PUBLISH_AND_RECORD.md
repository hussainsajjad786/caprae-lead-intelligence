# GitHub, live demo, and two-minute video

Complete these in order. The application code is local; a proposed GitHub address is not proof that a repository or deployment exists.

## Step 1 — Create the GitHub repository

1. Sign in to your own account at https://github.com.
2. Open https://github.com/new.
3. Owner: `hussainsajjad786`. Repository name: `caprae-lead-intelligence`.
4. Description: `Transparent lead scoring and data-quality interview MVP built with React, FastAPI and SQLite. Synthetic data only.`
5. Choose Public if you want recruiters to access it without an invitation; choose Private if your recruitment instructions require it and arrange access.
6. Leave “Add a README”, .gitignore and license initialization OFF because the project already contains these files.
7. Click Create repository.

Your repository address, once you have created it, is:

```text
https://github.com/hussainsajjad786/caprae-lead-intelligence
```

## Step 2 — Upload the prepared code

If the local repository has already been initialized and committed during preparation, open PowerShell and run:

```powershell
cd "C:\Users\maask\Documents\Codex\2026-09-18\hi-2\outputs\caprae-lead-intelligence"
git status
git remote -v
```

If no `origin` is listed:

```powershell
git remote add origin https://github.com/hussainsajjad786/caprae-lead-intelligence.git
```

Then:

```powershell
git push -u origin main
```

Complete GitHub sign-in if prompted. Never paste passwords or tokens into source code or chat. If `git` is not found in a new terminal, install Git for Windows or use the Git executable available on this computer:

```powershell
& "C:\Users\maask\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe" --version
```

You can substitute that executable prefix for `git` in the commands above. If a new remote contains commits, do not force-push; inspect the difference first.

### Manual alternative without Git commands

Extract the prepared `caprae-lead-intelligence-github.zip` into a temporary folder. In the empty repository, choose uploading an existing file, and upload the extracted contents, including dotfiles/configuration. Do not upload only the ZIP: recruiters and Render need the actual source files. Make sure `render.yaml`, `backend`, `frontend`, README, and package-lock.json are visible at the repository root after committing.

Check the GitHub Actions tab for build/test results once the repository is pushed. Local tests are not the same as a completed GitHub Actions run.

## Step 3 — Deploy one live demo on Render

This repository now includes `render.yaml`. It defines one Python web service that builds React and serves the dashboard and API together. No separate Vercel site or cross-origin API URL is required for this path.

1. Open https://dashboard.render.com and sign in or create your account yourself.
2. Choose New > Blueprint.
3. Connect GitHub and authorize access to this repository. Review the account permission screen yourself.
4. Select `hussainsajjad786/caprae-lead-intelligence`, branch `main`.
5. Use the root `render.yaml`. Review the proposed service and confirm it uses the **Free** instance plan. Do not select a paid plan unless you intend to pay.
6. Create/deploy the Blueprint. Wait for the deployment status to become Live.
7. Copy the actual `https://...onrender.com` URL shown by Render. The final hostname may vary; do not invent it.
8. Open that URL in a private/incognito window. Check the dashboard, filters, detail panel and CSV export.
9. Check `YOUR-LIVE-URL/health` and `YOUR-LIVE-URL/docs`.

### If you use New > Web Service instead

Select the same repository and use:

| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Branch | main |
| Root directory | Leave blank |
| Build command | `npm --prefix frontend ci && npm --prefix frontend run build && pip install -r backend/requirements.txt` |
| Start command | `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT --workers 1` |
| Instance | Free |
| Health check | `/health` |

Environment variables: `PYTHON_VERSION=3.12.10`, `NODE_VERSION=22.16.0`, `SERVE_FRONTEND=true`, `DATABASE_URL=sqlite:///./leads.db`. Leave `VITE_API_URL` empty/unset. Do not put private credentials in any VITE variable.

Free services can sleep after inactivity and take time to wake. Their local filesystem is ephemeral: the SQLite demo database is recreated and reseeded after it is lost. That is acceptable for this read-only synthetic demonstration, not durable production storage. Do not upload real data. Review Render's current usage limits and billing settings.

Official references checked 19 September 2026: https://render.com/docs/deploy-fastapi, https://render.com/docs/blueprint-spec, https://render.com/docs/free.

## Step 4 — Record your own 90–120 second video

On Windows 11, open Snipping Tool, switch to screen recording, select the browser area, enable your microphone if the recorder provides that control, and start. Microsoft's current shortcut is Windows+Shift+R. Make a short test first and play it back to confirm your voice is audible. If your installed recorder lacks microphone recording, use a recorder you already have that records both screen and microphone.

Keep private tabs, notifications, credentials and account settings out of the recording. A webcam is optional. Use your own narration; do not present AI-generated work as unaided personal work.

| Time | What to do | What to say |
|---|---|---|
| 0:00–0:15 | Show overview | “Hi, I'm Sajjad Hussain. This is Caprae Lead Intelligence. It focuses on lead prioritization and data quality. All of the data is synthetic.” |
| 0:15–0:35 | Point to the four stats | “A long prospect list is not enough. A researcher needs to know which companies fit and which records need attention. This workflow helps create an understandable shortlist.” |
| 0:35–0:55 | Search Aster, select SaaS, minimum score 90, Apply | “I can combine company, industry and score filters. The backend applies the same rules to the table and export, so the shortlist stays consistent.” |
| 0:55–1:20 | Open Aster details | “The score has six visible components, totaling one hundred points. This is a rule-based model, not machine learning. Format valid checks syntax only; it does not mean an email or company has been externally verified.” |
| 1:20–1:40 | Close details, show Data Quality | “Duplicate inputs are retained for review while the main list stays unique. Missing or malformed fields are flagged before export.” |
| 1:40–2:00 | Return to leads, export, briefly show README | “React calls FastAPI, with scoring and quality services over SQLAlchemy and SQLite. The live demo serves both on one host. I kept the scope to two workflows; production would need permitted data sources, PostgreSQL and background jobs.” |

Only say “live demo” if you actually deployed it. Otherwise say “local demo”. Rehearse once, shorten pauses, then save as `Sajjad-Hussain-Caprae-Demo.mp4`. Read VIDEO_SCRIPT.md for a fuller version. A script is not a finished video.

Microsoft reference: https://support.microsoft.com/en-us/windows/apps/use-snipping-tool-to-capture-screenshots.

## Step 5 — Share the video

Upload the MP4 to your chosen service, such as Google Drive, and configure it so the recruiter can view it. If using Drive, choose Share > General access > Anyone with the link > Viewer where your account permits this. Copy the link and test it in an incognito window. Do not make unrelated files public.

You need three distinct links: GitHub source, recorded video, and optional live demo. `localhost` and `127.0.0.1` are not public demo links.

## Step 6 — Complete and send the application

Finalize BUSINESS_ANSWERS.md with truthful details and replace the resume draft with your real updated resume. Use SUBMISSION_CHECKLIST.md's email draft. The handbook's recipient is `recruiting@capraecapital.com` and subject is `Full Stack Developer - Handbook Submission - Sajjad Hussain`. Review newer recruiting instructions if any. Send only after checking every link and attachment.
