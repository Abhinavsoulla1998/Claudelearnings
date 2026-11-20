# Level 7 — Advanced Configuration
> Audience: Team Lead, Developer | Duration: Days 25–26 | Prerequisites: Level 6

## Overview

Fine-tune Claude Code for your team: layered settings (global vs project), environment variables, network configuration, and alternative model providers (AWS Bedrock, Google Vertex AI).

Claude Code reads settings from two locations and merges them. Understanding the merge order lets you establish org-wide defaults in global settings while allowing individual projects to override specific values.

---

## 1. Settings and Configuration

### Settings File Locations

| Scope | Path | Applies to |
|-------|------|------------|
| Global (user) | `~/.claude/settings.json` | All Claude sessions for this OS user |
| Project | `.claude/settings.json` | Sessions started inside this repo |
| Local override | `.claude/settings.local.json` | Project overrides not committed to git |

**Merge order**: Global settings are loaded first. Project settings are merged on top, with project values taking precedence. `settings.local.json` takes precedence over `settings.json` at the same level.

Commit `.claude/settings.json` to source control so the whole team shares the same project-level configuration. Add `.claude/settings.local.json` to `.gitignore` for personal overrides.

### Full `settings.json` Schema

```json
{
  "model": "claude-sonnet-4-6",
  "effort": "normal",
  "theme": "dark",
  "editorMode": false,
  "permissionMode": "default",
  "hooks": {
    "PreToolUse": [],
    "PostToolUse": [],
    "Stop": [],
    "Start": []
  },
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run lint)",
      "Read(**)"
    ],
    "deny": [
      "Bash(git push*)",
      "Bash(rm -rf*)",
      "Bash(sudo *)"
    ]
  },
  "env": {
    "NODE_ENV": "development",
    "LOG_LEVEL": "debug"
  }
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `model` | string | Default model for new sessions. Valid values: `claude-opus-4-5`, `claude-sonnet-4-6`, `claude-haiku-4-5`. |
| `effort` | string | Default reasoning depth: `low`, `normal`, or `high`. Higher effort increases token usage. |
| `theme` | string | Terminal color theme: `dark`, `light`, or `auto`. |
| `editorMode` | boolean | When true, Claude reads the file before editing rather than requiring full content in the prompt. |
| `permissionMode` | string | Default permission mode: `default`, `plan`, `auto`, or `bypassPermissions`. |
| `hooks` | object | Shell commands to run on Claude events. See Level 6. |
| `permissions.allow` | array | Tool call patterns that are pre-approved and will not prompt. |
| `permissions.deny` | array | Tool call patterns that are always blocked. Deny takes precedence over allow. |
| `env` | object | Environment variables injected into every Claude session and hook command. |

### Permission Pattern Syntax

Patterns use the format `ToolName(argument-pattern)`. Glob wildcards are supported.

```
Bash(npm test)          — exact match
Bash(npm test -- *)     — npm test with any arguments
Bash(git push*)         — any git push variant (deny)
Read(**)                — any file read
Edit(src/**)            — edits under the src/ directory only
Edit(.env*)             — deny editing .env files
```

See `examples/settings-global.json` and `examples/settings-project.json` for fully annotated examples.

---

## 2. Environment Variables

Claude Code reads configuration from environment variables in addition to `settings.json`. Environment variables take precedence over the `env` block in `settings.json`.

### Authentication and API

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key. Required for direct API access. |
| `CLAUDE_CODE_USE_BEDROCK` | Set to `true` to route requests through AWS Bedrock. |
| `CLAUDE_CODE_USE_VERTEX` | Set to `true` to route requests through Google Vertex AI. |

### AWS Bedrock Variables

| Variable | Purpose |
|----------|---------|
| `AWS_ACCESS_KEY_ID` | AWS access key for Bedrock authentication. |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key for Bedrock authentication. |
| `AWS_SESSION_TOKEN` | AWS session token (for temporary credentials via STS). |
| `AWS_REGION` | AWS region where Bedrock is enabled (e.g., `us-east-1`). |

### Google Vertex AI Variables

| Variable | Purpose |
|----------|---------|
| `CLOUD_ML_REGION` | Google Cloud region for Vertex AI (e.g., `us-east5`). |
| `ANTHROPIC_VERTEX_PROJECT_ID` | Your Google Cloud project ID. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to a service account key JSON file (alternative to `gcloud` ADC). |

### Network and Proxy Variables

| Variable | Purpose |
|----------|---------|
| `HTTPS_PROXY` | HTTPS proxy URL for all Claude Code outbound requests. |
| `HTTP_PROXY` | HTTP proxy URL. |
| `NO_PROXY` | Comma-separated list of hostnames to bypass the proxy. |
| `NODE_EXTRA_CA_CERTS` | Path to a PEM file with additional CA certificates (for corporate TLS inspection). |

### Setting Variables

You can set variables in three places:

1. **Shell profile** (`~/.bashrc`, `~/.zshrc`) — permanent, applies to all sessions.
2. **`env` block in `settings.json`** — applies to Claude sessions only, committed with project settings.
3. **Inline before the command** — `ANTHROPIC_API_KEY=xxx claude "query"` — one-time override.

---

## 3. Network Configuration

### Corporate Proxy

If your organization routes traffic through an HTTP proxy, set the proxy variables in your shell profile:

```bash
export HTTPS_PROXY="https://proxy.corp.example.com:8080"
export NO_PROXY="localhost,127.0.0.1,.corp.example.com"
```

Or in `settings.json`:

```json
{
  "env": {
    "HTTPS_PROXY": "https://proxy.corp.example.com:8080",
    "NO_PROXY": "localhost,127.0.0.1,.corp.example.com"
  }
}
```

### TLS Inspection / Custom CA Certificates

If your organization performs TLS inspection with a corporate CA certificate:

```bash
export NODE_EXTRA_CA_CERTS="/etc/ssl/certs/corporate-ca.pem"
```

### Offline and Air-Gapped Environments

Claude Code requires network access to the Anthropic API (or to Bedrock/Vertex endpoints) to function. It cannot run fully offline. For air-gapped environments:

- Use AWS Bedrock with a VPC endpoint to keep traffic within your private network.
- Use Google Vertex AI with Private Service Connect.
- Route all traffic through a corporate proxy that has approved access to the relevant endpoints.

---

## 4. Alternative Model Providers

### AWS Bedrock

AWS Bedrock lets you access Claude models through your AWS account. Benefits: data stays in your AWS region, billing goes through AWS, you can apply IAM policies and VPC controls.

**Prerequisites:**
- An AWS account with Bedrock enabled in your target region.
- IAM permissions: `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` on the Claude model ARNs you intend to use.
- Bedrock model access approved in the AWS console (Settings > Model access).

**Configuration:**

```bash
export CLAUDE_CODE_USE_BEDROCK=true
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key

claude "Hello from Bedrock"
```

For production use, prefer IAM roles with short-lived credentials via AWS STS rather than long-lived access keys.

See `examples/bedrock-setup.sh` for a complete setup script.

**Supported Bedrock Regions (as of 2025):** `us-east-1`, `us-west-2`, `eu-west-1`, `ap-northeast-1`. Check the AWS Bedrock documentation for the current list.

### Google Vertex AI

Vertex AI lets you access Claude models through Google Cloud. Benefits: data stays in your GCP project, billing through GCP, IAM and VPC controls.

**Prerequisites:**
- A Google Cloud project with the Vertex AI API enabled.
- The Claude model enabled in your Vertex AI console.
- Authentication via Application Default Credentials (`gcloud auth application-default login`) or a service account key.

**Configuration:**

```bash
export CLAUDE_CODE_USE_VERTEX=true
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id

claude "Hello from Vertex AI"
```

**Supported Vertex Regions:** `us-east5`, `europe-west1`, `us-central1`. Check the Vertex AI documentation for the current list. Not all Claude models are available in all regions.

### Choosing a Provider

| Consideration | Direct API | AWS Bedrock | Google Vertex AI |
|---------------|------------|-------------|------------------|
| Billing | Anthropic invoice | AWS invoice | GCP invoice |
| Data residency | Anthropic infrastructure | Your AWS region | Your GCP region |
| IAM / access control | Anthropic API keys | AWS IAM | GCP IAM |
| VPC / private networking | No | Yes (VPC endpoints) | Yes (Private Service Connect) |
| Setup complexity | Low | Medium | Medium |
| Best for | Individual developers | AWS-first organizations | GCP-first organizations |

---

## 7.4 Network & Infrastructure

Links:
- [Network Configuration](https://code.claude.com/docs/en/network-config) — Proxy and firewall setup
- [Terminal Configuration](https://code.claude.com/docs/en/terminal-config) — Terminal-specific setup
- [Dev Container Support](https://code.claude.com/docs/en/devcontainer) — Use Claude Code in dev containers

Configure Claude Code to work through corporate proxies and firewalls using standard `HTTP_PROXY` / `HTTPS_PROXY` env vars. Dev Container support means Claude Code works inside VS Code devcontainers and GitHub Codespaces without additional setup.

**Exercise**
If you use a proxy, add to your shell profile:
```bash
export HTTP_PROXY="http://proxy.company.com:8080"
export HTTPS_PROXY="http://proxy.company.com:8080"
```
Then run `claude /doctor` to verify connectivity.

---

## 7.5 Voice & Accessibility

Links:
- [Voice Dictation](https://code.claude.com/docs/en/voice-dictation) — Use voice input with Claude Code
- [/voice Command](https://code.claude.com/docs/en/commands) — Toggle voice mode

Voice Dictation lets you speak prompts to Claude Code instead of typing. Run `/voice` to enable it, then speak your prompt — Claude transcribes and responds normally.

**Best Practices**
1. Voice works best for high-level prompts ("refactor this function to be more readable") rather than precise technical specs.
2. Always review Claude's interpretation before confirming.

---

## 7.6 Cost Management & Monitoring

Links:
- [Costs](https://code.claude.com/docs/en/costs) — Understand Claude Code pricing and token costs
- [/cost Command](https://code.claude.com/docs/en/commands) — View token usage statistics for the current session
- [Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage) — Track API usage across sessions
- [/usage Command](https://code.claude.com/docs/en/commands) — Check plan limits and rate limits

Use `/cost` at any point in a session to see how many tokens have been consumed. Use `/usage` to check your plan limits and remaining rate-limit headroom.

**Best Practices**
1. Run `/cost` at the end of complex tasks to build intuition for what operations are expensive.
2. For long CI runs, use `--model haiku` to reduce cost on straightforward tasks.
3. Set spending alerts in your Anthropic account dashboard to avoid surprise bills.

---

## 7.7 Server-Managed Settings

Links:
- [Server-Managed Settings](https://code.claude.com/docs/en/server-managed-settings) — Enterprise policy enforcement via server-side settings

Server-Managed Settings allow enterprise administrators to push configuration to all Claude Code installations in their organization — enforcing approved models, permission modes, and deny rules without requiring each user to configure manually. Individual users cannot override server-managed settings.

**When to use:** Organizations that need compliance guarantees — e.g., all users must use `plan` permission mode, or certain file paths are always off-limits.

---

## Summary

| Topic | Key point |
|-------|-----------|
| Settings merge order | Global < Project < Local override |
| Commit project settings | `.claude/settings.json` is for the team; `.claude/settings.local.json` is personal |
| Permission patterns | `ToolName(glob)` syntax; deny always wins over allow |
| Environment variables | Override any `settings.json` value; keep secrets out of committed files |
| Network proxy | Set `HTTPS_PROXY` and `NODE_EXTRA_CA_CERTS` for corporate environments |
| Bedrock | Set `CLAUDE_CODE_USE_BEDROCK=true` plus AWS credentials and region |
| Vertex AI | Set `CLAUDE_CODE_USE_VERTEX=true` plus GCP project and region |

## Next Steps

Proceed to **Level 8 — Agent SDK** to learn how to build programmatic agents using the Claude Code SDK from Python or TypeScript, enabling custom automation pipelines, CI tools, and intelligent data analysis scripts.

---

## Anthropic Academy Resources

Official lessons that complement this level:

### Claude with the Anthropic API
- [Accessing the API](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287726)
- [Getting an API key](https://anthropic.skilljar.com/claude-with-the-anthropic-api/296766)
