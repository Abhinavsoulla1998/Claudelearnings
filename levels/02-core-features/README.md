# Level 2 — Core Features
> Audience: Everyone | Duration: Days 4–7 | Prerequisites: Level 1

## Overview
Master the features you will use in every Claude Code session: project memory with CLAUDE.md, slash commands, permission modes, model selection, and session management. This level has the highest return on investment — CLAUDE.md alone can save hours of repeated context-setting.

## What You'll Learn
- Create a CLAUDE.md that makes Claude understand your project without prompting
- Use slash commands to manage context, cost, and conversation flow
- Configure permissions so Claude can run your tests automatically but cannot push code
- Choose the right model for each task to balance quality and cost
- Save and resume sessions without losing work

---

## 2.1 Commands & Slash Commands

### Reference Links
- [Commands Reference — Complete list of all commands](https://docs.anthropic.com/en/docs/claude-code/commands)
  - `/help`, `/model`, `/effort`, `/clear`, `/copy`, `/export`, `/resume`, `/branch`, `/rewind`, `/config`, `/status`

### Code

```bash
# Inside a Claude session — most-used command sequence
/model          # View current model and switch
/effort high    # Set reasoning depth for complex tasks
/context        # Check how much context window is consumed
/cost           # See tokens used so far this session
/export         # Save transcript before clearing
/clear          # Wipe context, start fresh in same session
```

### Command Reference Table

| Command | What it does | Category |
|---|---|---|
| `/help` | List all available commands | Navigation |
| `/status` | View account, current model, session ID | Info |
| `/cost` | Show token usage and estimated cost for this session | Cost |
| `/context` | Show what % of the context window is consumed | Context |
| `/clear` | Wipe conversation context (keep session open) | Context |
| `/export` | Save full conversation transcript to a file | Context |
| `/model [name]` | Switch AI model (haiku / sonnet / opus) | Model |
| `/effort [low/high]` | Adjust reasoning depth | Model |
| `/fast` | Toggle fast output mode (Opus only) | Model |
| `/branch` | Checkpoint current conversation state | Session |
| `/rewind` | Return to last checkpoint | Session |
| `/resume` | List and resume previous sessions | Session |
| `/memory` | Open and edit CLAUDE.md in your editor | Memory |
| `/permissions` | View and manage current allow/deny rules | Permissions |
| `/plan` | Enter plan-review mode mid-session | Planning |
| `/review` | Code review of all changed files in the branch | Quality |
| `/security-review` | Security-focused vulnerability scan | Quality |
| `/simplify` | Simplify overly complex code | Quality |
| `/ultrareview` | Deep multi-agent review (thorough, expensive) | Quality |
| `/config` | Open settings UI (theme, model, permissions) | Settings |
| `/doctor` | Diagnose installation and auth issues | Debug |
| `/debug` | Enable verbose debug logging | Debug |

### Exercise

1. Start a Claude session and have a short conversation (3–4 exchanges)
2. Run `/context` — note the percentage consumed
3. Run `/branch` to create a checkpoint
4. Ask Claude to take a different approach to the last question
5. Run `/rewind` to go back to the checkpoint

**Success criterion:** After `/rewind`, the conversation is back at the state before the alternative approach, and your files are unchanged.

### Best Practices

1. Check `/context` before submitting a large file paste — if above 70%, run `/clear` or start a new session to avoid truncation.
2. Use `/effort low` for simple lookups and file searches; use `/effort high` only for architecture decisions and complex debugging — this single habit can cut costs by 30–50%.
3. Run `/export` at the end of any long session before clearing — saved transcripts are useful for writing up what was done.

### Guardrails

> **WARNING:** `/clear` is irreversible within a session. If Claude has produced an important plan or intermediate result, run `/export` first to save it.

---

## 2.2 Project Memory & CLAUDE.md

### Reference Links
- [Memory (CLAUDE.md) — Create persistent project memory](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Context Window — Understand token limits](https://docs.anthropic.com/en/docs/claude-code/context-window)
- [/context Command — Visualize context usage](https://docs.anthropic.com/en/docs/claude-code/commands#context)

### Code

```bash
# Edit or create CLAUDE.md from inside a session
/memory

# Verify Claude read your CLAUDE.md at session start
claude "Summarize what you know about this project from CLAUDE.md"
```

> **Template:** See `templates/CLAUDE.md.template` in this folder for a complete starter template.

### Minimal CLAUDE.md Example

A focused 30-line CLAUDE.md outperforms a vague 200-line one. Here is a realistic example for a Node.js/TypeScript service:

````markdown
# Project: payment-service

## Tech Stack
- Runtime: Node.js 20, TypeScript 5.4
- Framework: Fastify 4
- ORM: Drizzle + PostgreSQL 15
- Tests: Vitest + supertest
- Lint: ESLint (airbnb config) + Prettier

## Commands
- Run tests: `npm test`
- Run tests with coverage: `npm run test:cov`
- Lint: `npm run lint`
- Build: `npm run build`
- Dev server: `npm run dev`

## Conventions
- All exported functions must have explicit TypeScript return types
- Error handling: throw typed errors, never return `null` to signal errors
- File names: kebab-case.ts
- Exports: named exports only — no default exports
- Validation: Zod schemas live in `src/schemas/`

## Architecture
- Route handlers → Service layer → Repository layer
- No database queries outside of repository files
- Async/await only — no callbacks or raw Promises

## Off-Limits
- Do NOT modify: `drizzle/migrations/` — auto-generated
- Do NOT edit: `.env`, `.env.local`
- Do NOT commit secrets, API keys, or connection strings
````

**Five sections every CLAUDE.md needs:**
1. **Tech Stack** — exact versions; Claude uses these to pick correct APIs
2. **Commands** — how to run tests and lint; Claude uses these autonomously
3. **Conventions** — naming, error handling, export style; the most-violated rules in generated code
4. **Architecture** — which layers exist and what belongs in each
5. **Off-Limits** — directories and files Claude must never modify

### Exercise

> **Files:** `templates/CLAUDE.md.template`, `exercises/01-setup-memory.md`

1. Copy `templates/CLAUDE.md.template` to your project root as `CLAUDE.md`
2. Fill in your actual tech stack, commands, and conventions
3. Start a new Claude session and ask: "What do you know about this project?"
4. Verify Claude references your CLAUDE.md content specifically (not a generic answer)
5. Ask Claude to write a small feature — verify it follows the conventions you documented

**Success criterion:** Claude generates code that follows the conventions in your CLAUDE.md (naming, error handling, file locations) without you repeating them in the prompt.

### Best Practices

1. Keep the "Commands" section current — Claude uses it to run tests and linting autonomously.
2. Add an "Off-Limits" section for directories Claude must never modify (generated code, vendor directories, migration files).
3. Document the error-handling pattern explicitly — it is the convention most often violated by generated code.
4. Treat CLAUDE.md like code: commit it, review changes in PRs, update it when conventions change.
5. In monorepos, add sub-project CLAUDE.md files in each package — Claude reads them hierarchically.

### Guardrails

> **WARNING:** Do not put secrets, API keys, or database credentials in CLAUDE.md. It is committed to version control and read at every session start.

> **WARNING:** A stale CLAUDE.md actively causes harm — Claude will confidently follow outdated conventions. Review and update it when your tech stack or patterns change.

---

## 2.3 Permissions & Security

### Reference Links
- [Permission Modes — default, plan, auto, bypassPermissions](https://docs.anthropic.com/en/docs/claude-code/permission-modes)
- [Permissions — Fine-grained access control](https://docs.anthropic.com/en/docs/claude-code/permissions)
- [Security — Security best practices](https://docs.anthropic.com/en/docs/claude-code/security)
- [Data Usage — How your data is handled](https://docs.anthropic.com/en/docs/claude-code/data-usage)

### Code

```bash
# Start in plan mode — Claude shows what it WILL do before doing it
claude --permission-mode plan

# Start in auto mode — Claude handles safe operations without prompting
claude --permission-mode auto

# Check current permission rules inside a session
/permissions
```

```json
// .claude/settings.json — project-level permission rules
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run lint)",
      "Bash(npm run build)",
      "Read(**)",
      "Edit(src/**)"
    ],
    "deny": [
      "Bash(git push*)",
      "Bash(git push --force*)",
      "Bash(rm -rf*)",
      "Bash(sudo*)",
      "Edit(.env*)"
    ]
  }
}
```

### Managing Permissions Mid-Session

```bash
# View what is currently allowed and denied
/permissions

# When Claude prompts during a session:
# "Run npm install? [y/n/always/never]"
#   y      — allow this one time
#   n      — deny this one time
#   always — allow for the rest of this session
#   never  — deny for the rest of this session
# Permanent rules go in .claude/settings.json
```

**Settings file hierarchy** (each level overrides the one above):

| File | Scope | Committed to git? |
|---|---|---|
| `~/.claude/settings.json` | All your projects (personal defaults) | No |
| `.claude/settings.json` | This project (team-shared) | Yes |
| `.claude/settings.local.json` | This project (personal overrides) | No (gitignore it) |
| `--permission-mode` flag | This session only | N/A |

### Exercise

> **Files:** `exercises/settings.json.example`

1. Create `.claude/settings.json` in your project with the allow/deny rules above (adjusted for your test command)
2. Start a Claude session and ask it to fix a failing test
3. Observe that Claude runs your test command without a permission dialog
4. Ask Claude to run `git push` — confirm it is blocked

**Success criterion:** Test command runs without a permission prompt; `git push` is denied.

### Best Practices

1. Default to `plan` mode for the first week on any new project — reviewing plans teaches you what Claude does before trusting `auto`.
2. Always deny `git push` and `git push --force` at the project level — these should always be manual human actions.
3. Use project-level `.claude/settings.json` for team-shared rules (commit it); use `~/.claude/settings.json` for personal defaults.

### Guardrails

> **WARNING:** `bypassPermissions` mode disables all safety checks. Never use it on production systems, shared machines, or codebases containing credentials or PII. It exists only for fully sandboxed, isolated environments.

> **WARNING:** `Bash(*)` in the allow list grants Claude unrestricted shell access — equivalent to giving it your terminal. Always be specific: `Bash(npm test)` not `Bash(*)`.

---

## 2.4 Model Selection & Configuration

### Reference Links
- [Model Configuration — Choose and configure models](https://docs.anthropic.com/en/docs/claude-code/model-configuration)
- [Fast Mode — Speed up responses](https://docs.anthropic.com/en/docs/claude-code/fast-mode)
- [Effort Levels — Control reasoning depth](https://docs.anthropic.com/en/docs/claude-code/effort-levels)

### Code

```bash
# Shorthand model names
claude --model haiku     # Fast, cheap
claude --model sonnet    # Balanced (default)
claude --model opus      # Most capable

# Full model IDs for pinning exact versions
claude --model claude-haiku-4-5-20251001
claude --model claude-sonnet-4-6
claude --model claude-opus-4-7

# Inside a session — switch models on the fly
/model haiku      # Switch to Haiku (fast, cheap)
/model sonnet     # Switch to Sonnet (balanced)
/model opus       # Switch to Opus (most capable)

# Set effort level
/effort low       # For lookups and simple tasks
/effort high      # For complex debugging and architecture

# Fast mode — faster output at same quality level (Opus only)
/fast
```

### Model Comparison

| Model | Best for | Relative cost | Speed |
|---|---|---|---|
| **Haiku** | File lookups, simple Q&A, grep-style queries, listing | 1x | Fastest |
| **Sonnet** | Code generation, debugging, refactoring, test writing | ~10x | Fast |
| **Opus** | Architecture review, complex multi-step reasoning, security audits | ~30x | Slower |

**Rule of thumb:** one sentence → Haiku. Writing or changing code → Sonnet. System design or security → Opus + high effort.

### Effort Levels

| Level | When to use | Token impact |
|---|---|---|
| `low` | File searches, "what does X do", listing all usages | Minimal |
| `medium` | Standard code gen, debugging, refactoring (default) | Normal |
| `high` | Architecture decisions, complex multi-file reasoning, security review | +30–50% |

### Exercise

1. Start a session with `/model haiku`
2. Ask it to explain a complex function in your codebase
3. Run `/cost` — note the token count
4. Switch to `/model sonnet` with `/model sonnet`
5. Ask the same question and run `/cost` again

**Success criterion:** You can articulate which model class you would choose for: quick file lookups (Haiku), code generation (Sonnet), architecture review (Sonnet + high effort).

### Best Practices

1. Use Haiku for: file searches, "what does this variable do" questions, listing files, simple grep-style tasks — it is ~10x cheaper than Sonnet.
2. Use Sonnet for: code generation, debugging, refactoring, writing tests.
3. Reserve high effort (`/effort high`) for architecture design, complex multi-file refactors, and security analysis — not as a default.

### Guardrails

> **WARNING:** `/effort high` significantly increases token consumption and cost per query. Do not set it as your session default — enable it deliberately for tasks that require deep reasoning.

---

## 2.5 Session Management

### Reference Links
- [Checkpointing — Save and restore conversation states](https://docs.anthropic.com/en/docs/claude-code/checkpointing)
- [/rewind Command — Navigate conversation history](https://docs.anthropic.com/en/docs/claude-code/commands#rewind)
- [/resume Command — Continue previous sessions](https://docs.anthropic.com/en/docs/claude-code/commands#resume)
- [/branch Command — Fork conversations](https://docs.anthropic.com/en/docs/claude-code/commands#branch)

### Code

```bash
# Continue the most recent session
claude -c

# Resume a specific session by ID (get ID from /status)
claude -r "session-id-here"

# Inside a session: create a checkpoint before a risky operation
/branch

# If the operation goes wrong: return to the checkpoint
/rewind
```

### Finding and Resuming Sessions

```bash
# List recent sessions with timestamps and initial prompts
claude --list-sessions

# Resume most recent session
claude -c

# Resume a specific session by ID
claude -r "session-id-here"

# Get the current session ID (note it down if you want to resume later)
/status
```

**Session hygiene pattern:**
```bash
# End of work session
/export                    # Save transcript
/status                    # Note the session ID

# Next day — related task
claude -c                  # Resume with context intact

# Next day — different task
claude "..."               # Start fresh, no -c flag
```

**When to start fresh vs. resume:**
- Resume (`-c`) when: continuing the same task, the codebase context is still relevant
- Start fresh when: switching to an unrelated task, `/context` shows >70%, more than 2 days have passed

### Exercise

1. Start a session and ask Claude to make a small edit to a file
2. Run `/branch` to create a checkpoint
3. Ask Claude to make a second, larger edit
4. Run `/rewind` to undo the second edit
5. Verify the file matches its state after the first edit (second edit is gone)

**Success criterion:** The file content matches the checkpoint state; the second edit is cleanly removed.

### Best Practices

1. Create a `/branch` checkpoint before any large-scale refactor, file deletion, or database migration operation.
2. Use `claude -c` for related tasks within the same day; start a fresh session for an unrelated task to avoid context pollution.
3. Run `/export` before long weekends or vacations — sessions expire server-side after a period of inactivity.

### Guardrails

> **WARNING:** Session state is stored server-side with a time-to-live limit. Do not rely on `/resume` for sessions older than a few days — the context may be gone even if the session ID is still valid locally.

---

## Summary

| Concept | What it does | When to use |
|---------|-------------|-------------|
| `CLAUDE.md` | Persistent project memory Claude reads every session | Every project — set it up once, benefit forever |
| `--permission-mode plan` | Review plan before Claude executes anything | First sessions on new projects; risky operations |
| `--permission-mode auto` | Allow safe operations without prompting | Daily use once you trust the project's allow/deny rules |
| `/branch` | Create a conversation checkpoint | Before any large or risky change |
| `/rewind` | Return to the last checkpoint | After a change that went wrong |
| `/effort high` | Deep reasoning mode | Complex architecture, security analysis |
| Haiku model | Fast, cheap model | Lookups, searches, simple questions |
| Sonnet model | Balanced model | Code generation, debugging, refactoring |

## Next Steps

[Level 3 — Daily Dev Workflows](../03-daily-dev-workflows/README.md)

---

## Anthropic Academy Resources

Official lessons that complement this level:

### Claude Code in Action
- [Adding context](https://anthropic.skilljar.com/claude-code-in-action/303241)
- [Controlling context](https://anthropic.skilljar.com/claude-code-in-action/303237)

### Claude 101
- [Introduction to projects](https://anthropic.skilljar.com/claude-101/383393)
- [Creating with artifacts](https://anthropic.skilljar.com/claude-101/383394)

### Claude with the Anthropic API
- [System prompts](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287733)
- [Temperature](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287728)
