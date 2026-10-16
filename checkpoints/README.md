# Manual recovery without losing work

Each checkpoint is a cumulative source patch against the pinned upstream commit,
not the preceding checkpoint. Apply exactly one patch to each newly cloned app.
Never stack patches or reset/delete a student's existing work.

| Checkpoint | Implemented result | Relevant gate |
|---|---|---|
| 00-baseline | Compatibility fixes, locks, template auth | test + build |
| 01-data | Models, migration, seed | migrate + seed |
| 02-categories | Category API and tests | test spec/tracker/test_categories.py |
| 03-issues | Issue CRUD and tests | test spec/tracker/test_issues.py |
| 04-assignment | Safe assignees, assignment regression | test spec/tracker/test_assignment.py |
| 05-filters | Search, filters, stable pagination | test spec/tracker/test_filters.py |
| 06-frontend | Complete reference including frontend/browser tests | test + build + e2e |

Stop the student's API and frontend with Ctrl+C. Follow the guide's
[manual cloning steps](../GUIDE.md#m2-clone-the-pinned-templates-explicitly) using a
new sibling destination such as issue-tracker-recovery. In the explicit Git patch
commands substitute the desired checkpoint directory for 00-baseline. All other
clone/pin commands stay the same. Run git apply --check before applying each patch.

Create root instructions, the SQLite profile and local environments as in M3–M7.
Select the recovered root as your working directory; there are no workspace flags.
Keep its SQLite files separate from the student's files. Use direct migrations,
pytest and npm commands; baseline has only the admin seed, while 01-data and later
also provide app.seed_tracker. Browser tests become available at 06-frontend.

Recovered servers use student ports 3000/8000, so stop the old servers before starting
the new ones. Start Claude at the recovered root and give it exact application paths,
accepted plan and handoff. Compare sources before deciding which work to continue;
recovery is not a merge and does not prove acceptance gates passed.
