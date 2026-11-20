# Claude Code — Permission Modes

Permission modes control how much autonomy Claude Code has when taking actions on your machine. Every tool call (file edit, shell command, web request) goes through the permission system before executing. The mode you choose determines which actions require explicit approval and which are automatically allowed.

Choosing the right mode is about balancing speed and safety for the specific situation. There is no universally best mode — the right choice depends on what you are doing, where you are doing it, and how much you trust the inputs Claude is working with.

---

## Mode Comparison

| Mode | What Claude asks permission for | Best for |
|------|--------------------------------|----------|
| `default` | File edits, shell commands, external requests — prompts before each | General use, new projects, sessions you haven't configured yet |
| `plan` | Everything — shows the full intended action plan before doing anything | First sessions on a codebase, large changes, risky operations, untrusted content |
| `auto` | Nothing safe — only truly destructive operations that match no allow rule | Daily use once you have a tuned `settings.json` with specific allow rules |
| `bypassPermissions` | Nothing — all permission checks disabled | Sandboxed CI/CD pipelines only — never on a developer machine |

---

## Project Settings: Allow and Deny Syntax

Allow and deny rules live in `.claude/settings.json` under `permissions.allow` and `permissions.deny`. The pattern format is:

```
ToolName(argument-glob)
```

`ToolName` is case-sensitive and must match the tool name exactly. The argument portion supports glob wildcards (`*` matches any characters except `/`; `**` matches any characters including `/`).

**Deny rules always take precedence over allow rules.** If a tool call matches both an allow rule and a deny rule, it is blocked.

### Concrete Examples

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm test -- *)",
      "Bash(git status)",
      "Bash(git diff*)",
      "Read(**)",
      "Edit(src/**)",
      "Edit(test/**)"
    ],
    "deny": [
      "Bash(git push*)",
      "Bash(rm -rf*)",
      "Bash(sudo *)",
      "Edit(.env*)",
      "Write(.env*)"
    ]
  }
}
```

### Pattern Reference

| Pattern | Meaning |
|---------|---------|
| `Bash(npm test)` | Allow running `npm test` with no arguments |
| `Bash(npm test -- *)` | Allow running `npm test` with any arguments after `--` |
| `Bash(git push*)` | Deny any command starting with `git push` (any flags, remotes, branches) |
| `Read(**)` | Allow reading any file anywhere in the project |
| `Edit(src/**)` | Allow editing any file under the `src/` directory (any depth) |
| `Edit(.env*)` | Deny editing any file whose name starts with `.env` |
| `Bash(curl * | bash)` | Deny curl-pipe-bash (supply chain attack vector) |
| `Bash(sudo *)` | Deny all commands starting with `sudo` |

---

## Decision Guide

Use this guide to choose the right mode for your current situation:

**Starting on a new project you have not used Claude Code with before**
Use `plan` mode. You do not yet know what Claude might try to do. Reviewing the plan before execution prevents surprises and builds your mental model of what Claude considers within scope.

**Running tests and linting as part of a refactor session**
Add `Bash(npm test)`, `Bash(npm run lint)`, and similar to your allow list, then use `auto` mode. You have approved these specific operations; there is no value in being prompted for them every time.

**Beginning a large refactor that touches many files**
Use `plan` mode for this task specifically (set it with `--permission-mode plan` for this session only). Review the scope before allowing execution.

**Daily development work in a repo with a tuned `settings.json`**
Use `auto` mode. The allow list covers your routine operations; the deny list blocks dangerous ones. Occasional prompts for unusual operations are expected and appropriate.

**CI/CD automation with no human available to approve actions**
Use `auto` mode with a carefully crafted allow list and deny list in the project `settings.json`. The agent must not block on a permission prompt because there is nobody to respond.

**Analyzing untrusted content (user-submitted text, web pages, third-party data)**
Use `plan` mode. Untrusted content may contain prompt injection — instructions embedded in the content designed to make Claude take actions the content author wants rather than what you want. Reviewing the plan before execution is your defense.

**Running in a sandboxed container with no production access**
`bypassPermissions` is acceptable here because the blast radius is limited to the container. Still, prefer `auto` with explicit allow rules — `bypassPermissions` should be a last resort even in containers.

**Production environment or any machine with production credentials**
Never use `bypassPermissions`. Use `default` or `plan`. If you need automation, use `auto` with a restrictive allow list and ensure production credentials are not accessible from the session.

---

## Setting the Mode

**For a single session (CLI flag):**
```bash
claude --permission-mode plan "Refactor the authentication module"
```

**In project settings (applies to all sessions in this repo):**
```json
{
  "permissionMode": "auto"
}
```

**In global settings (applies to all sessions):**
```json
{
  "permissionMode": "default"
}
```

**During a session:**
```
/permissions
```
Opens the permission manager where you can view current rules and change the mode for the current session.
