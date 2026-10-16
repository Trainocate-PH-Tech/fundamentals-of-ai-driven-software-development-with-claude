# Workshop review and revisions

The original material had useful concepts and examples, but several overlapping
lesson paths. Students had to infer working directories, package scripts and API
contracts. Some prompts described features without runnable verification. The
one-day framing did not match the requested full engineering workflow.

| Gap | Revision |
|---|---|
| Competing outlines and feature labs | Five ordered README walkthroughs; older pages point to the canonical route |
| Mutable template assumptions | Exact upstream commits, Python lock, npm lock and documented baseline repairs |
| PostgreSQL described but SQLite default | Explicit dev/test PostgreSQL containers and runner environment |
| No reliable end state | Separate working instructor reference and cumulative recovery checkpoints |
| Prompt success confused with application success | Real backend, build and Playwright gates; evidence tables |
| AGENTS loading assumptions | CLAUDE.md explicitly imports shared guidance and project profile |
| Skills described without lifecycle | File creation, restart/discovery, invocation, pre/post verification and independent task |
| Vague delegation | Read-only reviewer, explicit input/output contract, task monitoring and main-session ownership |
| Unsafe or ambiguous terminal steps | Root-resolving argv runner, no shell eval, separate test DB and refusal to overwrite recovery |
| Repeated configuration overwrites | Installer stages conflicts and preserves existing instructions |
| No professional transfer exercise | Generic kit plus project profile, handoffs, CI and adaptation capstone |

Required material is in module READMEs. Optional hooks, plugins, MCP and output
style experiments deepen the course after a working slice; they are not prerequisites
for the app. The original source PDF is preserved. No new production infrastructure
or unrelated product features were added to the capstone.

Usability assumptions: Bash/Linux/WSL2 primary; completion-first pacing; students
can inspect Git diffs and run commands. Each module names its entry requirement,
concrete result, guided task, independent task and exit gate. Instructors should
use checkpoint recovery when debugging would otherwise consume a whole session,
then have students explain the recovered change and rerun its gate.

## Windows portability revision

The former Unix-only launcher and Bash-only walkthroughs prevented native Windows
participation. The launcher now selects platform-specific Python/npm paths and
process cleanup; platform-specific requirements are reflected in every cumulative
checkpoint. PowerShell alternatives appear beside terminal exercises across all
five modules and the facilitator guide, including literal skill/agent file creation,
recovery and evidence capture. `WINDOWS_SETUP.md` distinguishes native Windows from
WSL2 and includes a full rehearsal checklist. Windows CI covers tooling/install/build
and shell syntax; Docker Desktop and full native browser acceptance require the
separate rehearsal. See `VALIDATION.md` for actual results and remaining limits.
