# Prompt Patterns for Daily Development Work

Copy, paste, and fill in the [PLACEHOLDERS]. These are starting points — adjust for your stack.

---

### Exploring Code

**Trace a Request Through the Stack**
```
Walk me through how a [REQUEST_TYPE] request to [ENDPOINT_OR_ENTRY_POINT] flows through this codebase,
tracing from the HTTP entry point to the database query.
Show the file path and function name at each step.
```
> Use when: you are new to a codebase and need to understand how a specific feature is wired together end to end.

**Understand a Module**
```
Explain what [FILE_OR_MODULE_PATH] does.
Describe: its purpose, its public interface, what it depends on, and what depends on it.
Do not summarize the code line by line — explain the intent.
```
> Use when: you need a mental model of a module before editing it or writing tests for it.

**Find All Usages of a Symbol**
```
Find every place in the codebase where [FUNCTION_NAME / CLASS_NAME / CONSTANT_NAME] is used.
For each usage, show: file path, line number, and a one-line description of what that call site does.
```
> Use when: you need to understand the blast radius before renaming, changing a signature, or deleting something.

**Architecture Overview**
```
Give me a high-level architecture overview of this codebase.
Cover: directory structure, main layers (e.g., API, service, data), key dependencies, and entry points.
Limit the response to [N] paragraphs and focus on what a new developer needs to know first.
```
> Use when: onboarding to a new project or preparing to explain the codebase to a new team member.

---

### Debugging

**Fix from an Error Message**
```
Fix this error:
[PASTE FULL ERROR MESSAGE AND STACK TRACE HERE]

The error occurs in [FILE_PATH] at line [LINE_NUMBER].
Do not change any files outside of [FILE_PATH] unless the root cause is definitively in another file.
After the fix, explain what caused the error.
```
> Use when: you have a stack trace and want a targeted fix without broad refactoring.

**Trace a Bug Through the Stack**
```
I expected [EXPECTED_BEHAVIOR] but got [ACTUAL_BEHAVIOR].
The relevant entry point is [FUNCTION_OR_ENDPOINT].
Trace through the code from that entry point and identify where the behavior diverges from my expectation.
```
> Use when: you know the symptom but not the location of the bug.

**Explain Unexpected Behavior**
```
This code in [FILE_PATH] between lines [START_LINE] and [END_LINE] is producing [UNEXPECTED_OUTPUT].
I expected [EXPECTED_OUTPUT].
Explain why the current code produces the unexpected output, then propose the minimal fix.
```
> Use when: you have isolated the problem to a specific block but cannot figure out why it misbehaves.

**Debug Async or Timing Issues**
```
I have an intermittent bug that may be a race condition or timing issue in [FILE_PATH].
The symptom is [SYMPTOM_DESCRIPTION].
Analyze the async code in that file and identify any patterns that could cause non-deterministic behavior.
List each suspect pattern and explain why it could cause the symptom.
```
> Use when: a bug only appears sometimes and you suspect async ordering, promise handling, or event timing.

**After-Fix Verification**
```
The fix for [BUG_DESCRIPTION] was applied in [FILE_PATH].
Run [TEST_COMMAND] and show me the full output.
If any tests still fail, explain whether they are related to this fix or pre-existing failures.
```
> Use when: you want Claude to confirm a fix works rather than just proposing code.

---

### Writing Code

**Add a Feature**
```
Add [FEATURE_DESCRIPTION] to [FILE_OR_MODULE_PATH].
Requirements:
- [REQUIREMENT_1]
- [REQUIREMENT_2]
- [REQUIREMENT_3]
Do not modify [FILES_TO_EXCLUDE].
Do not change the existing public API unless a requirement explicitly calls for it.
```
> Use when: implementing a well-defined feature with known requirements.

**New API Endpoint**
```
Add a [HTTP_METHOD] endpoint at [ROUTE_PATH] to [FILE_PATH].
It should [DESCRIBE_WHAT_IT_DOES].
Input validation: [VALIDATION_RULES or "use existing validation patterns in this file"].
Error responses: follow the pattern used by existing endpoints in this file.
Do not add a new middleware file — use the existing middleware stack.
```
> Use when: adding a route to an existing API, following established patterns in the codebase.

**Database Query**
```
Write a [ORM_OR_QUERY_LIBRARY] query in [FILE_PATH] that [DESCRIBE_WHAT_THE_QUERY_DOES].
The relevant table(s) are: [TABLE_NAMES].
The result should be: [DESCRIBE_RESULT_SHAPE].
Handle the case where no rows are found by [RETURNING_NULL / THROWING_ERROR / RETURNING_EMPTY_ARRAY].
```
> Use when: adding a new data access method to a repository or service layer.

**Add Input Validation**
```
Add input validation to [FUNCTION_OR_ENDPOINT] in [FILE_PATH] using [VALIDATION_LIBRARY, e.g., Zod, Joi, Pydantic].
Validate: [LIST_FIELDS_AND_CONSTRAINTS].
On validation failure, return [ERROR_FORMAT, e.g., HTTP 400 with a JSON error body].
Do not change the function's behavior for valid inputs.
```
> Use when: hardening an endpoint or function against bad input before merging or deploying.

**Implement from a Spec**
```
Implement the following spec in [FILE_PATH]:

[PASTE SPEC, TICKET, OR ACCEPTANCE CRITERIA HERE]

Use the patterns and libraries already present in this codebase.
Do not introduce new dependencies unless the spec requires something that cannot be done with existing libraries.
```
> Use when: you have a written spec, ticket, or acceptance criteria and want Claude to produce an initial implementation.

---

### Refactoring

**Extract a Function**
```
In [FILE_PATH], the block of code between lines [START_LINE] and [END_LINE] should be extracted into a separate function named [FUNCTION_NAME].
Move it to [SAME_FILE / NEW_FILE_PATH].
Update all call sites.
Do not change behavior — this is a pure structural refactor.
```
> Use when: a function is too long or a block of logic is duplicated and needs to be named and reused.

**Replace a Library**
```
Replace all usage of [OLD_LIBRARY] with [NEW_LIBRARY] in [FILE_PATH or "the entire codebase"].
The equivalent API mapping is:
- [OLD_API_1] -> [NEW_API_1]
- [OLD_API_2] -> [NEW_API_2]
Keep behavior identical. After replacing, run [TEST_COMMAND] to confirm nothing broke.
Remove [OLD_LIBRARY] from package.json once all usages are replaced.
```
> Use when: migrating from a deprecated or replaced dependency.

**Remove Duplication**
```
The following code pattern appears in multiple places in [FILE_OR_DIRECTORY]:
[DESCRIBE_OR_PASTE_THE_DUPLICATED_PATTERN]
Consolidate it into a shared [function / class / utility] at [TARGET_FILE_PATH].
Update all call sites to use the shared version.
Do not change the behavior at any call site.
```
> Use when: you have spotted a copy-paste pattern across files and want to DRY it up.

**Modernize Syntax**
```
Modernize the JavaScript/TypeScript in [FILE_PATH] to use [TARGET_SYNTAX, e.g., ES2022, async/await, optional chaining].
Do not change behavior.
Specifically:
- Replace [OLD_PATTERN_1] with [NEW_PATTERN_1]
- Replace [OLD_PATTERN_2] with [NEW_PATTERN_2]
Run [TEST_COMMAND] after to confirm nothing regressed.
```
> Use when: updating legacy code to match current language standards or team conventions.

---

### Code Review

**Structured Review**
```
Review [FILE_PATH] for the following categories:
1. Security vulnerabilities
2. Performance issues
3. Error handling gaps
4. Code clarity and maintainability
5. Adherence to conventions in CLAUDE.md

For each finding, output exactly:
[CATEGORY] [SEVERITY: high/medium/low] [LINE_NUMBER] [DESCRIPTION] [SUGGESTED_FIX]

If there are no findings in a category, say "No findings."
```
> Use when: doing a pre-merge review and you want structured, actionable output rather than prose.

**Pre-Merge Checklist**
```
Before I merge the changes in [FILE_PATH or "this branch"], confirm the following:
1. All new functions have error handling
2. No hardcoded credentials, secrets, or environment-specific values
3. No commented-out code blocks
4. All new public functions have at least a one-line doc comment
5. No obvious N+1 query patterns

Report each item as: [PASS / FAIL / NOT_APPLICABLE] — [brief reason]
```
> Use when: running a final pre-merge sanity check, especially on AI-generated code.

**Security Review**
```
Review [FILE_PATH] specifically for security vulnerabilities.
Focus on:
- Injection vulnerabilities (SQL, command, path traversal)
- Authentication and authorization gaps
- Insecure handling of user input
- Exposure of sensitive data in logs or responses
- Insecure use of cryptography or tokens

For each finding: [VULNERABILITY_TYPE] [SEVERITY] [LINE_NUMBER] [DESCRIPTION] [REMEDIATION]
```
> Use when: reviewing code that handles authentication, user input, file access, or external data before merging.

**Simplification Pass**
```
Review [FILE_PATH] for unnecessary complexity.
Look for:
- Abstractions that add indirection without value
- Functions that could be simplified or inlined
- Redundant variables or intermediate values
- Overly defensive code that is never triggered

For each finding, show the current code and a simpler equivalent.
Do not change behavior.
```
> Use when: cleaning up after a large AI-assisted implementation session or reviewing code that has grown organically over time.

---

### Documentation & PRs

**PR Description**
```
Write a pull request description for the changes in this branch.
Structure it as:
- Summary: one paragraph describing what changed and why
- Motivation: why this change was necessary (link to issue if known: [ISSUE_NUMBER])
- Changes: a bulleted list of the main changes grouped by file or component
- Testing: how to verify the change works, including specific commands
- Breaking changes: list any, or state "None"

Be concise. Avoid repeating what is already obvious from the diff.
```
> Use when: creating a PR and you want a description that gives reviewers real context, not a list of file names.

**JSDoc Comments**
```
Add JSDoc comments to every exported function and class in [FILE_PATH].
For each function, document: purpose, all parameters (name, type, description), return value, and any thrown errors.
Use the JSDoc style already present in this file, or [SPECIFY_STYLE] if there are no existing examples.
Do not change any implementation code.
```
> Use when: adding documentation to a file before publishing it as a library or reviewing it with a new team.

**Changelog Entry**
```
Write a changelog entry for the changes in this branch following [KEEPACHANGELOG / CONVENTIONAL_COMMITS / OUR_CUSTOM_FORMAT] format.
The audience is [end users / other developers / both].
Changes to include:
- [CHANGE_1]
- [CHANGE_2]
Group entries under the appropriate headings: Added, Changed, Fixed, Removed, Security.
```
> Use when: maintaining a CHANGELOG.md and you want a consistent, readable entry without writing it from scratch.

**README Update**
```
Update [README_FILE_PATH] to reflect the following changes:
- [WHAT_CHANGED_1]
- [WHAT_CHANGED_2]

Keep the existing structure and tone.
Do not rewrite sections that are not affected by these changes.
Add [SECTION_NAME] after [EXISTING_SECTION] if it does not already exist.
```
> Use when: a new feature, configuration option, or breaking change needs to be reflected in the project README.
