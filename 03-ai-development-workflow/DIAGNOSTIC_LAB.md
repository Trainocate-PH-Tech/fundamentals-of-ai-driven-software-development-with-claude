# Resolve contradictions and repair delegation

Complete the relevant [module prerequisites](README.md). Use student apps only.
This lab teaches symptom → reproduction → hypotheses → discriminating check →
minimal repair → regression. Evidence belongs to milestone `delegation-practice`.

## Guided scenario

Use this deliberately contradictory request: “Give every user the full /users list,
but preserve admin-only user access and expose only safe assignee display fields.”
Do not apply it to the application.

**Inside Claude:**

```text
In Plan Mode, inspect the specification and existing /users auth. Identify the
contradiction in the supplied request. Propose the smallest compatible interpretation
and ask one focused clarification before implementation. Do not change code.
```

## Expected evidence and verification

Expected: preserve /users and propose a separate safe selector, with explicit
acceptance required. Next, deliberately delegate backend-reviewer a nonexistent
plan path under milestone delegation-practice. It should return insufficient
evidence and name missing inputs. Supply the accepted real plan and source paths,
repeat the review, and compare results. Monitor the actual task; do not accept an
invented report. Main session saves both attempts without overwriting them.

Save inputs, observed facts, unsupported hypotheses, command/exit-code evidence
and remaining gaps under `workshop-output/milestones/delegation-practice/`. Read-only agents
return findings; the main session saves files, runs commands and owns repairs.

## Independent task

Give bug-investigator only a symptom without a log; evaluate whether it separates hypotheses from confirmed causes.

Debrief: what evidence ruled out a plausible cause, and which change was unnecessary?
