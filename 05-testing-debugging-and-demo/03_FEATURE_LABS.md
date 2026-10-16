# Optional automated review and workflow transfer

Complete [Module 5](README.md) first. Headless Claude (`claude -p`) is useful for
bounded reports after interactive prompts have been tested. It still consumes
account/API usage and does not make a generated report deterministic.

**Guided, Bash from course root:**

```bash
claude -p --permission-mode plan 'Read SOFTWARE_SPECIFICATIONS.md and workshop-output/milestones/final/evidence.md. Report unsupported completion claims with paths. Do not edit files or run commands.' > workshop-output/milestones/final/headless.txt
```

**PowerShell 7.4+ (Windows):**

```powershell
claude -p --permission-mode plan 'Read SOFTWARE_SPECIFICATIONS.md and workshop-output/milestones/final/evidence.md. Report unsupported completion claims with paths. Do not edit files or run commands.' > workshop-output/milestones/final/headless.txt
```

Check the exit status, report contents and account usage. A blank report or failed
authentication is not success. Do not bypass permissions to make automation pass.
**Independent:** run the same review against a deliberately incomplete copy of the
evidence file. Compare findings and false positives; retain deterministic CI tests
as the delivery gate.

Transfer the kit using the capstone exercise in Module 5. Keep workflow procedures
in skills, stable project facts in the profile, enforceable checks in scripts/tests,
and secrets in approved environment/credential storage.
