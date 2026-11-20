# Level 5 — MCP: Connecting Your Tools
> Audience: Everyone | Duration: Days 18–21 | Prerequisites: Level 4

## Overview
MCP (Model Context Protocol) transforms Claude Code from a coding assistant into a connected agent that can query your database, read GitHub issues, search Slack channels, browse web pages, and call internal APIs — all from a natural language prompt. This level covers 6 MCP server types, building a custom server, and using MCP programmatically in the Agent SDK.

## What You'll Learn
- Configure MCP servers in .claude/settings.json
- Connect Claude to PostgreSQL, SQLite, GitHub, Slack, and browser automation
- Build a custom MCP server in TypeScript to wrap any REST API
- Use MCP programmatically in Agent SDK scripts
- Apply least-privilege security patterns to all MCP configurations

---

### 5.1 MCP Concepts & Core Configuration

Links:
- MCP (Model Context Protocol) — Connect external data sources
  - Installing MCP servers
  - Configuring MCP
  - Using MCP tools
  - MCP prompts

Code:
```bash
# Add an MCP server via CLI
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Add filesystem MCP
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /path/to/docs

# Verify connected MCP servers inside a session
/mcp

# List all configured MCP servers
claude mcp list
```

```json
// .claude/settings.json — MCP configuration block
// See examples/mcp-settings-full.json for a complete reference
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "SECRET": "${ENV_VAR_NAME}"
      }
    }
  }
}
```

Exercise:
> Files: `examples/mcp-settings-full.json`
1. Copy the filesystem section from `examples/mcp-settings-full.json` into `.claude/settings.json`
2. Point it at a directory outside your project (e.g., your Documents folder)
3. Start a Claude session and ask: "Search my documents for anything related to [topic]"
4. Verify Claude reads files from outside the project directory
Success criterion: Claude returns content from the external directory, demonstrating cross-directory access via MCP.

Best Practices:
1. Always use environment variable references (`${VAR_NAME}`) for credentials in MCP config — never hardcode passwords, tokens, or connection strings.
2. Install only MCP servers you actively use — each adds a process and expands what Claude can access.
3. Use `claude mcp list` to audit which servers are configured before starting sensitive sessions.

Guardrails:
> WARNING: Each MCP server gives Claude access to the resources you configure. Apply the principle of least privilege: use read-only database credentials, scope filesystem access to specific directories, and use API tokens with the minimum required permissions.

---

### 5.2 Database MCP (PostgreSQL + SQLite)

Links:
- Plugins — Extend Claude Code with plugins

Code:
```bash
# Set up database credentials
export PGPASSWORD="your-dev-db-password"

# Add postgres MCP
claude mcp add postgres -- npx -y @modelcontextprotocol/server-postgres \
  "postgresql://username@localhost/dev_database"
```

```bash
# With the database MCP connected, Claude can answer these questions:
claude "Show me all users created in the last 7 days who haven't confirmed their email"
claude "Find the 5 slowest queries in the last hour based on the pg_stat_statements table"
claude "What indexes are missing on the orders table based on common query patterns?"
```

Exercise:
> Files: `examples/mcp-database.json`
1. Configure the postgres MCP (or sqlite if you have no local Postgres)
2. Start a Claude session
3. Ask: "Describe the schema of the [table_name] table and identify any potential data quality issues"
4. Ask: "Show me the 10 most recent records from [table_name] and summarize any anomalies"
Success criterion: Claude queries and returns real data from your database without you writing any SQL manually.

Best Practices:
1. Always use a read-only database user for MCP connections: `CREATE USER claude_readonly WITH PASSWORD '...' IN ROLE readonly;`
2. Use the dev database, never staging or production — a misunderstood prompt could run UPDATE or DELETE.
3. Create a dedicated MCP connection string that points to a limited schema if your database contains PII.

Guardrails:
> WARNING: NEVER point the database MCP at a production database. Even with read-only credentials, Claude may run expensive queries that impact production performance. Use a read replica or dev database.
> WARNING: If you use a read-write database user with the database MCP, a single misunderstood prompt ("remove the duplicate entries") can silently delete rows. Read-only credentials are non-negotiable for production data.

---

### 5.3 GitHub MCP

Code:
```bash
export GITHUB_TOKEN="ghp_your_fine_grained_token"
claude mcp add github -- npx -y @modelcontextprotocol/server-github
```

```bash
# With GitHub MCP connected:
claude "List all open PRs in this repo that have been waiting more than 3 days for review"
claude "Find all issues labeled 'bug' opened this week and group them by component"
claude "Show me which PRs are failing CI checks and what the failures are"
claude "Who are the top 3 contributors this month and what did they work on?"
```

Exercise:
> Files: `examples/mcp-github.json`
1. Create a fine-grained GitHub PAT scoped to only the repos Claude needs (Contents: read, Issues: read, Pull Requests: read)
2. Configure the GitHub MCP with your token
3. Start a session and ask: "Summarize the open issues in this repo by label"
4. Ask: "Which PRs have been open the longest without review?"
Success criterion: Claude retrieves real issue and PR data from GitHub without you pasting any API responses.

Best Practices:
1. Use a fine-grained PAT scoped to specific repositories, not a classic token with full repo access.
2. Limit the token to read-only permissions (Contents: read, Issues: read, Pull Requests: read) unless Claude needs to create issues or comments.
3. Rotate the GitHub MCP token on the same schedule as your other service account tokens.

Guardrails:
> WARNING: A GitHub token with write permissions on the Issues and PRs scopes allows Claude to create comments, close issues, and modify PR descriptions. Confirm you intend this before granting write scopes.

---

### 5.4 Slack MCP

Code:
```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_TEAM_ID="T01234567"
claude mcp add slack -- npx -y @modelcontextprotocol/server-slack
```

```bash
# With Slack MCP connected:
claude "Summarize the last 50 messages in #engineering-alerts and identify unresolved incidents"
claude "Find all messages from the last 24 hours where someone mentioned a bug or error"
claude "What were the main discussion topics in #dev-team this week?"
```

Exercise:
> Files: `examples/mcp-slack.json`
1. Create a Slack app with `channels:history` and `channels:read` scopes
2. Install the app to your workspace and get the bot token
3. Configure the Slack MCP with the token and team ID
4. Ask Claude to summarize yesterday's messages in a specific channel
Success criterion: Claude returns a coherent summary of real Slack messages without you copying them manually.

Best Practices:
1. Scope your Slack bot token to `channels:history` and `channels:read` only unless you need more.
2. Join the bot to only the channels Claude needs — it cannot read channels it has not been added to.

Guardrails:
> WARNING: A Slack bot token with broad channel access exposes private channel content to Claude. Scope the bot to specific channels only, and ensure those channels do not contain content that should not be processed by an AI (HR discussions, legal matters, etc.).

---

### 5.5 Browser / Puppeteer MCP

Code:
```bash
claude mcp add puppeteer -- npx -y @modelcontextprotocol/server-puppeteer
```

```bash
# With Puppeteer MCP connected:
claude "Open http://localhost:3000/login, fill in the test credentials admin/test123,
submit the form, and verify the dashboard loads. Report any console errors."

claude "Take a screenshot of http://localhost:3000/dashboard and describe what you see"

claude "Navigate to http://localhost:3000/users, count the rows in the table,
and check if pagination controls are present"
```

Exercise:
> Files: `examples/mcp-browser.json`
1. Configure the Puppeteer MCP
2. Start your local development server
3. Ask Claude to run a smoke test on 3 key pages: confirm they load, have no console errors, and key elements are visible
Success criterion: Claude navigates to 3 pages autonomously and reports the status of each, including any errors.

Best Practices:
1. Use Puppeteer MCP for exploratory testing and smoke tests — write permanent E2E tests in Playwright or Cypress for repeatability.
2. Provide URLs to your local or staging environment only — never run Puppeteer MCP against production.

Guardrails:
> WARNING: Puppeteer MCP can navigate to any URL and interact with any page it can reach. Never run it against production — it can trigger side effects including form submissions, purchases, or account deletions if prompts are misunderstood.
> WARNING: Puppeteer MCP can reach internal network URLs (localhost, 192.168.x.x, 10.x.x.x). Ensure your firewall rules prevent the MCP process from reaching sensitive internal services.

---

### 5.6 Custom REST API MCP Server

Links:
- MCP (Model Context Protocol) — Building custom servers

Code:
```typescript
// See examples/custom-mcp-server.ts for the complete TypeScript implementation
// See examples/custom-mcp-server.py for the Python equivalent
```

```json
// Register in .claude/settings.json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["ts-node", "./mcp-servers/custom-mcp-server.ts"],
      "env": {
        "JIRA_BASE_URL": "${JIRA_BASE_URL}",
        "JIRA_TOKEN": "${JIRA_TOKEN}"
      }
    }
  }
}
```

Exercise:
> Files: `examples/custom-mcp-server.ts`, `examples/custom-mcp-server.py`
1. Copy `examples/custom-mcp-server.ts` (or .py) to a `mcp-servers/` directory in your project
2. Update the server to wrap one endpoint from an internal API your team uses (ticket system, metrics, feature flags, etc.)
3. Register it in `.claude/settings.json`
4. Start a Claude session and invoke the custom tool by describing what you want in natural language
Success criterion: Claude retrieves data from your internal API by name without you pasting the API response manually.

Best Practices:
1. Keep custom MCP server tool definitions minimal — tools with complex input schemas are harder for Claude to call correctly.
2. Include example inputs in the tool description — Claude uses them to construct correct calls.
3. Return structured JSON from your MCP server tools — Claude processes structured output more reliably than raw text.

Guardrails:
> WARNING: Custom MCP servers run as child processes with access to the environment variables you pass. Use a secrets manager (AWS Secrets Manager, HashiCorp Vault) rather than storing credentials in `.claude/settings.json` directly.

---

### 5.7 MCP in the Agent SDK

Code:
```python
# See examples/mcp-sdk-example.py for the complete runnable example
from claude_code_sdk import query, ClaudeCodeOptions, MCPServerConfig

options = ClaudeCodeOptions(
    model="claude-sonnet-4-6",
    permission_mode="auto",
    mcp_servers=[
        MCPServerConfig(
            name="postgres",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-postgres",
                  "postgresql://localhost/dev_db"],
            env={"PGPASSWORD": "dev-password"}
        )
    ]
)
```

Exercise:
> Files: `examples/mcp-sdk-example.py`
1. Install the SDK: `pip install claude-code-sdk`
2. Run `examples/mcp-sdk-example.py` — it connects to a database via MCP and asks Claude a question
3. Modify it to ask a question relevant to your own database schema
Success criterion: The script runs to completion and returns a real answer based on your database's actual data.

Guardrails:
> WARNING: MCP servers configured in the SDK run as child processes of your script. Their credentials are visible in process listings (`ps aux`). Use environment variables loaded from a secrets manager rather than hardcoded strings.

---

### 5.8 MCP Security Patterns

Code:
```json
// Use a read-only database user in MCP config
{
  "mcpServers": {
    "postgres-readonly": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres",
               "postgresql://claude_readonly@localhost/mydb"],
      "env": { "PGPASSWORD": "${PGPASSWORD_READONLY}" }
    }
  }
}
```

```json
// Audit all MCP tool calls with a PostToolUse hook
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "mcp__*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date -u +%Y-%m-%dT%H:%M:%SZ) MCP_CALL tool=$CLAUDE_TOOL_NAME\" >> /var/log/claude-mcp-audit.log"
          }
        ]
      }
    ]
  }
}
```

Best Practices:
1. Always use read-only credentials for database and API MCP servers unless write access is explicitly required and reviewed.
2. Audit all MCP tool calls using PostToolUse hooks — this is required for compliance in many regulated environments.
3. Rotate MCP credentials on the same schedule as other service account credentials (quarterly minimum).
4. Document which MCP servers are configured in your project's CLAUDE.md — team members should know what external access Claude has.

Guardrails:
> WARNING: An MCP server connected to a write-capable database combined with `permissionMode: auto` is equivalent to giving Claude direct write access to your data store. This is a deliberate, high-privilege configuration — confirm it is intentional and document it.

---

## 5.9 Plugins & Slack Integration

Links:
- [Plugins](https://code.claude.com/docs/en/plugins) — Extend Claude Code with plugins (installing, marketplace, creating)
- [Slack Integration](https://code.claude.com/docs/en/slack) — Use Claude Code in Slack channels

**Plugins** extend Claude Code with new tools, skills, and capabilities. Browse the Plugin Marketplace to find community-built integrations, or build your own using the plugin API.

**Slack Integration** lets your team interact with Claude Code directly from Slack — ask questions, trigger tasks, and receive responses without leaving your communication tool.

---

## Summary

| MCP Server | What Claude can do | Credential needed | Example file |
|------------|-------------------|-------------------|-------------|
| PostgreSQL | Query tables, analyze schema, find data issues | Read-only DB user | `mcp-database.json` |
| SQLite | Query local database files | None | `mcp-database.json` |
| GitHub | Read issues, PRs, commits, repo data | Fine-grained PAT (read) | `mcp-github.json` |
| Slack | Read channel messages, search content | Bot token (channels:read) | `mcp-slack.json` |
| Puppeteer | Browser automation, screenshots, UI testing | None | `mcp-browser.json` |
| Custom REST | Any internal API wrapped as MCP tools | API token (via env var) | `custom-mcp-server.ts` |

Next Steps: [Level 6 — Automation & Hooks](../06-automation-hooks/README.md)

---

## Anthropic Academy Resources

Official lessons that complement this level:

### Claude Code in Action
- [MCP servers with Claude Code](https://anthropic.skilljar.com/claude-code-in-action/303239)

### Introduction to MCP
- [Welcome to the course](https://anthropic.skilljar.com/introduction-to-model-context-protocol/303756)
- [Introducing MCP](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296689)
- [MCP clients](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296690)
- [Project setup](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296694)
- [Defining tools with MCP](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296697)
- [The server inspector](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296693)
- [Implementing a client](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296696)
- [Defining resources](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296699)
- [Accessing resources](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296695)
- [Defining prompts](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296698)
- [Prompts in the client](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296692)

### MCP Advanced Topics
- [Let's get started!](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296349)
- [Sampling](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296288)
- [Sampling walkthrough](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/295172)
- [Log and progress notifications](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296284)
- [Notifications walkthrough](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/291036)
- [Roots](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296289)
- [Roots walkthrough](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/295839)
- [JSON message types](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296290)
- [The STDIO transport](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296291)
- [The StreamableHTTP transport](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296287)
- [StreamableHTTP in depth](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296286)
- [State and the StreamableHTTP transport](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296285)

### Claude with the Anthropic API — MCP
- [MCP review](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287790)
- [Enhancements with MCP servers](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287792)
