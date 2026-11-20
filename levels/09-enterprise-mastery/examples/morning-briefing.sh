#!/usr/bin/env bash
# morning-briefing.sh
# Non-interactive script that collects development activity from multiple sources
# and uses Claude to synthesize a concise morning briefing.
#
# Sources:
#   1. Git log for the last 24 hours (current repo)
#   2. Quick test run (fail/pass status)
#   3. Open PRs awaiting your review (via gh CLI)
#
# Output: formatted morning briefing printed to stdout.
#
# Requirements:
#   - ANTHROPIC_API_KEY environment variable must be set.
#   - claude CLI must be installed (npm install -g @anthropic-ai/claude-code).
#   - git must be available and the current directory must be a git repo.
#   - gh CLI is optional; a fallback message is shown if it is not installed.
#
# Usage:
#   ./morning-briefing.sh
#   ./morning-briefing.sh --help
#   ./morning-briefing.sh --no-tests      # skip the test run (faster)
#   ./morning-briefing.sh --repo /path    # run against a different repo

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_NAME="morning-briefing.sh"
SKIP_TESTS=false
REPO_DIR="$PWD"
TEST_COMMAND="${MORNING_BRIEFING_TEST_CMD:-npm test --silent 2>&1 | tail -10}"
TEST_TIMEOUT=60  # seconds; tests that take longer are skipped

# ---------------------------------------------------------------------------
# Help text
# ---------------------------------------------------------------------------
show_help() {
  cat <<EOF
$SCRIPT_NAME — Generate a morning development briefing using Claude.

Usage:
  $SCRIPT_NAME [options]

Options:
  --help        Show this help message and exit.
  --no-tests    Skip the test suite run (useful for repos with slow tests).
  --repo PATH   Path to the git repo to analyze (default: current directory).

Environment variables:
  ANTHROPIC_API_KEY             Required. Your Anthropic API key.
  MORNING_BRIEFING_TEST_CMD     Override the default test command.
                                Default: npm test --silent 2>&1 | tail -10

Examples:
  $SCRIPT_NAME
  $SCRIPT_NAME --no-tests
  $SCRIPT_NAME --repo /path/to/myrepo
  MORNING_BRIEFING_TEST_CMD="pytest -q" $SCRIPT_NAME
EOF
}

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --help|-h)
      show_help
      exit 0
      ;;
    --no-tests)
      SKIP_TESTS=true
      shift
      ;;
    --repo)
      REPO_DIR="${2:?'--repo requires a path argument'}"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Run '$SCRIPT_NAME --help' for usage." >&2
      exit 1
      ;;
  esac
done

# ---------------------------------------------------------------------------
# Dependency checks
# ---------------------------------------------------------------------------
check_dependency() {
  local cmd="$1"
  if ! command -v "$cmd" &>/dev/null; then
    return 1
  fi
  return 0
}

if ! check_dependency claude; then
  echo "Error: claude CLI is not installed." >&2
  echo "Install it with: npm install -g @anthropic-ai/claude-code" >&2
  exit 1
fi

if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "Error: ANTHROPIC_API_KEY is not set." >&2
  echo "Set it with: export ANTHROPIC_API_KEY=your-key-here" >&2
  exit 1
fi

if ! check_dependency git; then
  echo "Error: git is not installed." >&2
  exit 1
fi

# Change to the target repo directory.
cd "$REPO_DIR" || { echo "Error: Cannot access directory $REPO_DIR" >&2; exit 1; }

# Verify we are in a git repo.
if ! git rev-parse --git-dir &>/dev/null; then
  echo "Error: $REPO_DIR is not a git repository." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Data collection
# ---------------------------------------------------------------------------
REPO_NAME="$(basename "$(git rev-parse --show-toplevel)")"
DATE_NOW="$(date '+%A, %B %-d, %Y')"

echo "Generating morning briefing for $REPO_NAME — $DATE_NOW..."
echo ""

# Section 1: Git activity in the last 24 hours.
GIT_LOG=""
GIT_LOG=$(git log \
  --oneline \
  --since="24 hours ago" \
  --all \
  --format="%h %an: %s" \
  2>/dev/null || echo "(could not retrieve git log)")

if [[ -z "$GIT_LOG" ]]; then
  GIT_LOG="No commits in the last 24 hours."
fi

# Section 2: Currently uncommitted changes.
GIT_STATUS=""
GIT_STATUS=$(git status --short 2>/dev/null | head -20 || echo "(could not retrieve git status)")
if [[ -z "$GIT_STATUS" ]]; then
  GIT_STATUS="Working tree is clean."
fi

# Section 3: Test suite status.
TEST_OUTPUT="Test run skipped (--no-tests flag)."
if [[ "$SKIP_TESTS" == false ]]; then
  if check_dependency timeout; then
    TEST_OUTPUT=$(timeout "$TEST_TIMEOUT" bash -c "$TEST_COMMAND" 2>&1 || true)
  else
    TEST_OUTPUT=$(bash -c "$TEST_COMMAND" 2>&1 || true)
  fi
  TEST_OUTPUT="${TEST_OUTPUT:-Test command produced no output.}"
fi

# Section 4: Open PRs awaiting review.
PR_LIST=""
if check_dependency gh; then
  # gh pr list requires authentication. If the user is not authenticated, fail gracefully.
  if gh auth status &>/dev/null; then
    PR_LIST=$(gh pr list \
      --review-required \
      --json number,title,author,updatedAt \
      --template '{{range .}}#{{.number}} {{.title}} (by {{.author.login}}, updated {{.updatedAt}}){{"\n"}}{{end}}' \
      2>/dev/null | head -10 || echo "(could not retrieve PR list)")
    if [[ -z "$PR_LIST" ]]; then
      PR_LIST="No open PRs awaiting your review."
    fi
  else
    PR_LIST="gh CLI is installed but not authenticated. Run 'gh auth login' to enable PR listing."
  fi
else
  PR_LIST="gh CLI is not installed. Install it from https://cli.github.com/ to see open PRs."
fi

# ---------------------------------------------------------------------------
# Pipe collected data to Claude for synthesis.
# ---------------------------------------------------------------------------
BRIEFING_PROMPT="You are a senior developer's morning briefing assistant.
Synthesize the following development activity into a concise morning briefing.

Format the output with these sections:
1. Yesterday's Activity (2-4 bullet points summarizing commits)
2. Current State (uncommitted work, any obvious issues)
3. Test Health (pass/fail/unknown, with any notable failures)
4. PRs Needing Attention (list any PRs awaiting review)
5. Suggested Focus (one sentence: the most important thing to work on today based on the above)

Keep the entire briefing under 200 words. Use plain language. No jargon.

=== REPO: $REPO_NAME ===
=== DATE: $DATE_NOW ===

=== GIT LOG (last 24h) ===
$GIT_LOG

=== UNCOMMITTED CHANGES ===
$GIT_STATUS

=== TEST OUTPUT ===
$TEST_OUTPUT

=== OPEN PRS AWAITING REVIEW ===
$PR_LIST"

echo "============================================================"
echo "MORNING BRIEFING — $REPO_NAME — $DATE_NOW"
echo "============================================================"
echo ""

# -p flag: non-interactive, print response and exit.
# --output-format text: plain text output (no streaming JSON).
# --model: use Haiku for cost efficiency on this routine task.
echo "$BRIEFING_PROMPT" | claude -p --output-format text --model claude-haiku-4-5

echo ""
echo "============================================================"
echo "Generated by $SCRIPT_NAME at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
