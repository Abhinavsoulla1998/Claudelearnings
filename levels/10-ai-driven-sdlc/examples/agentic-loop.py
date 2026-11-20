"""
Agentic loop implementation using the Claude Agent SDK.
Domain 1, Task 1.1: Design and implement agentic loops for autonomous task execution.

Key pattern: continue when stop_reason == "tool_use", terminate on "end_turn".
Anti-patterns to avoid:
  - Parsing natural language signals to detect loop termination
  - Using arbitrary iteration caps as the primary stopping mechanism
  - Not appending tool results to conversation history between iterations
"""

import json
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "search_codebase",
        "description": (
            "Search the codebase for files matching a pattern. "
            "Use for finding function names, import statements, or error messages across files. "
            "Returns matching file paths and line numbers. "
            "Do NOT use for reading full file contents — use read_file for that."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Regex pattern to search for in file contents"
                },
                "file_extension": {
                    "type": "string",
                    "description": "File extension filter (e.g. '.py', '.ts'). Optional."
                }
            },
            "required": ["pattern"]
        }
    },
    {
        "name": "read_file",
        "description": (
            "Read the full contents of a file at the given path. "
            "Use after search_codebase to inspect specific files in detail. "
            "Do NOT use for searching across many files — use search_codebase for that."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative or absolute path to the file to read"
                }
            },
            "required": ["path"]
        }
    }
]


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool and return its result as a string."""
    if tool_name == "search_codebase":
        # Replace with real grep/glob logic in production
        return json.dumps({
            "matches": [
                {"file": "src/auth.py", "line": 15, "content": f"import {tool_input['pattern']}"},
                {"file": "src/api.py", "line": 42, "content": f"from {tool_input['pattern']} import client"}
            ]
        })
    elif tool_name == "read_file":
        # Replace with real file read in production
        return f"# Contents of {tool_input['path']}\n# (placeholder — replace with actual file read)"
    return json.dumps({"error": f"Unknown tool: {tool_name}"})


def run_agentic_loop(task: str) -> str:
    """
    Execute an agentic loop for the given task.

    The loop continues as long as the model requests tool use (stop_reason == "tool_use").
    It terminates when the model signals completion (stop_reason == "end_turn").

    Tool results are appended to conversation history after each iteration so the model
    can incorporate new information into its reasoning on the next turn.
    """
    messages = [{"role": "user", "content": task}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        # Append the assistant response to history so the model can reason about its own output
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            # Model has completed the task — extract final text response
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return "Task complete (no text response)"

        if response.stop_reason == "tool_use":
            # Execute each requested tool call and collect results
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # Append tool results as a user message so the model can use them in the next iteration
            # Without this step the model cannot incorporate tool output into its reasoning
            messages.append({"role": "user", "content": tool_results})
            # Loop continues — model will process tool results and decide next action

        else:
            # Unexpected stop reason (e.g. max_tokens) — exit gracefully
            return f"Loop ended with unexpected stop_reason: {response.stop_reason}"


if __name__ == "__main__":
    result = run_agentic_loop(
        "Find all Python files that import the 'anthropic' package and summarize what each one does."
    )
    print(result)
