# Recovery without losing work

Each numbered directory contains **cumulative** patches against the pinned upstream
commits, not against the preceding checkpoint. Never apply successive patches to
an existing working tree. The runner clones upstream at the exact commits and
applies one checkpoint into a new destination. Existing destinations are rejected.

| Checkpoint | Implemented result | Relevant gate |
|---|---|---|
| 00-baseline | Compatibility fixes, locks, template auth | test + build |
| 01-data | Models, migration, seed | migrate + seed |
| 02-categories | Category API and tests | test spec/tracker/test_categories.py |
| 03-issues | Issue CRUD and tests | test spec/tracker/test_issues.py |
| 04-assignment | Safe assignees, assignment regression | test spec/tracker/test_assignment.py |
| 05-filters | Search, filters, stable pagination | test spec/tracker/test_filters.py |
| 06-frontend | Complete reference including frontend/browser tests | test + build + e2e |

Example from course root (choose a new destination if it already exists):

```bash
./workshop recover 06-frontend recovery/completed
./workshop --workspace recovery/completed setup
./workshop --workspace recovery/completed db up
./workshop --workspace recovery/completed db migrate
./workshop --workspace recovery/completed db seed
./workshop --workspace recovery/completed test
./workshop --workspace recovery/completed build
```

Recovered workspaces use the **student** ports; stop student servers/databases before
running a recovered workspace. Each workspace has a separate Compose project/volume,
but host ports still conflict. `--reference` has separate ports and can coexist.
Pass the same `--workspace recovery/completed` to start/test/build/e2e/db stop.
Run the runner from the course root; do not copy it alone into recovered apps.

For continued Claude work, keep Claude at the course root and explicitly supply
recovery paths and matching runner arguments in the plan. Do not silently use the
student profile's root paths. Copy the relevant outputs to a handoff before changing
workspaces. Compare your code with recovery code, explain differences, and decide
which implementation to continue; recovery is not a merge operation.
