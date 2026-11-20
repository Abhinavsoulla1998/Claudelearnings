# Exercise 1 — Agentic Loops
### Domain 1, Task 1.1 · Exam weight: 27%

> Reference implementation: [`../examples/agentic-loop.py`](../examples/agentic-loop.py)

---

## Learning Objectives

- Implement correct `stop_reason` control flow: continue on `"tool_use"`, terminate on `"end_turn"`
- Append tool results to conversation history so the model can incorporate new information
- Identify and avoid the three most common agentic loop anti-patterns

---

## Concept Summary

**The agentic loop lifecycle:**

```
Send request → inspect stop_reason
  ├── "tool_use"  → execute tools → append results → loop back
  └── "end_turn"  → extract final response → done
```

**Why tool results must be appended:**
Each iteration, the model only sees the conversation history. Tool results that are not appended cannot influence the model's reasoning on the next turn. The model effectively has amnesia about any tool execution that was not recorded.

**Three anti-patterns to avoid:**

| Anti-Pattern | Why It Fails |
|---|---|
| Parse natural language to detect completion (`if "DONE" in text`) | Model phrasing varies; causes premature or missed termination |
| Use iteration cap as primary stopping mechanism (`for i in range(10)`) | Tasks needing more turns are cut off; `"end_turn"` is the authoritative signal |
| Skip appending tool results to history | Model cannot reason about tool outcomes in the next iteration |

---

## Exercises

### 1.1 — Read and Trace

Open `../examples/agentic-loop.py`. Read `run_agentic_loop()` and answer:

1. On which line does the loop terminate, and what condition triggers it?
2. What would happen if `messages.append({"role": "user", "content": tool_results})` were removed?
3. Where is the "arbitrary iteration cap" anti-pattern **absent** — and what replaces it?

---

### 1.2 — Add a Write Tool

Extend `agentic-loop.py` with a `write_file` tool:

**Requirements:**
- Add a tool definition with a description that clearly distinguishes it from `read_file`
- The description must specify: what it does, expected inputs, when to use it vs `read_file`
- Add execution logic in `execute_tool()`

**Verify**: Could a model correctly choose between `read_file` and `write_file` based on your descriptions alone?

---

### 1.3 — Spot the Anti-Patterns

The following agentic loop has three anti-patterns. List each one and explain why it fails:

```python
for i in range(10):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        messages=messages
    )

    last_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            last_text = block.text

    if "Task complete" in last_text or "I'm done" in last_text:
        return last_text

    if response.stop_reason == "tool_use":
        tool_results = execute_all_tools(response)
        # Tool results collected but NOT added to messages
```

**Anti-patterns found:** (fill in)
1. ___
2. ___
3. ___

---

### 1.4 — Exam Practice

**Scenario (Scenario 1: Customer Support Resolution Agent)**

You are building an agent with tools: `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`. The agent handles billing disputes autonomously.

Which termination strategy is correct?

- **A)** Terminate after 5 iterations to prevent runaway loops
- **B)** Terminate when `stop_reason == "end_turn"`
- **C)** Terminate when the assistant text contains "resolved" or "escalated"
- **D)** Terminate after all four tools have been called at least once

*Answer: **B** — `"end_turn"` is the only authoritative completion signal. (A) cuts off legitimately long tasks. (C) is fragile natural language parsing. (D) ignores tasks that complete without using every tool.*

---

### 1.5 — Reflection

After completing the exercises, rate your confidence (1–5):

- [ ] I can explain why `"end_turn"` is the correct termination signal
- [ ] I can describe the role of conversation history in multi-turn tool use
- [ ] I can identify all three anti-patterns in unfamiliar code
- [ ] I can implement a working agentic loop from scratch
