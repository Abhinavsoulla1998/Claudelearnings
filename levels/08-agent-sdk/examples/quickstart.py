#!/usr/bin/env python3
"""
quickstart.py — Claude Code Agent SDK: minimal working example.

Demonstrates:
  - Importing from claude_code_sdk
  - Configuring ClaudeCodeOptions (model, permission_mode, system_prompt)
  - Streaming a response using async for
  - Handling message types: text, tool_use, result
  - Basic error handling

Usage:
    export ANTHROPIC_API_KEY=your-key-here
    python quickstart.py
"""

import asyncio
import os
import sys

from claude_code_sdk import ClaudeCodeOptions, query


async def main() -> None:
    # Validate environment before making any API calls.
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        print("Set it with: export ANTHROPIC_API_KEY=your-key-here", file=sys.stderr)
        sys.exit(1)

    # ClaudeCodeOptions configures the agent session.
    options = ClaudeCodeOptions(
        # Model to use. claude-sonnet-4-6 is a good balance of capability and cost.
        # Use claude-haiku-4-5 for faster, cheaper responses in automated pipelines.
        model="claude-sonnet-4-6",
        # permission_mode controls how Claude handles tool calls.
        # 'auto' allows safe operations without prompting — appropriate for scripts.
        # 'default' would prompt a human for approval, which blocks non-interactive runs.
        permission_mode="auto",
        # system_prompt scopes Claude's behavior for this session.
        system_prompt=(
            "You are a helpful developer assistant. "
            "When asked about files, run shell commands to get accurate information. "
            "Be concise and precise."
        ),
    )

    prompt = "List the 5 most recently modified files in the current directory."

    print(f"Prompt: {prompt}")
    print("-" * 60)

    # query() returns an async generator. Each iteration yields one message event.
    # The generator drives the full agentic loop: Claude thinks, calls tools,
    # processes tool results, and continues until it has a final answer.
    try:
        async for message in query(prompt=prompt, options=options):
            if message.type == "text":
                # Claude is generating text output. Print it as it streams.
                print(message.text, end="", flush=True)

            elif message.type == "tool_use":
                # Claude is about to call a tool (e.g., Bash, Read, Glob).
                # message.name is the tool name; message.input is the tool parameters.
                print(f"\n[Tool call: {message.name}]", flush=True)
                if hasattr(message, "input") and message.input:
                    # For the Bash tool, 'command' is the key field.
                    cmd = message.input.get("command", "")
                    if cmd:
                        print(f"  Command: {cmd}", flush=True)

            elif message.type == "tool_result":
                # The tool has returned a result. Claude will process this before
                # continuing. We skip printing it to keep output clean, but you
                # could log it for debugging.
                pass

            elif message.type == "result":
                # The session has ended. message.stop_reason explains why.
                # message.cost_usd is the total cost of this session in USD.
                print(f"\n\n[Session complete]")
                print(f"  Stop reason: {message.stop_reason}")
                if hasattr(message, "cost_usd") and message.cost_usd is not None:
                    print(f"  Cost: ${message.cost_usd:.4f} USD")
                if hasattr(message, "duration_ms") and message.duration_ms is not None:
                    print(f"  Duration: {message.duration_ms}ms")

            elif message.type == "system":
                # System messages from the SDK (e.g., initialization, warnings).
                # Usually safe to ignore, but useful for debugging.
                pass

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError during agent session: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
