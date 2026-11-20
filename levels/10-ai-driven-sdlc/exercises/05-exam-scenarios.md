# Exercise 5 — Exam Scenarios Crosswalk & Practice Questions
### All 5 Domains · Claude Certified Architect – Foundations

> **Exam format**: 4 of 6 scenarios presented at random · Multiple choice · Scaled 100–1,000 · Pass: **720**
> **No penalty for guessing** — always answer every question.

---

## Scenario 1: Customer Support Resolution Agent

**Context**: Building a customer support agent with MCP tools: `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`. Target: 80%+ first-contact resolution.

*Primary domains: D1, D2, D5*

---

**Q1**: The agent must verify customer identity before processing any refund. Which approach guarantees compliance?

- A) System prompt: "Always call get_customer before process_refund"
- B) A programmatic prerequisite gate that blocks `process_refund` until `get_customer` returns a verified customer ID
- C) Add a validation warning in the `process_refund` tool description
- D) Set a high reasoning effort level so the model follows the sequence reliably

**Answer: B** — Programmatic enforcement is deterministic. System prompt instructions (A, C) have a non-zero failure rate. Reasoning effort (D) does not guarantee compliance.

---

**Q2**: Refunds over $500 must go to a human agent. Where should this rule be enforced?

- A) System prompt: "Never approve refunds over $500 automatically"
- B) In the `process_refund` tool description as a warning
- C) In a `PostToolUse` hook that intercepts the call and redirects to `escalate_to_human`
- D) In the agent's reasoning instructions with a "think carefully" directive

**Answer: C** — Business rules requiring guaranteed compliance need hooks (deterministic). Prompt and description instructions are probabilistic.

---

**Q3**: When escalating mid-process to a human agent who has no access to the conversation transcript, the handoff must include:

- A) The full raw conversation history as JSON
- B) Customer ID, root cause, refund amount requested, and recommended action
- C) Only the customer's most recent message
- D) A summary of which tools were called

**Answer: B** — Structured handoffs must be self-contained with all information needed for the receiving agent to act, since they cannot access the transcript.

---

**Q4**: Two MCP tools — `analyze_content` and `analyze_document` — have nearly identical descriptions. The agent consistently calls the wrong one. What is the root cause and fix?

- A) The agent needs a higher reasoning effort level
- B) Overlapping tool descriptions cause misrouting — rename and rewrite descriptions to clearly differentiate purpose, inputs, and boundaries
- C) Add a system prompt instruction: "Use analyze_content for web pages and analyze_document for files"
- D) Increase the number of few-shot examples in the prompt

**Answer: B** — Tool descriptions are the primary LLM tool selection mechanism. Ambiguous or overlapping descriptions cause systematic misrouting. The fix is to rename and rewrite, not add more prompt instructions.

---

## Scenario 2: Code Generation with Claude Code

**Context**: Using Claude Code for code generation, refactoring, debugging. Integrating into team workflow with CLAUDE.md and custom slash commands.

*Primary domains: D3, D5*

---

**Q5**: A new team member isn't receiving the project's coding standards when using Claude Code. They're using Claude Code with a user-level `CLAUDE.md`. What is the issue?

- A) Their Claude Code version is outdated
- B) Project standards are in project-level `.claude/CLAUDE.md` — user-level `~/.claude/CLAUDE.md` is not version-controlled and not shared
- C) They need to run `/memory` to load the standards
- D) The standards file exceeds the context window limit

**Answer: B** — User-level `CLAUDE.md` is personal and not shared. Team standards must be in project-level configuration.

---

**Q6**: You want testing conventions to apply only when editing test files (`**/*.test.ts`), not during regular development. Which approach is correct?

- A) Add a directory-level `CLAUDE.md` in the test folder
- B) Create a `.claude/rules/` file with YAML `paths: ["**/*.test.ts"]` frontmatter
- C) Invoke a custom skill manually when working on tests
- D) Add testing conventions to user-level `CLAUDE.md`

**Answer: B** — Path-specific rules in `.claude/rules/` with YAML `paths` glob fields load only when editing matching files. Directory-level `CLAUDE.md` (A) doesn't handle test files spread across the codebase.

---

**Q7**: A Claude Code skill that analyzes the full codebase produces very verbose output that pollutes the main conversation. What frontmatter option addresses this?

- A) `allowed-tools: []` — restricts tool access
- B) `context: fork` — runs the skill in an isolated sub-agent context, preventing output from entering the main session
- C) `argument-hint` — prompts for parameters before execution
- D) `max-tokens: 500` — limits output length

**Answer: B** — `context: fork` isolates skill execution in a sub-agent, so verbose discovery output does not pollute the main conversation context.

---

## Scenario 3: Multi-Agent Research System

**Context**: Coordinator agent delegates to search, analysis, and synthesis subagents for comprehensive research.

*Primary domains: D1, D2, D5*

---

**Q8**: The synthesis subagent produces reports that miss broad aspects of the research topic. Investigation shows the coordinator is using narrow search queries. The best fix is:

- A) Increase the synthesis subagent's `max_tokens`
- B) Improve the coordinator's system prompt to use broader search terms
- C) Have the coordinator evaluate synthesis output for coverage gaps, re-delegate targeted queries to search/analysis subagents, then re-invoke synthesis
- D) Add more subagent types to cover different research areas

**Answer: C** — The iterative refinement loop (coordinator evaluates → identifies gaps → re-delegates with targeted queries → re-synthesizes) is the correct pattern for ensuring complete coverage.

---

**Q9**: The coordinator needs to spawn three independent subagents. What is the correct spawning approach?

- A) Spawn search, wait for result, spawn analysis, wait, spawn synthesis
- B) Spawn all three in a single coordinator response as parallel `Task` tool calls
- C) Spawn across separate coordinator turns for better error isolation
- D) Have each subagent spawn the next one in a chain

**Answer: B** — Spawning parallel subagents in a single coordinator response minimizes latency and is the expected pattern. Sequential spawning (A, C) adds unnecessary waiting.

---

**Q10**: The synthesis subagent needs web search results to cite sources correctly. Who provides these, and how?

- A) The synthesis subagent calls `search_web` itself
- B) The coordinator includes complete search results explicitly in the synthesis subagent's prompt
- C) Results are stored in shared memory that all subagents can access
- D) The search subagent writes results to a file; the synthesis subagent reads it

**Answer: B** — Subagents do not inherit coordinator context or share memory. All information must be explicitly injected into the subagent's prompt by the coordinator.

---

## Scenario 5: Claude Code for CI/CD

**Context**: Integrating Claude Code into CI/CD pipelines for automated code review and test generation.

*Primary domains: D3, D4*

---

**Q11**: Your CI pipeline using Claude Code hangs indefinitely when triggered on a PR. Most likely cause and fix:

- A) Missing `ANTHROPIC_API_KEY` — add it to CI secrets
- B) Claude Code is running in interactive mode — add the `-p` flag
- C) The review prompt is too long — shorten it
- D) The CI runner doesn't have Node.js installed

**Answer: B** — Without `-p` / `--print`, Claude Code waits for interactive user input, blocking the pipeline indefinitely.

---

**Q12**: The pipeline is posting duplicate review comments on every new commit. The correct fix is:

- A) Delete all existing comments before each run
- B) Include prior review findings in context; instruct Claude to report only new or still-unaddressed issues
- C) Use a different Claude instance for each run
- D) Scope review only to lines changed in the latest commit

**Answer: B** — Including prior findings in context prevents re-reporting already-addressed issues without losing continuity.

---

**Q13**: For a weekly security audit running on 500 files, which API approach is most cost-effective?

- A) Synchronous API — needed for real-time feedback
- B) Message Batches API — 50% cost savings, appropriate for latency-tolerant overnight workloads
- C) Message Batches API — but only if each file fits within a single request
- D) Synchronous API — batch API doesn't support code analysis

**Answer: B** — Batch processing is ideal for non-blocking, latency-tolerant workloads (overnight audits, weekly reports). The 50% cost savings compound significantly at 500 files.

---

## Scenario 6: Structured Data Extraction

**Context**: Extracting structured data from unstructured documents; validating output with JSON schemas; integrating with downstream systems.

*Primary domains: D4, D5*

---

**Q14**: After switching to `tool_use` with a JSON schema, the pipeline still occasionally produces incorrect totals (e.g., `total: 150` when line items sum to `165`). Why?

- A) The JSON schema validation is not enabled correctly
- B) `tool_use` eliminates syntax errors but not semantic errors — calculated field validation must be done in application code
- C) The model needs a higher reasoning effort level for arithmetic
- D) The JSON schema needs stricter type constraints

**Answer: B** — `tool_use` with JSON schema guarantees schema compliance (syntax), not semantic correctness. Semantic validation (totals matching, conflict detection) must be implemented in application code.

---

**Q15**: Extraction retries are not fixing missing `line_number` fields. The source documents simply don't mention line numbers. The correct response is:

- A) Add a retry with a stronger instruction to find line numbers
- B) Make `line_number` a nullable field — retries are ineffective when information is absent from source
- C) Switch to a higher-capability model
- D) Add few-shot examples showing how to infer line numbers

**Answer: B** — Retries are only effective for format mismatches and structural errors. When information is absent from the source, retrying cannot produce it and will cause hallucination instead.

---

## Self-Assessment Checklist

Rate your confidence (1–5) before attempting the certification exam:

### Domain 1: Agentic Architecture & Orchestration (27%)
- [ ] `stop_reason` control flow: continue on `"tool_use"`, terminate on `"end_turn"`
- [ ] Coordinator-subagent hub-and-spoke architecture and responsibilities
- [ ] Explicit context injection — subagents do not inherit parent context
- [ ] Parallel subagent spawning in a single coordinator response
- [ ] Hooks (deterministic) vs prompt instructions (probabilistic) for enforcement
- [ ] Structured escalation/handoff protocols with required fields
- [ ] Session resumption vs fresh session with injected summary

### Domain 2: Tool Design & MCP Integration (18%)
- [ ] Tool descriptions as the primary LLM selection mechanism
- [ ] Identifying and fixing overlapping / ambiguous tool descriptions
- [ ] Scoped tool access per subagent role
- [ ] `tool_choice` options: `"auto"`, `"any"`, forced specific tool
- [ ] `.mcp.json` (project-scoped) vs `~/.claude.json` (user-scoped)
- [ ] `${ENV_VAR}` credential expansion — never commit secrets
- [ ] Structured error responses: `errorCategory`, `isRetryable`, `userMessage`

### Domain 3: Claude Code Configuration & Workflows (20%)
- [ ] CLAUDE.md hierarchy: user → project → directory; `@import` syntax
- [ ] Path-specific rules in `.claude/rules/` with YAML `paths` glob fields
- [ ] Custom skills: `context: fork`, `allowed-tools`, `argument-hint`
- [ ] `-p` / `--print` flag for non-interactive CI mode
- [ ] `--output-format json` + `--json-schema` for structured CI output
- [ ] Plan mode vs direct execution decision criteria
- [ ] Session context isolation for CI review

### Domain 4: Prompt Engineering & Structured Output (20%)
- [ ] `tool_use` + JSON schema: what it guarantees and what it doesn't
- [ ] `tool_choice` selection for different scenarios
- [ ] Nullable fields to prevent fabrication
- [ ] Retry-with-error-feedback: when effective vs ineffective
- [ ] Explicit categorical criteria vs vague instructions
- [ ] Few-shot examples for consistent classification
- [ ] Batch API: use cases, 50% savings, 24h window, no tool calling

### Domain 5: Context Management & Reliability (15%)
- [ ] Programmatic prerequisite gates for deterministic workflow ordering
- [ ] Session resumption strategy: resume vs fresh with summary
- [ ] Self-evaluation confidence for calibrated routing
- [ ] Conflict detection: `calculated_total` vs `stated_total`
- [ ] Schema design: nullable fields, `"unclear"` enum, `"other"` + detail
