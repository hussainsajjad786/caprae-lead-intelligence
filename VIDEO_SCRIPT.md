# 90–120 second walkthrough

Record this yourself after you can explain the code. Speak naturally at about 135–150 words/minute. The narration below is roughly 250 words; rehearse and trim pauses to keep the final recording below two minutes. Do not imply you personally wrote everything unaided or that coding took exactly five hours.

| Time | On screen | Narration |
|---|---|---|
| 0–15s | Overview | Hi, I'm Sajjad Hussain. This is Caprae Lead Intelligence, an interview MVP focused on two things: prioritizing relevant companies and making lead quality easier to assess. Every record here is synthetic. |
| 15–35s | Stats and top-leads button | A large lead list is only useful if a researcher knows where to start. I focused on a complete qualification workflow, so users can find a shortlist, understand its ranking, and see data problems before exporting. These are intended benefits, not measured sales results. |
| 35–60s | Click Explore top leads, filter SaaS, open Aster | The dashboard summarizes the dataset. I can narrow the list by industry, market, priority, and minimum score. Filters apply together, and results stay ordered by fit. This example company ranks highly; opening it explains why. |
| 60–85s | Score breakdown, then Data Quality | The score has six rule-based components, totaling one hundred points. It is not machine learning. The quality layer checks email and website formats and flags missing fields. Format valid does not mean externally verified. Duplicate inputs are retained for review instead of silently disappearing. |
| 85–105s | View a retained duplicate, return to leads, export | Here I can inspect the retained company. The export uses the applied filters across every page, giving the next workflow the same shortlist the user selected. CSV cells are protected against spreadsheet formulas. |
| 105–120s | Architecture diagram in README | React calls a FastAPI API, with separate scoring and quality services over SQLAlchemy and SQLite. Scores are stored at ingestion. I kept the MVP small; production would add permitted data connectors, PostgreSQL, and background jobs. |

## Recording checklist

- Start both servers; close unrelated tabs and notifications.
- Use readable browser zoom and demonstrate with real clicks.
- Explain why the choices matter, not every line of code.
- Keep “Demo / Synthetic Data” visible; do not call contacts verified.
- Briefly disclose AI assistance if required by recruiting; be ready to explain exactly what was generated, reviewed and tested.
- Upload the recording to your chosen service, test its viewing permissions, and include the link in your submission. No video has been recorded or uploaded by this project.
