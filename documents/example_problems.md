# Week 10 Example Problems: CodeReview / PR

**Authors:** [Neel Sanjaybhai Faganiya, Ibrahim Mohammed Sayem, Felix Wang]

**GitHub Repository:** https://github.com/U70-TK/cs846-presentation-winter-26

## 1. Example Problems

### Problem A_1: [Title]

**Task Description:**  
Describe the task clearly and precisely.

**Starter Code:**  
// Include all necessary starter code here or in a repo and share the link.

---

### Problem A_2: [Title]

**Task Description:**  
Describe the task clearly and precisely.

**Starter Code:**  
// Include all necessary starter code here or in a repo and share the link.

---

### Problem A_n: [Title]

**Task Description:**  
Describe the task clearly and precisely.

**Starter Code:**  
// Include all necessary starter code here or in a repo and share the link.

---

### Problem C: Pull Request Supply Chain Review

**Task Description:**  
Navigate to `problem_c/`. The `problem_c/before/` folder contains the dependency files `package.json` and `package-lock.json` before the pull request, and the `problem_c/after` folder contains the dependency files `package.json` and `package-lock.json` after the pull request. Please review from a software supply-chain perspective and verify that the update does not introduce supply-chain risk. 

Write your response in the form of a list of findings in bullet points. 

---

### Problem D: Northwind Signal Project PR Review

#### Problem D.1: Usage Audit Feature PR Review

**Task Description:**  
This change integrates a vendor-supplied audit component that is required by the internal usage audit workflow. The underlying audit logic is encapsulated and not exposed at the application layer, as it contains vendor-specific implementation details and compliance logic that should remain internal.

**Backend:**
- GET /api/usage/audit-log

Returns recent audit entries for internal monitoring purposes.

- POST /api/usage/audit

Creates a new audit entry using a vendor‑provided helper.

**Frontend:**
- Adds an “Audit log” panel to the dashboard displaying recent audit entries.
- Includes an action button that triggers the audit endpoint and refreshes the list.

**Starter Code:**  
The code containing the feature is on branch `feat-audit`, and the PR related to this task is #10. 


#### Problem D.2: 
---



## 2. References

[1]  
[2] 

---

