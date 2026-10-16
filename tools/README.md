# Maintenance utilities

The teaching path uses ordinary Claude requests and direct Git, Python, npm and
Playwright commands. These utilities are retained for maintainers and regression
checks, not as student prerequisites. The legacy launcher still targets PostgreSQL;
its successful execution does not establish the current SQLite teaching gates.

legacy-skills/ preserves historical procedure definitions outside Claude discovery.
Do not install them into active .claude/skills or reusable teaching templates.
check_docs.py validates teaching links/shell syntax and rejects retired orchestration
invocations outside explicitly historical records. CI separates these maintenance
checks from direct application acceptance.
