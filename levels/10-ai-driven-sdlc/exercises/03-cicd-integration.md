# Exercise 3 — CI/CD Integration
### Domain 3, Task 3.6 · Exam weight: 20%

> Reference implementation: [`../examples/ci-review.yml`](../examples/ci-review.yml)

---

## Learning Objectives

- Use `-p` / `--print` flag to run Claude Code non-interactively in CI pipelines
- Produce machine-parseable output with `--output-format json` and `--json-schema`
- Apply session context isolation: separate review instance from generation instance
- Use CLAUDE.md as a CI context carrier for testing standards and review criteria

---

## Concept Summary

### Non-Interactive Mode

```bash
# WRONG — hangs waiting for user input in CI
claude "review this PR"

# CORRECT — outputs to stdout and exits
claude -p "review this PR"
claude --print "review this PR"  # equivalent

# CORRECT — structured JSON output for automated processing
claude -p \
  --output-format json \
  --json-schema '{"type":"object","properties":{"issues":{"type":"array"}}}' \
  "review this PR"
```

### Session Context Isolation

A model retains reasoning context from code generation in its session. This makes it **less effective** at reviewing its own code — it is less likely to question decisions it already made. Use a **fresh, independent Claude instance** for code review in CI.

On re-runs after new commits: include prior review findings in the prompt and instruct Claude to report only **new or still-unaddressed** issues. This prevents duplicate PR comments.

### CLAUDE.md as CI Context

When invoked in CI, Claude Code reads the project CLAUDE.md. Include:
- Testing standards (test framework, fixture conventions, coverage requirements)
- Review criteria (what to report vs skip)
- Available test utilities and helper patterns

This ensures CI-invoked Claude has the same project context as a developer using it interactively.

### Synchronous vs Batch API

| Requirement | Use |
|-------------|-----|
| Must block PR merge until complete | Synchronous API |
| Can run overnight, cost-sensitive | Message Batches API (50% savings, 24h window) |
| Needs to call tools mid-request | Synchronous API only (Batch API does not support this) |

---

## Exercises

### 3.1 — Identify CI Mode Issues

Which of the following will work correctly in CI? Explain why each option works or fails:

```bash
# Option A
claude "Review the changed files in this PR for security issues"

# Option B
claude -p "Review the changed files in this PR for security issues"

# Option C
claude -p --output-format json "Review the changed files"

# Option D
claude --permission-mode auto "Review the changed files"
```

---

### 3.2 — Design a JSON Schema

Design a JSON schema for CI review output. The schema must capture:
- A list of issues (each with: file, line, severity, message)
- A boolean that determines whether the pipeline should fail
- A text summary for the PR comment body

**Decisions to make:**
1. Which fields should be required vs optional? Justify each choice.
2. Should `line` be `integer` or `["integer", "null"]`? Why?
3. What `enum` values should `severity` have?

Write the schema in JSON format.

---

### 3.3 — Review the GitHub Actions Workflow

Open `../examples/ci-review.yml` and answer:

1. Which step implements session context isolation, and how?
2. Where is the `-p` flag applied, and what would happen without it?
3. How does the workflow avoid duplicate PR comments on re-runs?
4. What project-specific information should be added to CLAUDE.md to improve review quality for this workflow?

---

### 3.4 — Batch vs Synchronous Decision

Your team wants to implement two separate Claude Code features:

**Feature A**: Block PR merges if critical security vulnerabilities are found. The check must complete within 3 minutes.

**Feature B**: Generate test cases for every modified file. Run weekly on Sunday nights. Results reviewed by the QA team on Monday morning.

For each feature, choose: **Synchronous API** or **Message Batches API**.
Justify your choice with at least one trade-off.

---

### 3.5 — Write a CLAUDE.md Review Section

Write the section of a project CLAUDE.md that would help CI-invoked Claude Code produce better code reviews. Include:
- What to report vs skip
- Severity classification criteria with examples
- Testing standards relevant to the project (invent plausible ones)
- Any fixtures or utilities available for test generation

---

### 3.6 — Reflection

Rate your confidence (1–5):

- [ ] I know when and why to use the `-p` flag
- [ ] I can write `--json-schema` inline for a CI command
- [ ] I understand why a fresh Claude instance is better for code review
- [ ] I can decide between synchronous and batch API for a given use case
- [ ] I know what belongs in CLAUDE.md to improve CI review quality
