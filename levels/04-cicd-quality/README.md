# Level 4 — CI/CD & Quality Automation
> Audience: QA Engineer, Team Lead | Duration: Days 15–17 | Prerequisites: Levels 2–3

## Overview
Integrate Claude Code into your CI/CD pipelines to automate code review, quality gates, test analysis, and release notes. By the end of this level, Claude will be reviewing every PR, blocking pipelines on HIGH severity findings, and generating release notes automatically.

## What You'll Learn
- Add Claude Code review as a GitHub Actions step triggered by PR comments
- Build a quality gate that exits non-zero to block the pipeline on findings
- Auto-generate release notes from git commit history
- Integrate with GitLab CI/CD merge request pipelines
- Pipe test output to Claude for root cause analysis

---

### 4.1 GitHub Actions — Automated PR Review

Links:
- [GitHub Actions](https://code.claude.com/docs/en/github-actions) — Integrate Claude Code with GitHub CI/CD

Code — show the full `github-actions-review.yml` inline (copy from the example file below), then explain the key fields.

```yaml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]
  issue_comment:
    types: [created]

jobs:
  review:
    name: Claude PR Review
    runs-on: ubuntu-latest
    if: |
      github.event_name == 'pull_request' ||
      (github.event_name == 'issue_comment' &&
       github.event.issue.pull_request &&
       contains(github.event.comment.body, '@claude'))
    permissions:
      contents: read
      pull-requests: write
      issues: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Claude Code Review
        uses: anthropics/claude-code-action@beta
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          trigger_phrase: "@claude"
          # Optional: customize the review focus
          # direct_prompt: |
          #   Review this PR for: security vulnerabilities, performance issues,
          #   missing error handling, and violations of our coding conventions.
          #   Output each finding with: severity, file:line, description, suggested fix.
```

Exercise:
> Files: `examples/github-actions-review.yml` (copy to `.github/workflows/`)
1. Copy `examples/github-actions-review.yml` to your repository's `.github/workflows/` directory
2. Add `ANTHROPIC_API_KEY` as a repository secret in GitHub Settings -> Secrets and Variables -> Actions
3. Open a pull request (or push to an existing one)
4. Comment `@claude review this PR` on the pull request
5. Wait for the workflow to run — a review comment should appear from the GitHub Actions bot

Success criterion: A review comment appears on the PR within 3 minutes of the `@claude` trigger comment, without any manual invocation.

Best Practices:
1. Use `trigger_phrase: "@claude"` to gate reviews — this prevents Claude from running on every single commit push, which can be expensive.
2. Pin `anthropics/claude-code-action` to a specific commit SHA in production: `uses: anthropics/claude-code-action@<sha>` to prevent supply-chain attacks from a tag change.
3. Store `ANTHROPIC_API_KEY` as an environment-scoped secret, not a repository-wide secret — limit it to the specific environment (e.g., "review") that runs CI.

Guardrails:
> WARNING: Never configure your CI pipeline to block merges solely based on Claude's review output without human sign-off. Claude reviews may contain false positives. Use them as signals that require human triage, not as automated gatekeepers by themselves.
> WARNING: The `@beta` tag in `anthropics/claude-code-action@beta` is mutable — it can change behavior without warning. For stable production pipelines, pin to a commit SHA.

---

### 4.2 CI Quality Gate (Blocks Pipeline on Findings)

Code:
```bash
# Run from CI — exits 1 if HIGH severity findings are found, 0 if all clear
# See examples/quality-gate.sh for the complete implementation
claude -p "Review the changed files in this branch for security vulnerabilities and critical bugs.
If you find any HIGH or CRITICAL severity issues, print each as:
  FINDING: [severity] [file:line] [description]
Then exit with code 1.
If no HIGH or CRITICAL issues are found, print PASSED and exit with code 0." \
  --permission-mode auto \
  --output-format text
echo "Exit code: $?"
```

```yaml
# GitHub Actions step using the quality gate
- name: Claude Quality Gate
  run: bash levels/04-cicd-quality/examples/quality-gate.sh
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  continue-on-error: false  # fail the pipeline on non-zero exit
```

Exercise:
> Files: `examples/quality-gate.sh`
1. Intentionally introduce a hardcoded secret in a test file (e.g., `const API_KEY = "sk-real-key-here"`)
2. Run `examples/quality-gate.sh` from your terminal
3. Confirm the script exits with code 1 and identifies the hardcoded secret
4. Remove the hardcoded secret and run again — confirm it exits with code 0

Success criterion: The script detects the hardcoded secret and exits non-zero; exits zero after the secret is removed.

Best Practices:
1. Tune the quality gate prompt for your team's specific concerns — generic prompts produce generic results.
2. Start with `continue-on-error: true` in CI and review findings for one sprint before switching to blocking mode — build trust in the signal before using it as a gate.

Guardrails:
> WARNING: A quality gate prompt that is too strict will block legitimate PRs and cause developer frustration. A prompt that is too loose will miss real issues. Calibrate by running it on 10 recent merged PRs and reviewing what it would have flagged.

---

### 4.3 Auto-Generate Release Notes

Code:
```bash
# Generate release notes from commits between two tags
git log v1.2.0..v1.3.0 --oneline | \
  claude -p "Generate release notes from these commits.
Use Keep a Changelog format with sections: ## What's New, ## Bug Fixes, ## Breaking Changes.
Write in user-facing language — no internal jargon or ticket numbers.
Be concise: one line per item." \
  --output-format text

# Save directly to a file
git log v1.2.0..v1.3.0 --oneline | \
  claude -p "Generate release notes. Format: ## New, ## Fixed, ## Breaking. User-facing language." \
  --output-format text > RELEASE_NOTES.md
```

Exercise:
> Files: `examples/github-actions-release-notes.yml`
1. Run the release notes command above against your last 10 commits: `git log HEAD~10..HEAD --oneline | claude -p "Generate release notes..."`
2. Read the output — identify any items that are wrong, missing, or use internal language
3. Edit the output to fix those items
4. Save the final version as `RELEASE_NOTES.md`

Success criterion: The generated release notes require fewer than 5 manual corrections to be publishable.

Best Practices:
1. Always human-review AI-generated release notes before publishing — hallucinations appear here as phantom features or incorrect descriptions.
2. Add instructions to exclude internal tickets and branch names from the output — commit messages often contain these.

Guardrails:
> WARNING: Claude generates release notes from commit messages. If your commit message quality is poor ("fix stuff", "wip", "changes"), the release notes will be poor. Fix commit quality before relying on this automation.

---

### 4.4 GitLab CI/CD Integration

Links:
- [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd) — GitLab pipeline integration

Code — show the full `gitlab-ci-review.yml` inline, then explain the key fields.

```yaml
# Add this job to your .gitlab-ci.yml
# Required CI/CD variable: ANTHROPIC_API_KEY (protected, masked)

claude-review:
  stage: test
  image: node:20-slim
  before_script:
    - npm install -g @anthropic-ai/claude-code
  script:
    - |
      echo "Running Claude Code review on merge request changes..."
      claude -p "Review the changes in this merge request.

      Check for:
      1. Security vulnerabilities (injection, XSS, hardcoded secrets, insecure dependencies)
      2. Logic errors and edge cases that could cause runtime failures
      3. Missing error handling for external calls
      4. Performance issues (N+1 queries, missing indexes, synchronous blocking operations)
      5. Violations of common coding conventions

      For each finding output:
        FINDING [severity: LOW|MEDIUM|HIGH|CRITICAL] [file:line]: [description]
        FIX: [specific suggested fix]

      If no issues found, output: REVIEW PASSED - no significant issues found.

      End with a one-line summary: 'X findings: Y critical, Z high, W medium, V low'" \
      --permission-mode auto \
      --output-format text
  variables:
    ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  allow_failure: true  # Change to false once you have calibrated the review prompt
  timeout: 5 minutes
```

Exercise:
> Files: `examples/gitlab-ci-review.yml`
1. Copy `examples/gitlab-ci-review.yml` content into your `.gitlab-ci.yml` as a new job
2. Add `ANTHROPIC_API_KEY` as a protected CI/CD variable in GitLab Settings -> CI/CD -> Variables
3. Open a merge request — the `claude-review` job should run automatically
4. Check the job output in the pipeline — review the findings

Success criterion: The `claude-review` job runs on MR creation and outputs a numbered list of findings (or "PASSED") in the job log.

Best Practices:
1. Use `rules: - if: $CI_PIPELINE_SOURCE == "merge_request_event"` to run Claude only on MR pipelines, not on every branch push.
2. Set `allow_failure: true` initially while you calibrate the review prompt.

Guardrails:
> WARNING: Store `ANTHROPIC_API_KEY` as a **protected** and **masked** CI variable, restricted to protected branches only. An unprotected CI variable is visible to all pipelines including those from fork branches.

---

### 4.5 Test Failure Analysis

Code:
```bash
# Run tests and pipe failures to Claude for root cause analysis
# See examples/test-failure-analysis.sh for the full implementation

npm test 2>&1 | claude -p "Analyze these test failures.
For each failing test:
1. Identify the root cause (code bug, test bug, or environment issue)
2. Suggest the specific fix (file, line, change)
3. Note if it looks like a flaky test (non-deterministic failure)
Format as a table: | Test name | Root cause | Suggested fix | Flaky? |" \
  --output-format text
```

Exercise:
> Files: `examples/test-failure-analysis.sh`
1. Break one test intentionally in your project (change an assertion value)
2. Run `examples/test-failure-analysis.sh`
3. Verify Claude identifies the correct root cause and the correct file/line to fix
4. Restore the test and run again — confirm Claude reports no failures

Success criterion: Claude correctly identifies the broken test's root cause and suggests the right fix location.

Best Practices:
1. Use this script at the start of a debugging session rather than staring at raw test output — it cuts time-to-diagnosis significantly.
2. For flaky test detection, run the script across 3–5 consecutive test runs and compare which tests appear in each.

---

## Summary

| Automation | Trigger | What it does | File to copy |
|------------|---------|--------------|--------------|
| PR Review | `@claude` comment on PR | Reviews changed files, posts findings as PR comment | `examples/github-actions-review.yml` |
| Quality Gate | Every CI run | Exits 1 on HIGH severity findings | `examples/quality-gate.sh` |
| Release Notes | Tag push | Generates Keep a Changelog formatted notes | `examples/github-actions-release-notes.yml` |
| GitLab Review | MR creation | Reviews MR changes, outputs findings to job log | `examples/gitlab-ci-review.yml` |
| Test Analysis | Pipe test output | Root cause analysis for failures | `examples/test-failure-analysis.sh` |

Next Steps: [Level 5 — MCP: Connecting Your Tools](../05-mcp-connecting-tools/README.md)

---

## Anthropic Academy Resources

Official lessons that complement this level:

### Claude Code in Action
- [Github integration](https://anthropic.skilljar.com/claude-code-in-action/303240)
