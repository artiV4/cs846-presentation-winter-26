# Evaluation – B3: Peer Review Comment Validation

## Evaluation Description

The review should:
- Quote the specific lines from the code that are directly relevant to the claim being validated.
- Explain whether those lines support or contradict the claim based on how FastAPI's `Depends()` mechanism actually works — not based on general intuition.
- Reach a clear classification: `Accurate`, `Partially Accurate`, or `Inaccurate`.
- Provide a brief, grounded reasoning and a concrete recommended follow-up action.

---

## Bad Example

### Prompt Used
```
Use an LLM to validate the comment against the PR description, diff, and code in user_helpers.py. Classify it as Accurate, Partially Accurate, or Inaccurate, then provide brief reasoning and a recommended follow-up action.
```

### Characteristics of Output
- Reaches the correct classification (`Inaccurate`) but does not quote the specific lines from the code that support this verdict.
- Explanation relies on general knowledge of FastAPI rather than the actual lines in the diff.
- The reasoning contradicts itself — first saying the reviewer's claim is "inaccurate" in the reasoning, then classifying it as "Accurate" in the header, suggesting the LLM was not anchored to the code.
- Recommended follow-up is vague: "add tests for unauthenticated access" is generic advice not tied to the specific claim.

### Why This Is Weak
Without being instructed to ground the verdict in specific lines, the LLM reasoned from general FastAPI knowledge rather than the actual code. This produced a self-contradicting output — the classification and reasoning disagreed — which is exactly the failure mode the guideline is designed to prevent. A student relying on this output would be unsure whether to trust the verdict.

---

## Good Example

### Prompt Used
```
I am validating a peer review comment against a pull request. Here is the diff, PR description, and the relevant code. [diff] [PR_description] [location to user_helpers.py] The peer reviewer made the following claim: "Although each route declares Depends(auth.get_current_user), the returned value is assigned to _ and discarded, which means authentication is effectively not enforced." Before accepting or rejecting this claim: 1. Quote the exact line(s) from the code that are relevant to this claim. 2. Explain whether those lines support or contradict the claim, based only on how FastAPI's Depends() mechanism actually works. 3. If you cannot ground your verdict in specific lines, do not include the finding. Classify the comment as Accurate, Partially Accurate, or Inaccurate, then provide brief reasoning and a recommended follow-up action.
```

### Characteristics of Output
- Quotes all four relevant lines across the endpoints where `_: dict = Depends(auth.get_current_user)` appears before reaching a verdict.
- Explains the mechanism precisely: FastAPI executes the dependency regardless of whether the return value is used, so assigning to `_` does not bypass enforcement.
- Classification (`Inaccurate`) is consistent with the reasoning — no contradiction.
- Recommended follow-up is concrete and scoped: reject the claim, no code change needed, optionally clarify in comments.

### Why This Is Better
By requiring the LLM to quote the relevant lines before reaching a verdict, the output is self-consistent and immediately verifiable — a student can check the quoted lines themselves and confirm the reasoning. The naive output reached the same general conclusion but contradicted itself, making it untrustworthy. The guided output is actionable: a reviewer can reject the comment confidently and explain why with specific evidence.
Backend code review problem setup and feedback implementation - Claude