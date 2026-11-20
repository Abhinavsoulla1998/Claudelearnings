# Level 8 — Agent SDK
> Audience: Developer (advanced) | Duration: Days 27–29 | Prerequisites: Level 7

## Overview

The Agent SDK lets you build programmatic agents that use Claude Code capabilities from Python or TypeScript scripts. Use it to build custom automation pipelines, CI tools, data analysis scripts, or any application that needs Claude to act as an intelligent agent with tool access.

Unlike the interactive CLI, the SDK is designed for headless, non-interactive execution. Your script drives the conversation: you provide the prompt, Claude executes tools (Bash, file read/write, web fetch), and your code processes the stream of events.

---

## Reference Links

**Fundamentals**
- [Agent SDK Overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Agent SDK Quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)
- [Agent Loop](https://code.claude.com/docs/en/agent-sdk/agent-loop)

**Language SDKs**
- [Python SDK](https://code.claude.com/docs/en/agent-sdk/python)
- [TypeScript SDK](https://code.claude.com/docs/en/agent-sdk/typescript)
- [Sessions](https://code.claude.com/docs/en/agent-sdk/sessions)

**Features**
- [Streaming vs. Single Mode](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode)
- [Streaming Output](https://code.claude.com/docs/en/agent-sdk/streaming-output)
- [Structured Outputs](https://code.claude.com/docs/en/agent-sdk/structured-outputs)
- [Custom Tools](https://code.claude.com/docs/en/agent-sdk/custom-tools)
- [Hooks](https://code.claude.com/docs/en/agent-sdk/hooks)
- [Skills](https://code.claude.com/docs/en/agent-sdk/skills)
- [Subagents](https://code.claude.com/docs/en/agent-sdk/subagents)

**Production**
- [File Checkpointing](https://code.claude.com/docs/en/agent-sdk/file-checkpointing)
- [Cost Tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)
- [Observability](https://code.claude.com/docs/en/agent-sdk/observability)
- [Permissions](https://code.claude.com/docs/en/agent-sdk/permissions)
- [Secure Deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- [Hosting](https://code.claude.com/docs/en/agent-sdk/hosting)
- [MCP Integration](https://code.claude.com/docs/en/agent-sdk/mcp)
- [Modifying System Prompts](https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts)

**Migration**
- [Migration Guide](https://code.claude.com/docs/en/agent-sdk/migration-guide)

---

## 1. SDK Fundamentals

### Installation

**Python:**
```bash
pip install claude-code-sdk
```

**TypeScript / Node.js:**
```bash
npm install @anthropic-ai/claude-code
```

### Python Quickstart

```python
import asyncio
from claude_code_sdk import query, ClaudeCodeOptions

async def main():
    options = ClaudeCodeOptions(
        model="claude-sonnet-4-6",
        permission_mode="auto",
        system_prompt="You are a helpful assistant for codebase analysis.",
    )

    async for message in query(
        prompt="List the 5 most recently modified files in the current directory.",
        options=options,
    ):
        if message.type == "text":
            print(message.text, end="", flush=True)
        elif message.type == "tool_use":
            print(f"\n[Tool: {message.name}]")
        elif message.type == "result":
            print(f"\n\nSession cost: ${message.cost_usd:.4f}")

asyncio.run(main())
```

See `examples/quickstart.py` for the complete runnable version with error handling.

### TypeScript Quickstart

```typescript
import { query, ClaudeCodeOptions } from "@anthropic-ai/claude-code";

async function main(): Promise<void> {
  const options: ClaudeCodeOptions = {
    model: "claude-sonnet-4-6",
    permissionMode: "auto",
    systemPrompt: "You are a helpful assistant for codebase analysis.",
  };

  for await (const message of query({
    prompt: "List the 5 most recently modified files in the current directory.",
    options,
  })) {
    if (message.type === "text") {
      process.stdout.write(message.text);
    } else if (message.type === "tool_use") {
      console.log(`\n[Tool: ${message.name}]`);
    } else if (message.type === "result") {
      console.log(`\n\nSession cost: $${message.cost_usd.toFixed(4)}`);
    }
  }
}

main().catch(console.error);
```

See `examples/quickstart.ts` for the complete runnable version.

### `ClaudeCodeOptions` Fields

| Field | Type | Description |
|-------|------|-------------|
| `model` | string | Claude model to use. |
| `permission_mode` | string | `default`, `plan`, `auto`, or `bypassPermissions`. |
| `system_prompt` | string | System prompt prepended to the conversation. |
| `max_turns` | int | Maximum number of turns (tool call cycles) before stopping. |
| `cwd` | string | Working directory for tool calls. Defaults to the process cwd. |
| `hooks` | dict | PreToolUse / PostToolUse hooks (see Section 6). |
| `allowed_tools` | list | Restrict which tools Claude may use. |
| `disallowed_tools` | list | Tools Claude is not allowed to use. |

---

## 2. Streaming vs Single Mode

### Streaming (recommended)

The `async for message in query(...)` pattern processes events as they arrive. This is the recommended approach for all SDK usage because:

- You see tool calls as they happen, not just the final output.
- You can process or log each event type independently.
- Large responses do not require buffering the full result in memory.

```python
async for message in query(prompt="...", options=options):
    match message.type:
        case "text":
            print(message.text, end="")
        case "tool_use":
            print(f"[Calling tool: {message.name}]")
        case "tool_result":
            pass  # tool result content
        case "result":
            print(f"Stop reason: {message.stop_reason}")
            print(f"Cost: ${message.cost_usd:.4f}")
```

### Message Types

| Type | Description | Key fields |
|------|-------------|------------|
| `text` | Claude text output | `text` |
| `tool_use` | Claude is about to call a tool | `name`, `input` |
| `tool_result` | Result returned from a tool call | `content` |
| `result` | Final session result | `stop_reason`, `cost_usd`, `duration_ms` |
| `system` | System messages from the SDK | `subtype`, `message` |

### Collecting the Full Output

If you only need the final text and do not need to process intermediate events:

```python
full_text = ""
async for message in query(prompt="...", options=options):
    if message.type == "text":
        full_text += message.text

print(full_text)
```

---

## 3. Structured Output

Claude can produce structured JSON output. The most reliable pattern is to instruct Claude in the system prompt to return JSON, then parse it after collecting the full response.

```python
import asyncio
import json
from claude_code_sdk import query, ClaudeCodeOptions

async def analyze_diff() -> dict:
    options = ClaudeCodeOptions(
        model="claude-sonnet-4-6",
        permission_mode="auto",
        system_prompt=(
            "You are a code review assistant. Always respond with valid JSON only. "
            "No markdown, no explanation — only the JSON object."
        ),
    )

    prompt = """
    Run: git diff HEAD~1
    
    Analyze the diff and return a JSON object with these exact fields:
    {
      "risk_level": "low" | "medium" | "high",
      "changed_files": ["list", "of", "file", "paths"],
      "summary": "one sentence summary of the change",
      "breaking_changes": true | false
    }
    """

    full_text = ""
    async for message in query(prompt=prompt, options=options):
        if message.type == "text":
            full_text += message.text

    return json.loads(full_text.strip())

result = asyncio.run(analyze_diff())
print(f"Risk level: {result['risk_level']}")
print(f"Breaking changes: {result['breaking_changes']}")
```

See `examples/structured-output.py` for the complete version with error handling and the no-diff case.

### Tips for Reliable JSON Output

- Include `"Always respond with valid JSON only"` in the system prompt.
- Show Claude the exact schema with field names and types in the prompt.
- Strip whitespace from the response before calling `json.loads`.
- Wrap `json.loads` in a try/except and retry with a corrective prompt if parsing fails.
- Avoid asking for markdown code fences — they break `json.loads`.

---

## 4. Custom Tools

You can define custom tools that Claude can call in addition to the built-in tools. This lets Claude interact with your specific APIs, databases, or services.

A custom tool definition consists of:
- A **name** and **description** that tell Claude when to use it.
- An **input schema** (JSON Schema) describing the parameters.
- A **handler function** in your code that executes when Claude calls the tool.

```python
weather_tool = {
    "name": "get_weather",
    "description": "Get the current weather for a location. Use this when the user asks about weather conditions.",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name or coordinates, e.g. 'San Francisco, CA' or '37.7749,-122.4194'",
            },
            "units": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature units. Defaults to celsius.",
            },
        },
        "required": ["location"],
    },
}
```

In the streaming loop, intercept `tool_use` messages with your tool's name and return the result:

```python
async for message in query(prompt="...", options=options, tools=[weather_tool]):
    if message.type == "tool_use" and message.name == "get_weather":
        result = call_my_weather_api(message.input["location"])
        # Inject the result back — the SDK handles the tool_result message
```

See `examples/custom-tool.py` for the complete pattern with mocked data.

---

## 5. SDK Hooks (PreToolUse / PostToolUse)

You can attach hook functions to SDK sessions programmatically. Unlike `settings.json` hooks (which run shell commands), SDK hooks are Python or TypeScript functions that execute in-process.

### Python SDK Hook Pattern

```python
from claude_code_sdk import query, ClaudeCodeOptions

def block_dangerous_commands(tool_name: str, tool_input: dict) -> dict | None:
    """PreToolUse hook: block rm -rf commands."""
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if "rm -rf" in command:
            return {
                "decision": "block",
                "reason": "rm -rf commands are not permitted in this agent.",
            }
    return None  # None means allow

def log_file_edits(tool_name: str, tool_input: dict, tool_output: dict) -> None:
    """PostToolUse hook: log all Edit tool calls to stdout."""
    if tool_name == "Edit":
        file_path = tool_input.get("path", "unknown")
        print(f"[AUDIT] Claude edited: {file_path}", flush=True)

options = ClaudeCodeOptions(
    model="claude-sonnet-4-6",
    permission_mode="auto",
    hooks={
        "PreToolUse": block_dangerous_commands,
        "PostToolUse": log_file_edits,
    },
)
```

### Hook Return Values

**PreToolUse hook:**
- Return `None` or `{"decision": "allow"}` — proceed with the tool call.
- Return `{"decision": "block", "reason": "..."}` — block the tool call. Claude receives the reason.

**PostToolUse hook:**
- Return value is ignored. Use for logging and side effects only.

See `examples/sdk-hooks.py` for the complete example.

---

## 6. Secure Deployment

### Authentication

The SDK uses `ANTHROPIC_API_KEY` from the environment by default. For production deployments:

```python
import os
from claude_code_sdk import query, ClaudeCodeOptions

# Validate the key is present before starting
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("ANTHROPIC_API_KEY is not set. Cannot start agent.")
```

Never hard-code API keys in source code. Use environment variables, a secrets manager (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault), or a CI/CD secrets store.

### Permission Mode for Automated Agents

| Scenario | Recommended permission_mode |
|----------|-----------------------------|
| Fully automated CI pipeline | `auto` with a carefully crafted allow list in settings.json |
| Script with human oversight | `default` |
| Sandboxed analysis (read-only) | `auto` with only `Read` in allowed_tools |
| Untrusted content analysis | `plan` (to surface what Claude intends to do) |

For fully automated agents, use `bypassPermissions` only inside an isolated container or VM with no access to production systems and no credentials beyond what the task requires.

### Principle of Least Privilege

Configure the agent to have access only to what it needs:

```python
options = ClaudeCodeOptions(
    model="claude-sonnet-4-6",
    permission_mode="auto",
    allowed_tools=["Bash", "Read"],   # Only these tools
    disallowed_tools=["Write", "Edit"],  # Explicitly block write tools
    cwd="/workspace/sandboxed-dir",   # Restrict working directory
)
```

### Rate Limiting and Cost Control

- Use `max_turns` to cap the number of tool call cycles and prevent runaway agents.
- Log `message.cost_usd` from the `result` message to track per-run costs.
- Set up usage alerts in the Anthropic console or your cloud billing dashboard.
- Use Haiku for high-volume automated tasks where quality requirements allow it.

```python
options = ClaudeCodeOptions(
    model="claude-haiku-4-5",  # Cheaper for high-volume automation
    max_turns=10,               # Stop after 10 tool cycles
)
```

---

## Summary

| Concept | Key point |
|---------|-----------|
| `query()` function | Main SDK entry point; returns an async generator of message events |
| Streaming loop | `async for message in query(...)` processes events as they arrive |
| Message types | `text`, `tool_use`, `tool_result`, `result`, `system` |
| Structured output | Instruct Claude in system prompt; parse with `json.loads` |
| Custom tools | Define name, description, and JSON Schema; handle in the streaming loop |
| SDK hooks | In-process Python/TS functions; return `{"decision": "block"}` to stop a tool |
| `permission_mode` | Use `auto` for automated agents; never use `bypassPermissions` outside a sandbox |
| `max_turns` | Always set a limit to prevent runaway agents |

## Next Steps

Proceed to **Level 9 — Enterprise and Mastery** to learn how to scale Claude Code across a team: standardize CLAUDE.md templates, set up agent teams for parallel workstreams, configure compliance and audit logging, and establish the patterns that distinguish expert users.

---

## Anthropic Academy Resources

Official lessons that complement this level:

### Claude Code in Action
- [The Claude Code SDK](https://anthropic.skilljar.com/claude-code-in-action/312001)

### Claude with the Anthropic API — Core API
- [Welcome to the course](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287818)
- [Making a request](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287725)
- [Multi-Turn conversations](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287735)
- [Response streaming](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287734)
- [Structured data](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287732)

### Claude with the Anthropic API — Tool Use
- [Introducing tool use](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287747)
- [Project overview](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287751)
- [Tool functions](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287756)
- [Tool schemas](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287753)
- [Handling message blocks](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287757)
- [Sending tool results](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287752)
- [Multi-turn conversations with tools](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287750)
- [Implementing multiple turns](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287758)
- [Using multiple tools](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287749)
- [Fine grained tool calling](https://anthropic.skilljar.com/claude-with-the-anthropic-api/313160)
- [The text edit tool](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287760)
- [The web search tool](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287755)

### Claude with the Anthropic API — Features of Claude
- [Extended thinking](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287773)
- [Image support](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287778)
- [PDF support](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287768)
- [Citations](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287771)
- [Prompt caching](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287772)
- [Rules of prompt caching](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287770)
- [Prompt caching in action](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287774)
- [Code execution and the Files API](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287777)
