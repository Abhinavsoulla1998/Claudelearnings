# Level 3 — Daily Dev Workflows
> Audience: Developer, QA | Duration: Days 8–12 | Prerequisites: Level 2

## Overview
Learn the patterns you will use every day: exploring unfamiliar codebases, fixing bugs, writing tests, doing code reviews, and creating PRs. This level is about repeatable workflows, not one-off prompts.

## What You'll Learn
- Explore and understand any codebase quickly
- Fix bugs using only the error message and file path
- Write test suites from scratch or fill coverage gaps
- Do thorough code reviews including security analysis
- Create PR descriptions, changelogs, and documentation
- Plan and execute large refactors safely

---

### 3.1 Common Development Tasks

Links:
- [Common Workflows](https://code.claude.com/docs/en/common-workflows) — Step-by-step guides for exploring codebases, debugging, refactoring, writing tests, creating pull requests, and code review workflows

Code:
```bash
# Explore an unfamiliar codebase
claude "Walk me through how a user login request flows through this codebase,
tracing from the HTTP entry point to the database query. Show the file path at each step."

# Fix a bug from an error message
claude "Fix this error: TypeError: Cannot read properties of undefined (reading 'userId')
in src/middleware/auth.ts line 42. Do not change any other files."

# Write tests for an existing function
claude "Write Vitest unit tests for src/services/payment.ts.
Cover: the happy path, invalid input, and network failure cases.
Place tests in tests/services/payment.test.ts."

# Targeted refactor
claude "Refactor src/utils/date-helpers.ts to use date-fns instead of moment.js.
Update all imports across the project. Keep behavior identical."

# Generate a PR description
claude "Write a PR description for the changes in this branch.
Include: summary (1 paragraph), motivation (why this change),
testing notes, and any breaking changes. Be concise."
```

```bash
# Create a new REST API endpoint from scratch
claude "Add a PATCH /api/users/:id endpoint to src/routes/users.ts.
Requirements:
- Validates the request body using the UserUpdateSchema in src/schemas/user.ts
- Updates only the fields provided (partial update)
- Returns the full updated user object
- Uses the same error handling pattern as the existing POST /api/users endpoint
Do not modify any other files."

# Generate TypeScript interfaces from a JSON API response
claude "Generate TypeScript interfaces for this API response:
$(cat sample-api-response.json)
Match the naming conventions in src/types/index.ts.
Export them from src/types/index.ts."

# Write a database migration
claude "Write a database migration that adds a nullable 'last_login_at' timestamp column
to the users table. Use Drizzle ORM format matching the existing migrations in drizzle/migrations/.
Name the file with the next sequential timestamp."

# Add Zod validation to an existing endpoint
claude "Add Zod validation to the POST /api/payments endpoint in src/routes/payments.ts.
Validate: amount is a positive number, currency is a 3-letter ISO 4217 code,
recipient_id is a UUID. Reject invalid input with HTTP 400 and a descriptive message.
Do not change any other endpoints or the existing function signature."

# Implement an interface
claude "Implement the PaymentGateway interface defined in src/interfaces/payment-gateway.ts
using the Stripe SDK. Create the file at src/gateways/stripe-gateway.ts.
Follow the error-handling pattern in src/gateways/paypal-gateway.ts."

# Upgrade a dependency safely
claude "Upgrade axios from v1 to v2 in this project.
Read the axios v2 migration guide to understand breaking changes.
Update all usages in src/ to the new API. Run 'npm test' after and fix any failures."

# Trace unfamiliar code without modifying anything
claude "I need to understand how payments are processed in this codebase.
Trace a payment from the API call in src/routes/payments.ts to the database write.
Show the file path and function name at each step. Do not modify any files."
```

Exercise:
1. Find a real bug or a failing test in any project (or create one intentionally)
2. Give Claude only the error message and the file path — no additional context
3. Observe which files Claude reads before proposing a fix
4. Evaluate whether the fix addresses the root cause or just the symptom

Success criterion: Claude reads the relevant source files and proposes a fix that makes the test pass or resolves the error.

Best Practices:
1. Always give Claude the verbatim error message, not a paraphrase — exact error text narrows the search space dramatically.
2. Scope refactoring requests to one file or module at a time — broad "refactor the whole codebase" prompts produce inconsistent results.
3. Ask Claude to run the test suite as part of the fix: "Fix this bug, then run `npm test` and show me the output."
4. For new features, specify "do not modify [X files]" as an explicit constraint — it prevents unintended scope creep.

Guardrails:
> WARNING: "Explore unfamiliar codebases" prompts can consume large amounts of context on large projects. Check `/context` — if above 60%, start a fresh focused session rather than continuing in the same one.
> WARNING: After any multi-file change, run `git diff` before staging. AI-generated refactors can introduce subtle issues in files you did not intend to change.

---

### 3.2 Code Review & Quality

Links:
- [Code Review](https://code.claude.com/docs/en/code-review) — Review code with Claude
- [/ultrareview Command](https://code.claude.com/docs/en/commands) — Deep multi-agent code review
- [/security-review Command](https://code.claude.com/docs/en/commands) — Security vulnerability scanning
- [/simplify Command](https://code.claude.com/docs/en/commands) — Code quality improvements

Code:
```bash
# Standard review — targeted at a specific file
claude "Review src/routes/users.ts for:
1. Security vulnerabilities
2. Performance issues
3. Error handling gaps
4. Adherence to conventions in CLAUDE.md
Output each finding as: [category] [severity] [line number] [description] [suggestion]"

# Built-in review skill
/review

# Security-focused review
/security-review

# Simplification pass after AI-generated code
/simplify

# Deep multi-agent review (most thorough — most expensive)
/ultrareview
```

```bash
# Pre-merge checklist — run before any PR merge
claude "Before I merge this branch, check the changed files for:
1. All edge cases handled (null inputs, empty arrays, network failures)
2. No hardcoded values (URLs, IDs, magic numbers, timeout values)
3. Tests exist for the changed logic
4. No console.log or debug logging left in
5. Error cases return appropriate status codes
6. No TODO or FIXME comments left unaddressed
7. No new dependencies added without updating package.json and the lock file
Report each as: PASS / FAIL / WARNING with specific file and line number if FAIL."

# Review a git diff directly
git diff main...HEAD | claude -p "Review this diff for:
- Security vulnerabilities (injection, auth bypass, data exposure)
- Missing error handling for new code paths
- Breaking changes to existing APIs or function signatures
List findings as: [SEVERITY: HIGH/MED/LOW] [FILE:LINE] [ISSUE] [SUGGESTED FIX]
If no issues found, output: 'No issues found.'"

# Dependency vulnerability audit
claude "Check all packages in package.json for known security vulnerabilities
by examining their versions. List any with HIGH or CRITICAL severity
and their safe upgrade path."

# Scan staged changes for secrets before committing
git diff --staged | claude -p "Scan this diff for hardcoded secrets, API keys,
connection strings, or passwords. Report file and line number for each finding.
If none found, output: 'No secrets found.'"
```

Exercise:
1. Run `/security-review` on a file that handles user input or authentication in your project
2. Read every finding — for each one, either fix it or write a comment explaining why it is a false positive
3. Run it again after your fixes — confirm the count of findings decreased

Success criterion: At least one finding was valid and fixed; all remaining findings have a documented rationale.

Best Practices:
1. Use `/security-review` on any code that handles: authentication tokens, user PII, file paths, SQL queries, or external API calls — before merging.
2. Run `/simplify` after a major AI-assisted implementation — AI-generated code tends toward verbosity and redundant abstractions.
3. Use the structured output format for reviews: `[category] [severity] [line] [description] [suggestion]` — it makes the findings actionable rather than a wall of text.

Guardrails:
> WARNING: `/ultrareview` spawns multiple subagents and can consume 10–20x the tokens of a standard review. Check `/cost` after running it on large files. Reserve it for security-sensitive code, complex PRs, or pre-release audits — not every commit.

---

### 3.3 Planning & Execution

Links:
- [Plan Mode](https://code.claude.com/docs/en/permission-modes) — Review plans before execution
- [/plan Command](https://code.claude.com/docs/en/commands) — Enter plan mode directly
- [/ultraplan Command](https://code.claude.com/docs/en/commands) — Draft plans in cloud sandbox
- [/batch Command](https://code.claude.com/docs/en/commands) — Orchestrate large-scale changes

Code:
```bash
# Start a session in plan mode — Claude proposes before it acts
claude --permission-mode plan "Migrate our authentication from JWT to session cookies"

# Switch to plan mode mid-session
/plan

# Ultra-plan for complex multi-week work (does not execute — planning only)
/ultraplan "Design a migration strategy to move from monolith to microservices"

# Batch mode for large-scale uniform changes
/batch "Add JSDoc comments to every exported function in src/"
```

```bash
# The "minimum change" constraint
claude "Fix only the failing test in tests/auth/login.test.ts.
Make the minimum change required to make the test pass.
Do not refactor surrounding code. Do not change other test files."

# Multi-file rename with explicit scope
claude --permission-mode plan "
Rename the UserService class to AccountService across the codebase.
Files to update: src/services/user-service.ts, src/routes/users.ts, src/types/index.ts.
Update imports in all files that import from those files.
Do not touch test files — I will update those separately."

# Large codebase task — break into audit + fix sessions
# Session 1: audit only, no changes
claude "Audit all API endpoints in src/routes/ for missing authentication middleware.
List each endpoint, its file path, and whether it has auth. Do not modify any files."

# Session 2: fix only (start a fresh session, paste the audit output)
claude "Based on this audit:
[paste audit output from session 1]
Add authentication middleware to each endpoint listed as missing it.
Only modify the files listed above."
```

Exercise:
1. Use `--permission-mode plan` on a real task: refactor 2–3 files or add a new feature
2. Read the full plan carefully before approving
3. If any step is out of scope, tell Claude "skip step N" before approving
4. After execution, run `git diff` — verify every change matches what the plan described

Success criterion: All file changes match the approved plan exactly; no unapproved files were modified.

Best Practices:
1. Use plan mode for any task touching more than 5 files — the review step catches scope creep before it happens.
2. When Claude's plan includes steps you did not ask for, explicitly reject them before approving — do not approve the whole plan without reading it.
3. `/ultraplan` outputs to a cloud sandbox and does not execute code — use it for high-level design and feasibility thinking before committing to an implementation approach.

Guardrails:
> WARNING: Plan approval is intent-level, not file-level. Claude may make minor implementation deviations from the described plan. Always run `git diff` after plan execution — do not assume the implementation exactly matches the written plan.

---

### 3.4 Prompt Patterns & Best Practices

Links:
- [Best Practices](https://code.claude.com/docs/en/best-practices) — Tips for effective Claude Code usage
- [Common Workflows](https://code.claude.com/docs/en/common-workflows) — Real-world patterns and examples

Code:
```bash
# Specify what to do AND what not to do
claude "Add input validation to the POST /users endpoint using Zod schemas.
Do not modify the existing test files.
Do not change the function signature."

# Request verification in the same prompt
claude "Fix the failing test in tests/payment.test.ts,
then run 'npm test' and show me the full output."

# Reference external context directories
claude --add-dir ../shared-lib "Update our imports to use the new API from shared-lib v2.
The breaking changes are documented in ../shared-lib/CHANGELOG.md."

# Constrain scope explicitly
claude "Make only the minimum change required to fix this bug.
Do not refactor surrounding code."
```

### The Anatomy of an Effective Claude Prompt

Every effective Claude Code prompt has three parts:
1. **What** — specific action + file paths + function names
2. **Constraints** — what NOT to do, which files to leave alone
3. **Verify** — the command to run to confirm success

```bash
# Template:
# "[WHAT] in [FILE]. [CONSTRAINTS]. After changes, run [VERIFY COMMAND] and show output."

# Full example:
claude "Add rate limiting to POST /api/auth/login in src/routes/auth.ts   # WHAT
using express-rate-limit: max 5 requests per IP per 15 minutes.          # HOW
Do not modify any other routes or the error response format.              # CONSTRAINTS
After changes, run 'npm test' and show the full output."                  # VERIFY
```

### Prompt Templates by Task

**New feature:**
```bash
claude "Add [FEATURE] to [FILE].
Requirements: [list].
Use the same pattern as [EXISTING SIMILAR THING].
Do not modify [OUT-OF-SCOPE FILES].
After adding, run [TEST COMMAND] and show output."
```

**Bug fix:**
```bash
claude "Fix this error:
[PASTE FULL ERROR AND STACK TRACE]
The error occurs when [TRIGGER].
Do not change files outside [SCOPE].
After fixing, run [TEST COMMAND] to confirm it is resolved."
```

**Refactor:**
```bash
claude "Refactor [FILE/FUNCTION] to [GOAL].
Keep behavior identical — do not change the public API.
Run [TEST COMMAND] after and confirm no regressions."
```

**Test writing:**
```bash
claude "Write [FRAMEWORK] tests for [FILE].
Cover: happy path, invalid inputs, boundary values, and error cases.
Place tests in [TEST FILE PATH].
After writing, run [TEST COMMAND] and fix any failures."
```

**Documentation:**
```bash
claude "Add JSDoc comments to all exported functions in [FILE].
Include @param types, @returns, @throws.
Match the style of existing JSDoc in [EXAMPLE FILE].
Do not change any code — only add comments."
```

### Using `--add-dir` for Multi-Repo Context

```bash
# Reference a shared library or monorepo package
claude --add-dir ../shared-lib \
  "Update our components in src/components/ to use the new tokens from
  ../shared-lib/tokens/colors.ts as documented in ../shared-lib/CHANGELOG.md."

# Reference multiple directories
claude --add-dir ../api-types --add-dir ../shared-utils \
  "Implement UserService using the types from ../api-types
  and the validators from ../shared-utils."
```

### Quick Reference: Constraint Patterns

| Situation | Add to your prompt |
|---|---|
| Don't touch test files | `"Do not modify any files in tests/"` |
| Don't change the API | `"Do not change function signatures or exported types"` |
| Stay in one file | `"Only change src/[file]. Do not touch other files."` |
| Minimum change only | `"Make only the minimum change required. Do not refactor."` |
| Verify after | `"After changes, run '[command]' and show full output."` |
| Follow existing patterns | `"Use the same pattern as [file/function]."` |

> See also: [Quick Reference: Prompt Patterns for Developers](../../quick-reference/prompt-patterns-developer.md) — 30 copy-paste prompts by category.

Exercise:
1. Take a task you would normally do manually (update a config, add a route, write a migration)
2. Write a Claude prompt with: (1) what to do, (2) what NOT to do, (3) a verification command to run after
3. Execute it and verify Claude stayed within the stated constraints

Success criterion: Claude completes the task, does not modify out-of-scope files, and provides verification output.

Best Practices:
1. Include a "do not" constraint in every prompt for tasks that touch shared or sensitive code.
2. Ask for verification commands in the same prompt — it closes the feedback loop automatically.
3. Break complex tasks into planning (`/plan`) and execution phases — do not ask Claude to plan and implement simultaneously for complex changes.
4. Check `git diff` before every commit when using Claude — treat it as mandatory, not optional.

Guardrails:
> WARNING: Avoid "clean up everything" or "improve this whole module" prompts without explicit constraints. These produce wide-ranging changes that are hard to review and often introduce regressions in code you did not ask to change.

---

### 3.5 Git Workflow Integration

Links:
- [Common Workflows](https://code.claude.com/docs/en/common-workflows) — Includes git workflow patterns

Code:
```bash
# Generate a conventional commit message from staged changes
git diff --staged | claude -p "Write a git commit message for these staged changes.
Format: type(scope): subject line (under 72 chars)
Optional body: explain WHY (2-3 sentences), not what the code does
Types: feat, fix, refactor, test, docs, chore, perf
Return only the commit message — no explanation or commentary."

# Summarize what changed in a branch before writing a PR
git log main...HEAD --oneline | claude -p "Summarize what these commits changed.
One clear sentence per commit. Flag any breaking changes or user-visible behavior changes."

# Resolve a merge conflict preserving both sides
claude "Help me resolve this merge conflict in [FILE].
Our branch: [what we added].
Their branch: [what they added].
We want both changes. Here is the conflict block:
[paste <<<<<<< HEAD ... >>>>>>> their-branch section]
Give me the resolved version."

# Generate a user-facing changelog from git history
git log v1.2.0...HEAD --oneline | claude -p "Write a changelog entry in Keep a Changelog format.
Group by: Added, Changed, Fixed, Deprecated, Removed.
Use user-facing language only — no commit SHAs, no internal jargon."

# Sanity check staged changes before committing
git diff --staged | claude -p "Review these staged changes for:
1. Anything unintentional (debug code, test data, commented-out blocks)
2. Missing error handling in new code paths
3. Obvious logic bugs
Output findings only. If clean, output: 'Looks good.'"
```

Exercise:
1. Make a small code change in any project and stage it with `git add`
2. Run: `git diff --staged | claude -p "Write a conventional commit message for these changes."`
3. Use the generated message as your commit (edit if needed)

Success criterion: The generated commit message accurately describes the change and follows conventional commit format (`type(scope): description`).

Best Practices:
1. Pipe `git diff --staged` to Claude before every commit — it takes 5 seconds and catches debug code, unintentional changes, and missing error handling.
2. Generate PR descriptions from `git log main...HEAD` rather than writing from memory — Claude sees every commit, not just what you remember.
3. For merge conflicts, give Claude both sides and the intent of each branch — it can usually produce a clean merge that preserves all behavior.

Guardrails:
> WARNING: Never pipe `git diff` output that contains secrets, credentials, or PII to Claude in a non-Zero Data Retention environment. Review the diff visually before piping it.
> WARNING: Always read the generated commit message before using it — Claude may misinterpret intent from code alone.

---

### 3.6 Debugging Patterns

Links:
- [Common Workflows](https://code.claude.com/docs/en/common-workflows) — Debugging workflow patterns

Code:
```bash
# Debug from a full error + stack trace (most common)
claude "This error appears in production:
[PASTE FULL ERROR AND STACK TRACE]
The code that triggers it is in [FILE]:[LINE].
Read the relevant files and find the root cause.
Diagnose first — do not make any changes until I approve your diagnosis."

# Debug unexpected behavior (no error message)
claude "This function returns [ACTUAL] but I expect [EXPECTED].
Here is the function:
[PASTE CODE]
Trace through the logic step by step and explain where it goes wrong.
Then propose the fix."

# Debug an async or timing issue
claude "This async function sometimes returns undefined:
[PASTE CODE]
This looks like a race condition or unhandled Promise rejection.
Read the calling code in [FILE] and identify the timing issue.
Do not fix it yet — explain the root cause first."

# Debug a test that passes locally but fails in CI
claude "This test passes locally but fails in CI:
Test file: [PASTE TEST CODE]
CI error output: [PASTE CI LOGS]
Differences I know about: [Node version, env vars, OS]
What environment assumptions is this test making that CI breaks?"

# Performance debugging
claude "This endpoint has a p95 of 2000ms. Here is the route handler:
[PASTE CODE]
Read the service and repository layers it calls.
Identify the most expensive operation in the call path.
Suggest an optimization — do not make changes yet."
```

Exercise:
1. Find (or intentionally create) a function with unexpected behavior in any project
2. Give Claude: (a) actual output, (b) expected output, (c) the function code
3. Ask Claude to trace the logic step-by-step before proposing a fix
4. Compare Claude's diagnosis to your own understanding

Success criterion: Claude identifies the root cause, not just a superficial fix, and the fix is minimal.

Best Practices:
1. Use "diagnose before fix" for bugs you do not understand — prevents symptomatic fixes that mask the real issue.
2. For async bugs, always give Claude the calling code too, not just the function — race conditions live in the interaction between components.
3. For CI-only failures, paste the exact CI log — the relevant error is often in the first 20 lines of the failure section.
4. Use `/effort high` for performance debugging — it benefits from deep reasoning about execution paths.

Guardrails:
> WARNING: Do not ask Claude to fix a bug it cannot reproduce. Always give it the full error, stack trace, and enough context to understand the failure mode — otherwise you get a patch, not a fix.

---

## Summary

| Workflow | Key prompt pattern | Verification step |
|----------|-------------------|-------------------|
| Fix a bug | Error message + file path + "do not change other files" | Run test suite |
| Write tests | File path + frameworks + coverage areas + output location | Run tests, check coverage |
| Code review | File path + review categories + output format | Act on each finding |
| Refactor | Scope + target pattern + "keep behavior identical" | Run tests + `git diff` |
| PR description | "Include: summary, motivation, testing notes, breaking changes" | Human review before merging |
| Large changes | Plan mode + step-by-step approval | `git diff` after execution |
| Commit message | `git diff --staged \| claude -p "Write conventional commit message"` | Review before using |
| Branch changelog | `git log main...HEAD --oneline \| claude -p "Summarize changes"` | Review for accuracy |
| Debug unknown bug | Provide: error + actual + expected + code | Verify root cause, not symptom |
| Merge conflict | Give both sides + intent of each branch | Review the merged result |

## Next Steps

[Level 4 — CI/CD & Quality Automation](../04-cicd-quality/README.md)

---

## Anthropic Academy Resources

Official lessons that complement this level:

### Claude Code in Action
- [Making changes](https://anthropic.skilljar.com/claude-code-in-action/303236)
- [Github integration](https://anthropic.skilljar.com/claude-code-in-action/303240)

### Claude 101
- [Getting better results](https://anthropic.skilljar.com/claude-101/383392)
- [Research mode for deep dives](https://anthropic.skilljar.com/claude-101/383399)

### Claude with the Anthropic API — Prompt Evaluation
- [Prompt evaluation](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287731)
- [A typical eval workflow](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287736)
- [Generating test datasets](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287739)
- [Running the eval](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287743)
- [Model based grading](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287742)
- [Code based grading](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287737)

### Claude with the Anthropic API — Prompt Engineering
- [Prompt engineering](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287745)
- [Being clear and direct](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287744)
- [Being specific](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287740)
- [Structure with XML tags](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287741)
- [Providing examples](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287746)
