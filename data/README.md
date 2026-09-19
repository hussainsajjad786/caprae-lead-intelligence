# Synthetic fixture

The reproducible dataset generator is `backend/app/seed/demo_data.py`: 34 source rows, 32 retained leads, 2 duplicate review records. No external dataset download is required.

Names are fictional, domains are reserved `example.com` subdomains, and telephone numbers are fictional `+1-202-555-0100` through `+1-202-555-0131`. Revenue and employee estimates are invented. Some rows intentionally contain invalid/missing data. No row is externally verified; “Format Valid” describes syntax alone.

Seed records remain in source control; generated SQLite files do not. Duplicate originals remain in the local database review table. Do not include the employer's confidential handbook in the repository.
