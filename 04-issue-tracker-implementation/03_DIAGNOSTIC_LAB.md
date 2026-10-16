# Assignment and UI integration diagnosis

Complete the relevant [module prerequisites](README.md). Use student apps only.
This lab teaches symptom → reproduction → hypotheses → discriminating check →
minimal repair → regression. Evidence belongs to milestone `assignment-diagnosis`.

## Guided scenario

After the assignment slice passes, create a clean Git branch for a reversible
exercise. In your student implementation only, temporarily replace the issue PATCH
schema dump's exclude_unset=True with the default behavior. If your implementation
uses another pattern, identify its equivalent with the instructor before editing.
Never alter the instructor solution. Run the assignment regression and retain output.

**Inside Claude:**

```text
Read the failing assignment output and the active backend schema, handler and
operation. Use bug-investigator to inspect the hypothesis that omitted fields
became null. Give it exact paths and the log, with no edits or commands. Main session:
reproduce using direct pytest for spec/tracker/test_assignment.py from issuetrackerapi with APP_ENV=test and DATABASE_URL=sqlite:///test.sqlite3, compare hypotheses,
propose a minimal repair and wait for acceptance. After acceptance, repair without
weakening tests, run assignment and issue regressions and save milestone evidence.
```

## Expected evidence and verification

Expected: the focused check fails for the intended semantic regression, not a
connection error. Restore correct behavior and prove the regression passes. If the
initial modification causes a different error, explain that result rather than
pretending it reproduced the target symptom. Remove all intentional defects before
continuing. For UI diagnosis, use the browser's offline mode to trigger a request
failure, then restore connectivity; compare error versus empty-result states.

Save inputs, observed facts, unsupported hypotheses, command/exit-code evidence
and remaining gaps under `workshop-output/milestones/assignment-diagnosis/`. Read-only agents
return findings; the main session saves files, runs commands and owns repairs.

## Independent task

Inspect a browser failure log and distinguish an incorrect selector, an unawaited save, and an actual failed API response before changing UI code.

Debrief: what evidence ruled out a plausible cause, and which change was unnecessary?
