# Level 1 — Foundations
> Audience: Everyone | Duration: Days 1–3 | Prerequisites: None

## Overview
Get Claude Code installed, authenticated, and running your first session. By the end of this level you will have Claude Code working in your terminal and understand how to start, stop, and navigate a session.

## What You'll Learn
- Install and authenticate Claude Code
- Understand the three ways to start a session (interactive, prompted, non-interactive)
- Navigate the interface: keyboard shortcuts, output modes, status line
- Know what Claude Code can access and why permission mode matters on day one

---

## 1.1 Understanding Claude Code

### Reference Links
- [Overview — What is Claude Code? Core capabilities and use cases](https://docs.anthropic.com/en/docs/claude-code/overview)
- [How Claude Code Works — Architecture, workflow, and agentic loop](https://docs.anthropic.com/en/docs/claude-code/how-it-works)
- [Features Overview — Complete feature set at a glance](https://docs.anthropic.com/en/docs/claude-code/features)

### Code

```bash
# Verify Claude Code is installed and responsive
claude --version
claude -p "What is 2 + 2?" --output-format text
```

### Exercise

1. Run `claude --version` — confirm a version number appears
2. Run `claude -p "In one sentence, what is Claude Code?"` — confirm you get a response

**Success criterion:** Both commands return output without an authentication error within 30 seconds.

### Best Practices

1. Understand the agentic loop before using Claude on a real project: Claude reads files, proposes changes, executes commands, and iterates — it is not a chatbot.
2. Distinguish Claude Code (local CLI agent with filesystem access) from the Anthropic API (raw model calls) — they serve different purposes.
3. Start Claude from your project root directory so it discovers `CLAUDE.md` and understands project structure.

### Guardrails

> **WARNING:** Claude Code has real read/write access to your filesystem from the first session. Never start a session as a root user or in a directory containing production credentials, private keys, or `.env` files until you understand permission modes (covered in Level 2).

---

## 1.2 Installation & Setup

### Reference Links
- [Setup & Installation — Install on macOS, Linux, or Windows](https://docs.anthropic.com/en/docs/claude-code/installation)
- [Troubleshooting Installation — Fix common install issues](https://docs.anthropic.com/en/docs/claude-code/troubleshooting)
- [Authentication — Sign in and manage your account](https://docs.anthropic.com/en/docs/claude-code/authentication)
- [CLI Reference — Command-line flags and startup options](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

### Code

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Set your API key — add to ~/.bashrc or ~/.zshrc for persistence
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Verify installation and authentication
claude /status
claude /doctor
```

### Exercise

> **Files:** `exercises/01-verify-install.sh` (clone repo to run)

1. Install Claude Code with `npm install -g @anthropic-ai/claude-code`
2. Set your `ANTHROPIC_API_KEY` environment variable
3. Run `claude /status` — confirm your email and default model appear
4. Run `claude /doctor` — confirm no errors are reported

**Success criterion:** `/status` displays your account email and a model name without an "unauthorized" error.

### Best Practices

1. Store `ANTHROPIC_API_KEY` in your shell profile (`~/.bashrc` or `~/.zshrc`), not in `.env` files inside project directories.
2. Run `/doctor` immediately after install — it catches 80% of common path and dependency issues before they become confusing errors.
3. In team environments, pin a specific version: `npm install -g @anthropic-ai/claude-code@<version>` to prevent behavior drift between team members.

### Guardrails

> **WARNING:** Never commit your API key to version control. Add `ANTHROPIC_API_KEY` and `.env` to your global `~/.gitignore`. Leaked keys are automatically detected and revoked by Anthropic but can expose billing to unauthorized use in the interim.

---

## 1.3 Your First Session

### Reference Links
- [Quickstart — Run your first Claude Code session](https://docs.anthropic.com/en/docs/claude-code/quickstart)
- [Interactive Mode — Learn keyboard shortcuts and input modes](https://docs.anthropic.com/en/docs/claude-code/interactive-mode)
- [Keybindings — Customize keyboard shortcuts](https://docs.anthropic.com/en/docs/claude-code/keybindings)

### Code

```bash
# Interactive session — start in your project directory
claude

# Start with an initial prompt (still interactive after)
claude "Explain the structure of this project in 2 paragraphs"

# Non-interactive: run a query and exit — for scripts and pipelines
claude -p "List all TODO comments in this codebase" --output-format text

# Continue the most recent session
claude -c
```

### Exercise

> **Files:** `exercises/02-first-session.sh`

1. Navigate to any project directory on your machine
2. Run `claude "In one paragraph, what does this codebase do?"`
3. Read the response — verify Claude read your actual files (not a generic answer)
4. Type `/cost` to see how many tokens were consumed
5. Type `exit` to end the session

**Success criterion:** Claude produces a specific summary referencing actual file names or technology choices from your project.

### Best Practices

1. Always start Claude from the root of your project — subdirectory starts can prevent Claude from finding `CLAUDE.md` and understanding project structure.
2. Use `claude -p` (non-interactive) for automation and scripts; use interactive mode for exploratory work and multi-step tasks.
3. Press `Escape` to interrupt a long-running operation — you do not need to kill the process.
4. Use `/context` during a session to check how much of the context window has been consumed before sending large prompts.

### Guardrails

> **WARNING:** In your first session, Claude may offer to edit files immediately after exploring the codebase. Use `--permission-mode plan` for your first few sessions on a real project until you understand what Claude will touch.

> **WARNING:** Interactive sessions keep context in memory. If you walk away for hours and resume, the context may have expired. Use `claude -c` to continue but verify the session is still coherent with a quick question.

---

## 1.4 Understanding the Interface

### Reference Links
- [Output Styles — Different rendering modes](https://docs.anthropic.com/en/docs/claude-code/output-styles)
- [Fullscreen Mode — Use the fullscreen renderer](https://docs.anthropic.com/en/docs/claude-code/fullscreen-mode)
- [Status Line — Configure the status bar](https://docs.anthropic.com/en/docs/claude-code/status-line)

### Code

```bash
# Start with specific output format (useful for piping to other tools)
claude -p "List all exported functions in src/" --output-format text

# Structured JSON output — for integrating with scripts
claude -p "Describe this project" --output-format json

# Open settings to configure theme, editor mode, status line
# (run from inside an interactive session)
# /config
```

### Exercise

1. Start an interactive Claude session: `claude`
2. Type `/config` and navigate to "Theme" — change it to your preference
3. Exit and restart Claude — confirm the theme persists without re-setting

**Success criterion:** The new theme is active in the restarted session, confirming settings are persisted.

### Best Practices

1. Use `--output-format text` when piping Claude output to other shell commands — it strips formatting characters.
2. Use `--output-format json` when Claude output feeds into scripts — it gives structured, parseable data.
3. Enable the status line — it shows token consumption and model in use at a glance, which builds intuition for cost management.

### Guardrails

> **WARNING:** `--output-format stream-json` outputs raw JSON including internal tool calls and intermediate reasoning steps. Never expose this output directly to end users.

---

## 1.5 Desktop Application

Links:
- [Claude Code Desktop](https://code.claude.com/docs/en/desktop) — Desktop app overview
- [Desktop Quickstart](https://code.claude.com/docs/en/desktop-quickstart) — Get started with Desktop
- [Desktop Scheduled Tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks) — Schedule tasks in Desktop
- [/desktop Command](https://code.claude.com/docs/en/commands) — Switch to Desktop app

**What it is:** Claude Code ships as both a CLI and a native Desktop application (macOS/Windows). The Desktop app gives you a persistent window, system tray access, and scheduled background tasks — useful if you prefer not to keep a terminal open.

**Exercise**
1. If you installed via npm, download the Desktop app from [claude.ai/download](https://claude.ai/download) and sign in with the same account.
2. Open the Desktop app and run `/desktop` to confirm you're in Desktop mode.
3. Explore Desktop Scheduled Tasks — useful for daily briefings (covered in Level 7).

**Best Practices**
1. Use the CLI in your terminal for interactive coding sessions; use Desktop for background/scheduled tasks.
2. Both share the same API key and CLAUDE.md files — they are the same tool, different shells.

---

## 1.6 IDE Quick Start

Links:
- [VS Code Integration](https://code.claude.com/docs/en/vs-code) — Use Claude Code in VS Code
- [JetBrains Integration](https://code.claude.com/docs/en/jetbrains) — Use Claude Code in JetBrains IDEs
- [/ide Command](https://code.claude.com/docs/en/commands) — Manage IDE integrations

**What it is:** Claude Code integrates directly into VS Code and JetBrains IDEs. Install the extension once and you get inline diffs, a Claude panel alongside your editor, and `/ide` to sync context between terminal and editor.

**Exercise**
1. Install the Claude Code extension for your IDE (VS Code: search "Claude Code" in Extensions; JetBrains: search in Plugin Marketplace).
2. Open a project and run `/ide` from the Claude terminal — your IDE should show the Claude panel.
3. Make a small edit via Claude and accept the inline diff.

> **VS Code settings example:** See [exercises/vscode-settings.json](exercises/vscode-settings.json) in this folder — drop it into your project's `.vscode/settings.json` to configure Claude Code for VS Code.

**Best Practices**
1. Install the extension on day 1 — even if you primarily use the terminal, inline diffs save review time.
2. Use `--permission-mode plan` in the IDE extension settings so you review plans before execution.

---

## 1.7 Settings & Configuration

Links:
- [Settings](https://code.claude.com/docs/en/settings) — Configure Claude Code (theme, editor mode, model, permissions)
- [Environment Variables](https://code.claude.com/docs/en/env-vars) — Configure via env vars

**Key settings to configure on Day 1:**

| Setting | Command | Options |
|---|---|---|
| Theme | `/config` → Appearance | Light / Dark / System |
| Editor mode | `/config` → Editor | Normal / Vim |
| Default model | `/config` → Model | sonnet / opus / haiku |
| Permission mode | `/config` → Permissions | default / plan / auto |

**Key environment variables:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."     # Required
export CLAUDE_MODEL="claude-sonnet-4-6"  # Override default model
export CLAUDE_PERMISSION_MODE="plan"     # Override permission mode
```

**Exercise**
1. Run `/config` and set your preferred theme and editor mode.
2. Run `/status` to confirm your API key, model, and account tier.

**Best Practices**
1. Set `ANTHROPIC_API_KEY` in your shell profile (`~/.zshrc` or `~/.bashrc`) so every session is authenticated automatically.
2. Start with `plan` permission mode until you trust the kinds of changes Claude makes in your codebase.

> *Server-Managed Settings (enterprise policy enforcement) is covered in [Level 8 — Advanced Config](../08-advanced-config/README.md).*

---

## Summary

| Concept | What it does | When to use |
|---------|-------------|-------------|
| `claude` | Start interactive session | Exploratory work, multi-step tasks |
| `claude -p "..."` | Non-interactive single query | Scripts, pipelines, quick lookups |
| `claude -c` | Continue last session | Resuming interrupted work |
| `--permission-mode plan` | Show plan before executing | First sessions on real projects |
| `/doctor` | Diagnose install issues | Any time Claude behaves unexpectedly |
| `/cost` | Show token usage for this session | Building cost intuition |

## Next Steps

[Level 2 — Core Features](../02-core-features/README.md)

---

## Anthropic Academy Resources

Official lessons that complement this level:

### Claude Code in Action
- [Introduction](https://anthropic.skilljar.com/claude-code-in-action/303233)
- [What is a coding assistant?](https://anthropic.skilljar.com/claude-code-in-action/303235)
- [Claude Code in action](https://anthropic.skilljar.com/claude-code-in-action/303242)
- [Claude Code setup](https://anthropic.skilljar.com/claude-code-in-action/301614)
- [Project setup](https://anthropic.skilljar.com/claude-code-in-action/301615)

### Claude 101
- [What is Claude?](https://anthropic.skilljar.com/claude-101/383389)
- [Your first conversation with Claude](https://anthropic.skilljar.com/claude-101/383390)
- [Claude desktop app: Chat, Cowork, Code](https://anthropic.skilljar.com/claude-101/440908)

### Claude with the Anthropic API
- [Overview of Claude models](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287722)
- [Anthropic apps](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287787)
- [Claude Code setup](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287788)
- [Claude Code in action](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287805)
