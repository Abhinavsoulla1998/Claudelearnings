# Level 6 — Automation & Hooks
> Audience: Developer, Team Lead | Duration: Days 22–24 | Prerequisites: Level 5

## Overview

Hooks let you run shell commands in response to Claude events — before/after tool calls, at session start/end. Skills are custom slash commands backed by prompt templates. Combined, they automate the repetitive parts of your workflow and enforce team policies automatically.

Hooks execute as your operating system user account with your full permissions. They are not sandboxed. A hook that runs `rm -rf` will delete files. A hook that calls an external API will make real network requests. Treat hook scripts with the same caution you apply to any shell script that runs automatically.

---

## 1. Hooks

Hooks are configured in `settings.json` under the `"hooks"` key. Each hook specifies:

- **event** — when it fires (`PreToolUse`, `PostToolUse`, `Stop`, `Start`)
- **matcher** — which tool name triggers it (for tool-scoped events)
- **command** — the shell command to run

### Hook Events

| Event | When it fires | Typical use |
|-------|---------------|-------------|
| `PreToolUse` | Before Claude calls a tool | Validation, blocking, logging intent |
| `PostToolUse` | After a tool call completes | Audit logging, notifications, cleanup |
| `Stop` | When Claude ends a session | Notifications, session summaries |
| `Start` | When Claude starts a session | Context injection, environment checks |

### Full `settings.json` Hook Format

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "ToolName",
        "hooks": [
          {
            "type": "command",
            "command": "your-shell-command-here"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "ToolName",
        "hooks": [
          {
            "type": "command",
            "command": "your-shell-command-here"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "your-shell-command-here"
          }
        ]
      }
    ]
  }
}
```

The `matcher` field matches against the tool name Claude reports. Common tool names: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `WebFetch`.

If a `PreToolUse` hook exits with a non-zero status code, Claude treats the tool call as blocked and will not proceed with it. This is how you enforce deny policies at the hook layer.

### Example 1: PreToolUse Git Push Blocker

This hook intercepts every `Bash` tool call and blocks any command that contains `git push`.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'git push' && echo 'BLOCKED: git push is not allowed from Claude sessions' && exit 1 || exit 0"
          }
        ]
      }
    ]
  }
}
```

`$CLAUDE_TOOL_INPUT` is an environment variable Claude sets to the JSON-encoded tool input before running the hook. For a `Bash` tool call, the input contains the command string. The hook greps for `git push`; if found, it prints a message and exits 1, which blocks the tool call.

See `examples/hooks-git-push-blocker.json` for the complete settings file.

### Example 2: PostToolUse File Edit Audit Log

This hook appends a timestamped record to `/tmp/claude-audit.log` every time Claude uses the `Edit` tool.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date -u +%Y-%m-%dT%H:%M:%SZ) EDIT $CLAUDE_TOOL_INPUT\" >> /tmp/claude-audit.log"
          }
        ]
      }
    ]
  }
}
```

`PostToolUse` hooks receive the same `$CLAUDE_TOOL_INPUT` as `PreToolUse` hooks, plus `$CLAUDE_TOOL_OUTPUT` containing the tool result. The exit code of a `PostToolUse` hook does not block the tool (the tool already ran); it only affects whether Claude sees an error from the hook itself.

See `examples/hooks-audit-log.json` for the complete settings file.

### Example 3: Stop Session Notification Hook

This hook fires when Claude ends a session and prints a timestamp to the terminal (or could be adapted to send a desktop notification or a Slack message).

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"Claude session ended at $(date -u +%Y-%m-%dT%H:%M:%SZ)\""
          }
        ]
      }
    ]
  }
}
```

See `examples/hooks-session-notify.json` for the complete settings file.

### Guardrails: Hooks Run as Your User Account

Hooks are shell commands executed by Claude Code with your full operating system permissions. There is no sandboxing, no capability restriction, and no prompt before execution.

This means:

- A hook with write access to `/etc` can modify system files.
- A hook that calls `curl` can exfiltrate data to an external server.
- A hook that runs `git push` can push code to remote repositories.
- A hook with access to AWS credentials can make API calls.

Follow these practices when writing hooks:

1. **Review every hook script before adding it** — treat it like code review.
2. **Pin external URLs** — if a hook fetches a script, use a content hash, not a mutable URL.
3. **Log to files you control** — use append-only log files under `/tmp` or a project-local directory.
4. **Do not embed secrets in `settings.json`** — reference environment variables instead.
5. **Test hooks in isolation** before adding them to a shared `settings.json`.
6. **Prefer project-level hooks** (`.claude/settings.json`) over global hooks for team workflows — they are reviewed with the codebase.

---

## 2. Skills (Custom Slash Commands)

Skills are Markdown files that define custom `/command` names. They live in `~/.claude/skills/` (global) or `.claude/skills/` (project-local). When you type the skill's slash command in Claude, Claude reads the skill file as a system prompt and executes it.

### Skill Frontmatter Format

```yaml
---
name: skill-name
description: One-sentence description shown in /skills list.
---
```

The rest of the file is the prompt body. Use standard Markdown. Reference tools, files, or shell commands as you would in any Claude prompt.

The filename determines the slash command: `daily-standup.md` becomes `/daily-standup`.

### Skill 1: Daily Standup

Location: `~/.claude/skills/daily-standup.md` or `.claude/skills/daily-standup.md`

This skill checks the last 24 hours of git history, identifies in-progress work, and formats a standup-ready summary.

Full content is in `examples/skill-daily-standup.md`.

Usage: type `/daily-standup` in a Claude session inside your git repo.

### Skill 2: Changelog Entry

Location: `~/.claude/skills/skill-changelog.md`

This skill reads recent git commits and generates a CHANGELOG.md entry in Keep a Changelog format (Added, Changed, Fixed, Removed sections).

Full content is in `examples/skill-changelog.md`.

Usage: type `/changelog` in a Claude session.

### Listing Available Skills

```
/skills
```

This shows all skills in both the global and project-local skills directories, with their descriptions from the frontmatter.

---

## 3. Scheduled Tasks: /loop and /schedule

### /loop — Repeat a Prompt on an Interval

`/loop` runs a prompt repeatedly on a fixed interval within the current Claude session. The session stays open between iterations.

```
/loop 5m check the CI status for the current branch and tell me if it passed
```

```
/loop 1m look for new entries in /var/log/app.log and summarize any errors
```

Pattern:

```
/loop [interval] [prompt]
```

Supported interval units: `s` (seconds), `m` (minutes), `h` (hours).

Use `/loop` when you want to monitor something within a working session — watching a build, polling a log file, or checking a queue.

To stop a loop, press `Escape` or `Ctrl+C`.

### /schedule — Create a Cloud Routine

`/schedule` creates a persistent scheduled agent that runs on a cron schedule, independent of your local session. The agent runs in the cloud and can be used for nightly reports, recurring code quality checks, or automated maintenance.

```
/schedule
```

Claude will prompt you for:
- What to do (the task description)
- When to run it (daily at 9am, every Monday, etc.)
- Where to run it (which repo or context)

Use `/schedule` for tasks that should persist across sessions and run without you being present.

### Choosing Between /loop and /schedule

| Use case | Tool |
|----------|------|
| Watch CI while I work | `/loop` |
| Poll a log during a debugging session | `/loop` |
| Nightly test summary emailed to the team | `/schedule` |
| Weekly changelog draft PR | `/schedule` |
| Run every 5 minutes for the next hour | `/loop` |
| Run every Monday at 8am indefinitely | `/schedule` |

---

## 4. External Integrations

Hooks and skills become more powerful when combined with external tools. Common patterns:

### Slack Notifications

```bash
# PostToolUse hook: notify Slack when Claude makes a file edit
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-type: application/json' \
  -d "{\"text\": \"Claude edited a file at $(date): $CLAUDE_TOOL_INPUT\"}"
```

Set `SLACK_WEBHOOK_URL` in the `env` block of `settings.json` or in your shell profile.

### GitHub Pull Request Automation

A skill can use the `gh` CLI to open a PR after making changes:

```
After completing the changes, run: gh pr create --title "[TITLE]" --body "[BODY]" --draft
```

### CI System Integration

A hook can trigger a CI build after Claude writes files:

```bash
# PostToolUse hook on Write: trigger CI
curl -X POST "https://your-ci.example.com/api/trigger" \
  -H "Authorization: Bearer $CI_API_TOKEN" \
  -d '{"branch": "'"$(git branch --show-current)"'"}'
```

### Key Integration Principles

- Store webhook URLs and tokens in environment variables, never in hook command strings committed to source control.
- Use project-level `.claude/settings.json` for integrations specific to one repo.
- Use global `~/.claude/settings.json` for integrations that apply across all your work.
- Test integrations with dry-run mode before enabling them for the full team.

---

## 6.4 Subagents & Delegation

Links:
- [Subagents](https://code.claude.com/docs/en/sub-agents) — Delegate tasks to specialized agents
- [/agents Command](https://code.claude.com/docs/en/commands) — Manage agent configurations

Subagents let Claude delegate work to specialized child agents running in parallel or in sequence. You define the agent's role, tools, and scope — Claude decides when to spin one up.

**Common uses:**
- One agent writes tests while another writes the implementation
- One agent searches documentation while another writes code
- Long research tasks delegated to a background agent

**Exercise**
Ask Claude: `"Use a subagent to search this codebase for all TODO comments and produce a prioritized list."` Observe how it spawns a child agent and returns results.

**Best Practices**
1. Give subagents a narrow, well-defined scope — they work best on focused tasks.
2. Review subagent output before using it, just as you would code from any collaborator.

---

## 6.5 Remote Control & Session Teleport

Links:
- [Remote Control](https://code.claude.com/docs/en/remote-control) — Control Claude Code from claude.ai
- [/remote-control Command](https://code.claude.com/docs/en/commands) — Enable remote control mode
- [/teleport Command](https://code.claude.com/docs/en/commands) — Move a session between terminal and web

Remote Control lets you monitor and send messages to a running Claude Code terminal session from the claude.ai web interface. Useful when you start a long task in your terminal and want to check on it from your browser.

**`/teleport`** moves your current session to the web UI (or vice versa) without losing conversation history.

**Exercise**
1. Start a Claude session in your terminal and run `/remote-control` to enable it.
2. Open claude.ai in your browser — you should see the active session listed.
3. Send a message from the browser and observe it appear in the terminal.

---

## Summary

| Concept | What it does | Where it lives |
|---------|--------------|----------------|
| `PreToolUse` hook | Runs before a tool call; exit 1 blocks it | `settings.json` → `hooks.PreToolUse` |
| `PostToolUse` hook | Runs after a tool call completes | `settings.json` → `hooks.PostToolUse` |
| `Stop` hook | Runs when Claude ends a session | `settings.json` → `hooks.Stop` |
| Skill file | Defines a custom `/command` | `~/.claude/skills/` or `.claude/skills/` |
| `/loop` | Repeats a prompt on an interval | Interactive session command |
| `/schedule` | Creates a persistent cloud routine | Interactive session command |
| `$CLAUDE_TOOL_INPUT` | Hook env var: tool input as JSON | Available in all hook commands |
| `$CLAUDE_TOOL_OUTPUT` | Hook env var: tool result | Available in PostToolUse hooks |

## Next Steps

Proceed to **Level 7 — Advanced Configuration** to learn how to layer settings across global and project scopes, configure environment variables, set up network proxies, and connect Claude Code to alternative model providers such as AWS Bedrock and Google Vertex AI.

---

## Anthropic Academy Resources

Official lessons that complement this level:

### Claude Code in Action — Hooks
- [Introducing hooks](https://anthropic.skilljar.com/claude-code-in-action/312000)
- [Defining hooks](https://anthropic.skilljar.com/claude-code-in-action/312002)
- [Implementing a hook](https://anthropic.skilljar.com/claude-code-in-action/312003)
- [Gotchas around hooks](https://anthropic.skilljar.com/claude-code-in-action/312423)
- [Useful hooks!](https://anthropic.skilljar.com/claude-code-in-action/312004)
- [Another useful hook](https://anthropic.skilljar.com/claude-code-in-action/312427)
- [Custom commands](https://anthropic.skilljar.com/claude-code-in-action/303234)

### Introduction to Agent Skills
- [What are skills?](https://anthropic.skilljar.com/introduction-to-agent-skills/434525)
- [Creating your first skill](https://anthropic.skilljar.com/introduction-to-agent-skills/434527)
- [Configuration and multi-file skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434526)
- [Skills vs. other Claude Code features](https://anthropic.skilljar.com/introduction-to-agent-skills/434528)
- [Sharing skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434529)
- [Troubleshooting skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434530)

### Introduction to Subagents
- [What are subagents?](https://anthropic.skilljar.com/introduction-to-subagents/450698)
- [Creating a subagent](https://anthropic.skilljar.com/introduction-to-subagents/450699)
- [Designing effective subagents](https://anthropic.skilljar.com/introduction-to-subagents/450700)
- [Using subagents effectively](https://anthropic.skilljar.com/introduction-to-subagents/450701)

### Claude with the Anthropic API
- [Workflows vs agents](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287794)
