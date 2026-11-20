#!/usr/bin/env bash
# Verifies Claude Code is correctly installed and authenticated.
# Run from any directory after setting ANTHROPIC_API_KEY.

set -e

echo "=== Claude Code Installation Check ==="

# Check Node.js
if ! command -v node &> /dev/null; then
  echo "FAIL: Node.js is not installed. Install from https://nodejs.org"
  exit 1
fi
echo "OK: Node.js $(node --version)"

# Check npm
if ! command -v npm &> /dev/null; then
  echo "FAIL: npm is not installed."
  exit 1
fi
echo "OK: npm $(npm --version)"

# Check claude
if ! command -v claude &> /dev/null; then
  echo "FAIL: claude is not installed. Run: npm install -g @anthropic-ai/claude-code"
  exit 1
fi
echo "OK: claude $(claude --version)"

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "FAIL: ANTHROPIC_API_KEY is not set."
  echo "Add this to your ~/.bashrc or ~/.zshrc:"
  echo '  export ANTHROPIC_API_KEY="sk-ant-api03-..."'
  exit 1
fi
echo "OK: ANTHROPIC_API_KEY is set (${#ANTHROPIC_API_KEY} characters)"

# Quick auth test
echo ""
echo "Testing API authentication..."
RESPONSE=$(claude -p "Reply with exactly: AUTH_OK" --output-format text 2>&1)
if echo "$RESPONSE" | grep -q "AUTH_OK"; then
  echo "OK: API authentication successful"
else
  echo "FAIL: Authentication test failed. Response was: $RESPONSE"
  exit 1
fi

echo ""
echo "=== All checks passed. Claude Code is ready to use. ==="
