---
paths:
  - "issuetrackerapi/**/*.py"
---
Use existing authentication dependencies and database sessions. Validate at the API
boundary and enforce uniqueness and relationships in the database. Add a regression
test for every repaired defect. Preserve omitted PATCH fields; distinguish null.
