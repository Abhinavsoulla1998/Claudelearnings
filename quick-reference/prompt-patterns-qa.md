# Claude Code — Prompt Patterns for QA Engineers

A library of 30 field-tested prompts for common QA and quality engineering tasks. Each prompt includes placeholders in CAPS for you to fill in. Copy, adapt, and use directly in Claude Code sessions.

---

## 1. Test Writing

**Unit Tests**
```
Write unit tests for [FUNCTION_OR_CLASS] in [FILE_PATH]. Cover: (1) the happy path with representative inputs, (2) boundary values (empty, zero, maximum, minimum), (3) invalid inputs that should throw or return an error, and (4) any documented edge cases mentioned in comments. Use [TEST_FRAMEWORK] and follow the patterns in [EXISTING_TEST_FILE_PATH]. Do not test implementation details — test observable behavior only.
```
> Use when: adding test coverage to a function that currently has none.

**Integration Tests**
```
Write integration tests for the [FEATURE_OR_MODULE] flow. The test should: start with [INITIAL_STATE], perform [SEQUENCE_OF_ACTIONS], and verify [EXPECTED_FINAL_STATE]. Use real dependencies (database, external service mocks as appropriate). Use [TEST_FRAMEWORK] and place the tests in [TEST_FILE_PATH].
```
> Use when: testing a multi-step flow involving multiple components or services.

**End-to-End with Playwright**
```
Write a Playwright test for the [USER_FLOW] scenario. The test should: (1) navigate to [START_URL], (2) [DESCRIBE EACH STEP — click, fill, assert], and (3) assert [FINAL_STATE]. Use the page object model if one exists in [TEST_DIR]. Handle potential timing issues with appropriate waits. The test should work against [ENVIRONMENT — local/staging].
```
> Use when: automating a critical user journey in the browser.

**API Contract Tests**
```
Write contract tests for the [ENDPOINT_PATH] endpoint. Verify: (1) the response schema matches [SCHEMA_DEFINITION or DESCRIBE EXPECTED SCHEMA], (2) required fields are always present, (3) field types are correct, (4) optional fields have the correct type when present. Use [TEST_FRAMEWORK]. These tests should fail if the API response changes in a breaking way.
```
> Use when: protecting against unintended API schema changes.

**Test Data Generation**
```
Generate a set of test data fixtures for [ENTITY_TYPE]. Include: (1) a valid base case, (2) boundary cases for [LIST_FIELDS — e.g., "name at max length", "age at 0"], (3) invalid cases that should fail validation (one per validation rule), and (4) [N] randomized valid examples for load/fuzz testing. Output as [JSON/TypeScript/Python] in a format compatible with [TEST_FRAMEWORK].
```
> Use when: you need structured test data for a new feature or entity.

**Find Missing Coverage**
```
Analyze the test file at [TEST_FILE_PATH] against the implementation at [IMPLEMENTATION_FILE_PATH]. Identify: (1) functions or branches in the implementation that have no corresponding test, (2) error paths that are tested in the implementation but not exercised in tests, and (3) any conditions that appear in the code but are untested. Do not generate the tests yet — just report the gaps.
```
> Use when: doing a coverage audit before a release.

---

## 2. Test Analysis

**Analyze Test Failures**
```
The following tests are failing:

[PASTE TEST OUTPUT / ERROR MESSAGES]

For each failure: (1) identify the root cause (code bug, test bug, environment issue, or flaky timing), (2) determine whether the failure is in the production code or in the test itself, and (3) recommend the appropriate fix. Do not make changes yet — explain the failures first.
```
> Use when: triaging a set of failing tests to understand what broke and why.

**Flaky Test Detection**
```
Analyze [TEST_FILE_PATH or TEST_SUITE_NAME] for potential sources of flakiness. Look for: tests with no fixed seed for random data, tests that depend on timing (sleeps, timeouts), tests that share mutable state, tests that depend on external services without mocks, tests that depend on the order of execution, and tests with hardcoded timestamps or dates. List each potential source of flakiness with a recommended fix.
```
> Use when: investigating intermittent CI failures.

**CI Pipeline Failure**
```
The CI pipeline failed on the [BRANCH_NAME] branch. Here is the relevant output:

[PASTE CI LOG]

Diagnose: (1) what step failed, (2) whether this is a real failure (code broken) or an infrastructure issue (timeout, network, flaky environment), and (3) what the fix is. If it is a real failure, identify which commit introduced it.
```
> Use when: debugging a CI failure you cannot reproduce locally.

**Regression Identification**
```
Compare the test results from [PREVIOUS_RUN / COMMIT / BRANCH] with the current results:

Before: [PASTE PREVIOUS RESULTS]
After: [PASTE CURRENT RESULTS]

Identify: (1) tests that were passing before and are now failing (regressions), (2) tests that were failing before and are now passing (fixes), and (3) any new test failures that did not exist before. For each regression, suggest what code change might have caused it.
```
> Use when: comparing test results across releases or pull requests.

**Performance Test Analysis**
```
Analyze these performance test results:

[PASTE RESULTS — latency percentiles, throughput numbers, error rates]

Against these baselines:

[PASTE BASELINES]

Identify: (1) which metrics have degraded beyond acceptable thresholds (define threshold as 10% degradation unless specified), (2) which metrics have improved, and (3) any anomalies (unexpected spikes, bimodal distributions). Recommend whether this build should be considered production-ready from a performance standpoint.
```
> Use when: reviewing load test or benchmark results before a release.

---

## 3. Security and Quality

**OWASP Top 10 Review**
```
Review [FILE_PATH or FEATURE_AREA] against the OWASP Top 10. For each applicable category (injection, broken auth, sensitive data exposure, XXE, broken access control, security misconfiguration, XSS, insecure deserialization, known vulnerable components, insufficient logging), check whether the code is at risk and describe the specific vulnerability if found. Provide a remediation recommendation for each finding.
```
> Use when: doing a pre-release security review of a feature involving user input, auth, or data.

**Dependency Vulnerability Audit**
```
Run `npm audit` (or `pip-audit` / `bundle audit` / appropriate tool) and analyze the output. For each vulnerability: (1) assess the actual exploitability in this codebase (is the vulnerable code path reachable?), (2) determine whether a non-breaking upgrade is available, (3) prioritize critical and high severity issues. Produce a prioritized remediation plan.
```
> Use when: doing a scheduled dependency health check or responding to a Dependabot alert.

**Auth Flow Review**
```
Review the authentication and authorization flow in [FILE_PATH or DESCRIBE AREA]. Check: (1) tokens or sessions are invalidated on logout, (2) password reset flows cannot be abused (token expiry, single use), (3) privilege escalation paths do not exist (user can only access resources they own), (4) brute force protections are in place, (5) auth errors do not leak information about valid usernames. Report findings with severity.
```
> Use when: security-reviewing a login, registration, or access control implementation.

**Input Validation Audit**
```
Audit all places in [FILE_PATH or ROUTE_HANDLER] where external input is accepted (request body, query params, headers, file uploads). For each input: (1) verify it is validated before use, (2) check the validation is done on the server side (not just client side), (3) identify any field that is used in a SQL query, shell command, or file path without sanitization. Report each unvalidated or unsafe input.
```
> Use when: reviewing new endpoints or endpoints that handle user-submitted data.

**Secret Scan**
```
Scan the current git diff (or the entire codebase at [PATH]) for accidentally committed secrets. Look for: API keys, tokens, passwords, connection strings, private keys (PEM format), AWS access key patterns (AKIA...), and any string that looks like a randomly generated credential. Check both code files and config files. Report each finding with the file path and line number.
```
> Use when: before opening a PR or as part of a pre-commit check.

---

## 4. CI/CD Automation

**Quality Gate**
```
Implement a quality gate check for the CI pipeline. The gate should: (1) run `[TEST_COMMAND]` and fail if any tests fail, (2) run `[LINT_COMMAND]` and fail if there are lint errors, (3) check test coverage is above [COVERAGE_THRESHOLD]%, and (4) run `[TYPE_CHECK_COMMAND]` and fail if there are type errors. Write this as a shell script that exits 0 on pass and 1 on failure, with clear output for each check.
```
> Use when: adding or improving CI quality gates.

**Test Suite Summary**
```
Run the full test suite (`[TEST_COMMAND]`) and produce a structured summary including: total tests, pass count, fail count, skip count, total duration, slowest 5 tests by duration, and any tests that failed with the failure message. Format the output as a table followed by a plain English sentence suitable for a Slack message.
```
> Use when: generating a test report for a team or stakeholder update.

**Release Readiness Check**
```
Perform a release readiness check for the [VERSION] release. Check: (1) all tests pass on the main branch, (2) no open critical or high severity bugs in [ISSUE_TRACKER_LINK or DESCRIBE], (3) CHANGELOG.md has been updated, (4) version number has been bumped in [PACKAGE_JSON or VERSION_FILE], (5) no TODO comments referencing this release remain in the code. Report pass/fail for each check with details.
```
> Use when: running a pre-release checklist.

**Load Test Script**
```
Write a load test script using [TOOL — k6, Locust, or Artillery] that: (1) simulates [N] concurrent users, (2) runs for [DURATION] minutes, (3) exercises the [ENDPOINT_LIST] endpoints with realistic request distributions, (4) includes ramp-up and ramp-down phases, and (5) fails the test if p95 latency exceeds [LATENCY_THRESHOLD]ms or error rate exceeds [ERROR_THRESHOLD]%. Use realistic test data from [DATA_SOURCE or describe].
```
> Use when: setting up load testing for a new feature or endpoint.

**Automated Release Notes**
```
Generate release notes for the [VERSION] release from the git history since the last tag. Format as:
## What's New
[bullet points for user-facing additions]

## Fixes
[bullet points for bug fixes]

## Under the Hood
[bullet points for internal improvements the user should be aware of]

Use plain language suitable for non-technical stakeholders. Omit internal refactors, test changes, and dependency bumps unless they affect users.
```
> Use when: preparing release notes for a product release or changelog update.

---

## 5. Bug Reporting

**Structured Bug Report**
```
I found a bug. Help me write a structured bug report. Here is what I know:

What I did: [DESCRIBE STEPS]
What I expected: [EXPECTED BEHAVIOR]
What happened: [ACTUAL BEHAVIOR]
Environment: [OS, browser/runtime version, app version]

Fill in any gaps by asking me questions, then produce a bug report with: title, severity, reproduction steps, expected result, actual result, environment, and any relevant logs or screenshots I should attach.
```
> Use when: creating a high-quality, actionable bug report.

**Reproduction Script**
```
Write a minimal reproduction script for the following bug: [DESCRIBE BUG]. The script should: (1) set up the minimum required state, (2) trigger the bug, (3) assert that the bug condition is true, and (4) be runnable with [COMMAND]. The script should be a failing test that passes once the bug is fixed.
```
> Use when: creating a reproducible test case to accompany a bug report.

**Impact Analysis**
```
Analyze the impact of the bug described as: [DESCRIBE BUG]. Determine: (1) which users or user segments are affected (all users, users with a specific configuration, users who performed a specific action), (2) the severity of the impact (data loss, incorrect behavior, UI glitch, performance degradation), (3) whether there is a workaround users can take right now, and (4) the priority for fixing (critical, high, medium, low) based on impact and workaround availability.
```
> Use when: triaging a newly discovered bug to determine response priority.

**Compare Environments**
```
The following behavior difference exists between [ENVIRONMENT_A] and [ENVIRONMENT_B]:

In [ENVIRONMENT_A]: [DESCRIBE BEHAVIOR]
In [ENVIRONMENT_B]: [DESCRIBE BEHAVIOR]

Help me identify potential causes. Check: (1) environment variables that differ between environments, (2) dependency versions that might differ, (3) configuration files that differ, (4) data differences that could explain the behavior, and (5) infrastructure differences (database version, cache configuration, network topology).
```
> Use when: debugging a "works on my machine" or "works in staging but not production" issue.

---

## 6. Exploratory Testing

**Test Plan**
```
Create a test plan for [FEATURE_NAME]. The feature does the following: [DESCRIBE FEATURE]. The test plan should cover: (1) functional test cases (happy path, alternate flows), (2) negative test cases (invalid inputs, error states), (3) boundary conditions, (4) integration points with other features, (5) performance considerations, and (6) security considerations. Format as a checklist.
```
> Use when: planning testing for a new feature before it ships.

**Boundary Analysis**
```
Perform boundary value analysis for [FUNCTION_OR_INPUT_FIELD]. The field accepts: [DESCRIBE TYPE AND CONSTRAINTS — e.g., "an integer between 1 and 100", "a string of max 255 characters"]. List all boundary values that should be tested (minimum valid, maximum valid, just below minimum, just above maximum, empty, null if applicable). For each boundary value, state the expected result.
```
> Use when: designing thorough test cases for inputs with defined constraints.

**UI Smoke Test via Puppeteer MCP**
```
Using the browser automation tools available, run a smoke test of [APP_URL]. Test these critical paths: (1) the page loads without errors, (2) [KEY_ELEMENT] is visible and interactive, (3) [CORE_USER_ACTION — e.g., "a user can log in with test credentials"], (4) [SECONDARY_USER_ACTION]. Report any failures with a screenshot if possible. This is a smoke test — stop at the first critical failure.
```
> Use when: verifying a deployment is healthy for critical user flows.

**API Exploratory Testing**
```
Perform exploratory testing on the [ENDPOINT_PATH] endpoint. Try: (1) the documented happy path, (2) missing required fields (one at a time), (3) unexpected field types (string where int expected, null where string expected), (4) extremely long strings (10,000+ characters), (5) special characters in string fields (single quotes, angle brackets, null bytes, Unicode), (6) concurrent duplicate requests. Report any unexpected responses, errors, or inconsistencies.
```
> Use when: exploring the robustness of a new or changed API endpoint.

**Acceptance Criteria to Test Cases**
```
Convert the following acceptance criteria into specific, runnable test cases:

[PASTE ACCEPTANCE CRITERIA — e.g., from a JIRA ticket or user story]

For each acceptance criterion, produce: (1) a test case name, (2) preconditions, (3) test steps, (4) expected result, and (5) a classification (automated / manual). Flag any criteria that are ambiguous or not testable as written.
```
> Use when: translating user stories or tickets into a structured test plan.

---

## Constraint Modifiers

Append these to any QA prompt to scope Claude's behavior:

- `Do not modify production code — only add or modify test files.`
- `Use only the testing libraries already installed in this project.`
- `After writing the tests, run them and show me the output.`
- `Write tests that can run without a network connection (mock all external calls).`
- `Flag any test that is inherently slow (>500ms) with a comment explaining why.`
- `Write tests that are deterministic — no random data without a fixed seed.`
- `Do not add test utilities or fixtures that do not already exist; use what is available.`
