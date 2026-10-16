# Validation record

Executed locally on 2026-10-15, Linux/Bash, Python 3.14.3, Node 24.13.0,
Docker Compose 2.35.1, PostgreSQL 17.6 and Claude Code 2.1.300.
Logs are local ignored artifacts under `workshop-output/`; rerun commands for fresh
evidence. No GitHub-hosted CI run is claimed.

| Check | Result |
|---|---|
| Reference install from Python/npm locks | Passed |
| Fresh PostgreSQL dev migration and seed | Passed; seed repeated without duplicate categories |
| Reference full backend suite | 105 passed, 22 skipped (upstream template/platform cases) |
| PostgreSQL migration preservation/rollback test | Passed; temporary DB, existing user retained, FK actions checked |
| Frontend production build | Passed; upstream Sass deprecation/bundle-size warnings remain |
| Real Chromium lifecycle | 2 passed; real login/API/PostgreSQL, category/issue CRUD, assignment, edits/reload, combined filters, deletion conflict/confirmation, empty/reset/network error |
| Fresh 06-frontend recovery | Setup, migration, seed, 105 backend tests, build, 2 browser tests passed |
| Fresh 00-baseline recovery | 82 passed, 22 skipped; frontend build passed |
| All cumulative checkpoints | 14 patches independently apply cleanly against pinned upstream commits |
| Installer/recovery tests | 3 passed: preserve conflicting guidance, repeatability, existing-destination refusal and invalid commands |
| Python syntax hook isolated fixtures | 9 passed |
| Claude skill smoke probe | Authenticated read-only `/workshop-plan` returned source-backed category-deletion plan and correct reference test command |

The first Claude probe hit its 8-turn limit; a narrower probe with a 20-turn limit
completed. It did not edit, execute tests or delegate. This validates one skill
invocation, not every workshop prompt or model response. The resulting plan correctly
identified missing response-body coverage in one category test; the browser test
independently checks visible conflict feedback. Inspect reports rather than treating
successful invocation as proof the agent's conclusions are complete.

Live VS Code interaction, custom reviewer delegation, permissions fixture activation,
plugin invocation, and PostToolUse hook activation were not exercised here. Their
student exercises explicitly require discovery and observed feedback. The hook's
standalone fixture tests are not evidence of live Claude activation. macOS/native
Windows and remote CI execution were not tested.

Backend tests include expected Alembic configuration deprecation warnings. npm emits
upstream install-script policy warnings; the installed esbuild executable and browser
were exercised successfully. Locks reproduce this local teaching baseline; they do
not establish production security approval. See the dependency audit note below.

Dependency audit: the initial template lock reported four advisories (one critical,
two high, one moderate). Compatible `npm audit fix` updates were applied to the
baseline and completed-reference locks, propagated to every checkpoint, and the
final audit reports **zero advisories**. The updated reference build and both
browser tests passed; the updated baseline build passed. The full fresh-recovery
run above preceded these lock-only fixes and source formatting; all final cumulative
patches were checked again afterward. Future audits can change as advisories evolve.

Documentation checks: `python3 tools/check_docs.py` checks course-relative links
and parses Bash fences with `bash -n`; this is syntax validation, not execution of
every student command. The required setup/recovery/test/build/browser commands were
executed as described above. Optional installation, platform-specific and account
setup instructions remain participant-run.

## Use-case workflow revision — 2026-10-16

This revision changes course instructions, kit definitions and installer scaffolding,
not application behavior. Earlier application results above remain historical;
backend/build/browser suites were not rerun for these documentation/workflow changes.

- Documentation checker: 36 documents, local links resolved, 59 Bash fences parsed.
  Guide/use-case table-of-contents anchors were checked separately.
- Four tooling tests passed, including expanded role/skill installation, preservation
  of a conflicting student implementation skill, repeatability and recovery refusal.
- Eighteen installed/template Claude frontmatter definitions parsed successfully.
  Shared kit definitions matched checked-in copies (course-specific AGENTS guidance
  is intentionally different). JSON configuration parsed successfully.
- All nine implementation increments have explicit plan/implement/verify invocations
  and matching milestone plan paths. Frontend evidence IDs are teaching increments,
  not additional recovery checkpoints.
- Live `/workshop-implement` missing-input probe: exited successfully after requesting
  milestone ID and accepted plan; noted missing student apps and Plan Mode; no edits.
- Live `/workshop-plan planning-probe ...`: returned source-backed current coverage,
  proposed test-only scope, milestone artifact paths and the correct reference test
  command. It separated read evidence from unexecuted runtime checks. No edits,
  application commands or delegation were authorized in this probe.
- Live delegated probes: actual Agent calls named `workshop-investigator` and
  `backend-reviewer` completed. The first examined runner/PATH hypotheses; the second
  inspected reference category deletion and its tests. The recorded tool stream
  contained Agent, Read and Grep calls, with no Bash/Write/Edit. Reports identified
  scope limits and checks not run. Findings are review proposals, not newly executed
  application verification or automatic authorization to modify the reference.

Local ignored logs: workshop-output/implementation-input-probe.txt,
workshop-output/milestone-planning-probe.txt and workshop-output/role-probes.jsonl.
The probes establish discovery and bounded behavior for these inputs, not universal
model compliance. Full live implementation/verification skill execution, the deliberately
failed-delegation student exercise, VS Code, permissions fixture activation, plugins
and live hooks were not rerun. The older “not exercised” statements above describe
the initial validation; only the specific delegated probes listed here were added.
