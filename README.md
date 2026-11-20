# Claude Code — Developer Curriculum
## From Zero to Expert: A Practical Guide for Development & QA Teams

This curriculum is structured for development and QA teams adopting Claude Code. Choose your role below for a recommended path, or work through all lessons sequentially. Each lesson links to the course folder, official documentation, and Anthropic Academy video lessons.

**To get the most from this curriculum:** Read each lesson's README on GitHub, then clone this repo to run the exercises locally.

```bash
git clone https://github.com/InnovaSolutions-GlobalEnggTeam/ClaudeCurriculum.git
cd ClaudeCurriculum
```

---

## Choose Your Learning Path

### I am a Developer
> Goal: Use Claude Code to write, debug, refactor, and review code faster every day.

**Recommended path (~24 hrs):**
Lesson 1 → Lesson 2 → Lesson 3 → Lesson 6 → Lesson 5 → Lesson 8 → Lesson 9

| Start here | Quick wins |
|------------|-----------|
| [Lesson 1 — Foundations](levels/01-foundations/README.md) | [Prompt Patterns for Developers](quick-reference/prompt-patterns-developer.md) · [CLAUDE.md Template](levels/02-core-features/templates/CLAUDE.md.template) |

---

### I am a QA Engineer
> Goal: Automate test writing, integrate Claude into CI/CD pipelines, and use it for quality and security analysis.

**Recommended path (~22 hrs):**
Lesson 1 → Lesson 2 → Lesson 3 → Lesson 4 → Lesson 5 → Lesson 6 → Lesson 9

| Start here | Quick wins |
|------------|-----------|
| [Lesson 1 — Foundations](levels/01-foundations/README.md) | [Prompt Patterns for QA](quick-reference/prompt-patterns-qa.md) · [GitHub Actions Review Workflow](levels/04-cicd-quality/examples/github-actions-review.yml) |

---

### I am a Team Lead / Architect
> Goal: Establish team standards, set up CI/CD automation, configure MCP, and manage cost and compliance.

**Recommended path (~30 hours total):**
All lessons in order. Focus especially on Lessons 2, 4, 5, 6, and 9.

| Start here | Quick wins |
|------------|-----------|
| [Lesson 2 — Core Features](levels/02-core-features/README.md) | [Team CLAUDE.md Template](levels/09-enterprise-mastery/examples/team-claude-md.template) · [Compliance Settings](levels/09-enterprise-mastery/examples/compliance-settings.json) |

---

## Study Plan

| Lesson | Title | Audience | Duration | Key Focus |
|--------|-------|----------|----------|-----------|
| [1](#lesson-1--foundations) | Foundations | Everyone | 1–2 hrs | Install, first session, Desktop app, IDE setup, settings |
| [2](#lesson-2--core-features) | Core Features | Everyone | 2–3 hrs | Commands, CLAUDE.md, permissions, model selection |
| [3](#lesson-3--daily-dev-workflows) | Daily Dev Workflows | Developer, QA | 3–5 hrs | Debugging, refactoring, code review, PRs, prompt engineering |
| [4](#lesson-4--cicd--quality-automation) | CI/CD & Quality Automation | QA, Team Lead | 2–3 hrs | GitHub Actions, GitLab CI, quality gates, test analysis |
| [5](#lesson-5--mcp-connecting-your-tools) | MCP — Connecting Your Tools | Everyone | 3–5 hrs | Database, GitHub, Slack, browser, custom MCP servers |
| [6](#lesson-6--automation--hooks) | Automation & Hooks | Developer, Team Lead | 2–4 hrs | Hooks, skills, subagents, scheduled tasks |
| [7](#lesson-7--advanced-configuration) | Advanced Configuration | Team Lead | 1–2 hrs | Settings hierarchy, env vars, network, alternative providers |
| [8](#lesson-8--agent-sdk) | Agent SDK | Developer (advanced) | 4–6 hrs | Python/TypeScript SDK, tool use, streaming, Claude features |
| [9](#lesson-9--enterprise--mastery) | Enterprise & Mastery | Team Lead | 3–5 hrs | Teams, compliance, RAG pipelines, agent workflows |
| [10](#lesson-10--ai-driven-sdlc--certification-prep) | AI-Driven SDLC | Dev, QA (Cert track) | 1–3 hrs | Agentic loops, MCP, CI/CD, structured output, reliability |
| | | | **~30 hrs total** | *(range: 22–38 hrs)* |

---

## Lessons

---

### Lesson 1 — Foundations
**1–2 hrs · Everyone**

[Open Lesson 1 →](levels/01-foundations/README.md)

**What you'll learn:**
- What Claude Code is and how the agentic loop works
- Installing and authenticating on macOS, Linux, and Windows
- Running your first interactive and non-interactive sessions
- Using the Desktop application and IDE integrations (VS Code, JetBrains)
- Configuring themes, permission modes, and the status line

**Official Documentation:**
[Overview](https://code.claude.com/docs/en/overview) · [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works) · [Setup & Installation](https://code.claude.com/docs/en/setup) · [Authentication](https://code.claude.com/docs/en/authentication) · [Quickstart](https://code.claude.com/docs/en/quickstart) · [CLI Reference](https://code.claude.com/docs/en/cli-reference) · [Interactive Mode](https://code.claude.com/docs/en/interactive-mode) · [Keybindings](https://code.claude.com/docs/en/keybindings) · [Output Styles](https://code.claude.com/docs/en/output-styles) · [Status Line](https://code.claude.com/docs/en/statusline) · [Settings](https://code.claude.com/docs/en/settings)

**Anthropic Academy:**

| Course | Lessons |
|--------|---------|
| Claude Code in Action | [Introduction](https://anthropic.skilljar.com/claude-code-in-action/303233) · [What is a coding assistant?](https://anthropic.skilljar.com/claude-code-in-action/303235) · [Claude Code in action](https://anthropic.skilljar.com/claude-code-in-action/303242) · [Claude Code setup](https://anthropic.skilljar.com/claude-code-in-action/301614) · [Project setup](https://anthropic.skilljar.com/claude-code-in-action/301615) |
| Claude 101 | [What is Claude?](https://anthropic.skilljar.com/claude-101/383389) · [Your first conversation with Claude](https://anthropic.skilljar.com/claude-101/383390) · [Claude desktop app: Chat, Cowork, Code](https://anthropic.skilljar.com/claude-101/440908) |
| Claude with the Anthropic API | [Overview of Claude models](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287722) · [Anthropic apps](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287787) · [Claude Code setup](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287788) · [Claude Code in action](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287805) |

---

### Lesson 2 — Core Features
**2–3 hrs · Everyone**

[Open Lesson 2 →](levels/02-core-features/README.md)

**What you'll learn:**
- Slash commands: `/help`, `/model`, `/cost`, `/branch`, `/rewind`, `/resume`, and more
- Creating and maintaining a `CLAUDE.md` project memory file
- Understanding and configuring permission modes (default, plan, auto)
- Selecting models (Haiku, Sonnet, Opus) and effort levels
- Session checkpointing and conversation branching

**Official Documentation:**
[Commands Reference](https://code.claude.com/docs/en/commands) · [Memory (CLAUDE.md)](https://code.claude.com/docs/en/memory) · [Context Window](https://code.claude.com/docs/en/context-window) · [Permission Modes](https://code.claude.com/docs/en/permission-modes) · [Permissions](https://code.claude.com/docs/en/permissions) · [Security](https://code.claude.com/docs/en/security) · [Model Configuration](https://code.claude.com/docs/en/model-config) · [Fast Mode](https://code.claude.com/docs/en/fast-mode) · [Checkpointing](https://code.claude.com/docs/en/checkpointing)

**Anthropic Academy:**

| Course | Lessons |
|--------|---------|
| Claude Code in Action | [Adding context](https://anthropic.skilljar.com/claude-code-in-action/303241) · [Controlling context](https://anthropic.skilljar.com/claude-code-in-action/303237) |
| Claude 101 | [Introduction to projects](https://anthropic.skilljar.com/claude-101/383393) · [Creating with artifacts](https://anthropic.skilljar.com/claude-101/383394) |
| Claude with the Anthropic API | [System prompts](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287733) · [Temperature](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287728) |

---

### Lesson 3 — Daily Dev Workflows
**3–5 hrs · Developer, QA**

[Open Lesson 3 →](levels/03-daily-dev-workflows/README.md)

**What you'll learn:**
- Common patterns: exploring codebases, fixing bugs, writing tests, refactoring
- Code review with `/review`, `/security-review`, `/simplify`, and `/ultrareview`
- Plan mode for multi-step changes and large refactors
- Prompt engineering techniques for reliable, repeatable results
- Git workflow integration: commit messages, PR descriptions, changelogs
- Debugging patterns for async errors, CI-only failures, and merge conflicts

**Official Documentation:**
[Common Workflows](https://code.claude.com/docs/en/common-workflows) · [Code Review](https://code.claude.com/docs/en/code-review) · [Plan Mode](https://code.claude.com/docs/en/permission-modes) · [Best Practices](https://code.claude.com/docs/en/best-practices)

**Anthropic Academy:**

| Course | Lessons |
|--------|---------|
| Claude Code in Action | [Making changes](https://anthropic.skilljar.com/claude-code-in-action/303236) · [Github integration](https://anthropic.skilljar.com/claude-code-in-action/303240) |
| Claude 101 | [Getting better results](https://anthropic.skilljar.com/claude-101/383392) · [Research mode for deep dives](https://anthropic.skilljar.com/claude-101/383399) |
| Claude with the Anthropic API — Prompt Evaluation | [Prompt evaluation](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287731) · [A typical eval workflow](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287736) · [Generating test datasets](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287739) · [Running the eval](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287743) · [Model based grading](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287742) · [Code based grading](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287737) |
| Claude with the Anthropic API — Prompt Engineering | [Prompt engineering](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287745) · [Being clear and direct](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287744) · [Being specific](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287740) · [Structure with XML tags](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287741) · [Providing examples](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287746) |

---

### Lesson 4 — CI/CD & Quality Automation
**2–3 hrs · QA, Team Lead**

[Open Lesson 4 →](levels/04-cicd-quality/README.md)

**What you'll learn:**
- Automated PR review with GitHub Actions (trigger via `@claude` comment)
- CI quality gate that exits 1 on HIGH severity findings
- Auto-generating release notes on tag push
- GitLab CI/CD integration for merge request review
- Automated test failure root-cause analysis

**Official Documentation:**
[GitHub Actions](https://code.claude.com/docs/en/github-actions) · [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd)

**Curriculum examples:**
[github-actions-review.yml](levels/04-cicd-quality/examples/github-actions-review.yml) · [quality-gate.sh](levels/04-cicd-quality/examples/quality-gate.sh) · [github-actions-release-notes.yml](levels/04-cicd-quality/examples/github-actions-release-notes.yml) · [gitlab-ci-review.yml](levels/04-cicd-quality/examples/gitlab-ci-review.yml) · [test-failure-analysis.sh](levels/04-cicd-quality/examples/test-failure-analysis.sh)

**Anthropic Academy:**

| Course | Lessons |
|--------|---------|
| Claude Code in Action | [Github integration](https://anthropic.skilljar.com/claude-code-in-action/303240) |

---

### Lesson 5 — MCP: Connecting Your Tools
**3–5 hrs · Everyone**

[Open Lesson 5 →](levels/05-mcp-connecting-tools/README.md)

**What you'll learn:**
- MCP concepts: tools, resources, prompts, and transports
- Connecting Claude to PostgreSQL, SQLite, GitHub, Slack, and browser
- Building a custom REST API MCP server from scratch
- Using MCP inside the Agent SDK
- MCP security patterns and least-privilege configuration

**Official Documentation:**
[MCP](https://code.claude.com/docs/en/mcp) · [Plugins](https://code.claude.com/docs/en/plugins) · [Slack Integration](https://code.claude.com/docs/en/slack) · [Plugin Marketplace](https://code.claude.com/docs/en/plugin-marketplaces)

**Anthropic Academy:**

| Course | Lessons |
|--------|---------|
| Claude Code in Action | [MCP servers with Claude Code](https://anthropic.skilljar.com/claude-code-in-action/303239) |
| Introduction to MCP | [Welcome to the course](https://anthropic.skilljar.com/introduction-to-model-context-protocol/303756) · [Introducing MCP](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296689) · [MCP clients](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296690) · [Project setup](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296694) · [Defining tools with MCP](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296697) · [The server inspector](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296693) · [Implementing a client](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296696) · [Defining resources](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296699) · [Accessing resources](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296695) · [Defining prompts](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296698) · [Prompts in the client](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296692) |
| MCP Advanced Topics | [Let's get started!](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296349) · [Sampling](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296288) · [Sampling walkthrough](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/295172) · [Log and progress notifications](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296284) · [Notifications walkthrough](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/291036) · [Roots](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296289) · [Roots walkthrough](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/295839) · [JSON message types](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296290) · [The STDIO transport](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296291) · [The StreamableHTTP transport](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296287) · [StreamableHTTP in depth](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296286) · [State and the StreamableHTTP transport](https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296285) |
| Claude with the Anthropic API — MCP | [MCP review](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287790) · [Enhancements with MCP servers](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287792) |

---

### Lesson 6 — Automation & Hooks
**2–4 hrs · Developer, Team Lead**

[Open Lesson 6 →](levels/06-automation-hooks/README.md)

**What you'll learn:**
- Writing PreToolUse and PostToolUse hooks for event-driven automation
- Building custom slash commands (skills) using Markdown
- Scheduling recurring tasks with `/loop` and `/schedule`
- Creating and managing subagents for parallel task delegation
- Remote control and session teleport between terminal and web

**Official Documentation:**
[Hooks Guide](https://code.claude.com/docs/en/hooks-guide) · [Hooks Reference](https://code.claude.com/docs/en/hooks) · [Skills](https://code.claude.com/docs/en/skills) · [Subagents](https://code.claude.com/docs/en/sub-agents) · [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks) · [Routines](https://code.claude.com/docs/en/routines) · [Desktop Scheduled Tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks) · [Remote Control](https://code.claude.com/docs/en/remote-control)

**Anthropic Academy:**

| Course | Lessons |
|--------|---------|
| Claude Code in Action — Hooks | [Introducing hooks](https://anthropic.skilljar.com/claude-code-in-action/312000) · [Defining hooks](https://anthropic.skilljar.com/claude-code-in-action/312002) · [Implementing a hook](https://anthropic.skilljar.com/claude-code-in-action/312003) · [Gotchas around hooks](https://anthropic.skilljar.com/claude-code-in-action/312423) · [Useful hooks!](https://anthropic.skilljar.com/claude-code-in-action/312004) · [Another useful hook](https://anthropic.skilljar.com/claude-code-in-action/312427) · [Custom commands](https://anthropic.skilljar.com/claude-code-in-action/303234) |
| Introduction to Agent Skills | [What are skills?](https://anthropic.skilljar.com/introduction-to-agent-skills/434525) · [Creating your first skill](https://anthropic.skilljar.com/introduction-to-agent-skills/434527) · [Configuration and multi-file skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434526) · [Skills vs. other Claude Code features](https://anthropic.skilljar.com/introduction-to-agent-skills/434528) · [Sharing skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434529) · [Troubleshooting skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434530) |
| Introduction to Subagents | [What are subagents?](https://anthropic.skilljar.com/introduction-to-subagents/450698) · [Creating a subagent](https://anthropic.skilljar.com/introduction-to-subagents/450699) · [Designing effective subagents](https://anthropic.skilljar.com/introduction-to-subagents/450700) · [Using subagents effectively](https://anthropic.skilljar.com/introduction-to-subagents/450701) |
| Claude with the Anthropic API | [Workflows vs agents](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287794) |

---

### Lesson 7 — Advanced Configuration
**1–2 hrs · Team Lead**

[Open Lesson 7 →](levels/07-advanced-config/README.md)

**What you'll learn:**
- The three-tier settings hierarchy (global → project → local override)
- Environment variables for auth, model routing, and feature flags
- Network configuration: proxy, TLS inspection, air-gapped environments
- Connecting Claude Code to AWS Bedrock and Google Vertex AI
- Cost monitoring and server-managed enterprise policy enforcement

**Official Documentation:**
[Settings](https://code.claude.com/docs/en/settings) · [Environment Variables](https://code.claude.com/docs/en/env-vars) · [Network Configuration](https://code.claude.com/docs/en/network-config) · [Terminal Configuration](https://code.claude.com/docs/en/terminal-config) · [Dev Container Support](https://code.claude.com/docs/en/devcontainer) · [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock) · [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai) · [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry) · [LLM Gateway](https://code.claude.com/docs/en/llm-gateway) · [Server-Managed Settings](https://code.claude.com/docs/en/server-managed-settings) · [Costs](https://code.claude.com/docs/en/costs) · [Voice Dictation](https://code.claude.com/docs/en/voice-dictation)

**Anthropic Academy:**

| Course | Lessons |
|--------|---------|
| Claude with the Anthropic API | [Accessing the API](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287726) · [Getting an API key](https://anthropic.skilljar.com/claude-with-the-anthropic-api/296766) |

---

### Lesson 8 — Agent SDK
**4–6 hrs · Developer (advanced)**

[Open Lesson 8 →](levels/08-agent-sdk/README.md)

**What you'll learn:**
- Python and TypeScript SDK fundamentals: `query()`, streaming loops, `ClaudeCodeOptions`
- Handling streaming message events (text, tool_use, tool_result, result)
- Extracting structured JSON output with schema validation and retry loops
- Defining custom tools with input schemas and handler functions
- In-process SDK hooks (PreToolUse / PostToolUse) for programmatic control
- Secure deployment: permission modes, rate limiting, least-privilege sandboxing

**Official Documentation:**
[Agent SDK Overview](https://code.claude.com/docs/en/agent-sdk/overview) · [Python SDK](https://code.claude.com/docs/en/agent-sdk/python) · [TypeScript SDK](https://code.claude.com/docs/en/agent-sdk/typescript) · [Agent Loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) · [Streaming vs. Single Mode](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode) · [Structured Outputs](https://code.claude.com/docs/en/agent-sdk/structured-outputs) · [Custom Tools](https://code.claude.com/docs/en/agent-sdk/custom-tools) · [SDK Hooks](https://code.claude.com/docs/en/agent-sdk/hooks) · [Subagents](https://code.claude.com/docs/en/agent-sdk/subagents) · [Secure Deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment) · [Observability](https://code.claude.com/docs/en/agent-sdk/observability) · [Cost Tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)

**Anthropic Academy:**

| Course | Lessons |
|--------|---------|
| Claude Code in Action | [The Claude Code SDK](https://anthropic.skilljar.com/claude-code-in-action/312001) |
| Claude with the Anthropic API — Core API | [Welcome to the course](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287818) · [Making a request](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287725) · [Multi-Turn conversations](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287735) · [Response streaming](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287734) · [Structured data](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287732) |
| Claude with the Anthropic API — Tool Use | [Introducing tool use](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287747) · [Project overview](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287751) · [Tool functions](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287756) · [Tool schemas](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287753) · [Handling message blocks](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287757) · [Sending tool results](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287752) · [Multi-turn conversations with tools](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287750) · [Implementing multiple turns](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287758) · [Using multiple tools](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287749) · [Fine grained tool calling](https://anthropic.skilljar.com/claude-with-the-anthropic-api/313160) · [The text edit tool](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287760) · [The web search tool](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287755) |
| Claude with the Anthropic API — Features of Claude | [Extended thinking](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287773) · [Image support](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287778) · [PDF support](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287768) · [Citations](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287771) · [Prompt caching](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287772) · [Rules of prompt caching](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287770) · [Prompt caching in action](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287774) · [Code execution and the Files API](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287777) |

---

### Lesson 9 — Enterprise & Mastery
**3–5 hrs · Team Lead**

[Open Lesson 9 →](levels/09-enterprise-mastery/README.md)

**What you'll learn:**
- Standardizing CLAUDE.md templates and onboarding at organization scale
- Setting up agent teams for parallel workstreams
- Enterprise features: GitHub Enterprise Server, Slack, analytics
- Privacy and compliance: Zero Data Retention, audit logging, prompt injection defense
- Advanced patterns: morning briefings, pipeline composition, parallel reviews, cost management
- Retrieval Augmented Generation (RAG) and agentic search workflows

**Official Documentation:**
[Agent Teams](https://code.claude.com/docs/en/agent-teams) · [Channels](https://code.claude.com/docs/en/channels) · [GitHub Enterprise Server](https://code.claude.com/docs/en/github-enterprise-server) · [Slack Integration](https://code.claude.com/docs/en/slack) · [Analytics](https://code.claude.com/docs/en/analytics) · [Zero Data Retention](https://code.claude.com/docs/en/zero-data-retention) · [Legal & Compliance](https://code.claude.com/docs/en/legal-and-compliance) · [Sandboxing](https://code.claude.com/docs/en/sandboxing) · [Best Practices](https://code.claude.com/docs/en/best-practices) · [Changelog](https://code.claude.com/docs/en/changelog) · [Claude Directory](https://code.claude.com/docs/en/claude-directory) · [Third-Party Integrations](https://code.claude.com/docs/en/third-party-integrations)

**Anthropic Academy:**

| Course | Lessons |
|--------|---------|
| Claude 101 | [Working with skills](https://anthropic.skilljar.com/claude-101/383396) · [Enterprise search](https://anthropic.skilljar.com/claude-101/383398) · [Claude in action: use-cases by role](https://anthropic.skilljar.com/claude-101/383401) · [Other ways to work with Claude](https://anthropic.skilljar.com/claude-101/383402) |
| Claude with the Anthropic API — RAG and Agentic Search | [Introducing Retrieval Augmented Generation](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287763) · [Text chunking strategies](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287776) · [Text embeddings](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287759) · [The full RAG flow](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287764) · [Implementing the RAG flow](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287761) · [BM25 lexical search](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287767) · [A Multi-Index RAG pipeline](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287766) |
| Claude with the Anthropic API — Agents and Workflows | [Agents and workflows](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287796) · [Parallelization workflows](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287804) · [Chaining workflows](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287800) · [Routing workflows](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287801) · [Agents and tools](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287803) · [Environment inspection](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287798) |

---

### Lesson 10 — AI-Driven SDLC (Certification Prep)
**Certification track · Developer, QA**

[Open Lesson 10 →](levels/10-ai-driven-sdlc/README.md)

**Certification:** Claude Certified Architect – Foundations · Passing score: 720 / 1,000

**Domain weights:**

| Domain | Topic | Weight |
|--------|-------|--------|
| D1 | Agentic Architecture & Orchestration | 27% |
| D2 | Tool Design & MCP Integration | 18% |
| D3 | Claude Code Config & Workflows | 20% |
| D4 | Prompt Engineering & Structured Output | 20% |
| D5 | Context Management & Reliability | 15% |

**What you'll learn:**
- Agentic loop control: `stop_reason` handling, coordinator-subagent pattern
- CLAUDE.md hierarchy and path-specific rules for large codebases
- Non-interactive CI/CD mode (`-p` flag, `--output-format json`)
- Structured output with JSON schema, retry loops, and conflict detection
- MCP project-scoped vs. user-scoped config, error response design
- Context window management, long session strategies, human-in-the-loop gates

**Exam Scenarios:**

| Scenario | SDLC Phase | Key Domains | Exercises |
|----------|-----------|-------------|-----------|
| 1: Customer Support Resolution Agent | Agentic Automation | D1, D2, D5 | [10.5, 10.6](levels/10-ai-driven-sdlc/README.md) |
| 2: Code Generation with Claude Code | Development | D3, D5 | [10.2, 10.6](levels/10-ai-driven-sdlc/README.md) |
| 3: Multi-Agent Research System | Planning / Analysis | D1, D2, D5 | [10.1, 10.5, 10.6](levels/10-ai-driven-sdlc/README.md) |
| 4: Developer Productivity with Claude | Development | D2, D3, D1 | [10.2, 10.5](levels/10-ai-driven-sdlc/README.md) |
| 5: Claude Code for CI/CD | Testing / CI-CD | D3, D4 | [10.4](levels/10-ai-driven-sdlc/README.md) |
| 6: Structured Data Extraction | Quality / Reporting | D4, D5 | [10.3, 10.6](levels/10-ai-driven-sdlc/README.md) |

→ Practice questions: [exercises/05-exam-scenarios.md](levels/10-ai-driven-sdlc/exercises/05-exam-scenarios.md)

**Curriculum examples:**
[agentic-loop.py](levels/10-ai-driven-sdlc/examples/agentic-loop.py) · [coordinator-subagent.py](levels/10-ai-driven-sdlc/examples/coordinator-subagent.py) · [ci-review.yml](levels/10-ai-driven-sdlc/examples/ci-review.yml) · [structured-output.py](levels/10-ai-driven-sdlc/examples/structured-output.py) · [mcp-config.json](levels/10-ai-driven-sdlc/examples/mcp-config.json)

**Anthropic Academy:**

| Course | Lessons |
|--------|---------|
| Claude Code in Action | [Summary and next steps](https://anthropic.skilljar.com/claude-code-in-action/303238) |
| Claude 101 | [Claude in action: use-cases by role](https://anthropic.skilljar.com/claude-101/383401) |

---

## Quick Reference

### Slash Commands

| Command | What it does |
|---------|-------------|
| `/help` | Show available commands |
| `/model` | Switch AI model |
| `/effort` | Adjust reasoning effort |
| `/clear` | Start fresh conversation |
| `/resume` | Continue previous session |
| `/branch` | Fork conversation at current point |
| `/rewind` | Return to last checkpoint |
| `/plan` | Enter plan mode |
| `/ultraplan` | Draft plan in cloud sandbox |
| `/batch` | Orchestrate large-scale changes |
| `/loop [interval]` | Run prompt on a schedule |
| `/schedule` | Create a cloud-hosted routine |
| `/memory` | Edit CLAUDE.md |
| `/permissions` | Manage allow/deny rules |
| `/config` | Open settings |
| `/status` | View account and version info |
| `/cost` | Show token usage for this session |
| `/debug` | Enable debug logging |
| `/doctor` | Diagnose installation issues |
| `/export` | Export conversation |
| `/review` | Code review in current context |
| `/ultrareview` | Deep multi-agent code review |
| `/security-review` | Security vulnerability scan |
| `/simplify` | Code quality improvements |
| `/remote-control` | Enable browser-based remote control |
| `/teleport` | Move session between terminal and web |
| `/release-notes` | View recent release notes |

### CLI Flags

```
claude                              Start interactive session
claude "query"                      Start with initial prompt
claude -p "query"                   Non-interactive (pipeline/CI use)
claude -c                           Continue last session
claude -r "session-name"            Resume specific named session
claude --model claude-sonnet-4-6    Use specific model
claude --effort high                Set effort level (low/medium/high)
claude --permission-mode plan       Start in plan mode
claude --system-prompt "..."        Custom system prompt
claude --add-dir /path              Add extra working directory
claude --output-format json         Machine-readable JSON output
claude --debug                      Enable debug mode
claude --help                       Show all flags
```

### Permission Modes

| Mode | Behavior | When to use |
|------|----------|-------------|
| `default` | Prompts on sensitive operations | New projects, unfamiliar codebases |
| `plan` | Shows full plan before executing | Risky operations, onboarding |
| `auto` | Allows safe operations silently | Daily use once config is trusted |
| `bypassPermissions` | Skips all permission checks | Sandboxed CI environments only |

### Reference Files

| Resource | Description |
|----------|-------------|
| [Command Cheatsheet](quick-reference/command-cheatsheet.md) | All slash commands with descriptions |
| [CLI Flags Cheatsheet](quick-reference/cli-flags-cheatsheet.md) | All CLI flags with examples |
| [Permission Modes Guide](quick-reference/permission-modes.md) | Permission mode comparison |
| [Prompt Patterns — Developer](quick-reference/prompt-patterns-developer.md) | 30 copy-paste prompts for developers |
| [Prompt Patterns — QA](quick-reference/prompt-patterns-qa.md) | 30 copy-paste prompts for QA engineers |
| [CurriculumReference.md](CurriculumReference.md) | Original documentation-only reference |
