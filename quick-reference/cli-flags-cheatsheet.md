# Claude Code — CLI Flags Cheatsheet

A complete reference for command-line flags when invoking `claude` from your terminal. These flags control session mode, model selection, permission handling, output format, and context injection.

---

## Starting a Session

| Command | Description |
|---------|-------------|
| `claude` | Start an interactive session. Claude waits for your input. |
| `claude "query"` | Start an interactive session with an initial prompt. |
| `claude -p "query"` | Non-interactive (print) mode. Claude responds and exits immediately. Ideal for scripting. |
| `claude -c` | Continue the most recent session, restoring conversation context. |
| `claude -r "session-id"` | Resume a specific session by its ID (find IDs with `/resume`). |

---

## Model and Effort

| Flag | Description |
|------|-------------|
| `--model claude-sonnet-4-6` | Use Claude Sonnet 4.6 (balanced capability and cost — default). |
| `--model claude-opus-4-5` | Use Claude Opus 4.5 (most capable; higher cost). |
| `--model claude-haiku-4-5` | Use Claude Haiku 4.5 (fastest and cheapest; good for scripting). |
| `--effort low` | Minimal reasoning depth. Faster and cheaper. Best for simple, well-defined tasks. |
| `--effort normal` | Standard reasoning depth. The default. |
| `--effort high` | Extended thinking enabled. More thorough for complex problems. Uses more tokens. |

---

## Permission Control

| Flag | Description |
|------|-------------|
| `--permission-mode default` | Ask before file edits and shell commands. The standard starting point. |
| `--permission-mode plan` | Show a full plan of all intended actions before executing anything. Good for first sessions and risky operations. |
| `--permission-mode auto` | Auto-approve safe operations. Only prompts for genuinely destructive actions. Best used with a tuned `settings.json` allow/deny list. |
| `--permission-mode bypassPermissions` | Disable all permission checks. Use only in isolated CI/CD environments. Never use on a machine with access to production systems. |

---

## Output Control

| Flag | Description |
|------|-------------|
| `--output-format text` | Plain text output. Best for piping to other commands or scripts. |
| `--output-format json` | Structured JSON containing the full response. Good for parsing in scripts. |
| `--output-format stream-json` | Streaming JSON that includes individual tool calls and results as they happen. Useful for debugging or building monitoring dashboards. |

---

## Context and Customization

| Flag | Description |
|------|-------------|
| `--add-dir /path/to/dir` | Add a directory to Claude's working context. Claude can read files in this directory even if it is outside the current working directory. Can be specified multiple times. |
| `--system-prompt "..."` | Replace the default system prompt with a custom one. |
| `--append-system-prompt "..."` | Append additional instructions to the default system prompt without replacing it. |

---

## Debugging

| Flag | Description |
|------|-------------|
| `--debug` | Enable verbose debug logging. Outputs tool call details, timing, and internal state. |
| `--help` | Show all available flags and a brief description of each. |

---

## Common Combinations

```bash
# Review changed files in CI — non-interactive, plain text output, exits after response.
git diff HEAD~1 | claude -p "Review for bugs and security issues" --output-format text

# Non-interactive with Haiku for cost efficiency in scripts.
claude -p "summarize this file" --model claude-haiku-4-5 --output-format text < myfile.txt

# Start a fresh session in plan mode before a risky refactor.
# Claude will show the full plan before touching any files.
claude --permission-mode plan "Migrate the database schema to add a user_preferences table with JSON storage"

# Add context from a sibling repository to check API contract alignment.
claude --add-dir ../api-contracts "Do our API calls in the current repo match the contracts defined in the api-contracts repo?"

# Parse structured JSON output in a shell script.
RESULT=$(claude -p "List the top 3 TODOs in this codebase as JSON" --output-format json)
echo "$RESULT" | jq '.content[0].text'
```

---

## Notes

**`-p` vs interactive mode** — Use `-p` for any automation, CI pipeline, git hook, or script. It exits cleanly after the response, making it composable with standard Unix tools via pipes and redirection.

**`--output-format text` with `-p`** — The combination `claude -p "..." --output-format text` is the most script-friendly form. The output is plain text with no JSON wrapping, safe to pipe directly to `grep`, `awk`, `sed`, or other tools.

**`--add-dir`** — The current working directory is always in context. Use `--add-dir` only for directories outside the cwd. Useful for monorepos, shared contract repos, or documentation repos that live alongside your code.

**`--permission-mode bypassPermissions`** — This flag should never appear in a developer's shell alias or daily workflow. It is intended exclusively for sandboxed, automated environments (Docker containers, ephemeral CI runners) where there is no risk of unintended side effects on production systems.
