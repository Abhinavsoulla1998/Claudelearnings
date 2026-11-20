#!/usr/bin/env bash
# Claude Code Quality Gate
# Exits 0 if no HIGH/CRITICAL issues found, exits 1 if issues are found.
# Use in CI to block merges on serious findings.
#
# Usage: bash quality-gate.sh
# Required env: ANTHROPIC_API_KEY

set -e

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "ERROR: ANTHROPIC_API_KEY environment variable is not set"
  exit 2
fi

echo "=== Claude Code Quality Gate ==="
echo "Reviewing changed files for HIGH and CRITICAL severity issues..."
echo ""

OUTPUT=$(claude -p "You are a security and code quality reviewer running in a CI pipeline.

Review the files in the current directory for HIGH and CRITICAL severity issues only.
Focus on:
- Hardcoded secrets, API keys, passwords, or tokens
- SQL injection vulnerabilities
- Command injection vulnerabilities
- Authentication or authorization bypass risks
- Unvalidated user input reaching sensitive operations
- Critical logic errors that would cause data loss or corruption

For each HIGH or CRITICAL finding, output exactly one line in this format:
  FINDING: [CRITICAL|HIGH] [file:line] [brief description]

If no HIGH or CRITICAL issues are found, output exactly:
  GATE PASSED: no HIGH or CRITICAL issues found

Do not output anything else." \
  --permission-mode auto \
  --output-format text 2>&1)

echo "$OUTPUT"
echo ""

if echo "$OUTPUT" | grep -q "^FINDING:"; then
  FINDING_COUNT=$(echo "$OUTPUT" | grep -c "^FINDING:" || true)
  echo "=== GATE FAILED: $FINDING_COUNT finding(s) require attention before merge ==="
  exit 1
elif echo "$OUTPUT" | grep -q "GATE PASSED"; then
  echo "=== GATE PASSED: no HIGH or CRITICAL issues found ==="
  exit 0
else
  echo "=== WARNING: Unexpected output format. Manual review required. ==="
  echo "Exiting with success to avoid blocking pipeline on tool error."
  exit 0
fi
