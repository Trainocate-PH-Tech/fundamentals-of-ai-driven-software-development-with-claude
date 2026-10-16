# Build an Issue Tracker with Claude Code

A completion-first, multi-session workshop in professional AI-assisted engineering.
You will build and verify a FastAPI/PostgreSQL API and a React administration UI,
using Claude Code for exploration, planning, implementation, review, and debugging.
Allow multiple sessions; advance when a module's exit gate passes, not when time runs out.

Instructors: use the **[facilitator guide](GUIDE.md)** for preparation, delivery scripts,
copy-paste prompts, assessment, and troubleshooting.

Start with **[Module 1](01-project-setup/README.md)**. Follow the five READMEs in order.
Other pages are references and optional extension labs. Code fences labelled `bash`
run in your terminal from this course's root unless explicitly stated otherwise.
Fences labelled `text` are prompts to paste **inside Claude Code**, never into Bash.
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
[workflow kit](workflow-kit/README.md) provides reusable project configuration.
[Reference instructions](instructor-reference/README.md) run the completed solution;
[checkpoints](checkpoints/README.md) restore a known milestone into a **new** directory.
[Review findings](WORKSHOP_REVIEW.md) explain the changes and
[validation](VALIDATION.md) distinguishes executed checks from live Claude exercises.

Required environment: Bash on Linux or WSL2, Python 3.14, Node 24, Git, Docker with
Compose, a browser, and Claude Code with a supported account or API billing.
macOS can use Bash and Docker Desktop; the Linux reference run does not establish
macOS verification. Native Windows commands are outside this course's tested path.

The application is a local teaching MVP. Existing JWT authentication and User are
reused; only Category and Issue are added. Instructor source is separate from the
student `issuetrackerapi/` and `issuetrackerweb/` directories. Never paste API keys
into the application or browser environment. Claude authentication is independent
of the Issue Tracker's local admin login.
