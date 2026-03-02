# Evaluation — Problem B Test Tasks

This evaluation describes what a strong answer should cover for each task, and contrasts weak vs. strong model outputs.

---

## Task 1 — Code Review (Overall PR Review)

### What to Review For

- **Correctness and error handling** in `user_helpers.py` given the PR’s goal (user display lookup for the dashboard header and support email lookup).
- **Security and data exposure**, especially anything surfaced to the UI (names, roles, emails) vs. what must remain server-side.
- **Performance and responsiveness**, including unnecessary or redundant API calls and how they affect the dashboard render path.
- **Alignment with PR constraints and scope** in `test/PR.md` (no internal IDs in UI, 2s timeout, dashboard responsiveness, “Out of scope” section).

### Bad Example

**Characteristics of Output:**

- Focuses mostly on **style and formatting** (imports inside functions, docstring style, variable naming).
- Mentions generic ideas like “add logging” or “add comments” without tying them to the PR goal.
- Points out the hardcoded URL but does not connect it to risk in this specific context.
- Does not mention **timeout handling**, **dashboard responsiveness**, or **constraints** from the PR.
- Treats the file as an isolated script instead of part of a dashboard header path.

**Why This Is Weak**

- Feedback is **generic and context-agnostic**; another file could receive the same comments.
- It ignores the **stated constraints** (no internal IDs, 2-second timeout, responsive dashboard).
- It fails to identify concrete risks like redundant API calls or missing error handling that would affect the dashboard UX.
- The review does not help a maintainer decide **what to fix first** or why.

### Good Example

**Characteristics of Output:**

- Checks that `format_user_for_header` and related helpers are **correct** for the PR goal (proper name/role display, handling of missing roles, handling user-not-found).
- Calls out **lack of timeout and error handling** on external API calls and connects this to the “dashboard must not block” requirement.
- Highlights **redundant or repeated calls** to the user API (e.g., fetching full lists for simple lookups) and explains their impact on **latency** and **responsiveness**.
- Mentions **security/data-exposure issues** (e.g., returning or exposing fields that should not reach the UI) where relevant.
- Explicitly references the **constraints and “Out of scope”** items from the PR and avoids asking for unrelated refactors.

**Why This Is Strong**

- Feedback is **anchored to the PR description** and constraints, not just general best practices.
- It balances correctness, security, and performance with a clear sense of **impact on the dashboard**.
- The comments are **actionable** (e.g., “add timeout parameter here,” “avoid calling `get_user_list()` on every header render”) and easy to implement.
- It respects scope, which increases **trust** in the review and makes it realistic for production use.

---

## Task 2 — Security and Data-Exposure Concerns

### What to Review For

- **Which data is exposed** to the UI vs. kept server-side (names, roles, emails, IDs).
- **Where inputs are not validated** or sanitized (e.g., `user_id`, `role`, `email`), taking into account that some validation is upstream.
- **URL construction and injection risks**, including query parameters based on user-controlled inputs.
- **Enumeration or scraping risks**, such as unbounded user listing or email-based lookups that could leak information.
- Whether the findings are **prioritized** according to the PR’s security constraints (no internal IDs in UI) and realistic attack surface.

### Bad Example

**Characteristics of Output:**

- Lists a long set of **generic security concerns** (e.g., SSL verification, lack of auth, generic “PII exposure”) without reference to the PR context.
- Mentions that emails are PII but does not distinguish between UI vs. server-only use.
- Flags many theoretical issues (e.g., “what if the API is compromised?”) that are **not grounded in this code**.
- Does not mention the PR’s explicit **“do not expose internal IDs”** constraint.
- Lacks any prioritization; all bullet points appear equally important.

**Why This Is Weak**

- The answer feels **boilerplate** and not tailored to `user_helpers.py`.
- It fails to highlight the **main contract** in the PR (no internal IDs in the front end) and whether the code respects or violates it.
- The lack of prioritization makes it hard to understand what to fix first.
- Some speculative risks distract from the **real data flows** in this PR.

### Good Example

**Characteristics of Output:**

- Explicitly analyzes what each helper returns and **where the data is consumed** (dashboard header vs. support tool).
- Calls out any exposure of **internal IDs** or sensitive fields that could reach the UI, and confirms when helper usage is server-only.
- Identifies **URL construction risks** (e.g., concatenating `role` into a query string) and suggests safer alternatives.
- Notes **user enumeration** or email lookup risks and explains the impact (e.g., potential to probe for valid accounts).
- Prioritizes risks according to the PR constraints and provides **concrete mitigations**.

**Why This Is Strong**

- It is **specific to this PR and code**, not generic security advice.
- The analysis aligns with the **stated constraints** and system boundaries (auth & validation upstream).
- Recommendations are **actionable** and scoped (e.g., “avoid returning IDs to UI,” “validate/sanitize role values,” “rate-limit or log abuse on email lookups”).
- The reviewer shows clear understanding of **which data paths matter most** for real-world exposure.

---

## Task 3 — Test and Edge-Case Suggestions

### What to Review For

- **Concrete test scenarios** for the helpers in `user_helpers.py`, especially around the external API behavior.
- **Failure modes**: network errors, timeouts, invalid JSON, missing fields, user not found, empty lists.
- **Boundary conditions**: unusual roles, duplicate emails, large user lists.
- Coverage of both **dashboard header behavior** and **support tool lookups**, connected back to the PR’s risks and constraints.

### Bad Example

**Characteristics of Output:**

- Suggests only very broad test categories: “test success cases,” “test failure cases,” “test invalid input.”
- Does not mention the **external API** or how it might fail (timeouts, partial responses, bad JSON).
- Ignores the PR’s constraints and risks (e.g., dashboard responsiveness, no internal IDs in UI).
- Fails to distinguish between **UI-facing behavior** and **internal support tool behavior**.
- Offers few or no examples of specific inputs or conditions.

**Why This Is Weak**

- The suggestions are **too high-level** for a tester to turn directly into test cases.
- It does not help ensure coverage of **realistic edge cases** for this dashboard + API scenario.
- It misses critical failure paths (e.g., slow API, empty user list, missing keys), leaving the most important behavior untested.
- There is no linkage to the **constraints in the PR** or to the previous review findings.

### Good Example

**Characteristics of Output:**

- Proposes tests for **success and failure** of each helper, with **specific scenarios**, such as:
  - API returns 200 but missing `name`, `email`, or `role` keys.
  - API returns 4xx/5xx or invalid JSON.
  - `get_user_list(role=\"admin\")` with no admins, or with mixed roles.
  - `format_user_for_header` when user is not found in `get_user_list`.
  - `lookup_by_email` with duplicate emails, unknown email, and mixed-case email.
- Includes tests related to **performance and responsiveness**, such as ensuring that repeated calls don’t block the dashboard (or are cached/limited if design allows).
- Connects tests to **constraints** (e.g., “verify that no internal IDs ever appear in the header output”).
- Suggests both **unit-level tests** and a few **integration-style checks** aligned with the PR’s Testing section.

**Why This Is Strong**

- The tests are **immediately implementable** and clearly derived from the code and PR.
- They explicitly cover **edge cases and failure modes** that would cause user-visible issues.
- They reinforce the PR’s constraints (no IDs in UI, responsiveness, correct role display).
- This kind of test plan would **significantly reduce regression risk** for this change.

---

## Task 4 — High-Risk Areas and Review Focus

### What to Review For

- Identification of **high-risk or complex areas** in the change (e.g., external API calls in the render path, data shaping for UI output, email lookup behavior).
- Clear proposal of **what the review should focus on**, aligned with the PR’s Risk & Impact and Constraints sections.
- Explicit mention of **what is out of scope** or should be deprioritized (e.g., broad refactors, style-only issues).

### Bad Example

**Characteristics of Output:**

- States that “everything that changed is high risk” or lists the entire file without prioritization.
- Repeats generic concerns (e.g., “check for bugs and security issues”) without tying them to specific parts of the code.
- Ignores the PR’s **Risk & Impact**, **Constraints**, and **Out of Scope** sections.
- Suggests focusing on style, naming, or unrelated refactors despite being marked out of scope.

**Why This Is Weak**

- The answer fails to **prioritize reviewer attention**; it treats all lines as equally important.
- It does not use the rich context provided by `PR.md` to identify where issues would be most harmful.
- It conflicts with the PR’s scope, which can waste reviewer and developer time.
- It offers no concrete guidance that would improve the effectiveness of an LLM-assisted review.

### Good Example

**Characteristics of Output:**

- Identifies specific **high-risk zones**, such as:
  - External API calls in `get_user_display` and `get_user_list` (latency, timeout, error handling).
  - Logic in `format_user_for_header` that shapes what appears in the dashboard header.
  - User lookup by email and its implications for support and potential enumeration.
- States that review should **focus on**:
  - Correctness and error handling for these helpers.
  - Performance impact on the dashboard path.
  - Data exposure to the UI (ensuring no internal IDs are surfaced).
- Explicitly notes **what to deprioritize**, citing the PR’s “Out of scope” list (e.g., no broad refactors, no auth redesign).
- Uses the PR’s **Risk & Impact** section to justify why certain functions are higher priority.

**Why This Is Strong**

- It gives reviewers a **clear, prioritized map** of where to spend effort.
- The focus areas are **well-justified by the PR context**, constraints, and declared risks.
- It aligns with the guideline’s emphasis on **structured, scoped prompts** and explicit non-goals.
- This kind of answer would help students (and models) produce **more targeted, valuable reviews** on the second (guided) pass.

