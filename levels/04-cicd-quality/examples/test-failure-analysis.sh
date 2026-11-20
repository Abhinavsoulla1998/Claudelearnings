#!/usr/bin/env bash
# Pipes test output to Claude for root cause analysis.
# Run after a failing test suite to get a structured breakdown.
#
# Usage: bash test-failure-analysis.sh [test-command]
# Default test command: npm test
# Example: bash test-failure-analysis.sh "pytest tests/"
#
# Required env: ANTHROPIC_API_KEY

set -e

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "ERROR: ANTHROPIC_API_KEY environment variable is not set"
  exit 1
fi

TEST_COMMAND="${1:-npm test}"

echo "=== Test Failure Analysis ==="
echo "Running: $TEST_COMMAND"
echo ""

# Capture test output (both stdout and stderr)
TEST_OUTPUT=$(eval "$TEST_COMMAND" 2>&1 || true)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "All tests passed. No analysis needed."
  echo "$TEST_OUTPUT"
  exit 0
fi

echo "Tests failed. Sending output to Claude for analysis..."
echo ""

echo "$TEST_OUTPUT" | claude -p "Analyze this test output from '$TEST_COMMAND'.

For each failing test, provide:
1. Test name
2. Root cause (is this a code bug, a test bug, or an environment/setup issue?)
3. The specific fix: file name, approximate line number, and what to change
4. Flaky indicator: is this likely a timing or non-deterministic issue? (yes/no)

Format as a markdown table with columns: | Test | Root Cause | Suggested Fix | Flaky? |

After the table, provide a one-line summary: 'N tests failed: X code bugs, Y test bugs, Z environment issues, W possible flakes'

Here is the test output:
" \
  --permission-mode auto \
  --output-format text

echo ""
echo "=== Analysis complete. Original exit code: $EXIT_CODE ==="
exit $EXIT_CODE
