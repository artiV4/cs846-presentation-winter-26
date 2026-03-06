# Evaluation – B2: Test Adequacy

## Evaluation Description

The review should:
- Identify brittle or misleading tests by pointing to specific test names and the exact lines that make them brittle.
- Identify missing edge cases by referencing the specific test or function that lacks coverage.
- Identify gaps between intended behavior and actual coverage by citing both the code and the test (or lack of one).
- Propose only the minimum additional tests needed before merge — not a comprehensive wishlist.
- Ground every finding in a specific line or test name from the diff.

---

## Bad Example

### Prompt Used
```
Review only test quality. Identify brittle/misleading tests, missing edge cases, and gaps between intended behavior and coverage. Propose the minimum additional tests needed before merge.
```

### Characteristics of Output
- Findings reference test names but rarely quote the specific lines that make them brittle (e.g., "hardcoded user counts" without citing the actual assertion).
- Flags missing tests for JWT expiry, RBAC, and SQL injection — none of which are in scope for this PR or its stated constraints.
- "Minimum additional tests" list contains 7 items, several of which are out of scope (role-based access control, SQL injection, seed logic rollback).
- No distinction between what the tests *document intentionally* (e.g., the skipped test) and what is genuinely missing.
- Summary repeats the findings without adding new information.

### Why This Is Weak
Without being instructed to ground findings in specific lines, the LLM drifted into generic test advice — suggesting tests for concerns the PR explicitly does not address. The "minimum tests before merge" list is not minimum at all; it includes items that would be appropriate for a broader test audit but not for this specific PR.

---

## Good Example

### Prompt Used
```
I am reviewing a pull request. Below is the diff, PR description, and test file. [diff] [PR_description] [location to test_user_helpers.py]. Review only for test quality: brittle or misleading tests, missing edge cases, and gaps between intended behavior and coverage. For each finding: 1. Quote the specific test or line of code that supports your claim. 2. Explain the gap using only those lines. 3. If you cannot point to a specific line, do not include the finding. End with the minimum list of additional tests needed before merge.
```

### Characteristics of Output
- Every finding quotes the exact assertion or decorator that is the problem (e.g., `assert len(calls["urls"]) == 2` in `test_format_user_for_header_avoids_extra_calls`).
- Correctly distinguishes between intentionally skipped tests (documented behavior not yet implemented) and genuinely missing coverage.
- Identifies that `test_get_user_list_filters_role_and_hides_internal_id` is misleading because it asserts `"id" in u` while the comment implies the opposite intent — a subtle but important finding that requires reading the specific line.
- Minimum tests list contains 5 targeted items, all tied directly to gaps identified in the diff.
- Does not suggest out-of-scope tests (JWT, RBAC, SQL injection).

### Why This Is Better
By requiring line-level evidence, the LLM caught a subtle misleading test that the naive prompt missed entirely — the test that *documents* ID exposure while *implying* it should be hidden. The minimum tests list is genuinely minimal because the LLM could only include items it could justify with a specific line, which filtered out the generic suggestions that appeared in the naive output.