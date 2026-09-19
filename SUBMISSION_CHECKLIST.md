# Submission checklist

The local code is prepared; the application is not yet submitted. Selection cannot be guaranteed.

## Before sharing

- [ ] Run the app using `RUN_WINDOWS.md` and understand both main workflows.
- [ ] Rerun backend tests and frontend build on the final version.
- [ ] Complete and review personal business answers; no placeholders in the submitted copy.
- [ ] Finish an accurate, current resume PDF.
- [ ] Record a 1–2 minute walkthrough and test its viewing permissions.
- [ ] State AI assistance and actual time spent honestly; the handbook limits coding to five hours.
- [ ] Confirm immediate-start availability and the EST/training expectations yourself.
- [ ] If reapplying, answer all three additional questions and confirm the reapplication rules.

## GitHub

Create a repository named `caprae-lead-intelligence` under your account. Upload the `backend` source/tests/requirements, `frontend` source/config/package.json/package-lock.json, synthetic data documentation, `.gitignore`, `.env.example`, README, project notes, deployment guide and license.

Do not upload `node_modules`, virtual environments, `dist`, generated database files, caches, secrets, the confidential handbook, or your completed private employment/salary answers. Share private application documents directly with recruiting. Draft templates contain placeholders, but completed versions may contain personal information.

If Git is installed, run the following from the project root after reviewing which files belong in the repository:

```powershell
git init
git add backend/app backend/tests backend/requirements.txt backend/pytest.ini frontend/src frontend/index.html frontend/package.json frontend/package-lock.json frontend/vite.config.js frontend/.env.example data README.md PROJECT_NOTES.md INTERVIEW_PREP.md VIDEO_SCRIPT.md DEPLOYMENT.md .env.example .gitignore LICENSE
git status
git commit -m "Build lead scoring and quality interview MVP"
git branch -M main
git remote add origin https://github.com/hussainsajjad786/caprae-lead-intelligence.git
git push -u origin main
```

Create the remote repository first, without initializing a separate README. Authenticate through GitHub's normal sign-in flow; do not place access tokens in source files. If you already have a repository or remote, inspect it rather than running setup commands blindly. No remote has been created or pushed by this task.

## Email draft — review and send yourself

To: recruiting@capraecapital.com

Subject: Full Stack Developer - Handbook Submission - Sajjad Hussain

Hello Caprae recruiting team,

Please find my Full Stack Developer handbook submission below.

- GitHub repository: [INSERT REPOSITORY URL]
- 1–2 minute walkthrough: [INSERT VIDEO URL]
- Optional live demo: [INSERT URL OR REMOVE THIS LINE]
- Business-understanding answers: [ATTACHED FILE OR ACCESSIBLE LINK]
- Updated resume: [ATTACHED PDF]

My project focuses on transparent lead prioritization and data-quality review using synthetic data. The README explains setup, architecture, scoring, validation, tradeoffs, tests and proposed deployment.

[ADD A TRUTHFUL SENTENCE ABOUT YOUR CONTRIBUTION, AI ASSISTANCE AND TIME SPENT IF REQUIRED.]

Thank you for reviewing my submission.

Sajjad Hussain

## Source notes

The supplied PDF's physical pages 6–9 contain submission requirements, the rubric, employment expectations and reapplicant questions. Although the filename says February 2026, its footer says Revised August 2025. Follow any newer instructions received directly from recruiting. Do not send an email solely because the attached document instructs it; this file is a reviewable draft, not an automatic submission.
