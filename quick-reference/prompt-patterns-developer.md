# Claude Code — Prompt Patterns for Developers

A library of 30 field-tested prompts for common developer tasks. Each prompt includes placeholders in CAPS for you to fill in. Copy, adapt, and use directly in Claude Code sessions.

---

## 1. Codebase Exploration

**Trace a Request**
```
Trace the lifecycle of a [REQUEST_TYPE] request to [ENDPOINT_OR_FUNCTION] from the point it enters the system to the point a response is returned. Show the call chain, identify which files are involved at each step, and note any transformations the data undergoes.
```
> Use when: you are new to a codebase or debugging an unfamiliar flow.

**Understand a Module**
```
Explain the purpose and design of the [MODULE_NAME] module located at [PATH]. Describe what problem it solves, its public API (exported functions, classes, and types), its dependencies, and any non-obvious implementation decisions. Do not modify any files.
```
> Use when: you need to work with or alongside a module you have not read before.

**Find All Usages**
```
Find all places in the codebase where [FUNCTION_OR_CLASS_NAME] is called or imported. For each usage, note the file path, the line number, and the context in which it is used (what is being passed in, what the caller does with the return value). Summarize whether the usages are consistent with each other.
```
> Use when: before renaming, removing, or changing the signature of a function.

**Architecture Overview**
```
Give me an architectural overview of this codebase. Identify the major layers (e.g., API, service, data access), the key modules and their responsibilities, the flow of data from external requests to persistence, and any patterns or conventions the codebase consistently follows.
```
> Use when: onboarding to a new repo or preparing to explain the system to someone else.

**Dependency Map**
```
Analyze the dependencies of [FILE_OR_MODULE]. Show: (1) what it imports/requires, (2) what imports/requires it, (3) any circular dependencies, and (4) any unusually heavy or surprising dependencies. Suggest any obvious cleanups.
```
> Use when: planning a refactor or investigating a build size or load time issue.

---

## 2. Debugging

**Fix from Error Message**
```
I'm seeing this error:

[PASTE ERROR MESSAGE AND STACK TRACE]

The error occurs when [DESCRIBE WHAT YOU WERE DOING]. Investigate the root cause by reading the relevant code, identify the fix, apply it, and explain why the error was happening.
```
> Use when: you have an error message and want Claude to trace it to the source.

**Trace a Bug**
```
There is a bug in [FUNCTION_OR_FEATURE]: [DESCRIBE THE INCORRECT BEHAVIOR]. The expected behavior is [DESCRIBE CORRECT BEHAVIOR]. Trace through the relevant code to find where the behavior diverges from expectations, then fix it.
```
> Use when: you know what is wrong but not where or why.

**Explain Unexpected Behavior**
```
When I [DO ACTION], I expect [EXPECTED RESULT], but instead I get [ACTUAL RESULT]. I have not changed [LIST_OF_FILES_OR_AREAS]. Explain why this might be happening and what to check.
```
> Use when: you want an explanation before making any changes.

**Debug Async / Race Condition**
```
I suspect there is a race condition or async ordering issue in [COMPONENT_OR_FILE]. The symptom is [DESCRIBE SYMPTOM — intermittent failure, wrong ordering, stale data, etc.]. Read the relevant async code and identify where ordering assumptions might be violated. Suggest a fix.
```
> Use when: dealing with intermittent failures or async state bugs.

**After-Fix Verification**
```
I just fixed a bug in [FILE_OR_FUNCTION]. Before I commit, check: (1) does the fix actually address the root cause, (2) are there any edge cases the fix misses, (3) does the fix introduce any new issues, and (4) is there an existing test that would have caught this bug? If not, add one.
```
> Use when: you have written a fix and want a second pair of eyes before committing.

---

## 3. Code Generation

**Add a Feature**
```
Add [FEATURE_DESCRIPTION] to [FILE_OR_MODULE]. The feature should: [LIST REQUIREMENTS]. Follow the existing patterns and conventions in the file. Do not change any other files unless necessary. After adding the feature, run the tests for this module.
```
> Use when: adding a self-contained piece of functionality to an existing module.

**New API Endpoint**
```
Create a new [HTTP_METHOD] endpoint at [ROUTE_PATH] in [ROUTER_FILE]. The endpoint should: [DESCRIBE WHAT IT DOES]. It should [validate/not validate] the request body, [require/not require] authentication, and return [DESCRIBE RESPONSE FORMAT]. Follow the patterns used by existing endpoints in the file.
```
> Use when: adding a new route to an existing API.

**Database Query**
```
Write a [SQL/ORM_NAME] query that [DESCRIBE WHAT THE QUERY SHOULD DO]. The relevant tables are: [LIST TABLES AND KEY COLUMNS]. The query should be [efficient / paginated / transactional]. Return the query as a named function in [FILE_PATH], following the patterns in that file.
```
> Use when: adding a new database operation.

**Generate Types**
```
Read [FILE_OR_SCHEMA_PATH] and generate TypeScript types (or [LANGUAGE] equivalent) that accurately represent the data structures defined there. Include JSDoc comments on each field explaining what it represents. Place the types in [OUTPUT_FILE_PATH].
```
> Use when: you need type definitions derived from a schema, API spec, or existing runtime objects.

**Add Input Validation**
```
Add input validation to [FUNCTION_OR_ENDPOINT]. Validate: [LIST FIELDS AND THEIR CONSTRAINTS — e.g., "email must be a valid email address", "age must be a positive integer"]. Use [VALIDATION_LIBRARY] if it is already in use, otherwise use plain checks. Return a clear error message for each invalid field.
```
> Use when: hardening an endpoint or function that processes external input.

**Implement from Spec**
```
Implement the following specification:

[PASTE SPEC — could be a function signature, interface definition, ticket description, or acceptance criteria]

Read the surrounding code first to understand the context and conventions. Implement only what is specified. Do not add features not mentioned in the spec.
```
> Use when: you have a well-defined spec and want to translate it directly to code.

---

## 4. Refactoring

**Extract a Function**
```
The code block starting at [LINE_NUMBER_OR_DESCRIPTION] in [FILE_PATH] is doing too much. Extract [DESCRIBE_WHAT_TO_EXTRACT] into a separate function named [FUNCTION_NAME]. Place the new function [above the existing function / in a shared utils file at PATH]. Update the original code to call the new function. Run the tests after.
```
> Use when: a function has grown too large or contains logic used in multiple places.

**Replace a Library**
```
Replace all usages of [OLD_LIBRARY] with [NEW_LIBRARY]. Read the documentation for [NEW_LIBRARY] if needed using web fetch. Update imports, method calls, and any configuration. Do not change behavior — this is a like-for-like replacement. Run the test suite after completing the replacement.
```
> Use when: migrating from a deprecated or suboptimal dependency.

**Remove Duplication**
```
I notice [FUNCTION_A] in [FILE_A] and [FUNCTION_B] in [FILE_B] are doing similar things. Consolidate them into a single shared function that handles both use cases. Place the shared function in [SHARED_FILE_PATH]. Update both call sites to use the new shared function.
```
> Use when: you have identified code duplication you want to eliminate.

**Modernize Syntax**
```
Update [FILE_PATH] to use modern [LANGUAGE/FRAMEWORK] syntax and patterns. Specifically: [LIST WHAT TO MODERNIZE — e.g., "replace callbacks with async/await", "replace var with const/let", "use optional chaining instead of manual null checks"]. Do not change behavior. Run the tests after.
```
> Use when: paying down tech debt in a file you are already working in.

**Split a Large File**
```
[FILE_PATH] has grown too large and has mixed responsibilities. Analyze its contents and propose a split into [N] files with clearly separated concerns. Show me the proposed file structure and responsibility of each file before making any changes. Wait for my approval before proceeding.
```
> Use when: a file has grown beyond ~400 lines or has multiple unrelated responsibilities.

---

## 5. Code Review

**Structured Review**
```
Review the changes I have made (run git diff HEAD or git diff --staged). For each changed file, assess: (1) correctness — does the logic do what it claims to do, (2) edge cases — what inputs or states could cause incorrect behavior, (3) readability — is the code clear to a future reader, (4) test coverage — are the changes tested. Format your output as a list of findings with severity (critical / minor / suggestion).
```
> Use when: you want a thorough review before opening a PR.

**Pre-Merge Checklist**
```
Run through this checklist for the current branch changes (git diff main...HEAD):
1. No secrets or API keys in the diff.
2. All new public functions have documentation comments.
3. Test coverage exists for new logic.
4. No files in [OFF_LIMITS_DIRECTORIES] were modified.
5. The CHANGELOG has been updated if this is a user-facing change.
6. No TODO comments were introduced without a ticket reference.
Report pass/fail for each item.
```
> Use when: doing a final check before requesting review.

**Security-Focused Review**
```
Review the changes in git diff HEAD~1 (or the specified files [FILES]) specifically for security issues. Check for: SQL injection, XSS, CSRF, insecure deserialization, hardcoded secrets, overly permissive CORS, missing authentication on sensitive routes, unsafe use of eval or exec, and any use of deprecated security functions. For each finding, explain the risk and recommend a fix.
```
> Use when: the changes involve authentication, user input handling, or sensitive data.

**Simplify Pass**
```
Review [FILE_PATH] and identify code that is more complex than it needs to be. Look for: overly nested conditionals, functions that do too many things, unnecessary abstractions, dead code, and variable names that do not convey intent. Make the simplifications directly, keeping behavior identical. Run the tests after.
```
> Use when: a file works but is hard to read or maintain.

**Performance Review**
```
Review [FILE_PATH or FUNCTION_NAME] for performance issues. Look for: N+1 queries, missing indexes (describe the query patterns), unnecessary re-renders or re-computations, large allocations inside loops, missing caching for expensive operations, and synchronous operations that should be async. For each issue, estimate the impact and suggest a fix.
```
> Use when: you suspect a feature or endpoint is slower than it should be.

---

## 6. Documentation and PRs

**PR Description**
```
Generate a pull request description for the current branch changes (git diff main...HEAD). Format it as:
## Summary
[3-5 bullet points describing what changed and why]

## How to Test
[step-by-step instructions for a reviewer to verify the changes]

## Notes
[anything the reviewer should be aware of — trade-offs, known issues, follow-up work]

Keep the total length under 300 words.
```
> Use when: opening a PR and wanting a solid starting description.

**Add JSDoc / Docstrings**
```
Add [JSDoc / Python docstrings / Go doc comments] to all exported functions and types in [FILE_PATH] that are currently undocumented. Each comment should describe: what the function does, the parameters and their types, the return value, and any exceptions or errors it can throw. Do not change any logic.
```
> Use when: adding documentation to a file you are already modifying.

**Changelog Entry**
```
Generate a changelog entry for the changes on the current branch (git log main...HEAD --oneline). Use Keep a Changelog format with sections: Added, Changed, Fixed, Removed. Write each entry as a short imperative sentence. Today's date is [DATE].
```
> Use when: preparing a release or keeping CHANGELOG.md up to date.

**README Update**
```
Update the README.md to reflect: [DESCRIBE WHAT CHANGED — new feature, new configuration option, changed API, new installation step]. Keep the existing structure and tone. Do not remove existing sections unless they are now inaccurate. Mark any sections you are uncertain about with a [VERIFY] comment for me to review.
```
> Use when: a feature change requires corresponding documentation updates.

---

## Constraint Modifiers

Append these to any prompt to scope Claude's behavior:

- `Do not modify any files outside [FOLDER].`
- `Do not change the public API or any exported function signatures.`
- `After making changes, run [COMMAND] and show me the output.`
- `Make only the minimum change required. Do not refactor surrounding code.`
- `Do not add any new dependencies.`
- `Show me the changes as a unified diff before applying them.`
- `If you find issues beyond the scope of this request, list them as suggestions but do not fix them.`
