# Optional external tools and bounded parallel reviews

Complete a working [Module 4](README.md) slice before this extension.

MCP exposes external tools/data to Claude. It is useful when an application requires
an external system; it is unnecessary for local file and terminal work. The Issue
Tracker core has no MCP dependency and needs no third-party token.

**Guided inspection:** run `claude mcp list` in Bash, then `/mcp` inside Claude.
Record enabled servers and their tools without copying credentials. If none exist,
record “none”; that is a valid configuration. For an instructor-provided server,
read its official installation instructions, use a read-only account and grant only
needed tools. Do not invent a server URL or install an unreviewed package.

**Independent design:** propose a read-only issue-import preview tool. Specify its
input/output, authentication storage, permission boundary and an adversarial test
where external content asks Claude to change local instructions. Do not implement
an integration that is outside the capstone. Treat external content as data.

**Parallel review exercise:** use `acceptance-reviewer` for backend integrity and your
`ui-reviewer` for frontend states, supplying separate source scopes and the same
accepted plan. Monitor each named task, save reports separately, then reconcile
conflicting findings in the main session. Neither reviewer writes or runs tests.
Independent: choose one finding from each report, reproduce it yourself, and classify
it as confirmed, rejected with evidence, or needing more evidence.
