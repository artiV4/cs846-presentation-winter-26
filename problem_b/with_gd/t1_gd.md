You are reviewing this pull request for Problem B1: Security and Data Exposure.

**Step 1 — Context summary**
- **Intent:**
    - Introduces a new user helpers backend and API endpoints for user data (display, list, header, lookup).
    - Refactors database schema and seed logic to support richer user data and more robust testing.
    - Adds comprehensive backend and endpoint tests, improves test isolation, and updates dependencies.
- **Affected components:**
    - `user_helpers.py` (new backend module and router)
    - Database schema (`database.py`, `seed.py`)
    - API endpoints: `/users`, `/users/{user_id}/display`, `/users/{user_id}/header`, `/users/lookup`
    - Test infrastructure and fixtures
- **High-risk areas:**
    - Exposure of internal user IDs and roles via API responses
    - Authentication enforcement on new endpoints
    - Input validation for user lookup and list filtering
    - Use of external API calls (requests)

**Step 2 — Focused review: Security and Data Exposure**

Assumptions:
- Authentication is handled via FastAPI dependency (`auth.get_current_user`).
- Input validation for query parameters is managed by FastAPI and Pydantic.
- Database access is limited to the service boundary; no direct external exposure.
- External API base URL is trusted and set via environment variable.

Non-goals:
- Do not review architectural design or suggest new frameworks.
- Do not refactor unrelated modules or endpoints.
- Do not review for performance, correctness, or style unless it impacts security/data exposure.

Review only for:
- Security/trust-boundary risks
- Sensitive data exposure
- Internal ID leakage
- Input handling
- URL/external-call safety

---

### Security and Data Exposure Risks

**1. Internal ID Leakage**
- **Attack/failure path:** Internal user IDs are exposed in API responses (`/users`, `/users/lookup`, backend helpers) and may be used by attackers for enumeration or privilege escalation.
- **Impacted endpoints/helpers:**
    - `/users` (returns `id` for each user)
    - `/users/lookup` (returns `user_id`)
    - Backend helper `get_user_list` and `lookup_by_email` expose `id`
- **Mitigation:**
    - Consider returning opaque/public IDs or limiting exposure to trusted clients.
    - Document and restrict usage of internal IDs in frontend/UI contexts.
    - Ensure endpoints requiring IDs enforce authentication and authorization.

**2. Role Exposure and Privilege Disclosure**
- **Attack/failure path:** User roles are returned in `/users` and `/users/{user_id}/header`, potentially revealing privilege structure to unauthorized users.
- **Impacted endpoints/helpers:**
    - `/users` (role field)
    - `/users/{user_id}/header` (role in display string)
- **Mitigation:**
    - Ensure only authenticated users can access these endpoints (already enforced via dependency).
    - Consider role-based access control for listing roles or restricting role visibility to admins/support.

**3. Authentication Enforcement**
- **Attack/failure path:** Endpoints may be accessed without valid authentication, leaking user data.
- **Impacted endpoints/helpers:**
    - All new endpoints (`/users`, `/users/{user_id}/display`, `/users/{user_id}/header`, `/users/lookup`)
- **Mitigation:**
    - All endpoints use `Depends(auth.get_current_user)`, enforcing authentication.
    - Tests confirm 401 for unauthenticated requests; maintain coverage for future changes.

**4. Input Handling and Validation**
- **Attack/failure path:** Malformed or missing query parameters (e.g., email in `/users/lookup`) could cause errors or unintended data exposure.
- **Impacted endpoints/helpers:**
    - `/users/lookup` (missing or invalid email)
    - `/users` (role filter)
- **Mitigation:**
    - FastAPI and Pydantic enforce required parameters and types; 422 returned for missing/invalid input.
    - Continue to rely on framework validation and test for edge cases.

**5. URL/External Call Safety**
- **Attack/failure path:** Backend helpers make requests to external API URLs using user-supplied data (e.g., user ID, email), risking SSRF or data leakage if not properly sanitized.
- **Impacted helpers:**
    - `get_user_display`, `get_user_list`, `format_user_for_header`, `lookup_by_email` (all use `requests.get`)
- **Mitigation:**
    - API base URL is fixed and trusted; user input is only used in path/query parameters, not in the base URL.
    - Validate/sanitize user input before constructing URLs if base URL ever becomes user-configurable.
    - Monitor for future changes that could introduce SSRF or open redirects.

---

**Summary:**
- Internal IDs and roles are exposed in API responses; ensure exposure is intentional and access is authenticated.
- Authentication and input validation are enforced by FastAPI dependencies and Pydantic models.
- External API calls are currently safe due to fixed base URL, but future changes should be reviewed for SSRF risk.
- No evidence of direct sensitive data leakage beyond intended fields.
