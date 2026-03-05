# Evaluation – B4: Correctness and Constraint Fit

## Evaluation Description

The correctness and constraint-fit review should:

- Focus strictly on functional correctness and alignment with the PR description.
- Tie each finding to a specific violated requirement or constraint.
- Clearly classify severity (Blocker, Major, Minor, Question).
- Provide a minimal, actionable fix for each issue.
- Avoid rehashing B1/B2 without new synthesis.
- End with a justified merge decision grounded in prior findings.

---

## Bad Example

### Characteristics of Output:

- Lists issues but does not clearly anchor them to explicit PR constraints.
- Blends functional correctness and test concerns without prioritization.
- Repeats earlier findings without synthesizing them.
- Provides minimal fixes that are somewhat broad (“restrict exposure,” “add tests”) without scoping impact.
- Merge decision is reasonable but not tightly justified against constraint violations.
- Does not explicitly frame findings relative to the PR’s stated intent and scope.

### Why This Is Weak

- The review reads like a continuation of B1/B2 rather than a final integration step.
- It lacks strong alignment between findings and the PR’s documented constraints.
- Severity labels are present, but prioritization logic is not strongly articulated.
- The merge decision feels somewhat procedural rather than clearly constraint-driven.
- It does not clearly separate functional correctness from broader hardening suggestions.

The output is technically reasonable but lacks synthesis and constraint-focused rigor.

---

## Good Example

### Prompt Used

The prompt included:

- A structured context summary requirement.
- Explicit scope limitation to correctness and constraint alignment.
- Assumptions about authentication and validation boundaries.
- Non-goals preventing performance/security drift.
- Explicit instruction to classify severity and provide minimal fixes.
- Requirement to end with a merge decision.

### Characteristics of the Output

- Begins with structured PR intent and affected components.
- Separates findings into clearly scoped categories.
- Ties each issue to a requirement or constraint.
- Assigns severity levels in a disciplined manner.
- Provides minimal, proportional fixes rather than broad redesign.
- Distinguishes between Major vs Minor vs Question findings.
- Ends with a merge decision grounded in identified gaps.
- Synthesizes prior B1–B3 concerns without duplicating analysis.

### Why This Is Better

- The review is clearly PR-aligned rather than generic.
- Findings are organized by constraint impact.
- Severity classifications feel more deliberate.
- It demonstrates merge-readiness thinking (what must change before merge vs what can wait).
- It shows boundary discipline: no architectural redesign drift.
- It resembles how senior reviewers evaluate production PRs before approval.

---

## Overall Comparative Insight

Across this task:

- The unguided output identified relevant issues but lacked strong synthesis and constraint anchoring.
- The guided output demonstrated improved prioritization, structure, and PR-scope awareness.
- The guided version better distinguished between:
  - Critical constraint violations,
  - Test coverage gaps,
  - Documentation/maintainability concerns.
- The merge decision in the guided output is more clearly justified by Major findings.

This task highlights that structured prompting improves:
- Constraint alignment,
- Severity calibration,
- Merge decision clarity,
- And production-level review framing.

However, both versions remain technically competent — the improvement is primarily in rigor and discipline rather than raw correctness.