# Module 4 — Implement bounded, verified changes

**Entry:** verified application map and accepted data plan. **Result:** complete
Issue Tracker. Use the [specification](../SOFTWARE_SPECIFICATIONS.md) and
[workflow recipes](../CLAUDE_USE_CASES.md). Read each app's AGENTS.md. Student apps
are the active workspace; consult the instructor solution only after an attempt.

## Required cycle for every increment

1. Invoke the planning prompt below in Plan Mode. Inspect source paths, scope and checks.
2. Accept the plan, leave Plan Mode, and explicitly ask Claude to save it to the
   milestone's `plan.md` without implementing yet. Saving alone is not approval.
3. Invoke the listed implementation command. It requires that explicit acceptance.
4. Run the Bash gate yourself, then the verification skill and a bounded review.
5. Repair confirmed failures within accepted scope; rerun affected checks and save
   evidence/handoff. Review the diff before committing in the affected app repo.

Every milestone directory is `workshop-output/milestones/<id>/`. Preserve earlier
plans/reviews/logs. Record workspace, app revisions, dirty state and actual outcomes.
The [use-case guide](../CLAUDE_USE_CASES.md) contains exact save, review and repair
patterns. The commands below are **inside Claude** unless marked Bash.

## 1. Data — 01-data

```text
/workshop-plan 01-data Inspect issuetrackerapi and plan only the persistence slice: Category and Issue, existing string UUID User references, case-insensitive uniqueness, category RESTRICT/user SET NULL, status/priority constraints, UTC timestamps, migration and idempotent category seed. Preserve users. Identify integrity and migration checks before implementation.
```

Accept/save to `workshop-output/milestones/01-data/plan.md`, then:

```text
/workshop-implement 01-data workshop-output/milestones/01-data/plan.md
```

**Bash:**

```bash
./workshop db migrate
./workshop db seed
./workshop db seed
./workshop test
```

Expected: existing users preserved; repeated category seed does not duplicate the
four sample categories. The local demo seed updates `admin@example.com` / `password`;
never target a real deployment. Independent: prove database uniqueness and user
preservation during migration. Recovery checkpoint: `01-data`.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 01-data workshop-output/milestones/01-data/plan.md Verify the accepted increment and report criterion-level evidence.
```

## 2. Categories — 02-categories

```text
/workshop-plan 02-categories Inspect existing backend patterns and add authenticated category CRUD only. Trim/validate names, enforce case-insensitive uniqueness, paginate alphabetically and reject deletion of linked categories with 409. Add spec/tracker/test_categories.py. No issue endpoints or frontend changes.
```

Accept/save to `workshop-output/milestones/02-categories/plan.md`, then:

```text
/workshop-implement 02-categories workshop-output/milestones/02-categories/plan.md
```

**Bash:**

```bash
./workshop test spec/tracker/test_categories.py
```

Expected: 201 create, 409 duplicate/protected deletion, 422 invalid input, 404 missing,
204 empty successful delete. Independent: duplicate rename and association preservation.
Recovery checkpoint: `02-categories`.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 02-categories workshop-output/milestones/02-categories/plan.md Verify the accepted increment and report criterion-level evidence.
```

## 3. Issues — 03-issues

```text
/workshop-plan 03-issues Inspect Category/User integration and add authenticated issue CRUD. Validate title/description/status/priority and references; default open/medium. Preserve omitted PATCH fields and allow null only for nullable fields. Return safe display data. Add spec/tracker/test_issues.py. No UI changes.
```

Accept/save to `workshop-output/milestones/03-issues/plan.md`, then:

```text
/workshop-implement 03-issues workshop-output/milestones/03-issues/plan.md
```

**Bash:**

```bash
./workshop test spec/tracker/test_issues.py
```

Independent: boundary lengths, whitespace-only title and unauthenticated writes.
Recovery checkpoint: `03-issues`.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 03-issues workshop-output/milestones/03-issues/plan.md Verify the accepted increment and report criterion-level evidence.
```

## 4. Assignment — 04-assignment

```text
/workshop-plan 04-assignment Inspect current assignment behavior. Add authenticated read-only GET /assignees returning only ID/full_name for non-deleted existing users. Preserve admin-only /users. Test assign, omitted-field preservation, invalid reference, null clearing and ordinary-user access in spec/tracker/test_assignment.py.
```

Accept/save to `workshop-output/milestones/04-assignment/plan.md`, then:

```text
/workshop-implement 04-assignment workshop-output/milestones/04-assignment/plan.md
```

**Bash:**

```bash
./workshop test spec/tracker/test_assignment.py
```

Independent: verify ordinary-user assignee access without exposing /users or sensitive
fields. Complete the [assignment diagnosis](03_DIAGNOSTIC_LAB.md). Recovery: `04-assignment`.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 04-assignment workshop-output/milestones/04-assignment/plan.md Verify the accepted increment and report criterion-level evidence.
```

## 5. Filters — 05-filters

```text
/workshop-plan 05-filters Inspect issue listing and add literal case-insensitive title substring search plus AND-combined status, priority, category_id and assigned_user_id filters. Preserve pagination. Sort updated_at descending then ID. Test literal percent/underscore, no matches and equal-timestamp pagination in spec/tracker/test_filters.py.
```

Accept/save to `workshop-output/milestones/05-filters/plan.md`, then:

```text
/workshop-implement 05-filters workshop-output/milestones/05-filters/plan.md
```

**Bash:**

```bash
./workshop test spec/tracker/test_filters.py
```

Independent: equal-timestamp paging without repetition or omission. Recovery: `05-filters`.

## 6. Frontend — four teaching increments

These four IDs organize evidence, **not recovery snapshots**. The existing
`06-frontend` checkpoint restores the completed UI only. Each prompt must produce
an accepted plan before the corresponding implementation invocation.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 05-filters workshop-output/milestones/05-filters/plan.md Verify the accepted increment and report criterion-level evidence.
```

### 06a-categories-ui: category management

```text
/workshop-plan 06a-categories-ui Inspect the existing React layout, routing and services. Add category navigation/list/create/edit/delete using real API calls and existing auth headers. Include labels, loading/error/empty states and protected-deletion feedback. Add exact Playwright dev dependency, configuration, test:e2e script and a focused category browser test. Do not build issue screens yet.
```

Accept/save to `workshop-output/milestones/06a-categories-ui/plan.md`, then:

```text
/workshop-implement 06a-categories-ui workshop-output/milestones/06a-categories-ui/plan.md
```

Observe create/edit/delete and validation feedback in the browser. Independent:
verify an API error is visible rather than rendered as an empty successful list.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 06a-categories-ui workshop-output/milestones/06a-categories-ui/plan.md Verify the accepted increment and report criterion-level evidence.
```

### 06b-issue-create-details: creation and persistence

```text
/workshop-plan 06b-issue-create-details Inspect the completed category UI. Add issue listing, creation and details using real endpoints. Fetch all category option pages and safe assignees. Include required labels, validation, loading/error/empty states. Extend browser tests to create an issue and verify details after reload. No editing/filtering/deletion yet.
```

Accept/save to `workshop-output/milestones/06b-issue-create-details/plan.md`, then:

```text
/workshop-implement 06b-issue-create-details workshop-output/milestones/06b-issue-create-details/plan.md
```

Observe creation through the form and persisted details after reload. Independent:
no categories available must produce useful guidance rather than an unusable save.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 06b-issue-create-details workshop-output/milestones/06b-issue-create-details/plan.md Verify the accepted increment and report criterion-level evidence.
```

### 06c-edit-assignment: updates and clearing

```text
/workshop-plan 06c-edit-assignment Add issue editing through existing services. Persist category, status, priority and assignee changes. Distinguish omitted fields from null clearing. Extend browser tests to edit/reload and unassign/reload. Keep authentication and existing pages intact.
```

Accept/save to `workshop-output/milestones/06c-edit-assignment/plan.md`, then:

```text
/workshop-implement 06c-edit-assignment workshop-output/milestones/06c-edit-assignment/plan.md
```

Observe changed fields after reload and an unassigned issue after explicit clearing.
Independent: reproduce a rejected API update and verify the UI explains it.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 06c-edit-assignment workshop-output/milestones/06c-edit-assignment/plan.md Verify the accepted increment and report criterion-level evidence.
```

### 06d-filters-deletion: discovery and confirmed removal

```text
/workshop-plan 06d-filters-deletion Add issue search, combined filters/reset, pagination and delete confirmation. Extend browser tests for matching/nonmatching results, reset, cancel and confirm deletion and category conflict feedback. Preserve existing issue/category behaviors and complete the specification's browser lifecycle.
```

Accept/save to `workshop-output/milestones/06d-filters-deletion/plan.md`, then:

```text
/workshop-implement 06d-filters-deletion workshop-output/milestones/06d-filters-deletion/plan.md
```

Observe filtered matches, reset, cancellation preserving an issue, and confirmed
removal. Independent: no matches and network error must remain distinct UI states.


After the applicable Bash/browser gate, verify inside Claude:

```text
/workshop-verify 06d-filters-deletion workshop-output/milestones/06d-filters-deletion/plan.md Verify the accepted increment and report criterion-level evidence.
```

### Browser gates for each increment

Run **Bash** after implementation:

```bash
./workshop build
(cd issuetrackerweb && npx playwright install chromium)
```

Start API and web in separate root terminals and keep them running:

```bash
./workshop start api
```

```bash
./workshop start web
```

In a third terminal:

```bash
./workshop e2e
```

Use `http://localhost:8000/#/login` with the local demo account. Each increment adds
tests for implemented behavior only; do not run tests for future screens as a passing
gate. For missing Linux browser libraries, follow Playwright's system-dependency setup.
At the completed frontend milestone, run `./workshop test` and the full browser suite.

## Verification, review and repair example

For categories, invoke:

```text
/workshop-verify 02-categories workshop-output/milestones/02-categories/plan.md Category CRUD and integrity
```

Use the same pattern with the exact milestone ID/plan for every increment.

```text
Use backend-reviewer for milestone 02-categories. Supply its plan, specification,
issuetrackerapi and milestone evidence/logs. Request path-backed contract/auth/
integrity findings without edits or commands. Main session: save review.md in that
milestone, reproduce findings and classify each as confirmed, rejected with evidence
or needing more evidence. Do not inspect instructor-reference.
```

Use ui-reviewer for frontend increments. Monitor actual tasks and file reads; a
reviewer's verdict cannot replace Bash/browser results. For a confirmed defect,
use the bounded repair prompt in the [recipes](../CLAUDE_USE_CASES.md). Preserve
failed-run evidence and append the repaired run. Review diffs and commit in the
affected app repository once the gate passes.

**Exit:** the complete real browser lifecycle works. Continue to
[Module 5](../05-testing-debugging-and-demo/README.md).

Apply this workflow in the [diagnostic lab](03_DIAGNOSTIC_LAB.md).
