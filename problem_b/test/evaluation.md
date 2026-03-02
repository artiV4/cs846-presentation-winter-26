## Evaluation Problem B

---

## Task 1: Code review

### What to review for

- **Correctness**: Whether the helpers implement the intended behavior from the PR without logical bugs.
- **Error handling**: Handling of network/API failures, timeouts, malformed responses, and missing fields.
- **Security / UI exposure**: Avoid exposing internal IDs or unintended fields to the UI.
- **Performance / latency**: Avoid redundant API calls and hot-path latency, especially for the dashboard header.
- **Alignment with PR constraints**: Explicitly tie comments to constraints from `PR.md` (timeouts, no internal IDs, scope).

### Bad example

- **Characteristics**
  - Provides a reasonable review, but:
    - Less explicit structuring of context vs. review criteria.
    - Weaker “stepwise” framing; jumps straight into sections without a clear “job description” for the model.
    - Mentions constraints (e.g., timeouts, internal IDs) but does not foreground them as the primary lens for every comment.
    - Less emphasis on assumptions/non-goals and how they relate to the PR description.
- **Why this is weak**
  - Easier for the model to give generic or partially-scoped feedback because the prompt and answer structure do not strictly separate “context summary” from “focused review.”
  - Constraints are referenced, but not consistently mapped back for each recommendation, making it harder to see traceability to the PR.

### Good example

- **Characteristics**
  - Follows a **structured, context-first pattern**:
    - `Step 1 — Context summary` (intent, affected components, high-risk areas).
    - `Step 2 — Focused review` with clearly scoped dimensions (correctness, error handling, security, performance).
  - **Strong alignment with guidelines**:
    - Ties each concern (timeouts, internal IDs, error handling, performance) explicitly to PR constraints.
    - Calls out assumptions and non-goals (authentication upstream, no architectural redesign).
  - **Actionable and targeted**:
    - Concrete recommendations (e.g., add `timeout=2`, handle `KeyError`, avoid redundant API calls, consider pagination).
- **Why it is good**
  - Mirrors the “structured, context-first prompt” guideline and “explicitly state assumptions and non-goals.”
  - High signal-to-noise: focuses on high-impact issues and reduces generic style feedback.
  - Easier to review and verify against PR requirements.

---

## Task 2: Security and data-exposure concerns

### What to review for

- **Data exposure**: Where internal IDs, emails, roles, or other sensitive data might reach the UI.
- **Input validation assumptions**: What is trusted upstream vs. what should be validated here.
- **Injection / URL construction risks**: How user-controlled values are interpolated into URLs or parameters.
- **Scope alignment**: Security considerations that are in scope (API integration, exposure to UI) vs. out of scope (auth, session, unrelated modules).

### Bad example

- **Characteristics**
  - Enumerates relevant concerns (IDs, emails, URL construction, API response validation).
  - Mentions in/out-of-scope topics, but:
    - Less explicit context-first framing (no clear “Step 1 — Context summary”).
    - Weaker linkage between each recommendation and specific PR constraints.
    - More diffuse structure; security themes are present but not tightly organized under a review focus.
- **Why it is bad**
  - Harder to see which issues are highest risk vs. nice-to-have, because focus is less clearly scoped.
  - Lacks the explicit structured prompt style emphasized in the guideline, so it is more likely to drift into generic comments or overreach.

### Good example

- **Characteristics**
  - Starts with a **context summary** (intent, affected components, high-risk areas) before listing issues.
  - Clearly labeled sections for **data exposure risks**, **input validation**, **injection/URL risks**, and **other security considerations**.
  - Explicitly aligns with PR assumptions and non-goals (auth and validation upstream, no architectural redesign).
  - Recommendations are concrete and scoped (e.g., avoid passing `id` to frontend, consider `params` for `requests.get`, validate emails if usage expands).
- **Why it is good**
  - Directly operationalizes the guideline: context-first, focused review on high-impact security and exposure risks.
  - Keeps security feedback inside the stated system boundary, reducing hallucinated architectural advice.
  - Makes it easier for reviewers to decide what to fix immediately vs. what to monitor.

---

## Task 3: Test and edge-case suggestions

### What to review for

- **Coverage of critical failure modes**: Network/API failures, timeouts, non-200 responses, malformed JSON.
- **Data integrity scenarios**: Empty responses, missing keys, unexpected types.
- **User-centric edge cases**: User not found, duplicate users, role filters returning no users.
- **Performance-related scenarios**: Large responses, repeated calls in hot paths.
- **Security/privacy testing**: Ensuring internal IDs and sensitive fields are not exposed even under unusual API responses.

### Bad example

- **Characteristics**
  - Lists many relevant edge cases (network failure, timeouts, malformed JSON, empty responses, missing keys, large user list, unexpected fields).
  - Focuses on “what to test” but:
    - Lacks an explicit context summary or high-risk framing tied to the PR description.
    - Treats all edge cases somewhat uniformly, without prioritizing those that matter most for the PR’s constraints.
    - Less explicit about assumptions/non-goals.
- **Why it is bad**
  - Without context-first structuring, it is harder to see **why** these tests are chosen and which are most critical.
  - The absence of scoped focus makes it closer to a generic “test everything” list rather than a prioritized, PR-specific plan.

### Good example

- **Characteristics**
  - Begins with a **context summary** (intent, affected components, high-risk/complex areas).
  - Groups tests under clear categories: network/API failures, malformed responses, user-not-found scenarios, role filtering, performance, data exposure, input edge cases.
  - Aligns test ideas explicitly with PR focus (API timeout, dashboard responsiveness, internal ID exposure).
  - States assumptions and non-goals at the end.
- **Why it is good**
  - Reflects the guideline’s emphasis on **context first, then focused criteria** (here, mapped to testing dimensions).
  - Prioritizes high-impact tests (timeouts, data exposure, hot-path behavior) over generic or low-value ones.
  - Easier to translate directly into a concrete test plan for this PR.

---

## Task 4: High-risk areas and review focus

### What to review for

- **High-risk areas**:
  - External API integration and reliability (errors, timeouts, malformed data).
  - Data exposure to the UI (IDs, emails, roles).
  - Performance issues and redundant calls in hot paths (especially header rendering).
  - Fragile assumptions about the external API (pagination, fields always present).
- **Review focus vs. non-goals**:
  - Focus on correctness, security, performance in the new helpers.
  - Avoid architectural redesign, upstream auth/session concerns, and unrelated refactoring.

### Bad example

- **Characteristics**
  - Correctly identifies key high-risk areas (API error handling, data exposure, performance, upstream validation assumptions).
  - Provides “review should focus on” and “review should avoid” sections.
  - However:
    - Does not explicitly use the context-summary-first structure.
    - Less tightly connected to the specific guideline about structured, AI-led review.
    - Slightly more generic; could apply to many PRs without clearly tying back to the detailed PR description.
- **Why it is bad**
  - Misses the opportunity to first summarize the PR intent and components, which is key for AI-led review workflows.
  - Focus/avoid lists are good but not clearly grounded in high-risk areas identified via a structured context pass.

### Good example

- **Characteristics**
  - Uses a **two-step structure**: context summary followed by high-risk areas and review focus.
  - High-risk areas are precisely articulated (external API integration, data exposure, performance, API assumptions).
  - Review focus is tightly scoped to:
    - Correctness of API integration and response validation.
    - Data exposure/privacy and internal ID protection.
    - Performance in hot paths.
    - Edge-case handling for empty/malformed responses.
  - Clear list of what to avoid/deprioritize, aligned with PR non-goals.
- **Why it is good**
  - Exemplifies the guideline’s pattern: **context → focused criteria → explicit boundaries**.
  - Makes it easy for a human reviewer (or an LLM) to allocate attention where it matters most and ignore out-of-scope issues.
  - Reduces noise and increases the usefulness of the review, especially for large or unfamiliar PRs.

