# Exercise 2 — Multi-Agent Systems
### Domain 1, Tasks 1.2–1.3, 1.7 · Exam weight: 27%

> Reference implementation: [`../examples/coordinator-subagent.py`](../examples/coordinator-subagent.py)

---

## Learning Objectives

- Design a coordinator-subagent (hub-and-spoke) architecture
- Pass explicit context to subagents (they do NOT inherit parent context)
- Spawn parallel subagents in a single coordinator response turn
- Choose between session resumption and fresh session with injected summary

---

## Concept Summary

### Hub-and-Spoke Architecture

```
                    ┌─────────────────┐
                    │   Coordinator   │
                    │  (orchestrator) │
                    └────────┬────────┘
           ┌─────────────────┼─────────────────┐
           ▼                 ▼                 ▼
    [Search-Agent]   [Analysis-Agent]   [Synthesis-Agent]
    (isolated ctx)   (isolated ctx)     (isolated ctx)
```

**Coordinator responsibilities:** task decomposition, delegation, result aggregation, error routing, information flow control.

**Subagent context isolation:** subagents receive NO automatic parent context. Every fact they need must be explicitly included in their prompt. This is one of the most commonly tested concepts on the exam.

### Parallel vs Sequential Spawning

```python
# CORRECT: spawn all independent subagents in ONE coordinator turn
# (multiple Task tool calls in a single response)
response = coordinator.messages.create(...)
# Response contains: [Task(search), Task(analysis), Task(synthesis)]

# WRONG: spawn subagents across separate turns
response1 = coordinator.messages.create(...)  # spawns search
response2 = coordinator.messages.create(...)  # spawns analysis  ← unnecessary latency
```

### Session Management (D1 T1.7)

| Situation | Best Approach |
|-----------|--------------|
| Prior context is mostly valid, file changes are minor | `--resume <name>` + inform session of changed files |
| Prior tool results are stale (files heavily modified) | Fresh session with structured summary injected as context |
| Exploring two different refactoring strategies | `fork_session` from shared analysis baseline |

---

## Exercises

### 2.1 — Trace the Context Flow

Open `../examples/coordinator-subagent.py`. For `run_subagent()`:

1. Why does `run_subagent()` create a fresh messages list instead of using the coordinator's?
2. The synthesis subagent needs search results to produce a good report. Who is responsible for passing those results, and how?
3. If the coordinator discovers mid-task that analysis is incomplete, what should it do next according to the iterative refinement pattern?

---

### 2.2 — Design a Code Review Pipeline

Design a coordinator-subagent system for PR code review with three subagents:
- `security-reviewer` — checks for vulnerabilities
- `performance-reviewer` — checks for N+1 queries, missing indexes
- `test-coverage-checker` — verifies test coverage for changed code

For each subagent specify:

| Subagent | Tool set (max 4 tools) | Context coordinator must pass | Runs in parallel? |
|----------|----------------------|-------------------------------|-------------------|
| security-reviewer | | | |
| performance-reviewer | | | |
| test-coverage-checker | | | |

Then write the coordinator prompt that would spawn all three in a single response.

---

### 2.3 — Session Management Decision

You resumed an investigation session (`--resume auth-investigation`) from last week. Your teammate has since pushed 12 commits modifying 40 files in the auth module.

Which approach is correct?

- **A)** Resume the session — Claude will automatically notice the file changes
- **B)** Resume the session and tell it: "Files X, Y, Z have changed since our last session — please re-analyze only those"
- **C)** Always start fresh — resumed sessions with stale tool results are always unreliable
- **D)** Use `fork_session` to compare old auth analysis with a new one

*Answer: **B** — Informing a resumed session of specific changed files enables targeted re-analysis without losing the context from files that haven't changed. (A) is wrong — Claude doesn't auto-detect changes. (C) is too absolute — resumption is valuable when most prior context is still valid. (D) is useful for comparing approaches, not for updating stale analysis.*

---

### 2.4 — Task Decomposition Strategy

Choose the correct decomposition strategy for each scenario:

**Scenario A**: Add structured logging to every API endpoint across a 50-file codebase. The format is predefined and the same change applies to each file.

- Fixed sequential pipeline (prompt chaining)
- Adaptive decomposition based on intermediate findings

**Scenario B**: "Add comprehensive tests to this legacy codebase." You don't know the structure yet.

- Fixed sequential pipeline (prompt chaining)
- Adaptive decomposition based on intermediate findings

*Explain your reasoning for each choice.*

---

### 2.5 — Reflection

Rate your confidence (1–5):

- [ ] I can explain why subagents require explicit context injection
- [ ] I can design a coordinator prompt that spawns parallel subagents in one turn
- [ ] I know when to resume a session vs start fresh
- [ ] I understand the iterative refinement pattern for coverage gaps
