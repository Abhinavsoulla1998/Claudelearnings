You're absolutely right! Let me create a comprehensive, detailed curriculum that covers everything. Let me first explore the full documentation structure.Now let me get more details on key pages to create a truly comprehensive curriculum:Perfect! Now I have comprehensive information. Let me create a detailed, hand-holding curriculum:Perfect! Now I have the complete picture. Let me create a comprehensive, detailed curriculum:

> This file preserves the original reference links. For the full curriculum with code snippets, exercises, and runnable examples, see the [levels/](levels/) folder or start at the [README](README.md).

---

# **Claude Code: Complete Developer Curriculum**

## From Beginner to Expert

This is a structured, hand-holding curriculum designed to take you from zero to mastery of Claude Code. Follow it sequentially for best results.

---

## **LEVEL 1: FOUNDATIONS (Days 1-3)**

*Get Claude Code installed and understand the basics*

### **1.1 Understanding Claude Code**

- **[Overview](https://code.claude.com/docs/en/overview)** — What is Claude Code? Core capabilities and use cases
- **[How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works)** — Architecture, workflow, and agentic loop
- **[Features Overview](https://code.claude.com/docs/en/features-overview)** — Complete feature set at a glance

### **1.2 Installation & Setup**

- **[Setup & Installation](https://code.claude.com/docs/en/setup)** — Install on macOS, Linux, or Windows
- **[Troubleshooting Installation](https://code.claude.com/docs/en/troubleshooting)** — Fix common install issues
- **[Authentication](https://code.claude.com/docs/en/authentication)** — Sign in and manage your account
- **[CLI Reference](https://code.claude.com/docs/en/cli-reference)** — Command-line flags and startup options

### **1.3 Your First Session**

- **[Quickstart](https://code.claude.com/docs/en/quickstart)** — Run your first Claude Code session
- **[Interactive Mode](https://code.claude.com/docs/en/interactive-mode)** — Learn keyboard shortcuts and input modes
- **[Keybindings](https://code.claude.com/docs/en/keybindings)** — Customize keyboard shortcuts

### **1.4 Understanding the Interface**

- **[Output Styles](https://code.claude.com/docs/en/output-styles)** — Different rendering modes
- **[Fullscreen Mode](https://code.claude.com/docs/en/fullscreen)** — Use the fullscreen renderer
- **[Status Line](https://code.claude.com/docs/en/statusline)** — Configure the status bar

---

## **LEVEL 2: CORE FEATURES (Days 4-7)**

*Master the essential features you'll use daily*

### **2.1 Commands & Slash Commands**

- **[Commands Reference](https://code.claude.com/docs/en/commands)** — Complete list of all 100+ commands
  - `/help` — View available commands
  - `/model` — Switch AI models
  - `/effort` — Adjust reasoning effort
  - `/clear` — Start fresh conversation
  - `/copy` — Copy responses to clipboard
  - `/export` — Export conversations
  - `/resume` — Continue previous sessions
  - `/branch` — Create conversation branches
  - `/rewind` — Go back to previous points
  - `/config` — Open settings
  - `/status` — View account & version info

### **2.2 Project Memory & Context**

- **[Memory (CLAUDE.md)](https://code.claude.com/docs/en/memory)** — Create persistent project memory
  - How to write effective CLAUDE.md files
  - Auto-memory feature
  - Memory best practices
- **[Context Window](https://code.claude.com/docs/en/context-window)** — Understand token limits
- **[/context Command](https://code.claude.com/docs/en/commands)** — Visualize context usage

### **2.3 Permissions & Security**

- **[Permission Modes](https://code.claude.com/docs/en/permission-modes)** — default, plan, auto, bypassPermissions
- **[Permissions](https://code.claude.com/docs/en/permissions)** — Fine-grained access control
- **[/permissions Command](https://code.claude.com/docs/en/commands)** — Manage permission rules
- **[Security](https://code.claude.com/docs/en/security)** — Security best practices
- **[Data Usage](https://code.claude.com/docs/en/data-usage)** — How your data is handled

### **2.4 Model Selection & Configuration**

- **[Model Configuration](https://code.claude.com/docs/en/model-config)** — Choose and configure models
- **[Fast Mode](https://code.claude.com/docs/en/fast-mode)** — Speed up responses
- **[Effort Levels](https://code.claude.com/docs/en/fast-mode)** — Control reasoning depth

### **2.5 Session Management**

- **[Checkpointing](https://code.claude.com/docs/en/checkpointing)** — Save and restore conversation states
- **[/rewind Command](https://code.claude.com/docs/en/commands)** — Navigate conversation history
- **[/resume Command](https://code.claude.com/docs/en/commands)** — Continue previous sessions
- **[/branch Command](https://code.claude.com/docs/en/commands)** — Fork conversations

---

## **LEVEL 3: PRACTICAL WORKFLOWS (Days 8-12)**

*Learn real-world development patterns*

### **3.1 Common Development Tasks**

- **[Common Workflows](https://code.claude.com/docs/en/common-workflows)** — Step-by-step guides for:
  - Exploring unfamiliar codebases
  - Debugging and fixing bugs
  - Refactoring code
  - Writing tests
  - Creating pull requests
  - Code review workflows

### **3.2 Code Review & Quality**

- **[Code Review](https://code.claude.com/docs/en/code-review)** — Review code with Claude
- **[/ultrareview Command](https://code.claude.com/docs/en/commands)** — Deep multi-agent code review
- **[/security-review Command](https://code.claude.com/docs/en/commands)** — Security vulnerability scanning
- **[/simplify Command](https://code.claude.com/docs/en/commands)** — Code quality improvements

### **3.3 Planning & Execution**

- **[Plan Mode](https://code.claude.com/docs/en/permission-modes)** — Review plans before execution
- **[/plan Command](https://code.claude.com/docs/en/commands)** — Enter plan mode directly
- **[/ultraplan Command](https://code.claude.com/docs/en/commands)** — Draft plans in cloud sandbox
- **[/batch Command](https://code.claude.com/docs/en/commands)** — Orchestrate large-scale changes

### **3.4 Best Practices**

- **[Best Practices](https://code.claude.com/docs/en/best-practices)** — Tips for effective Claude Code usage
- **[Common Workflows](https://code.claude.com/docs/en/common-workflows)** — Real-world patterns and examples

---

## **LEVEL 4: AUTOMATION & INTEGRATION (Days 13-17)**

*Automate repetitive tasks and integrate with external systems*

### **4.1 Hooks & Event-Driven Automation**

- **[Hooks Guide](https://code.claude.com/docs/en/hooks-guide)** — Introduction to hooks
- **[Hooks Reference](https://code.claude.com/docs/en/hooks)** — Complete hook API
  - `onSessionStart` — Run code when session starts
  - `onSessionEnd` — Run code when session ends
  - `onToolCall` — Intercept tool calls
  - `onToolResult` — Process tool results
  - `onMessage` — React to messages
  - Custom hook events

### **4.2 Skills (Custom Commands)**

- **[Skills](https://code.claude.com/docs/en/skills)** — Create your own commands
  - Writing skill prompts
  - Skill parameters
  - Bundled vs. custom skills
  - Skill best practices
- **[/skills Command](https://code.claude.com/docs/en/commands)** — List and manage skills

### **4.3 Scheduled Tasks & Routines**

- **[Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks)** — Run prompts on a schedule with `/loop`
  - Interval-based scheduling
  - Self-paced execution
  - Autonomous maintenance checks
- **[Routines](https://code.claude.com/docs/en/routines)** — Cloud-hosted recurring tasks with `/schedule`
  - Creating routines
  - Routine triggers
  - Managing routines
- **[Desktop Scheduled Tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)** — Schedule tasks in Desktop app

### **4.4 External Integrations**

- **[MCP (Model Context Protocol)](https://code.claude.com/docs/en/mcp)** — Connect external data sources
  - Installing MCP servers
  - Configuring MCP
  - Using MCP tools
  - MCP prompts
- **[Plugins](https://code.claude.com/docs/en/plugins)** — Extend Claude Code with plugins
  - Installing plugins
  - Plugin marketplace
  - Plugin dependencies
  - Creating plugins
- **[Slack Integration](https://code.claude.com/docs/en/slack)** — Use Claude Code in Slack
- **[GitHub Actions](https://code.claude.com/docs/en/github-actions)** — Integrate with CI/CD
- **[GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd)** — GitLab integration

---

## **LEVEL 5: ADVANCED FEATURES (Days 18-22)**

*Master advanced capabilities for power users*

### **5.1 Subagents & Delegation**

- **[Subagents](https://code.claude.com/docs/en/sub-agents)** — Delegate tasks to specialized agents
  - Creating subagents
  - Subagent configuration
  - Using subagents in workflows
  - `/agents Command]([https://code.claude.com/docs/en/commands](https://code.claude.com/docs/en/commands))** — Manage agent configurations

### **5.2 Advanced Session Features**

- **[Remote Control](https://code.claude.com/docs/en/remote-control)** — Control Claude Code from claude.ai
- **[/remote-control Command](https://code.claude.com/docs/en/commands)** — Enable remote control
- **[/teleport Command](https://code.claude.com/docs/en/commands)** — Move sessions between terminal and web

### **5.3 Browser & Web Automation**

- **[Chrome Integration](https://code.claude.com/docs/en/chrome)** — Browser automation and testing
- **[Computer Use](https://code.claude.com/docs/en/computer-use)** — Control your computer screen
- **[Claude Code on the Web](https://code.claude.com/docs/en/claude-code-on-the-web)** — Use Claude Code in browser
- **[Web Quickstart](https://code.claude.com/docs/en/web-quickstart)** — Get started on the web

### **5.4 Cost Management & Monitoring**

- **[Costs](https://code.claude.com/docs/en/costs)** — Understand pricing and costs
- **[/cost Command](https://code.claude.com/docs/en/commands)** — View token usage statistics
- **[Monitoring Usage](https://code.claude.com/docs/en/monitoring-usage)** — Track API usage
- **[/usage Command](https://code.claude.com/docs/en/commands)** — Check plan limits and rate limits
- **[/extra-usage Command](https://code.claude.com/docs/en/commands)** — Configure extra usage

### **5.5 Advanced Debugging**

- **[/debug Command](https://code.claude.com/docs/en/commands)** — Enable debug logging
- **[/doctor Command](https://code.claude.com/docs/en/commands)** — Diagnose installation issues
- **[/heapdump Command](https://code.claude.com/docs/en/commands)** — Diagnose memory issues
- **[Errors](https://code.claude.com/docs/en/errors)** — Common error messages and solutions

---

## **LEVEL 6: ADVANCED CONFIGURATION (Days 23-25)**

*Fine-tune Claude Code for your workflow*

### **6.1 Settings & Configuration**

- **[Settings](https://code.claude.com/docs/en/settings)** — Configure Claude Code
  - Theme and appearance
  - Editor mode (Vim/Normal)
  - Default model and effort
  - Permission defaults
- **[Environment Variables](https://code.claude.com/docs/en/env-vars)** — Configure via env vars
- **[Server-Managed Settings](https://code.claude.com/docs/en/server-managed-settings)** — Enterprise settings

### **6.2 Network & Infrastructure**

- **[Network Configuration](https://code.claude.com/docs/en/network-config)** — Proxy and firewall setup
- **[Terminal Configuration](https://code.claude.com/docs/en/terminal-config)** — Terminal-specific setup
- **[Dev Container Support](https://code.claude.com/docs/en/devcontainer)** — Use Claude Code in dev containers

### **6.3 Alternative Model Providers**

- **[Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock)** — Use AWS Bedrock models
- **[Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai)** — Use Google Vertex AI models
- **[Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry)** — Microsoft integration
- **[LLM Gateway](https://code.claude.com/docs/en/llm-gateway)** — Custom LLM routing

### **6.4 Voice & Accessibility**

- **[Voice Dictation](https://code.claude.com/docs/en/voice-dictation)** — Use voice input
- **[/voice Command](https://code.claude.com/docs/en/commands)** — Toggle voice mode

---

## **LEVEL 7: AGENT SDK (For Developers Building Agents)**

*Build custom agents programmatically*

### **7.1 Agent SDK Fundamentals**

- **[Agent SDK Overview](https://code.claude.com/docs/en/agent-sdk/overview)** — What is the Agent SDK?
- **[Agent SDK vs. Other Tools](https://code.claude.com/docs/en/agent-sdk/overview#compare-the-agent-sdk-to-other-claude-tools)** — Comparison guide
- **[Agent SDK Quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)** — Install and create first agent

### **7.2 Core Agent SDK Concepts**

- **[Python SDK](https://code.claude.com/docs/en/agent-sdk/python)** — Python API reference
- **[TypeScript SDK](https://code.claude.com/docs/en/agent-sdk/typescript)** — TypeScript API reference
- **[Agent Loop](https://code.claude.com/docs/en/agent-sdk/agent-loop)** — How agents work
- **[Sessions](https://code.claude.com/docs/en/agent-sdk/sessions)** — Manage agent sessions

### **7.3 Agent SDK Features**

- **[Streaming vs. Single Mode](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode)** — Response modes
- **[Streaming Output](https://code.claude.com/docs/en/agent-sdk/streaming-output)** — Handle streaming responses
- **[Structured Outputs](https://code.claude.com/docs/en/agent-sdk/structured-outputs)** — Get validated JSON
- **[Custom Tools](https://code.claude.com/docs/en/agent-sdk/custom-tools)** — Create custom tools
- **[Hooks](https://code.claude.com/docs/en/agent-sdk/hooks)** — Event-driven automation in SDK
- **[Skills](https://code.claude.com/docs/en/agent-sdk/skills)** — Create skills in SDK
- **[Subagents](https://code.claude.com/docs/en/agent-sdk/subagents)** — Delegate to subagents
- **[Slash Commands](https://code.claude.com/docs/en/agent-sdk/slash-commands)** — Add custom commands

### **7.4 Advanced Agent SDK**

- **[File Checkpointing](https://code.claude.com/docs/en/agent-sdk/file-checkpointing)** — Save/restore state
- **[Cost Tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)** — Monitor API costs
- **[Observability](https://code.claude.com/docs/en/agent-sdk/observability)** — Monitor agent behavior
- **[Permissions](https://code.claude.com/docs/en/agent-sdk/permissions)** — Control agent access
- **[Secure Deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)** — Deploy safely
- **[Hosting](https://code.claude.com/docs/en/agent-sdk/hosting)** — Deploy agents to production
- **[MCP Integration](https://code.claude.com/docs/en/agent-sdk/mcp)** — Use MCP in agents
- **[Modifying System Prompts](https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts)** — Customize behavior
- **[User Input](https://code.claude.com/docs/en/agent-sdk/user-input)** — Handle user interactions
- **[Todo Tracking](https://code.claude.com/docs/en/agent-sdk/todo-tracking)** — Track tasks
- **[Tool Search](https://code.claude.com/docs/en/agent-sdk/tool-search)** — Find available tools

### **7.5 Agent SDK Migration**

- **[Migration Guide](https://code.claude.com/docs/en/agent-sdk/migration-guide)** — Migrate from Claude Code SDK

---

## **LEVEL 8: ENTERPRISE & TEAM FEATURES (Days 26-27)**

*Scale Claude Code across teams*

### **8.1 Team Collaboration**

- **[Agent Teams](https://code.claude.com/docs/en/agent-teams)** — Work with multiple agents
- **[/team-onboarding Command](https://code.claude.com/docs/en/commands)** — Generate team guides
- **[Channels](https://code.claude.com/docs/en/channels)** — Team communication channels
- **[Channels Reference](https://code.claude.com/docs/en/channels-reference)** — Channel API

### **8.2 Enterprise Features**

- **[GitHub Enterprise Server](https://code.claude.com/docs/en/github-enterprise-server)** — Enterprise GitHub
- **[Slack Integration](https://code.claude.com/docs/en/slack)** — Team Slack integration
- **[Analytics](https://code.claude.com/docs/en/analytics)** — Usage analytics
- **[/insights Command](https://code.claude.com/docs/en/commands)** — Generate usage reports

### **8.3 Privacy & Compliance**

- **[Zero Data Retention](https://code.claude.com/docs/en/zero-data-retention)** — Privacy option
- **[Legal & Compliance](https://code.claude.com/docs/en/legal-and-compliance)** — Legal information

---

## **LEVEL 9: MASTERY & OPTIMIZATION (Ongoing)**

*Become an expert and optimize your workflow*

### **9.1 Advanced Patterns**

- **[Best Practices](https://code.claude.com/docs/en/best-practices)** — Expert tips and patterns
- **[Common Workflows](https://code.claude.com/docs/en/common-workflows)** — Real-world examples
- **[Sandboxing](https://code.claude.com/docs/en/sandboxing)** — Isolated execution environments

### **9.2 Staying Updated**

- **[Changelog](https://code.claude.com/docs/en/changelog)** — Track new features
- **[What's New](https://code.claude.com/docs/en/whats-new)** — Latest updates
- **[/release-notes Command](https://code.claude.com/docs/en/commands)** — View release notes

### **9.3 Troubleshooting & Support**

- **[Troubleshooting](https://code.claude.com/docs/en/troubleshooting)** — Common issues and solutions
- **[/doctor Command](https://code.claude.com/docs/en/commands)** — Diagnose problems
- **[/feedback Command](https://code.claude.com/docs/en/commands)** — Report bugs
- **[Errors](https://code.claude.com/docs/en/errors)** — Error reference

### **9.4 Community & Resources**

- **[Claude Directory](https://code.claude.com/docs/en/claude-directory)** — Find Claude Code resources
- **[Plugin Marketplace](https://code.claude.com/docs/en/plugin-marketplaces)** — Discover plugins
- **[Discover Plugins](https://code.claude.com/docs/en/discover-plugins)** — Browse available plugins
- **[Third-Party Integrations](https://code.claude.com/docs/en/third-party-integrations)** — External tools

---

## **LEVEL 10: AI DRIVEN SDLC — CERTIFICATION PREP**

*For team members preparing for the Claude Certified Architect – Foundations certification.*
*Use alongside the exam guide and hands-on practice. Passing score: 720 / 1000.*

**Domain weights**: D1 Agentic Architecture 27% · D2 Tool Design & MCP 18% · D3 Claude Code Config 20% · D4 Prompt Engineering 20% · D5 Context & Reliability 15%

### **10.1 Planning & Architecture** *(Domain 1)*

- **[Plan Mode](https://code.claude.com/docs/en/permission-modes)** — `--permission-mode plan`, `/plan`, `/ultraplan` for multi-file architectural decisions
- **Task Decomposition** (D1 T1.6) — prompt chaining for predictable workflows; adaptive decomposition for open-ended investigation
- **Explore Subagent** — isolates verbose discovery from main conversation context; prevents context window exhaustion during multi-phase tasks
- **Session Forking** — `fork_session` explores divergent approaches from a shared analysis baseline
- **Session Resumption** — `--resume <session-name>`; inform resumed session of file changes for targeted re-analysis; prefer fresh session with injected summary when prior tool results are stale
- → Level folder: [`levels/10-ai-driven-sdlc/exercises/02-multi-agent-system.md`](levels/10-ai-driven-sdlc/exercises/02-multi-agent-system.md)
- → Cross-ref: Level 3.3, Level 5.2

### **10.2 Development & Code Generation** *(Domain 3)*

- **[CLAUDE.md Hierarchy](https://code.claude.com/docs/en/memory)** (D3 T3.1) — user-level (`~/.claude/CLAUDE.md`) → project-level (`.claude/CLAUDE.md`) → directory-level; `@import` for modular standards files
- **[Path-Specific Rules](https://code.claude.com/docs/en/settings)** (D3 T3.3) — `.claude/rules/` with YAML `paths` glob fields; rules load only when editing matching files, reducing irrelevant context
- **[Custom Skills](https://code.claude.com/docs/en/skills)** (D3 T3.2) — `.claude/commands/` for project-scoped team slash commands; `context: fork` isolates verbose output from main session; `allowed-tools` restricts tool access; `argument-hint` prompts for parameters
- **Iterative Refinement** (D3 T3.5) — concrete I/O examples beat prose; test-driven iteration; interview pattern to surface design considerations before implementing
- **Built-in Tool Selection** (D2 T2.5) — Grep→content search, Glob→filename patterns, Read→full file, Edit→unique-text modification, Read+Write fallback when Edit anchor is non-unique
- → Level folder: [`levels/10-ai-driven-sdlc/examples/`](levels/10-ai-driven-sdlc/examples/)
- → Cross-ref: Level 2, Level 3, Level 6

### **10.3 Code Review & Quality** *(Domain 4)*

- **Multi-Instance Review** (D4 T4.6) — independent Claude instance reviews generated code; generating model retains reasoning context making self-review less effective at catching subtle issues
- **Multi-Pass Review** — per-file local analysis passes + separate cross-file integration pass to avoid attention dilution and contradictory findings
- **Explicit Criteria** (D4 T4.1) — define report-vs-skip categories; avoid vague "be conservative"; high false-positive categories undermine trust in accurate findings
- **Few-Shot Prompting** (D4 T4.2) — 2–4 examples showing location/issue/severity/fix format for consistent classification and ambiguous-case handling
- `detected_pattern` field in findings schema enables systematic false-positive analysis
- `/ultrareview`, `/security-review`, `/simplify`
- → Cross-ref: Level 3.2

### **10.4 Testing & CI/CD Integration** *(Domains 3 + 4)*

- **Non-Interactive Mode** (D3 T3.6) — `-p` / `--print` flag prevents interactive input hangs in pipelines; `--output-format json` + `--json-schema` for machine-parseable structured PR comment output
- **Structured Output** (D4 T4.3) — `tool_use` + JSON schema eliminates syntax errors; `tool_choice: "any"` guarantees tool call over conversational text; forced `{"type":"tool","name":"..."}` for sequenced pipelines
- **Batch Processing** (D4 T4.5) — Message Batches API for overnight/weekly workloads (50% cost savings, 24h window); NOT for blocking pre-merge checks; batch API does not support mid-request tool calling
- **Session Context Isolation** — separate Claude instance for CI review vs code generation; include prior review findings on re-runs so only new/unaddressed issues are reported
- **Validation & Retry** (D4 T4.4) — append specific validation errors to retry prompt for model self-correction; retries are ineffective when information is absent from source document
- **[GitHub Actions](https://code.claude.com/docs/en/github-actions)** | **[GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd)**
- → Level folder: [`levels/10-ai-driven-sdlc/examples/ci-review.yml`](levels/10-ai-driven-sdlc/examples/ci-review.yml), [`exercises/03-cicd-integration.md`](levels/10-ai-driven-sdlc/exercises/03-cicd-integration.md)
- → Cross-ref: Level 4

### **10.5 Agentic Automation & Tool Integration** *(Domains 1 + 2)*

- **Agentic Loop** (D1 T1.1) — continue when `stop_reason` is `"tool_use"`, terminate on `"end_turn"`; append tool results to conversation history each iteration; anti-patterns: natural language termination detection, arbitrary iteration caps as primary stopping mechanism
- **Coordinator-Subagent Pattern** (D1 T1.2) — hub-and-spoke; coordinator handles task decomposition, delegation, result aggregation, error routing; subagents operate with isolated context (no automatic parent context inheritance)
- **Subagent Spawning** (D1 T1.3) — `Task` tool + `allowedTools: ["Task"]` for coordinator; explicit context injection required in subagent prompt; spawn parallel subagents in single coordinator response; `AgentDefinition` configures system prompt and tool restrictions per subagent type
- **Hooks for Enforcement** (D1 T1.5) — `PostToolUse` hook normalizes heterogeneous data formats (Unix timestamps, ISO 8601, numeric status codes) before model processes them; hook-based enforcement is deterministic vs prompt-based instructions (probabilistic)
- **Structured Escalation** (D1 T1.4) — include task/customer ID, root cause, recommended action in handoff; programmatic prerequisite gates block downstream tools until prerequisites complete
- **Tool Interface Design** (D2 T2.1) — tool description is the primary LLM selection mechanism; include input format, examples, edge cases, boundaries; rename/split overlapping tools to eliminate misrouting
- **Tool Distribution** (D2 T2.3) — scope each subagent's tool set to its role; too many tools degrade selection reliability; `tool_choice`: `"auto"` / `"any"` / forced specific tool
- **[MCP Integration](https://code.claude.com/docs/en/mcp)** (D2 T2.4) — `.mcp.json` project-scoped for shared team tooling (version-controlled); `~/.claude.json` user-scoped for personal/experimental servers; `${ENV_VAR}` expansion for credential management without committing secrets
- **MCP Error Responses** (D2 T2.2) — return `errorCategory` (transient/validation/permission), `isRetryable` boolean, human-readable description; distinguish access failures from valid empty results
- → Level folder: [`levels/10-ai-driven-sdlc/examples/agentic-loop.py`](levels/10-ai-driven-sdlc/examples/agentic-loop.py), [`coordinator-subagent.py`](levels/10-ai-driven-sdlc/examples/coordinator-subagent.py), [`post-tool-use-hook.json`](levels/10-ai-driven-sdlc/examples/post-tool-use-hook.json), [`mcp-config.json`](levels/10-ai-driven-sdlc/examples/mcp-config.json)
- → Cross-ref: Level 5, Level 6, Level 7

### **10.6 Context Management & Reliability** *(Domain 5)*

- **Human-in-the-Loop** — programmatic prerequisite gates enforce ordering when deterministic compliance is required (prompt instructions alone have non-zero failure rate)
- **Long Session Management** — structured summaries injected between sessions; `--resume` for named continuation; inform resumed session of specific file changes for targeted re-analysis
- **Self-Evaluation Patterns** — model self-reports confidence per finding to enable calibrated review routing
- **Conflict Detection** — `calculated_total` vs `stated_total` fields; `conflict_detected` boolean for inconsistent source data
- **Schema Design for Reliability** (D4 T4.3) — optional/nullable fields prevent model fabrication; `"unclear"` enum for ambiguous cases; `"other"` + detail string for extensible categorization
- **[Context Window](https://code.claude.com/docs/en/context-window)** | **[Costs](https://code.claude.com/docs/en/costs)** | **[Zero Data Retention](https://code.claude.com/docs/en/zero-data-retention)**
- → Cross-ref: Level 2.2, Level 5.4

### **10.7 Certification Exam Scenarios Crosswalk**

| Scenario | Primary SDLC Phase | Key Domains | Level 10 Section |
|----------|--------------------|-------------|-----------------|
| 1: Customer Support Resolution Agent | Agentic Automation | D1, D2, D5 | 10.5, 10.6 |
| 2: Code Generation with Claude Code | Development | D3, D5 | 10.2, 10.6 |
| 3: Multi-Agent Research System | Planning / Analysis | D1, D2, D5 | 10.1, 10.5, 10.6 |
| 4: Developer Productivity with Claude | Development | D2, D3, D1 | 10.2, 10.5 |
| 5: Claude Code for CI/CD | Testing / CI-CD | D3, D4 | 10.4 |
| 6: Structured Data Extraction | Quality / Reporting | D4, D5 | 10.3, 10.6 |

- → Level folder: [`levels/10-ai-driven-sdlc/exercises/05-exam-scenarios.md`](levels/10-ai-driven-sdlc/exercises/05-exam-scenarios.md)

---

## **QUICK REFERENCE GUIDES**

### **Command Cheat Sheet**

```
/help                    Show all available commands
/model                   Switch AI model
/effort                  Adjust reasoning effort
/clear                   Start new conversation
/resume                  Continue previous session
/branch                  Fork conversation
/rewind                  Go back to previous point
/plan                    Enter plan mode
/loop [interval]         Run prompt on schedule
/schedule                Create cloud routine
/memory                  Edit CLAUDE.md
/permissions             Manage access rules
/config                  Open settings
/status                  View account info
/cost                    Show token usage
/debug                   Enable debug logging
/doctor                  Diagnose issues
/export                  Export conversation
/copy                    Copy response to clipboard
```

### **CLI Flags Cheat Sheet**

```
claude                   Start interactive session
claude "query"           Start with initial prompt
claude -p "query"        Non-interactive mode (SDK)
claude -c                Continue last session
claude -r "session"      Resume specific session
claude --model sonnet    Use specific model
claude --effort high     Set effort level
claude --permission-mode plan    Start in plan mode
claude --system-prompt "..."     Custom system prompt
claude --add-dir path    Add working directory
claude --debug           Enable debug mode
claude --help            Show all flags
```

### **Permission Modes Quick Guide**

```
default          Ask for permission on sensitive operations
plan             Review plan before execution
auto             Automatically allow safe operations
bypassPermissions Skip all permission prompts (dangerous)
```

---

## **LEARNING TIMELINE**


| Level | Duration   | Focus                  | Key Skills                                   |
| ----- | ---------- | ---------------------- | -------------------------------------------- |
| 1     | Days 1-3   | Foundations            | Install, first session, Desktop, IDE setup, settings |
| 2     | Days 4-7   | Core Features          | Commands, memory, permissions, models        |
| 3     | Days 8-12  | Daily Dev Workflows    | Debugging, refactoring, code review, PRs     |
| 4     | Days 13-15 | CI/CD & Quality        | GitHub Actions, GitLab, quality gates        |
| 5     | Days 16-19 | MCP — Connecting Tools | Database, GitHub, Slack, browser, custom MCP |
| 6     | Days 23-25 | Advanced Configuration | Settings, network, alternative providers             |
| 7     | Days 25-27 | Agent SDK              | Build custom agents (Python/TypeScript)              |
| 8     | Days 28+   | Enterprise & Mastery   | Teams, compliance, best practices                    |
| 9     | Ongoing    | Mastery & Optimization | Advanced patterns, troubleshooting, community        |
| 10    | Cert Prep  | AI Driven SDLC         | Agentic loops, MCP, CI/CD, structured output, reliability |


---

