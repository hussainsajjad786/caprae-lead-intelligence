# Start here: Windows guide for Sajjad

## 1. Open the project

The project folder on this computer is:

```text
C:\Users\maask\Documents\Codex\2026-09-18\hi-2\outputs\caprae-lead-intelligence
```

Press Windows+E, paste that path into File Explorer's address bar, and press Enter. In VS Code, choose File > Open Folder and select this folder. You do not need to open the PDF or paste source code again.

## 2. Start the backend on this computer

Open PowerShell (or a VS Code terminal) and run these two commands:

```powershell
cd "C:\Users\maask\Documents\Codex\2026-09-18\hi-2\outputs\caprae-lead-intelligence\backend"
& "C:\Users\maask\Documents\Codex\2026-09-18\hi-2\work\.venv\Scripts\python.exe" -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The prepared environment already contains the Python dependencies. Wait for “Application startup complete”. Leave this terminal running. First startup creates and seeds the SQLite database.

Open http://127.0.0.1:8000/health — it should show `{"status":"ok"}`. API documentation is at http://127.0.0.1:8000/docs.

## 3. Start the frontend

Open a SECOND terminal. Leave the backend terminal running.

```powershell
cd "C:\Users\maask\Documents\Codex\2026-09-18\hi-2\outputs\caprae-lead-intelligence\frontend"
npm.cmd run dev
```

Dependencies were installed during preparation. If `node_modules` is missing, run `npm.cmd ci` first. Open the exact Local URL printed by Vite; normally http://127.0.0.1:5173.

If either server says its port is already in use, first try opening its URL: an earlier session may still be running. Do not start repeated copies. Stop the earlier server in its terminal with Ctrl+C if you need to restart it.

## 4. Check the app

1. Overview should show 32 leads, 16 high-priority leads, 26 format-valid records, and average score 71.2.
2. Search `Aster`, select industry `SaaS`, set minimum score `90`, and press Apply filters. One company should remain.
3. Click View. Read the six score contributions, which sum to 100.
4. Close the panel. Click Export CSV. The exported list should match the applied filters.
5. Clear filters. Open Data Quality, inspect the two prevented duplicates, and use Review flagged leads.
6. Open Analytics. These charts describe the whole dataset, not the filtered shortlist.

“Format Valid” is only syntax validation. All companies and contacts are synthetic, and no contact is externally verified.

## 5. Run tests and build

In a THIRD terminal:

```powershell
cd "C:\Users\maask\Documents\Codex\2026-09-18\hi-2\outputs\caprae-lead-intelligence\backend"
& "C:\Users\maask\Documents\Codex\2026-09-18\hi-2\work\.venv\Scripts\python.exe" -m pytest -q
```

The tested version passed 71 tests. Then build the frontend:

```powershell
cd "C:\Users\maask\Documents\Codex\2026-09-18\hi-2\outputs\caprae-lead-intelligence\frontend"
npm.cmd run build
```

The build creates `frontend/dist`. The development server is for local work; a production host serves the built assets.

## 6. If you move the project or use another computer

The `work/.venv` path above is specific to this prepared computer. Create a new environment inside the backend after installing Python 3.12:

```powershell
cd "YOUR-PROJECT-FOLDER\backend"
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Use Node.js 22.12+ or Node 24 for the frontend. In `frontend`, run `npm.cmd ci`, then `npm.cmd run dev`. Never upload or copy virtual environments and node_modules as source code.

## 7. Finish the application materials

- Read `PROJECT_NOTES.md` and `INTERVIEW_PREP.md` until you can explain the app yourself.
- Complete every placeholder in `BUSINESS_ANSWERS.md`, including US work status, salary/currency/payment period, weekly availability, schedule acceptance and start date.
- Replace `RESUME_DRAFT.md` with your accurate, updated resume and export a PDF from your preferred editor. The draft is not a verified employment history.
- Record a 90–120 second walkthrough using `VIDEO_SCRIPT.md`. Show the actual running app and explain the two features and architecture.
- Follow `SUBMISSION_CHECKLIST.md` for GitHub and the email draft.
- A public demo is optional. Follow `DEPLOYMENT.md` if you choose to deploy; localhost links work only on your computer.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Browser cannot connect to 5173 | Start the frontend and use the Local URL printed in its terminal. |
| Dashboard says request failed | Check backend `/health`; start the backend on port 8000 and click Retry. |
| `npm` is not recognized | Install Node.js, then reopen the terminal. |
| PowerShell blocks npm.ps1 | Use `npm.cmd`, as shown above. |
| Python module not found | Use the prepared `.venv` interpreter; otherwise install requirements into your own environment. |
| Port already in use | Open the existing service or stop its terminal with Ctrl+C before restarting. |
| No leads match | Click Clear filters. |
| Different statistics | Existing local data may differ; inspect it before resetting. Do not delete a database containing data you need. |

To stop the project, press Ctrl+C in both server terminals. Starting it later uses the same commands.
