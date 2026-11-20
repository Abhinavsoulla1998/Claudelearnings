#!/usr/bin/env python3
"""
sdk-hooks.py — Claude Code Agent SDK: PreToolUse and PostToolUse hooks.

Demonstrates:
  - A PreToolUse hook that blocks rm -rf commands in Bash tool calls
  - A PostToolUse hook that logs all Edit tool calls to stdout
  - How to attach hooks to ClaudeCodeOptions
  - The hook return value contract (allow vs block)

Unlike settings.json hooks (which are shell commands), SDK hooks are Python
functions that run in-process. They have access to your Python environment,
can make function calls, and can raise exceptions.

Usage:
    export ANTHROPIC_API_KEY=your-key-here
    python sdk-hooks.py
"""

import asyncio
import datetime
import os
import sys
from typing import Any

from claude_code_sdk import ClaudeCodeOptions, query


# ---------------------------------------------------------------------------
# PreToolUse hook
#
# Called before every tool invocation. Return value controls whether the
# tool call is allowed:
#
#   None or {"decision": "allow"}
#       -> The tool call proceeds normally.
#
#   {"decision": "block", "reason": "explanation"}
#       -> The tool call is blocked. Claude receives the reason string and
#          can adjust its approach (e.g., use a safer command instead).
#
# The hook receives:
#   tool_name  (str) — the name of the tool Claude wants to call
#   tool_input (dict) — the parameters Claude passed to the tool
# ---------------------------------------------------------------------------
def pre_tool_use_hook(
    tool_name: str,
    tool_input: dict[str, Any],
) -> dict[str, Any] | None:
    """
    Block dangerous Bash commands before Claude runs them.
    Log all tool calls to stdout for visibility.
    """
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    print(f"[{timestamp}] PRE-TOOL: {tool_name}", flush=True)

    # Block rm -rf in any Bash command.
    if tool_name == "Bash":
        command = tool_input.get("command", "")

        dangerous_patterns = [
            "rm -rf",
            "rm -fr",
            "sudo rm",
            ":(){ :|:& };:",    # fork bomb
            "> /dev/sda",       # disk wipe
        ]

        for pattern in dangerous_patterns:
            if pattern in command:
                reason = (
                    f"Command blocked by safety hook: '{pattern}' is not permitted. "
                    f"If you need to delete files, use a more targeted command."
                )
                print(f"[{timestamp}] BLOCKED: {command!r} (matched: {pattern!r})", flush=True)
                return {"decision": "block", "reason": reason}

    # Block writing to sensitive system paths.
    if tool_name in ("Write", "Edit"):
        path = tool_input.get("path", "") or tool_input.get("file_path", "")
        blocked_prefixes = ["/etc/", "/usr/", "/bin/", "/sbin/", "/boot/"]
        for prefix in blocked_prefixes:
            if path.startswith(prefix):
                reason = f"Writing to {prefix} is not permitted from this agent."
                print(f"[{timestamp}] BLOCKED write to: {path}", flush=True)
                return {"decision": "block", "reason": reason}

    # Allow everything else.
    return None


# ---------------------------------------------------------------------------
# PostToolUse hook
#
# Called after a tool call completes. The return value is ignored — this
# hook is for side effects only (logging, metrics, notifications).
#
# The hook receives:
#   tool_name   (str)  — the name of the tool that ran
#   tool_input  (dict) — the parameters that were passed to the tool
#   tool_output (dict) — the result returned by the tool
# ---------------------------------------------------------------------------
def post_tool_use_hook(
    tool_name: str,
    tool_input: dict[str, Any],
    tool_output: dict[str, Any],
) -> None:
    """Log all file edit operations to stdout for audit purposes."""
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    if tool_name == "Edit":
        file_path = tool_input.get("path", tool_input.get("file_path", "unknown"))
        print(f"[{timestamp}] AUDIT EDIT: {file_path}", flush=True)

    elif tool_name == "Write":
        file_path = tool_input.get("path", tool_input.get("file_path", "unknown"))
        content_length = len(str(tool_input.get("content", "")))
        print(f"[{timestamp}] AUDIT WRITE: {file_path} ({content_length} chars)", flush=True)

    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        # Log commands that modify files (heuristic based on common write patterns).
        write_indicators = [">", "tee ", "mv ", "cp ", "mkdir ", "touch ", "chmod "]
        if any(ind in command for ind in write_indicators):
            print(f"[{timestamp}] AUDIT BASH (write-like): {command[:120]}", flush=True)


# ---------------------------------------------------------------------------
# Main: wire hooks into ClaudeCodeOptions and run a test session.
# ---------------------------------------------------------------------------
async def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    options = ClaudeCodeOptions(
        model="claude-sonnet-4-6",
        permission_mode="auto",
        system_prompt=(
            "You are a helpful coding assistant. "
            "Complete the task and then try to run 'rm -rf /tmp/test_sdk_hooks' "
            "to demonstrate that the safety hook blocks dangerous commands."
        ),
        # Attach hooks here. The SDK calls these functions at the appropriate points
        # in the tool execution lifecycle.
        hooks={
            "PreToolUse": pre_tool_use_hook,
            "PostToolUse": post_tool_use_hook,
        },
    )

    # This prompt is designed to trigger both the allowed path (file write)
    # and the blocked path (rm -rf) so you can see both hook behaviors.
    prompt = (
        "1. Create a file at /tmp/sdk_hooks_demo.txt containing 'Hello from SDK hooks'.\n"
        "2. Then try to run: rm -rf /tmp/sdk_hooks_demo.txt\n"
        "3. Tell me what happened with each step."
    )

    print("Running SDK hooks demonstration...")
    print("=" * 60)

    async for message in query(prompt=prompt, options=options):
        if message.type == "text":
            print(message.text, end="", flush=True)
        elif message.type == "result":
            print(f"\n\n[Session complete — stop reason: {message.stop_reason}]")


if __name__ == "__main__":
    asyncio.run(main())
