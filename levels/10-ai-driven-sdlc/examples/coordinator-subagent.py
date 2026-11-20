"""
Coordinator-subagent pattern using the Claude Agent SDK.
Domain 1, Tasks 1.2-1.3: Orchestrate multi-agent systems with coordinator-subagent patterns.

Key patterns:
- Hub-and-spoke: coordinator manages all inter-subagent communication
- Subagents have ISOLATED context — they do NOT inherit the coordinator's history
- Spawn parallel subagents in a SINGLE coordinator response (not across turns)
- Pass all necessary context explicitly in each subagent's prompt
"""

import anthropic

client = anthropic.Anthropic()

# The Task tool enables a coordinator to spawn subagents.
# allowedTools must include "Task" for the coordinator to invoke subagents.
COORDINATOR_TOOLS = [
    {
        "name": "Task",
        "description": (
            "Spawn a specialized subagent to execute a specific task. "
            "The subagent starts with NO prior context — provide all necessary information in the prompt. "
            "Spawn all independent subagents in a single response (multiple Task calls) for parallel execution."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Short label identifying this subagent task"
                },
                "prompt": {
                    "type": "string",
                    "description": (
                        "Complete instructions + context for the subagent. "
                        "Must be fully self-contained — the subagent cannot access this conversation."
                    )
                },
                "subagent_type": {
                    "type": "string",
                    "enum": ["search-agent", "analysis-agent", "synthesis-agent"],
                    "description": "Specialized subagent type to invoke"
                }
            },
            "required": ["description", "prompt", "subagent_type"]
        }
    }
]

# Each subagent type has a specialized system prompt and restricted tool set.
SUBAGENT_CONFIG = {
    "search-agent": {
        "system": (
            "You are a search specialist. Search the provided codebase context and return "
            "structured findings. Be thorough — cover all subtopics in the research scope provided."
        ),
        "max_tokens": 2048
    },
    "analysis-agent": {
        "system": (
            "You are a code analysis specialist. Analyze the provided code or findings and return "
            "structured analysis with specific file references and line numbers where applicable."
        ),
        "max_tokens": 2048
    },
    "synthesis-agent": {
        "system": (
            "You are a synthesis specialist. Combine the provided research findings into a "
            "coherent, cited report. Preserve source attribution from the input data."
        ),
        "max_tokens": 4096
    }
}


def run_subagent(subagent_type: str, prompt: str) -> str:
    """
    Execute a subagent with its own isolated context.

    Critical: subagents start fresh — they have no access to the coordinator's
    conversation history or other subagents' results unless explicitly passed in the prompt.
    """
    config = SUBAGENT_CONFIG.get(subagent_type, SUBAGENT_CONFIG["analysis-agent"])

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=config["max_tokens"],
        system=config["system"],
        messages=[{"role": "user", "content": prompt}]
        # No shared conversation history — isolated fresh context per subagent
    )
    return response.content[0].text if response.content else "(no output)"


def run_coordinator(research_goal: str) -> str:
    """
    Coordinator agent that decomposes the task and delegates to specialized subagents.

    The coordinator:
    1. Analyzes the research goal and breaks it into subtasks
    2. Spawns parallel subagents in a SINGLE response (multiple Task tool calls in one turn)
    3. Evaluates synthesis output for coverage gaps and re-delegates if needed
    4. Aggregates results into the final report
    """
    coordinator_prompt = f"""You are coordinating a multi-agent research pipeline.

Research goal: {research_goal}

Your responsibilities:
1. Decompose this goal into distinct subtasks for specialized subagents
2. Spawn ALL independent subagents in a SINGLE response (parallel Task calls in one turn — not sequential turns)
3. Evaluate the synthesis for coverage gaps; if gaps exist, re-delegate to search/analysis agents with targeted queries
4. Produce the final aggregated report

Available subagent types:
- search-agent: web search and document retrieval
- analysis-agent: code analysis, pattern identification
- synthesis-agent: combines findings into a coherent report

IMPORTANT: Each subagent prompt must be fully self-contained. Include all relevant context,
findings from prior agents, and specific criteria — subagents cannot access this conversation."""

    messages = [{"role": "user", "content": coordinator_prompt}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8096,
            tools=COORDINATOR_TOOLS,
            messages=messages
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return "Coordinator complete"

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use" and block.name == "Task":
                    # In production: run these concurrently with asyncio or ThreadPoolExecutor
                    # Here shown sequentially for clarity
                    subagent_result = run_subagent(
                        block.input["subagent_type"],
                        block.input["prompt"]
                    )
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": subagent_result
                    })

            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    result = run_coordinator(
        "Research the authentication patterns used in this codebase, "
        "identify security gaps, and produce a prioritized remediation report."
    )
    print(result)
