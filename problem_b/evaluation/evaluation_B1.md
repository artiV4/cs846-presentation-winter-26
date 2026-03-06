# Evaluation – B1: Security and Data Exposure

## Evaluation Description

The review should:
- Identify security and trust-boundary risks scoped only to the code introduced in the diff.
- For each risk, include: the attack/failure path, the impacted endpoint or helper function with a line reference, and a concrete mitigation.
- Avoid flagging issues that are explicitly out of scope per the PR description (e.g., authentication handled upstream, architectural redesign).
- Not repeat general security advice unrelated to the specific code changes.

---

## Bad Example

### Prompt Used
```
Please solve this question for me: Review only security/trust-boundary risks: auth boundaries, sensitive data exposure, internal ID leakage, input handling, and URL/external-call safety. 
For each risk, include: attack/failure path, impacted endpoint/helper, and mitigation.
```

### Characteristics of Output
- Findings are listed without reference to specific line numbers or function names in the diff.
- Flags authentication gaps (e.g., missing token validation, role-based access control) even though the PR explicitly states authentication is handled upstream.
- Suggests adding tests for token expiry and privilege escalation — out of scope for a security review pass.
- Mitigations are generic (e.g., "ensure all endpoints consistently require and validate JWTs") rather than tied to the actual code.
- Summary repeats points already made in the findings without adding new insight.

### Why This Is Weak
The LLM was given no boundaries, so it hallucinated concerns about the surrounding system (auth, RBAC, token validation) that the PR explicitly says are out of scope. Without line references, none of the findings are immediately actionable, a reviewer would need to re-read the entire diff to locate the issue themselves.

---

## Good Example

### Prompt Used
```
I am reviewing a pull request. Below is the diff and PR description. [diff] [PR_description] Assumptions: - Authentication and input validation are handled upstream. - Only evaluate code introduced in this diff. Non-goals: - Do not flag out-of-scope items from the PR description. - Do not suggest architectural redesigns. Review only for security and trust-boundary risks: auth boundaries, sensitive data exposure, internal ID leakage, and URL/external-call safety. For each risk: state the attack/failure path, the impacted function (with line reference), and a mitigation.
```

### Characteristics of Output
- Each finding includes specific line numbers and function names (e.g., `get_user_list` lines 61–75, `lookup_by_email` lines 89–101).
- Authentication is acknowledged as enforced by FastAPI's dependency injection rather than flagged as a gap which is consistent with the PR's stated assumptions.
- External call safety finding is precise: correctly notes the base URL is fixed and trusted, and scopes the SSRF risk only to future changes.
- Mitigations are concrete and tied to the specific lines identified.
- Does not suggest architectural redesigns or out-of-scope changes.

### Why This Is Better
By stating assumptions and non-goals upfront, the LLM stayed within the actual scope of the PR. The findings are immediately actionable because each one is anchored to a specific location in the code. The output is shorter and more precise, a reviewer can act on it directly without filtering out noise.