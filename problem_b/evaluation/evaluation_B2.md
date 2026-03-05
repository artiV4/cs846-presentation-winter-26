# Evaluation – B2: Test Adequacy

## Evaluation Description

The test adequacy review should:

- Focus strictly on test quality, not re-reviewing production code.
- Identify brittle or misleading tests (e.g., hardcoded assumptions, fragile fixtures).
- Detect meaningful gaps between intended behavior and actual coverage.
- Highlight missing edge cases relevant to the PR’s scope.
- Avoid drifting into architectural redesign or unrelated concerns.
- Propose the minimum additional tests required before merge.

---

## Bad Example

### Characteristics of Output:

- Mixes test-quality critique with broader security and architectural concerns.
- Expands into areas not directly tied to the PR’s scope (e.g., SQL injection, privilege escalation).
- Suggests many additional tests without clearly prioritizing minimum necessary coverage.
- Raises speculative concerns not strongly grounded in the actual test suite.
- Does not clearly separate brittle tests from general missing coverage.
- Overgeneralizes risk categories without tying them to specific test files or fixtures.

### Why This Is Weak

- The review partially drifts into broader system hardening rather than strictly evaluating test quality.
- It proposes an extensive list of additional tests without distinguishing essential coverage from nice-to-have improvements.
- It treats the test suite as incomplete in general rather than evaluating it in the context of this specific PR.
- It lacks disciplined scope control, reducing clarity about what is actually required before merge.

While many suggestions are reasonable, the output resembles a generalized test-hardening checklist rather than a scoped PR test adequacy review.

---

## Good Example

### Prompt Used

The prompt included:

- A structured context summary requirement.
- Explicit assumptions about test isolation and fixtures.
- Clear non-goals (no performance/security review unless it affects tests).
- Explicit instruction to review only test quality.
- Focus on brittle tests, edge cases, coverage gaps, and minimum additions.

### Characteristics of the Output

- Begins with a structured summary of intent, affected components, and high-risk areas.
- Clearly separates brittle tests from missing edge cases.
- Identifies specific weaknesses (e.g., skipped timeout test, reliance on certain response fields).
- Stays within test quality scope without re-reviewing implementation logic.
- Distinguishes between documented intended behavior and actual coverage.
- Proposes targeted, minimal additional tests rather than broad system redesign.
- Avoids architectural suggestions or unrelated refactoring.

### Why This Is Better

- The review is disciplined and narrowly scoped to test adequacy.
- It avoids conflating test critique with production code critique.
- It identifies concrete coverage gaps directly tied to PR behavior.
- It focuses on reliability and isolation rather than speculative system risks.
- It proposes incremental, merge-ready improvements rather than a large expansion of scope.
- The structure mirrors how real PR reviewers evaluate test coverage before approval.

---

## Overall Comparative Insight

Both outputs identify meaningful gaps in test coverage. However, the guided version demonstrates:

- Stronger scope discipline.
- Clearer separation between brittle tests and missing coverage.
- Better prioritization of minimal additional tests before merge.
- Reduced drift into broader security or architectural concerns.

The unguided version, while technically sound, tends to:

- Over-expand into general system hardening.
- Propose broader test additions without clearly prioritizing necessity.
- Blend multiple risk domains rather than staying test-focused.

This comparison shows that structured, context-first prompting improves precision and scope control in LLM-assisted test adequacy reviews.