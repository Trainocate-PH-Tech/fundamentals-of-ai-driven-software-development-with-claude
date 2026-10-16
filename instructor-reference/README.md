# Tested instructor solution

Source is kept separately from student work. Run from the **course root**:

```bash
./workshop --reference doctor
./workshop --reference setup
./workshop --reference db up
./workshop --reference db migrate
./workshop --reference db seed
./workshop --reference test
./workshop --reference build
```

Then run in separate terminals:

```bash
./workshop --reference start api
```

```bash
./workshop --reference start web
```

Open `http://localhost:8001/#/login`; local demo account:
`admin@example.com` / `password`. The seed creates/updates this account for local
teaching use. API documentation is `http://localhost:3001/docs`. The reference
uses development PostgreSQL on 54331 and test PostgreSQL on 54332; student ports
are different. Stop foreground servers with Ctrl+C; stop DBs with
`./workshop --reference db stop`. Dev volume persists; test storage is disposable.

```bash
(cd instructor-reference/issuetrackerweb && npx playwright install chromium)
./workshop --reference e2e
```

Pinned upstreams (the workshop patches extend these, never latest):

- API: `cloudband-solutions/default_api_fast`, `6afada28350e93d5a2cdff7dddcbe88c2036e299`.
- Web: `cloudband-solutions/admin-panel-web`, `47578e05f4cca5c035ea51c0b5e92b55d0818928`.

Python dependencies are frozen in `issuetrackerapi/requirements.lock.txt`.
Node dependencies use `issuetrackerweb/package-lock.json`; use `npm ci`.
Reference tested on Python 3.14.3, Node 24.13.0 and PostgreSQL 17.6 on Linux.
The original template READMEs remain upstream references; course runner commands
are authoritative for this PostgreSQL workshop. Existing SQLite configuration
remains for upstream tests and compatibility, not the main course database.

Baseline fixes: focused pytest selection, PostgreSQL fixture safety, SQLAlchemy URL
assertion compatibility, undeclared frontend component assignments, accessible login
labels, configurable web port and compatible dependency audit fixes. Final UI also supplies real sidebar link targets.
The reference adds two models, migrations, category/issue API, safe assignees,
search/filters, React integration and browser tests. Existing User/auth remain.
See [validation](../VALIDATION.md) for actual outcomes and limits.

The reference directories are ordinary source files so a parent course repository
can track them without accidental nested Git links. Local template Git metadata
used during authoring is kept under ignored `.workshop/upstream-git/`; it is not
needed to run the reference. Students' generated applications remain independent
Git repositories. Checkpoint verification can clone the pinned upstreams if the
local authoring cache is absent.
