# Claude Code — Command Cheatsheet

A complete reference for slash commands available in Claude Code interactive sessions. Commands are typed directly into the Claude prompt. Some commands open a sub-menu or wizard; others execute immediately.

---

## Slash Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show all available commands and their descriptions | `/help` |
| `/model` | Switch the AI model for the current session | `/model haiku` |
| `/effort` | Set reasoning depth (affects token usage and response quality) | `/effort high` |
| `/clear` | Start a fresh conversation (clears context, keeps settings) | `/clear` |
| `/context` | Show current context window usage (tokens used vs. available) | `/context` |
| `/cost` | Show token usage and estimated cost for the current session | `/cost` |
| `/copy` | Copy the last Claude response to the clipboard | `/copy` |
| `/export` | Export the full conversation to a file | `/export` |
| `/resume` | Continue a previous session by selecting from recent sessions | `/resume` |
| `/branch` | Fork the current conversation into a new branch | `/branch` |
| `/rewind` | Go back to a previous checkpoint in the conversation | `/rewind` |
| `/plan` | Enter plan mode — Claude shows a plan before executing anything | `/plan` |
| `/loop [interval]` | Run a prompt repeatedly on a fixed interval | `/loop 5m check for failing tests` |
| `/schedule` | Create a persistent cloud routine that runs on a cron schedule | `/schedule` |
| `/memory` | Open and edit the CLAUDE.md file for the current project | `/memory` |
| `/permissions` | View and manage tool access rules (allow/deny) for this session | `/permissions` |
| `/config` | Open the settings configuration viewer | `/config` |
| `/status` | View account information, plan, and usage limits | `/status` |
| `/debug` | Enable debug logging for the current session | `/debug` |
| `/doctor` | Diagnose installation issues and verify configuration | `/doctor` |
| `/mcp` | Show connected MCP servers and their available tools | `/mcp` |
| `/ide` | Manage IDE integrations (VS Code, JetBrains, etc.) | `/ide` |
| `/agents` | Manage subagent configurations for parallel workstreams | `/agents` |
| `/skills` | List all available custom skills (slash commands) | `/skills` |
| `/security-review` | Run a security vulnerability scan on changed files | `/security-review` |
| `/review` | Run a code review on changed or specified files | `/review` |
| `/simplify` | Run a code quality pass to improve readability and reduce complexity | `/simplify` |
| `/ultrareview` | Deep multi-agent code review with multiple perspectives | `/ultrareview` |
| `/ultraplan` | Draft complex plans in a cloud sandbox before executing locally | `/ultraplan` |
| `/batch` | Apply a change at scale across many files | `/batch "add JSDoc to all exports"` |
| `/usage` | Check current plan limits and how much of each limit is used | `/usage` |
| `/feedback` | Report a bug or send feedback to Anthropic | `/feedback` |
| `/release-notes` | View the release notes for the currently installed version | `/release-notes` |

---

## Key Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Escape` | Interrupt Claude mid-response (stops generation; Claude can resume) |
| `Ctrl+C` | Exit the Claude Code session entirely |
| `Up Arrow` | Recall the previous prompt (prompt history navigation) |
| `Ctrl+L` | Clear the terminal screen (does not clear conversation context) |

---

## Notes on Specific Commands

**`/loop`** — The interval is optional. `/loop check for errors` without an interval lets Claude self-pace the repetition. Press `Escape` to stop a running loop.

**`/plan`** — Plan mode applies to the current task. Claude shows a numbered list of steps it intends to take and waits for confirmation before proceeding. Type "go" or press Enter to approve, or edit the plan before approving.

**`/branch`** — Branching creates a parallel conversation from the current point. Useful when you want to try two different approaches without losing the first one.

**`/rewind`** — Rewind goes back to a checkpoint (typically after a significant Claude action). The conversation continues from the rewound point; actions taken after the checkpoint are undone in the conversation but not in the filesystem unless you explicitly undo them.

**`/batch`** — Designed for sweeping changes across many files. Claude will show you the scope of the change before executing. Pair with `/plan` mode for large batches.
