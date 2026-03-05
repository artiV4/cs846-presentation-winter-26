You are reviewing this pull request for Problem B4: Correctness and Constraint Fit.

**Step 1 — Context summary**
- **Intent:**
    - Adds a new user helpers backend and API endpoints, refactors database schema/seed logic, and introduces comprehensive tests and fixtures.
    - Improves test isolation, reliability, and coverage for user-related backend logic.
- **Affected components:**
    - `user_helpers.py` (backend logic and endpoints)
    - `database.py`, `seed.py` (schema and seed logic)
    - Test files: `tests/user_helpers/*`, `tests/test_user_helpers_requests.py`, `tests/conftest.py`, `tests/test_auth_flow.py`
- **High-risk areas:**
    - Authentication enforcement
    - Data exposure and schema correctness
    - Test coverage and reliability

**Step 2 — Focused review: Correctness and Constraint Fit**

Assumptions:
- Authentication is enforced via FastAPI dependency injection.
- Input validation is handled by FastAPI and Pydantic.
- Only the changes in this PR are under review.

Non-goals:
- Do not review for performance or style unless it affects correctness or constraints.
- Do not propose architectural redesigns or new frameworks.

Review only for:
- Functional correctness
- PR-constraint alignment
- Severity classification
- Minimal fix recommendations
- Merge decision

---

### Findings

**1. Authentication Enforcement**
- **Severity:** Question
- **Impacted file(s):** `user_helpers.py`
- **Violated requirement/constraint:** Reviewer concern about authentication enforcement (see B3).
- **Minimal fix:** Add code comments clarifying that authentication is enforced by FastAPI dependency injection, even if assigned to `_`. Optionally, use a named variable for clarity.

**2. Data Exposure and Schema Correctness**
- **Severity:** Major
- **Impacted file(s):** `user_helpers.py`, API responses
- **Violated requirement/constraint:** Internal IDs and roles are exposed in API responses (`/users`, `/users/lookup`).
- **Minimal fix:** Restrict exposure of internal IDs and roles to trusted/internal clients only, or document intended exposure. Use dedicated response models for public vs. internal endpoints.

**3. Test Coverage and Reliability**
- **Severity:** Major
- **Impacted file(s):** `tests/user_helpers/test_user_helpers_requests.py`, `tests/user_helpers/test_user_display.py`, etc.
- **Violated requirement/constraint:** Missing edge case tests (invalid IDs/emails, external API failures, expired JWTs, schema drift).
- **Minimal fix:** Implement the skipped test for backend timeout/malformed response. Add tests for invalid/malformed user IDs/emails, external API failures, expired/invalid JWTs, and response schema validation.

**4. Seed Logic and Idempotency**
- **Severity:** Minor
- **Impacted file(s):** `seed.py`, `database.py`
- **Violated requirement/constraint:** Seed logic is tested for idempotency, but not for conflicting or partial data.
- **Minimal fix:** Add tests for conflicting/partial seed data scenarios.

**5. Documentation and Maintainability**
- **Severity:** Minor
- **Impacted file(s):** All
- **Violated requirement/constraint:** Lack of documentation for some design decisions (e.g., why authenticated user object is unused).
- **Minimal fix:** Add code comments explaining design choices and intended exposure.

---

**Merge Decision:**
- **Request Changes**
    - The PR introduces valuable improvements and robust backend logic, but has major gaps in test coverage and data exposure constraints. Addressing the above major findings (test coverage, data exposure) is required before merge. Minor issues (documentation, seed logic) can be addressed in follow-up PRs.
