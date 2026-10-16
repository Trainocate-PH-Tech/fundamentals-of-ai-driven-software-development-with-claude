# Completed instructor solution — direct SQLite rehearsal

Open this directory as the active root; its two app folders already contain the
completed solution. Follow [the instructor rehearsal](../GUIDE.md#rehearse-the-completed-reference-before-class)
and M4–M7 in the guide. Do not clone over these folders or apply baseline patches.

Install Python/npm locks directly. Create storage and configure a local SQLite
`.env` yourself, preserving existing settings. Run Alembic, existing admin seed,
then tracker seed twice. Direct pytest uses APP_ENV=test and
DATABASE_URL=sqlite:///test.sqlite3 from the API directory. Development uses
sqlite:///storage/development.sqlite3. There is no database service to start.

Use API port 3001 and frontend port 8001; configure API_BASE_URL and WEB_PORT
accordingly. Run Uvicorn and npm start in separate terminals. The local demo login
is admin@example.com / password; seeding resets this account for teaching only.
Install Chromium, run the existing Playwright suite with E2E_BASE_URL on 8001 and
E2E_API_URL on 3001, and perform the specification's browser demo.

Windows uses `.venv/Scripts/python.exe` and npm.cmd; Linux/WSL uses
`.venv/bin/python` and npm. Exact alternatives and environment isolation are in
[the guide](../GUIDE.md). Stop foreground processes with Ctrl+C. Preserve the SQLite
file to retain development data; do not use destructive tests against that file.

Pinned upstreams remain:

- API: cloudband-solutions/default_api_fast, 6afada28350e93d5a2cdff7dddcbe88c2036e299.
- Web: cloudband-solutions/admin-panel-web, 47578e05f4cca5c035ea51c0b5e92b55d0818928.

The reference is ordinary source, not nested Git submodules. Original template
READMEs remain upstream references; the current teaching commands are in the guide.
The source also retains PostgreSQL compatibility and its conditional migration
test. Record skips explicitly; use the guide's SQLite migration-preservation
exercise for this delivery. See [validation](../VALIDATION.md) for actual outcomes.
