# Evaluation – B4: Correctness and Constraint Fit

## Evaluation Description

The review should:
- Begin with a structured context summary: PR intent, affected components, and high-risk areas.
- List findings with severity (`Blocker`, `Major`, `Minor`, `Question`), impacted file(s), violated requirement or constraint, and a minimal fix.
- Not repeat security or test findings already covered in B1 and B2.
- End with a justified merge decision (`Approve`, `Request Changes`, or `Reject`) based on the findings.

---

## Bad Example

### Prompt Used
```
Review functional correctness and PR-constraint alignment. List findings with severity 
(Blocker, Major, Minor, Question) and include: impacted file(s), violated requirement constraint, and minimal fix. End with a merge decision based on all prior considerations.
```

### Characteristics of Output
- Jumps directly into findings without first establishing what the PR is trying to do or which components are affected.
- Repeats findings from B1 (internal ID exposure) and B2 (missing edge case tests, brittle assertions) instead of focusing on new correctness and constraint-fit issues.
- Finding 5 ("Functional Correctness") is not a finding, it states no bugs were found and suggests a vague audit, which adds no actionable value.
- The merge decision ("Request Changes") is based largely on B1 and B2 findings rather than anything specific to correctness or constraint fit.
- No findings tied to specific files like `database.py` or `seed.py`, which are the most complex parts of this PR.

### Why This Is Weak
Without a context summary step, the LLM had no structured understanding of the PR before reviewing it. It defaulted to rehashing prior findings rather than identifying new correctness issues. The most technically complex parts of the diff, the database migration logic and seed normalization, were not examined at all.

---

## Good Example

### Prompt Used
```
I am reviewing a pull request. Below is the diff and PR description. [diff] [PR_description] Step 1 — Context summary: - Summarize the intent of this PR. - Identify the affected components. - Highlight any high-risk or complex areas. Step 2 — Focused review: Review only for functional correctness and PR-constraint alignment. For each finding include: - Severity (Blocker, Major, Minor, or Question) - Impacted file(s) - Violated requirement or constraint from the PR description - Minimal fix Do not repeat security or test findings from prior review passes. End with a merge decision: Approve, Request Changes, or Reject.
```

### Characteristics of Output
- Opens with a structured context summary that identifies affected components (including `database.py`, `seed.py`, `main.py`) and flags the migration logic and seed normalization as high-risk areas before any findings are listed.
- Findings are scoped to new correctness issues not covered in B1/B2: the `created_at` migration default being set to an empty string instead of `CURRENT_TIMESTAMP`, and the missing fallback in `_normalize_user` when both `name` and `full_name` are absent.
- Does not re-raise security or test concerns from earlier passes.
- Merge decision ("Request Changes") is justified specifically by the two correctness findings, making it easy to trace back to the evidence.

### Why This Is Better
The context summary forced the LLM to read and understand the full scope of the PR before issuing findings. This is what surfaced the `database.py` migration bug and the seed normalization gap, both of which require understanding what the PR intends before you can identify where it falls short. The naive prompt skipped this step entirely and missed the most technically substantive issues in the diff.