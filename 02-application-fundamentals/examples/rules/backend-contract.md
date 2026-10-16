---
paths:
  - "issuetrackerapi/**/*.py"
---

# Backend contract guidance

When discussing or modifying matching backend files, identify the existing validation and authentication patterns before proposing changes. Use SOFTWARE_SPECIFICATIONS.md as the functional contract.

For assignment updates, distinguish an omitted assigned_user_id from explicit null. Reference the existing User ID type; do not invent user records or a second user model.

Label statements as observed implementation, required behavior, or proposed change. Cite the relevant file/symbol. A source inspection is not an executed test.
