# Diagnose a browser failure from evidence

Complete the relevant [module prerequisites](README.md). Use student apps only.
This lab teaches symptom → reproduction → hypotheses → discriminating check →
minimal repair → regression. Evidence belongs to milestone `browser-diagnosis`.

## Guided scenario

Use an actual failed local browser test if available. Otherwise, temporarily stop
your own local API, run the browser suite and keep its failure output, then restart
the API in its original terminal/workspace. This changes local service availability,
not application code. Do not use shared or production services.

**Inside Claude:**

```text
Inspect the supplied browser failure log, trace location and API startup output.
Compare service availability, authentication, selector and application-regression
hypotheses. Do not edit source until evidence discriminates between them. Propose
the smallest next check. Record diagnosis and actual rerun results under milestone
browser-diagnosis. Do not add sleeps, skip assertions or claim to view an unavailable
trace. If a tool cannot inspect it, give me exact manual inspection steps.
```

## Expected evidence and verification

Expected: identify unavailable API when that is the deliberately introduced failure,
restore the service and rerun npm run test:e2e from issuetrackerweb (PowerShell: npm.cmd run test:e2e). Use the trace command printed by
Playwright for the actual trace path; do not invent a successful browser observation.
Compare failed and passing runs with timestamps, workspace and source state.

Save inputs, observed facts, unsupported hypotheses, command/exit-code evidence
and remaining gaps under `workshop-output/milestones/browser-diagnosis/`. Read-only agents
return findings; the main session saves files, runs commands and owns repairs.

## Independent task

Give a reviewer a stale passing log after a new source edit. Require it to mark current behavior unverified and request fresh evidence.

Debrief: what evidence ruled out a plausible cause, and which change was unnecessary?
