# Evaluation – B1: Code Review

## Evaluation Description

The review should:

- Stay scoped strictly to security and trust-boundary concerns.
- Identify internal identifier leakage and sensitive data exposure.
- Analyze authentication enforcement realistically.
- Evaluate input validation within stated assumptions.
- Assess URL construction and external-call safety without speculative redesign.
- Respect explicitly stated assumptions and non-goals.
- Avoid hallucinating missing functionality.
- Tie risks to specific endpoints/helpers and describe attack/failure paths.
- Provide mitigation strategies grounded in system context.

---

## Bad Example

### Characteristics of Output:

- Jumps directly into issue listing without structured context summary.
- Blends security concerns with general robustness and validation suggestions.
- Mentions test coverage gaps and token validation details not directly tied to the diff.
- Introduces speculative risks (e.g., privilege escalation) without clear boundary reasoning.
- Does not clearly separate in-scope risks from integration-level concerns.
- Lacks explicit assumptions about authentication and validation boundaries.
- Treats the system as a standalone artifact rather than a bounded PR change.

### Why This Is Weak

- The output is generally correct but not disciplined.
- It expands beyond the defined trust model and system boundaries.
- It does not clearly frame security analysis within the PR’s constraints.
- It partially evaluates imagined behavior rather than strictly reviewing the provided change.
- It risks reducing reviewer trust due to slight scope drift and speculative concerns.

While the issues identified are valid, the analysis lacks structured boundary control and precision.

---

## Good Example

### Prompt Used

The prompt included:

- A context-first structured summary requirement.
- Explicit scope limitation to security and data exposure only.
- Clearly stated assumptions (authentication handled upstream, validation via framework).
- Explicit non-goals (no architectural redesign, no unrelated refactoring).
- Instruction to review only trust-boundary, identifier leakage, and external-call safety concerns.

### Characteristics of the Output

- Begins with a structured summary of intent, affected components, and high-risk areas.
- Explicitly identifies internal ID exposure and ties it to specific endpoints.
- Analyzes role exposure as privilege disclosure risk in a scoped manner.
- Evaluates authentication enforcement based on actual dependency usage.
- Recognizes framework-based validation (FastAPI/Pydantic) rather than redundantly demanding manual validation.
- Assesses external API call construction within a defined trust boundary.
- Avoids hallucinating missing functions or unimplemented features.
- Distinguishes between real security risk and acceptable design under assumptions.
- Provides mitigation strategies aligned with the existing architecture.

### Why This Is Better

- The analysis is disciplined and boundary-aware.
- It aligns directly with the PR’s intent and constraints.
- It avoids overreach into architectural redesign.
- It reduces speculative or hypothetical attack modeling.
- It correctly respects authentication and validation assumptions.
- It resembles a production-level security review rather than a general vulnerability brainstorm.
- It demonstrates improved precision, structure, and trustworthiness.

---

## Overall Comparative Insight

The guided version improves:

- Scope discipline  
- Trust-boundary reasoning  
- Alignment with stated assumptions  
- Reduction of speculative concerns  
- Structural clarity  

The unguided version, while technically competent, demonstrates:

- Broader and less constrained reasoning  
- Partial scope drift  
- Slightly more speculative threat modeling  

This comparison shows that structured, context-first prompting with explicit assumptions significantly improves precision and boundary control in LLM-assisted security review tasks.