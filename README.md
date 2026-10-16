# Build an Issue Tracker with Claude Code

A completion-first, multi-session workshop in professional AI-assisted engineering.
You will build and verify a FastAPI/SQLite API and a React administration UI,
using Claude Code for exploration, planning, implementation, review, and debugging.
Allow multiple sessions; advance when a module's exit gate passes, not when time runs out.

Instructors: use the **[facilitator guide](GUIDE.md)** for preparation, delivery scripts,
copy-paste prompts, assessment, and troubleshooting.

Start with **[Module 1](01-project-setup/README.md)**. Follow the five READMEs in order.
Other pages are references and optional extension labs. Code fences labelled `bash`
run in your terminal from the active project root unless explicitly stated otherwise.
The downloaded course is reference material; Module 1 creates a separate workspace.
Fences labelled `powershell` run in PowerShell 7.4+. Choose the block for your shell.
Fences labelled `text` are prompts to paste **inside Claude Code**, never into a shell.
Use ordinary Claude requests and direct Git/Python/npm/Playwright commands.
No course launcher, installer or orchestration skill is required.
Generated code must pass the same gates as the instructor solution.

| Module | Working result | Main engineering techniques |
|---|---|---|
| [1. Setup](01-project-setup/README.md) | Pinned applications, database, instructions | Context, memory imports, permissions, instruction probes |
| [2. Fundamentals](02-application-fundamentals/README.md) | Verified repository and request-flow map | Read-only exploration, scoped rules, evidence-based subagents |
| [3. Workflow](03-ai-development-workflow/README.md) | Accepted plan, reusable skills, reviewer | Plan Mode, skills, task boundaries, monitoring, handoffs |
| [4. Implementation](04-issue-tracker-implementation/README.md) | Full issue/category/assignment/filter UI | Small slices, tests, review, checkpoint recovery |
| [5. Verification](05-testing-debugging-and-demo/README.md) | Tested browser lifecycle and handoff | Regression debugging, hooks, CI, acceptance evidence |

Use [Claude use-case recipes](CLAUDE_USE_CASES.md) to choose a workflow, provide task inputs,
and evaluate the output.

The [specification](SOFTWARE_SPECIFICATIONS.md) defines behavior. The
[instruction examples](workflow-kit/README.md) provide optional files for manual adoption.
[Reference instructions](instructor-reference/README.md) run the completed solution;
[checkpoints](checkpoints/README.md) restore a known milestone into a **new** directory.
[Review findings](WORKSHOP_REVIEW.md) explain the changes and
[validation](VALIDATION.md) distinguishes executed checks from live Claude exercises.

Required environment: Bash on Linux/WSL2 or native Windows PowerShell 7.4+,
Python 3.14, Node 24, Git, a browser,
and Claude Code with a supported account or API billing.
Start with [Windows setup](WINDOWS_SETUP.md) for native Windows or WSL2.
Windows automation and instructions are included; see [validation](VALIDATION.md)
for checks actually performed. macOS verification also requires its own rehearsal.

The application is a local teaching MVP. Existing JWT authentication and User are
reused; only Category and Issue are added. Instructor source is separate from the
student `issuetrackerapi/` and `issuetrackerweb/` directories. Never paste API keys
into the application or browser environment. Claude authentication is independent
of the Issue Tracker's local admin login.
