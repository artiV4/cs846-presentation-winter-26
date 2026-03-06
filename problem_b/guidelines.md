# Guideline 4: Use a Structured, Context-First Review Prompt [Task B4]

## Description

When prompting an LLM for code review, first have it produce a structured summary of the pull request (intent, affected components, and high-risk areas). Then, give explicitly scoped review criteria (for example, correctness, security, and performance) as clear bullet-point instructions.

## Reasoning

Effective LLM-assisted code review requires context understanding before issue detection. Developers preferred AI-led summaries first to reduce cognitive load and improve contextual understanding before diving into findings [3]. Jumping straight to issue detection without grounding the model in the PR's intent produces unfocused, noisy feedback — which increases PR closure time and reduces reviewer trust over time [7]. Structuring the prompt itself with headings and bullet points further improves consistency and reduces ambiguity in LLM outputs.

Together, these findings converge on the same principle: the model needs to understand the change before it can review it well, and the prompt structure is what enforces that order.

## Examples

### Good Example

```
Ask the LLM to summarize the PR's intent first and identify high-risk areas, then instruct it to review only for a specific, named set of concerns.
```

### Bad Example

```
Review this pull request and suggest improvements.
```

----

# Guideline 5: Require Evidence-Grounded Justification Before Accepting LLM Claims [Task B2 and B3]

## Description

When prompting an LLM to evaluate tests or validate a reviewer comment, explicitly instruct it to cite specific line numbers, function names, or test cases as evidence before reaching a conclusion. Do not accept a finding unless the model can point to the exact code that supports it.

## Reasoning

LLMs reviewing code tend to produce confident-sounding but loosely grounded outputs, asserting that a test is missing or a security risk exists without pointing to the specific code that demonstrates it. Empirical studies on code review workflows show that developers only act on and trust LLM feedback when it is tied to concrete code artifacts rather than general observations [3]. Practitioner guidance on writing effective LLM instructions similarly emphasizes requiring the model to cite locations as a key technique for improving precision and reducing hallucinated architectural criticism.

Requiring evidence-grounded justification addresses all of these failure modes in a single instruction: it forces the model to anchor every claim in the actual diff before surfacing it.

## Examples

### Good Example

```
For each finding, you must:
1. Quote the specific line(s) of code that support your claim.
2. Explain the failure path using only those lines.
3. If you cannot point to a specific line, do not include the finding.
```

### Bad Example

```
Review the tests and identify what's missing.
```

----

# Guideline 6: Explicitly State Assumptions and Non-Goals [Task B1]

## Description

When prompting an LLM for code review, explicitly state what assumptions the model should make and what it should **not** evaluate. Clarify system boundaries, trust model, and review scope exclusions to prevent overreach and hallucinated concerns.

---

### Reasoning

Even when given context, LLMs may:

- Assume missing system components  
- Critique hypothetical architectures  
- Suggest redesigns outside the PR scope  
- Flag issues that are handled elsewhere in the system  

By explicitly stating assumptions and non-goals, you:

- Prevent hallucinated architectural criticism  
- Reduce overreach beyond PR scope  
- Keep feedback aligned with the actual change  
- Improve precision in real-world reviews  

This complements the structured, context-first guideline:

- **Structured, context-first guideline** → Controls *how* the review is structured  
- **This guideline** → Controls *what boundaries* the model must respect  

---

### Good Example

```text
Explicitly list the assumptions about what the system handles outside this PR (e.g., auth, validation), and state what the model should not do (e.g., suggest redesigns, flag out-of-scope modules). Then get a focused review of what's within the boundaries
```

### Bad Example

```text
Review this PR and suggest improvements.
```