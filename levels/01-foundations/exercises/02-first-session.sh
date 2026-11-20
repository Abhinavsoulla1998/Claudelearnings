#!/usr/bin/env bash
# Demonstrates the three Claude Code session modes.
# Run from a project directory for best results.

echo "=== Claude Code: Three Session Modes Demo ==="
echo ""
echo "Current directory: $(pwd)"
echo ""

echo "--- Mode 1: Non-interactive query ---"
echo "Running: claude -p \"In one sentence, what kind of project is in the current directory?\""
echo ""
claude -p "In one sentence, what kind of project is in the current directory?" --output-format text
echo ""

echo "--- Mode 2: Query with structured output ---"
echo "Running: claude -p \"List the top 3 files by likely importance\" --output-format text"
echo ""
claude -p "List the top 3 files by likely importance, one per line, no explanation." --output-format text
echo ""

echo "--- Mode 3: Start interactive session ---"
echo "Starting interactive session. Type 'exit' or Ctrl+C to quit."
echo ""
claude "Hello! What files do you see in this directory?"
