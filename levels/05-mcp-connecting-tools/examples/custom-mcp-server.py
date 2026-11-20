"""
Custom MCP Server — Jira REST API wrapper (Python)

This is the Python equivalent of custom-mcp-server.ts. It implements the same
two tools (get_jira_issue and create_jira_comment) using the official MCP
Python SDK.

Required dependencies:
    pip install mcp httpx

Register in .claude/settings.json:
    {
      "mcpServers": {
        "jira": {
          "command": "python",
          "args": ["./mcp-servers/custom-mcp-server.py"],
          "env": {
            "JIRA_BASE_URL": "${JIRA_BASE_URL}",
            "JIRA_TOKEN": "${JIRA_TOKEN}"
          }
        }
      }
    }

Environment variables required:
    JIRA_BASE_URL  — e.g. https://your-org.atlassian.net
    JIRA_TOKEN     — Base64-encoded "user@example.com:api_token" string
                     Generate at: https://id.atlassian.com/manage-profile/security/api-tokens
                     Encode in Python: import base64; base64.b64encode(b"user@example.com:your-api-token").decode()
"""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Any

import httpx
import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

# ---------------------------------------------------------------------------
# Environment validation
# ---------------------------------------------------------------------------

JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL", "").rstrip("/")
JIRA_TOKEN = os.environ.get("JIRA_TOKEN", "")

if not JIRA_BASE_URL or not JIRA_TOKEN:
    sys.stderr.write(
        "Error: JIRA_BASE_URL and JIRA_TOKEN environment variables must be set.\n"
    )
    sys.exit(1)

ISSUE_KEY_PATTERN = re.compile(r"^[A-Z]+-\d+$")

# ---------------------------------------------------------------------------
# Jira API helpers
# ---------------------------------------------------------------------------

def _jira_headers() -> dict[str, str]:
    return {
        "Authorization": f"Basic {JIRA_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _jira_get(path: str) -> Any:
    """Perform a GET request to the Jira REST API v3."""
    url = f"{JIRA_BASE_URL}/rest/api/3/{path}"
    with httpx.Client(timeout=15.0) as client:
        response = client.get(url, headers=_jira_headers())

    if not response.is_success:
        raise RuntimeError(
            f"Jira API error {response.status_code} {response.reason_phrase}: "
            f"{response.text}"
        )
    return response.json()


def _jira_post(path: str, body: dict[str, Any]) -> Any:
    """Perform a POST request to the Jira REST API v3."""
    url = f"{JIRA_BASE_URL}/rest/api/3/{path}"
    with httpx.Client(timeout=15.0) as client:
        response = client.post(url, headers=_jira_headers(), json=body)

    if not response.is_success:
        raise RuntimeError(
            f"Jira API error {response.status_code} {response.reason_phrase}: "
            f"{response.text}"
        )
    return response.json()


def _extract_plain_text(node: Any, depth: int = 0) -> str:
    """
    Recursively extract plain text from a Jira ADF (Atlassian Document Format)
    node. Returns an empty string for null or non-ADF values.
    """
    if not node or not isinstance(node, dict):
        return ""

    if node.get("type") == "text":
        return node.get("text", "")

    content = node.get("content")
    if not isinstance(content, list):
        return ""

    block_types = {
        "paragraph", "heading", "bulletList", "orderedList",
        "listItem", "blockquote", "codeBlock",
    }

    child_text = "".join(_extract_plain_text(child, depth + 1) for child in content)

    if node.get("type") in block_types and depth > 0:
        return child_text + "\n"

    return child_text


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def get_jira_issue(issue_key: str) -> str:
    """Retrieve a Jira issue and return its key fields as a JSON string."""
    issue_key = issue_key.strip().upper()

    if not ISSUE_KEY_PATTERN.match(issue_key):
        raise ValueError(
            f'Invalid issue key "{issue_key}". Expected format: PROJECT-123'
        )

    fields = "summary,status,assignee,description,priority,labels,created,updated"
    data = _jira_get(f"issue/{issue_key}?fields={fields}")
    f = data["fields"]

    description_text = _extract_plain_text(f.get("description")) or "(No description provided)"
    labels = f.get("labels") or ["(none)"]

    result = {
        "key": data["key"],
        "summary": f["summary"],
        "status": f["status"]["name"],
        "assignee": f["assignee"]["displayName"] if f.get("assignee") else "Unassigned",
        "priority": f["priority"]["name"] if f.get("priority") else "None",
        "labels": labels,
        "created": f["created"],
        "updated": f["updated"],
        "description": description_text,
    }

    return json.dumps(result, indent=2)


def create_jira_comment(issue_key: str, comment_body: str) -> str:
    """Add a plain-text comment to a Jira issue and return confirmation as JSON."""
    issue_key = issue_key.strip().upper()

    if not ISSUE_KEY_PATTERN.match(issue_key):
        raise ValueError(
            f'Invalid issue key "{issue_key}". Expected format: PROJECT-123'
        )

    comment_body = comment_body.strip()
    if not comment_body:
        raise ValueError("Comment body must not be empty.")

    # Jira Cloud REST API v3 requires Atlassian Document Format.
    adf_body = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": comment_body}],
            }
        ],
    }

    response = _jira_post(f"issue/{issue_key}/comment", {"body": adf_body})

    result = {
        "success": True,
        "commentId": response["id"],
        "issueKey": issue_key,
        "created": response["created"],
        "message": f"Comment successfully added to {issue_key}.",
    }

    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# MCP Server setup
# ---------------------------------------------------------------------------

server: Server = Server("jira-mcp-server")

TOOL_DEFINITIONS: list[types.Tool] = [
    types.Tool(
        name="get_jira_issue",
        description=(
            "Retrieve a Jira issue by its key and return its summary, status, assignee, "
            "priority, labels, and description. "
            "Use this tool when asked about a specific Jira ticket. "
            "Examples: get_jira_issue('PROJ-123'), get_jira_issue('BACKEND-456')"
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "issue_key": {
                    "type": "string",
                    "description": (
                        "The Jira issue key in the format PROJECT-NUMBER, "
                        "e.g. PROJ-123 or BACKEND-456."
                    ),
                }
            },
            "required": ["issue_key"],
        },
    ),
    types.Tool(
        name="create_jira_comment",
        description=(
            "Add a comment to an existing Jira issue. "
            "Use this tool when asked to comment on, update, or reply to a Jira ticket. "
            "The comment is posted as plain text and will appear in the issue's comment thread. "
            "Examples: create_jira_comment('PROJ-123', 'Investigated and confirmed the root cause is X.')"
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "issue_key": {
                    "type": "string",
                    "description": "The Jira issue key in the format PROJECT-NUMBER, e.g. PROJ-123.",
                },
                "comment_body": {
                    "type": "string",
                    "description": (
                        "The plain-text body of the comment to add. "
                        "Keep it concise and factual."
                    ),
                },
            },
            "required": ["issue_key", "comment_body"],
        },
    ),
]


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return TOOL_DEFINITIONS


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any]
) -> list[types.TextContent]:
    try:
        if name == "get_jira_issue":
            result = get_jira_issue(arguments["issue_key"])
        elif name == "create_jira_comment":
            result = create_jira_comment(
                arguments["issue_key"], arguments["comment_body"]
            )
        else:
            raise ValueError(f'Unknown tool: "{name}"')

        return [types.TextContent(type="text", text=result)]

    except Exception as exc:
        error_payload = json.dumps({"error": str(exc)}, indent=2)
        return [types.TextContent(type="text", text=error_payload)]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main() -> None:
    sys.stderr.write("Jira MCP server running on stdio.\n")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
