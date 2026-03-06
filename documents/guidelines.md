# Week 10 Guidelines: CodeReview / PR

**Authors:** [Neel Sanjaybhai Faganiya, Ibrahim Mohammed Sayem, Felix Wang]

**Readings Assigned:**  
- Accountability in Code Review: The Role of Intrinsic Drivers and the Impact of LLMs [1]
- Prompting and Fine-tuning Large Language Models for Automated Code Review Comment Generation [2]
- Rethinking Code Review Workflows with LLM Assistance: An Empirical Study [3]
- The Impact of Large Language Models (LLMs) on Code Review Process [4]
- LLMs as Code Review Agents: A Rapid Review [5]
- Evaluating Large Language Models for Code Review [6]
- Automated Code Review In Practice [7]
- GitHub blog: Code review in the age of AI [8] 
- Unlocking the full power of Copilot code review: Master your instructions files [9]
- Using GitHub Copilot code review [10]
- uReview: Scalable, Trustworthy GenAI for Code Review at Uber [11] 
- Detecting malicious pull requests at scale with LLMs [12]

## Relevant Guidelines per Problem
| Question |          Guidelines               |
|----------|-----------------------------------|
| A.1 |  |
| A.2 |  |
| A.3 |  |
| B.1 | 6 |
| B.2 | 5 |
| B.3 | 5 |
| B.4 | 4 |
| C | 2.2 |
| D.1 | 1, 3 |
| D.2 | 1, 2.1, 2.3 | 

## 1. Guidelines

> **Note:** Guidelines should be actionable, specific, and usable during real coding tasks.

### Guideline 1: Create a structured instruction file [9].

**Description:**  

Add a Copilot Code Review instructions file that is concise, structured, and scoped to where it should apply:

* Use repo-wide `.github/copilot-instructions.md` for standards that apply everywhere.

* Use path-specific `.github/instructions/*.instructions.md` with applyTo frontmatter for language/module-specific rules. 

Your instruction file should be concise and structured, consider including sections like: "Naming Conventions", "Code Style", "Error Handling", "Testing", and "Example".

**Reasoning:**  
LLMs struggle with complex tasks that require extensive contextual or repository understanding [5], and due to the inherent undeterministic nature of LLMs, their outputs can drift in unexpected directions without clear constraints. Github Copilot recently added support for repo-wide and path-specific instructions [9] so that you can define a universal and customized guidelines for your Copilot agent to fit into your workflow. By providing structured headings and bullet points, it helps Copilot to access organized and focued instruction. However, long instruction files (over 1000 lines) should be avoided, as this leads to inconsistent behaviours and may cause "Lost in the middle" effect [16]. 

**Good Example:**  

```
---
applyTo: "**/*.ts"
---
# TypeScript Coding Standards
This file defines our TypeScript coding conventions for Copilot code review.

## Naming Conventions

- [Define your naming conventions here.]

## Code Style

- [Define your code style expectations here.]

## Error Handling

- [Define your error handling expectations here.]

## Testing

- [Define your testing expectations here. ]

## Example

```typescript
// Good
[One good example here]

// Bad
[One bad example here]
```

**Bad Example:**

```
Perform a Pull Request review.
```

---

### Guideline 2: Use Automated CI Gates [8]

#### Guideline 2.1: Continue Using Static Analysis Tools [11]

**Description:**

Integrate static analysis tools (e.g., linters, type checkers, security scanners) into your CI pipeline and configure them as mandatory checks before pull request merge. GitHub CI supports assorted static analysis tool integrations like CodeQL (primarily for security), Semgrep (pattern based bug finding with customized rules), and your ecosystem’s usual linters/type checkers (ESLint/tsc, pylint/mypy, etc.). 

**Reasoning:**

Unlike LLMs, most static analysis tools like Semgrep, CodeQL, etc. are deterministic and rule-based. They enforce predefined constraints across all changes, which can provide a consistent and systematic guarantee to your project. Depending on its proprietary, static analysis tools are generally capable of detecting: Syntax and type errors, Code style violations, Security vulnerabilities, Dead code or unreachable branches, and Complexity thresholds. However, this is not in conflict with LLM-assisted Code Review, as static analysis tools sometimes lack flexibility and may generate false alarms. These tools should be combined together. 

**Good Example:**

Customized static analysis patterns should neither be overly broad nor overly strict.

- If it's too broad, it may trigger too many false positives. 
- If it's too strict, it likely will not catch anything. 

A good static analysis pattern definition should find a balance in between, and match project-specific conventions and expectations. 

A static analysis tool pattern definition file template for Semgrep could be found in `.github/semgrep.yml`, please use the LLM to generate more suitable patterns and see the results if you want, or you can check the static analysis result using our template at [PR #11 -> Files Changed](https://github.com/U70-TK/cs846-presentation-winter-26/pull/11/changes).

**Bad Example:**

Static analysis patterns being too broad or too strict. 

#### Guideline 2.2: Use Automated Dependency Management Tools

**Description:**

Enable automated dependency monitoring and update mechanisms in your CI/CD workflow to continuously detect and remediate vulnerable or outdated third-party packages before merge.

**Reasoning:**

A large portion of modern security risk does not originate from first-party code, but from third-party dependencies [17]. Even if your internal code is perfectly written, a vulnerable library version can introduce critical vulnerabilities into production. Automated dependency management tools like Dependabot are continuously monitoring vulnerability databases and ensuring the packages used are free of known vulnerabilities, so as to mitigate software supply-chain attacks. 

**Good Example:**

In GitHub, fork the current repository (to make sure you have admin access), then go to:

Settings -> Security -> Advanced Security -> Dependabot -> Enable Dependabot Alerts -> Enable. 

Trigger a push on main branch, then go to: 

Security -> Vulnerability Alerts -> Dependabot. 

**Bad Example:**

```
You are an experienced coding agent, please verify the dependency versions for me: [path-to-file].
```

#### Guideline 2.3 Enforce Test Quality over Coverage [18]

**Description:**

Before approving a pull request, verify that automated tests are executed in CI and that the change is covered by meaningful tests. Ensure that the project’s minimum test coverage threshold is met, and dedicatedly review the tests themselves to confirm they validate real behavior rather than merely increasing coverage numbers.

**Reasoning:**

While static analysis and dependency scanning catch structural and known vulnerability issues, they do not validate runtime behavior. Tests provide behavioral guarantees and protect against regressions.

**Good Example:**

Ensure good testing principles like Blackbox testing, Whitebox testing, MC/DC testing, mutation test etc, in alignment with project-specific conventions and risk expectations. Establish a team-wide test coverage as a threshold. 

**Bad Example:**

Writing meaningless test cases to inflate high test coverage.

---

### Guideline 3: Be Extra Cautious about Binary Executables [13]
**Description:**  
Avoid committing binary executables (e.g., .exe, .dll, .jar, compiled artifacts, vendor-provided binaries) directly into the repository unless absolutely necessary. If inclusion is required, document their origin for accountability [1]. 

**Reasoning:**  

Previous studies have shown that many known CVE vulnerabilities are embedded within third-party components and precompiled binaries committed into repositories [13–15]. Unlike source code, binary artifacts cannot be meaningfully reviewed, diffed, or statically analyzed using standard development workflows. This creates a blind spot in both human review and automated tooling. However, opaqueness requirements do exist, and it also happens a lot in testing. Thus, binary files they must be treated as high-risk supply chain elements rather than normal source files.

**Good Example:**

Require the PR submitter to explicitly justify its inclusion. Explicitly document it for accountability. 

**Bad Example:**

Ignore it and merge it into the repo. 

---

### Guideline 4: Use a Structured, Context-First Review Prompt

**Description:**

When prompting an LLM for code review, first have it produce a structured summary of the pull request (intent, affected components, and high-risk areas). Then, give explicitly scoped review criteria (for example, correctness, security, and performance) as clear bullet-point instructions.

**Reasoning:**

Effective LLM-assisted code review requires context understanding before issue detection. Developers preferred AI-led summaries first to reduce cognitive load and improve contextual understanding before diving into findings [3]. Jumping straight to issue detection without grounding the model in the PR's intent produces unfocused, noisy feedback — which increases PR closure time and reduces reviewer trust over time [7]. Structuring the prompt itself with headings and bullet points further improves consistency and reduces ambiguity in LLM outputs.

Together, these findings converge on the same principle: the model needs to understand the change before it can review it well, and the prompt structure is what enforces that order.

**Examples:**

**Good Example:**

```
Ask the LLM to summarize the PR's intent first and identify high-risk areas, then instruct it to review only for a specific, named set of concerns.
```

**Bad Example:**

```
Review this pull request and suggest improvements.
```

----

### Guideline 5: Require Evidence-Grounded Justification Before Accepting LLM Claims
**Description:**

When prompting an LLM to evaluate tests or validate a reviewer comment, explicitly instruct it to cite specific line numbers, function names, or test cases as evidence before reaching a conclusion. Do not accept a finding unless the model can point to the exact code that supports it.

**Reasoning:**

LLMs reviewing code tend to produce confident-sounding but loosely grounded outputs, asserting that a test is missing or a security risk exists without pointing to the specific code that demonstrates it. Empirical studies on code review workflows show that developers only act on and trust LLM feedback when it is tied to concrete code artifacts rather than general observations [3]. Practitioner guidance on writing effective LLM instructions similarly emphasizes requiring the model to cite locations as a key technique for improving precision and reducing hallucinated architectural criticism.

Requiring evidence-grounded justification addresses all of these failure modes in a single instruction: it forces the model to anchor every claim in the actual diff before surfacing it.

**Examples:**

**Good Example:**

```
For each finding, you must:
1. Quote the specific line(s) of code that support your claim.
2. Explain the failure path using only those lines.
3. If you cannot point to a specific line, do not include the finding.
```

**Bad Example:**

```
Review the tests and identify what's missing.
```

----

### Guideline 6: Explicitly State Assumptions and Non-Goals

**Description:**

When prompting an LLM for code review, explicitly state what assumptions the model should make and what it should **not** evaluate. Clarify system boundaries, trust model, and review scope exclusions to prevent overreach and hallucinated concerns.

---

**Reasoning:**

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

**Examples:**

**Good Example:**

```text
Explicitly list the assumptions about what the system handles outside this PR (e.g., auth, validation), and state what the model should not do (e.g., suggest redesigns, flag out-of-scope modules). Then get a focused review of what's within the boundaries
```

**Bad Example:**

```text
Review this PR and suggest improvements.
```

---

### Guideline N: [Short, Actionable Title]
(Repeat the same structure for each guideline.)

---


## 2. References

[1] Alami, Adam, et al. ‘Accountability in Code Review: The Role of Intrinsic Drivers and the Impact of LLMs’. ACM Trans. Softw. Eng. Methodol., vol. 34, no. 8, Association for Computing Machinery, Oct. 2025, https://doi.org/10.1145/3721127.

[2] Haider, Md Asif, et al. "Prompting and fine-tuning large language models for automated code review comment generation." arXiv preprint arXiv:2411.10129 (2024).

[3] Aðalsteinsson, Fannar Steinn, et al. "Rethinking code review workflows with llm assistance: An empirical study." 2025 ACM/IEEE International Symposium on Empirical Software Engineering and Measurement (ESEM). IEEE, 2025.
[4] Collante, Antonio, et al. "The Impact of Large Language Models (LLMs) on Code Review Process." arXiv preprint arXiv:2508.11034 (2025).

[5] Kawalerowicz, Marcin, Marcin Pietranik, and Krzysztof Stępniak. "LLMs as Code Review Agents: A Rapid Review and Experimental Evaluation with Human Expert Judges." International Conference on Computational Collective Intelligence. Cham: Springer Nature Switzerland, 2025.

[6] Cihan, Umut, et al. "Evaluating Large Language Models for Code Review." arXiv preprint arXiv:2505.20206 (2025).

[7] Cihan, Umut, et al. "Automated code review in practice." 2025 IEEE/ACM 47th International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP). IEEE, 2025.

[8] Shwer, Elle, et al. “Code Review in the Age of AI: Why Developers Will Always Own the Merge Button.” The GitHub Blog, 14 July 2025, github.blog/ai-and-ml/generative-ai/code-review-in-the-age-of-ai-why-developers-will-always-own-the-merge-button.

[9] Gopu, Ria, et al. “Unlocking the Full Power of Copilot Code Review: Master Your Instructions Files.” The GitHub Blog, 15 Nov. 2025, github.blog/ai-and-ml/unlocking-the-full-power-of-copilot-code-review-master-your-instructions-files.

[10] “Using GitHub Copilot Code Review - GitHub Docs.” GitHub Docs, docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review.

[11] Mahajan, Sonal. “uReview: Scalable, Trustworthy GenAI for Code Review at Uber | Uber Blog.” Uber Blog, 3 Sept. 2025, www.uber.com/en-CA/blog/ureview.

[12] Qian, Callan Lamb Christoph Hamsen, Julien Doutre, Jason Foral, Kassen. “Detecting Malicious Pull Requests at Scale With LLMs | Datadog.” Datadog, 21 Oct. 2025, www.datadoghq.com/blog/engineering/malicious-pull-requests.


---
