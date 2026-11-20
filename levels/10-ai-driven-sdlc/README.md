# Level 10 — AI Driven SDLC (Certification Prep)

> Audience: Dev / QA Engineers | Certification: Claude Certified Architect – Foundations | Prerequisites: Levels 1–9

## Overview

This level maps the software development lifecycle to the 5 exam domains of the **Claude Certified Architect – Foundations** certification. Each section covers a distinct SDLC phase using Claude capabilities tested in the exam.

**Exam format**: 4 of 6 scenarios presented at random · Multiple choice · Scaled score 100–1,000 · Passing score: **720**

Use this level alongside the official exam guide PDF and hands-on practice with each example.

---

## What You'll Learn

- Implement correct agentic loop control flow using `stop_reason` (`"tool_use"` vs `"end_turn"`)
- Design coordinator-subagent (hub-and-spoke) multi-agent pipelines with explicit context passing
- Configure CLAUDE.md hierarchies, path-specific rules, and custom skills for team workflows
- Integrate Claude Code into CI/CD pipelines using non-interactive mode and structured JSON output
- Design MCP tool interfaces with clear descriptions, scoped access, and structured error responses
- Apply few-shot prompting and JSON schema enforcement for reliable structured extraction
- Implement human-in-the-loop escalation, hook-based enforcement, and context management

---

## Domain Coverage

| Domain | Weight | SDLC Phase | Section |
|--------|--------|------------|---------|
| D1: Agentic Architecture & Orchestration | 27% | Planning, Agentic Automation | 10.1, 10.5 |
| D2: Tool Design & MCP Integration | 18% | Development, Agentic Automation | 10.2, 10.5 |
| D3: Claude Code Config & Workflows | 20% | Development, Testing / CI-CD | 10.2, 10.4 |
| D4: Prompt Engineering & Structured Output | 20% | Code Review, Testing / CI-CD | 10.3, 10.4 |
| D5: Context Management & Reliability | 15% | All phases | 10.6 |

---

## Exam Scenarios Quick Reference

| # | Scenario | Primary SDLC Phase | Key Domains |
|---|----------|--------------------|-------------|
| 1 | Customer Support Resolution Agent | Agentic Automation | D1, D2, D5 |
| 2 | Code Generation with Claude Code | Development | D3, D5 |
| 3 | Multi-Agent Research System | Planning / Analysis | D1, D2, D5 |
| 4 | Developer Productivity with Claude | Development | D2, D3, D1 |
| 5 | Claude Code for CI/CD | Testing / CI-CD | D3, D4 |
| 6 | Structured Data Extraction | Quality / Reporting | D4, D5 |

---

## Section 10.1 — Planning & Architecture *(Domain 1)*

**Plan mode** for multi-file / architectural decisions: `--permission-mode plan`, `/plan`, `/ultraplan`

**Task decomposition** (D1 T1.6):
- Prompt chaining for predictable multi-step workflows (e.g., analyze each file → run cross-file integration pass)
- Adaptive decomposition for open-ended tasks that generate subtasks based on what is discovered at each step

**Explore subagent pattern**: isolates verbose discovery output from main conversation context, preventing context window exhaustion during multi-phase tasks.

**Session forking**: `fork_session` creates parallel branches from a shared analysis baseline to explore divergent approaches (e.g., two refactoring strategies).

**Session resumption** (D1 T1.7):
- `--resume <session-name>` to continue named sessions across work sessions
- Inform a resumed session of specific file changes for targeted re-analysis rather than full re-exploration
- Prefer a fresh session with an injected structured summary when prior tool results are stale

→ Exercises: [`exercises/02-multi-agent-system.md`](exercises/02-multi-agent-system.md)

---

## Section 10.2 — Development & Code Generation *(Domain 3)*

**CLAUDE.md hierarchy** (D3 T3.1):
- User-level: `~/.claude/CLAUDE.md` — personal preferences, not shared via version control
- Project-level: `.claude/CLAUDE.md` or root `CLAUDE.md` — shared team standards
- Directory-level: subdirectory `CLAUDE.md` files for package-specific conventions
- `@import` syntax for modular standards (e.g., `@import .claude/rules/testing.md`)

**Path-specific rules** (D3 T3.3): `.claude/rules/` files with YAML `paths` frontmatter containing glob patterns. Rules load only when editing matching files — reduces irrelevant context and token usage.

```yaml
# .claude/rules/testing.md
---
paths: ["**/*.test.ts", "**/*.spec.ts"]
---
# Testing conventions apply only when editing test files
```

**Custom skills** (D3 T3.2):
- `.claude/commands/` — project-scoped slash commands shared via version control
- `~/.claude/commands/` — personal slash commands
- `context: fork` frontmatter — isolates verbose skill output from main session
- `allowed-tools` — restricts tool access during skill execution
- `argument-hint` — prompts developer for parameters when invoking without arguments

**Iterative refinement** (D3 T3.5):
- Concrete input/output examples beat prose when natural language produces inconsistent results
- Test-driven iteration: write test suite first, then share test failures to guide improvement
- Interview pattern: have Claude ask clarifying questions before implementing in unfamiliar domains
- Single message for interacting issues vs sequential messages for independent issues

**Built-in tool selection** (D2 T2.5):

| Tool | Use for |
|------|---------|
| Grep | Content search across a codebase (function names, error messages, import statements) |
| Glob | Finding files by name or extension patterns (`**/*.test.tsx`) |
| Read | Loading full file contents |
| Edit | Targeted modifications using unique text matching |
| Read + Write | Fallback when Edit cannot find a unique anchor |

→ Examples: [`examples/`](examples/)
→ Exercises: [`exercises/01-agentic-loops.md`](exercises/01-agentic-loops.md)

---

## Section 10.3 — Code Review & Quality *(Domain 4)*

**Multi-instance review** (D4 T4.6): A model retains reasoning context from code generation, making it less likely to question its own decisions in the same session. Use an **independent** Claude instance (without prior reasoning context) for review — more effective at catching subtle issues.

**Multi-pass review**: split large reviews into per-file local analysis passes, then a separate cross-file integration pass to avoid attention dilution and contradictory findings.

**Explicit criteria over vague instructions** (D4 T4.1):
- Bad: "Be conservative and only report high-confidence findings"
- Good: "Report ONLY: (1) bugs where code behavior contradicts documented intent, (2) SQL injection / XSS vulnerabilities. Skip: style issues, naming conventions, local patterns."

General instructions like "be conservative" fail to improve precision compared to specific categorical criteria. High false-positive categories undermine developer trust in accurate categories.

**Few-shot prompting** (D4 T4.2): 2–4 targeted examples showing desired output format (location, issue, severity, suggested fix) for consistent classification and ambiguous-case handling. Few-shot examples enable the model to generalize judgment to novel patterns.

`detected_pattern` field in findings schema: enables systematic analysis of which code patterns trigger dismissals, allowing prompt refinement over time.

Slash commands: `/ultrareview`, `/security-review`, `/simplify`

→ Exercises: [`exercises/04-structured-output.md`](exercises/04-structured-output.md)

---

## Section 10.4 — Testing & CI/CD Integration *(Domains 3 + 4)*

**Non-interactive mode** (D3 T3.6):
```bash
# Use -p / --print to prevent interactive input hangs in CI
claude -p "review the changed files" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"issues":{"type":"array"}}}'
```

**Structured CI output**: `--output-format json` + `--json-schema` produces machine-parseable findings for automated posting as inline PR comments.

**Session context isolation**: use a fresh, independent Claude instance for CI code review — not the same session that generated the code. On re-runs after new commits, include prior review findings in context and instruct Claude to report only new or still-unaddressed issues.

**CLAUDE.md as CI context carrier**: include testing standards, fixture conventions, review criteria, and available test utilities so CI-invoked Claude Code has full project context.

**Batch processing** (D4 T4.5):

| Use case | API |
|----------|-----|
| Blocking pre-merge checks | Synchronous API (immediate response) |
| Overnight test generation | Message Batches API (50% cost savings, 24h window) |
| Weekly security audits | Message Batches API |

Batch API limitation: does NOT support mid-request tool calling.

**Validation & retry loops** (D4 T4.4):
- Append specific validation errors to the retry prompt for model self-correction
- Retries are ineffective when required information is simply absent from the source document
- Retries are effective for format mismatches and structural output errors

→ Examples: [`examples/ci-review.yml`](examples/ci-review.yml), [`examples/structured-output.py`](examples/structured-output.py)
→ Exercises: [`exercises/03-cicd-integration.md`](exercises/03-cicd-integration.md), [`exercises/04-structured-output.md`](exercises/04-structured-output.md)

---

## Section 10.5 — Agentic Automation & Tool Integration *(Domains 1 + 2)*

**Agentic loop control** (D1 T1.1):
- Continue loop when `stop_reason == "tool_use"`
- Terminate loop when `stop_reason == "end_turn"`
- Append tool results to conversation history between iterations
- Anti-patterns: parsing natural language for termination signals, using iteration caps as the primary stopping mechanism

**Coordinator-subagent pattern** (D1 T1.2) — hub-and-spoke:
- Coordinator decomposes tasks, delegates, aggregates results, handles error routing
- Subagents operate with **isolated context** — they do NOT inherit the coordinator's conversation history automatically
- Route all subagent communication through the coordinator for observability and consistent error handling

**Subagent spawning** (D1 T1.3):
- `Task` tool + `allowedTools: ["Task"]` required for a coordinator to invoke subagents
- All context must be **explicitly injected** in the subagent's prompt
- Spawn parallel subagents in a **single** coordinator response (not across separate turns)
- `AgentDefinition` configures system prompt, tool restrictions per subagent type

**Hooks for enforcement** (D1 T1.5):
- `PostToolUse` hook: intercepts tool results for transformation before the model processes them
- Hook-based enforcement = **deterministic** compliance
- Prompt-based instructions = **probabilistic** compliance (non-zero failure rate)
- Use hooks when business rules require guaranteed compliance (e.g., refund thresholds, PII handling)

**Structured escalation/handoff** (D1 T1.4): include customer/task ID, root cause, recommended action in handoffs so human agents who lack conversation access can act immediately.

**Tool interface design** (D2 T2.1):
- Tool descriptions are the primary mechanism LLMs use for tool selection
- Minimal descriptions lead to unreliable selection among similar tools
- Include: input format, example queries, edge cases, boundary explanations
- Rename or split tools to eliminate functional overlap (e.g., split `analyze_document` into `extract_data_points`, `summarize_content`, `verify_claim_against_source`)

**Tool distribution** (D2 T2.3):
- Scope each subagent's tool set to its role — too many tools (18 vs 4–5) degrades reliability
- `tool_choice` options: `"auto"` (may return text), `"any"` (must call a tool), `{"type":"tool","name":"..."}` (must call specific tool)

**MCP integration** (D2 T2.4):
- `.mcp.json` — project-scoped, version-controlled, shared team tooling
- `~/.claude.json` — user-scoped, personal/experimental servers
- `${ENV_VAR}` expansion for credentials — never commit secrets directly
- MCP resources: expose content catalogs (issue summaries, DB schema) to reduce exploratory tool calls

**MCP error responses** (D2 T2.2): return `errorCategory` (transient/validation/permission), `isRetryable` boolean, human-readable description. Distinguish access failures (need retry decisions) from valid empty results (successful query with no matches).

→ Examples: [`examples/agentic-loop.py`](examples/agentic-loop.py), [`examples/coordinator-subagent.py`](examples/coordinator-subagent.py), [`examples/post-tool-use-hook.json`](examples/post-tool-use-hook.json), [`examples/mcp-config.json`](examples/mcp-config.json)
→ Exercises: [`exercises/01-agentic-loops.md`](exercises/01-agentic-loops.md), [`exercises/02-multi-agent-system.md`](exercises/02-multi-agent-system.md)

---

## Section 10.6 — Context Management & Reliability *(Domain 5)*

**Human-in-the-loop**: programmatic prerequisite gates enforce step ordering when deterministic compliance is required. Prompt instructions alone have a non-zero failure rate for compliance-critical sequences (e.g., block `process_refund` until `get_customer` returns a verified ID).

**Long session management**:
- `--resume <session-name>` for named session continuation across work sessions
- Inform resumed sessions of specific file changes for targeted re-analysis
- When prior tool results are stale: start a fresh session with a structured summary rather than resuming

**Self-evaluation patterns**: model self-reports confidence per finding alongside structured output, enabling calibrated routing (high-confidence findings post automatically; low-confidence findings route to human review).

**Conflict detection in extraction**: include `calculated_total` alongside `stated_total` to flag discrepancies; add `conflict_detected` boolean for cases where source data is internally inconsistent.

**Schema design for reliability** (D4 T4.3):
- Make fields nullable when source documents may not contain the information — prevents fabrication
- `"unclear"` enum value for genuinely ambiguous cases
- `"other"` + detail string for extensible categorization beyond predefined lists

→ Exercises: [`exercises/04-structured-output.md`](exercises/04-structured-output.md), [`exercises/05-exam-scenarios.md`](exercises/05-exam-scenarios.md)

---

## Section 10.7 — Certification Exam Scenarios Crosswalk

| Scenario | Primary SDLC Phase | Key Domains | Section |
|----------|--------------------|-------------|---------|
| 1: Customer Support Resolution Agent | Agentic Automation | D1, D2, D5 | 10.5, 10.6 |
| 2: Code Generation with Claude Code | Development | D3, D5 | 10.2, 10.6 |
| 3: Multi-Agent Research System | Planning / Analysis | D1, D2, D5 | 10.1, 10.5, 10.6 |
| 4: Developer Productivity with Claude | Development | D2, D3, D1 | 10.2, 10.5 |
| 5: Claude Code for CI/CD | Testing / CI-CD | D3, D4 | 10.4 |
| 6: Structured Data Extraction | Quality / Reporting | D4, D5 | 10.3, 10.6 |

→ Practice questions for all 6 scenarios: [`exercises/05-exam-scenarios.md`](exercises/05-exam-scenarios.md)

---

## Folder Contents

```
10-ai-driven-sdlc/
├── README.md                          ← This file
├── examples/
│   ├── agentic-loop.py                ← D1 T1.1: stop_reason control flow
│   ├── coordinator-subagent.py        ← D1 T1.2-1.3: hub-and-spoke pattern
│   ├── post-tool-use-hook.json        ← D1 T1.5: hook-based enforcement
│   ├── ci-review.yml                  ← D3 T3.6: GitHub Actions CI pipeline
│   ├── structured-output.py           ← D4 T4.3-4.4: JSON schema + retry loop
│   └── mcp-config.json               ← D2 T2.4: MCP server configuration
└── exercises/
    ├── 01-agentic-loops.md            ← D1 T1.1 exercises
    ├── 02-multi-agent-system.md       ← D1 T1.2-1.3, 1.7 exercises
    ├── 03-cicd-integration.md         ← D3 T3.6 exercises
    ├── 04-structured-output.md        ← D4 T4.1-4.4 exercises
    └── 05-exam-scenarios.md           ← Practice questions + self-assessment
```

---

## Anthropic Academy Resources

Official lessons that complement this level (full-course review):

### Claude Code in Action
- [Summary and next steps](https://anthropic.skilljar.com/claude-code-in-action/303238)

### Claude 101
- [Claude in action: use-cases by role](https://anthropic.skilljar.com/claude-101/383401)
