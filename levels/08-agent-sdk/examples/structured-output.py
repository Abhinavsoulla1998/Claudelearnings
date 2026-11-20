#!/usr/bin/env python3
"""
structured-output.py — Claude Code Agent SDK: structured JSON output.

Demonstrates:
  - Instructing Claude to return only JSON (no markdown, no prose)
  - Running a shell command first (git diff HEAD~1) and feeding results to Claude
  - Parsing the JSON response with json.loads
  - Handling the case where no diff exists (empty repo or single commit)
  - Defining and validating the expected output schema

Output schema:
    {
      "risk_level": "low" | "medium" | "high",
      "changed_files": ["list", "of", "file", "paths"],
      "summary": "one sentence summary of the change",
      "breaking_changes": true | false
    }

Usage:
    export ANTHROPIC_API_KEY=your-key-here
    python structured-output.py
"""

import asyncio
import json
import os
import subprocess
import sys
from typing import TypedDict

from claude_code_sdk import ClaudeCodeOptions, query


class DiffAnalysis(TypedDict):
    risk_level: str          # "low", "medium", or "high"
    changed_files: list[str] # list of file paths touched by the diff
    summary: str             # one-sentence plain English description
    breaking_changes: bool   # true if the change likely breaks existing callers


EMPTY_ANALYSIS: DiffAnalysis = {
    "risk_level": "low",
    "changed_files": [],
    "summary": "No changes found in the diff.",
    "breaking_changes": False,
}

SYSTEM_PROMPT = """
You are a code review assistant that analyzes git diffs.

IMPORTANT RULES:
1. Always respond with a single valid JSON object. No markdown. No code fences. No explanation.
2. The JSON object must have exactly these fields:
   - "risk_level": one of "low", "medium", or "high"
   - "changed_files": array of file path strings
   - "summary": a single sentence in plain English describing what changed
   - "breaking_changes": boolean, true if the change could break existing callers

Risk level guide:
  low    — test-only changes, documentation, formatting, minor dependency bumps
  medium — logic changes with backward-compatible behavior, new optional parameters
  high   — removed public APIs, changed function signatures, changed data contracts,
            security-relevant changes, database schema changes
"""


def get_git_diff() -> str | None:
    """Run git diff HEAD~1 and return the output, or None if it fails."""
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD~1"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            # Not a git repo, or only one commit
            return None
        diff = result.stdout.strip()
        return diff if diff else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def validate_analysis(data: dict) -> DiffAnalysis:
    """Validate and coerce the parsed JSON into a DiffAnalysis."""
    risk_level = data.get("risk_level", "low")
    if risk_level not in ("low", "medium", "high"):
        risk_level = "medium"  # safe default for unknown values

    changed_files = data.get("changed_files", [])
    if not isinstance(changed_files, list):
        changed_files = []

    summary = data.get("summary", "")
    if not isinstance(summary, str):
        summary = str(summary)

    breaking_changes = data.get("breaking_changes", False)
    if not isinstance(breaking_changes, bool):
        breaking_changes = bool(breaking_changes)

    return DiffAnalysis(
        risk_level=risk_level,
        changed_files=[str(f) for f in changed_files],
        summary=summary,
        breaking_changes=breaking_changes,
    )


async def analyze_diff() -> DiffAnalysis:
    """Ask Claude to analyze the current git diff and return structured JSON."""
    diff = get_git_diff()

    if diff is None:
        print("No git diff found (empty repo, single commit, or not a git repo).")
        print("Returning empty analysis.")
        return EMPTY_ANALYSIS

    # Truncate very large diffs to avoid hitting context limits.
    max_diff_chars = 20_000
    if len(diff) > max_diff_chars:
        diff = diff[:max_diff_chars] + "\n\n[DIFF TRUNCATED — showing first 20,000 chars]"

    prompt = f"""
Analyze the following git diff and return the JSON analysis object.

GIT DIFF:
{diff}
"""

    options = ClaudeCodeOptions(
        model="claude-sonnet-4-6",
        permission_mode="auto",
        system_prompt=SYSTEM_PROMPT,
        # Disallow tool use — we only want Claude to analyze the diff text we provided,
        # not run additional shell commands. This also makes the response faster.
        disallowed_tools=["Bash", "Edit", "Write", "Glob", "Grep", "WebFetch"],
    )

    full_response = ""
    async for message in query(prompt=prompt, options=options):
        if message.type == "text":
            full_response += message.text

    # Strip markdown code fences if Claude adds them despite instructions.
    cleaned = full_response.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first line (```json or ```) and last line (```)
        cleaned = "\n".join(lines[1:-1]).strip()

    try:
        parsed = json.loads(cleaned)
        return validate_analysis(parsed)
    except json.JSONDecodeError as e:
        print(f"Warning: Claude returned invalid JSON: {e}", file=sys.stderr)
        print(f"Raw response: {full_response[:500]}", file=sys.stderr)
        # Fall back to empty analysis rather than crashing.
        return EMPTY_ANALYSIS


async def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    print("Analyzing git diff HEAD~1...")
    print("-" * 60)

    analysis = await analyze_diff()

    print(f"Risk level:       {analysis['risk_level'].upper()}")
    print(f"Breaking changes: {analysis['breaking_changes']}")
    print(f"Summary:          {analysis['summary']}")
    print(f"Changed files ({len(analysis['changed_files'])}):")
    for f in analysis["changed_files"]:
        print(f"  - {f}")

    # Exit with code 1 if risk is high — useful in CI pipelines.
    if analysis["risk_level"] == "high":
        print("\nHigh-risk change detected. Manual review required.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
