/**
 * Custom MCP Server — Jira REST API wrapper
 *
 * Required dependencies (add to your package.json):
 * {
 *   "dependencies": {
 *     "@modelcontextprotocol/sdk": "^1.0.0"
 *   },
 *   "devDependencies": {
 *     "@types/node": "^20.0.0",
 *     "ts-node": "^10.9.0",
 *     "typescript": "^5.0.0"
 *   }
 * }
 *
 * Install:
 *   npm install @modelcontextprotocol/sdk
 *   npm install -D @types/node ts-node typescript
 *
 * Register in .claude/settings.json:
 * {
 *   "mcpServers": {
 *     "jira": {
 *       "command": "npx",
 *       "args": ["ts-node", "./mcp-servers/custom-mcp-server.ts"],
 *       "env": {
 *         "JIRA_BASE_URL": "${JIRA_BASE_URL}",
 *         "JIRA_TOKEN": "${JIRA_TOKEN}"
 *       }
 *     }
 *   }
 * }
 *
 * Environment variables required:
 *   JIRA_BASE_URL  — e.g. https://your-org.atlassian.net
 *   JIRA_TOKEN     — Base64-encoded "user@example.com:api_token" string
 *                    Generate at: https://id.atlassian.com/manage-profile/security/api-tokens
 *                    Encode: btoa("user@example.com:your-api-token")
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";

// ---------------------------------------------------------------------------
// Environment validation
// ---------------------------------------------------------------------------

const JIRA_BASE_URL = process.env.JIRA_BASE_URL;
const JIRA_TOKEN = process.env.JIRA_TOKEN;

if (!JIRA_BASE_URL || !JIRA_TOKEN) {
  process.stderr.write(
    "Error: JIRA_BASE_URL and JIRA_TOKEN environment variables must be set.\n"
  );
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Jira API helpers
// ---------------------------------------------------------------------------

interface JiraIssue {
  key: string;
  fields: {
    summary: string;
    status: { name: string };
    assignee: { displayName: string } | null;
    description: string | null;
    priority: { name: string } | null;
    labels: string[];
    created: string;
    updated: string;
  };
}

interface JiraComment {
  id: string;
  author: { displayName: string };
  body: string;
  created: string;
}

interface JiraAddCommentResponse {
  id: string;
  created: string;
  body: string;
}

async function jiraRequest<T>(
  path: string,
  method: "GET" | "POST" = "GET",
  body?: Record<string, unknown>
): Promise<T> {
  const url = `${JIRA_BASE_URL}/rest/api/3/${path}`;
  const options: RequestInit = {
    method,
    headers: {
      Authorization: `Basic ${JIRA_TOKEN}`,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  };

  if (body !== undefined) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Jira API error ${response.status} ${response.statusText}: ${errorText}`
    );
  }

  return response.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Tool implementations
// ---------------------------------------------------------------------------

async function getJiraIssue(issueKey: string): Promise<string> {
  if (!issueKey || !/^[A-Z]+-\d+$/.test(issueKey.trim())) {
    throw new Error(
      `Invalid issue key "${issueKey}". Expected format: PROJECT-123`
    );
  }

  const issue = await jiraRequest<JiraIssue>(
    `issue/${issueKey.trim()}?fields=summary,status,assignee,description,priority,labels,created,updated`
  );

  const { fields } = issue;

  // Jira description uses Atlassian Document Format (ADF); extract plain text.
  const descriptionText = extractPlainText(fields.description);

  const result = {
    key: issue.key,
    summary: fields.summary,
    status: fields.status.name,
    assignee: fields.assignee?.displayName ?? "Unassigned",
    priority: fields.priority?.name ?? "None",
    labels: fields.labels.length > 0 ? fields.labels : ["(none)"],
    created: fields.created,
    updated: fields.updated,
    description: descriptionText || "(No description provided)",
  };

  return JSON.stringify(result, null, 2);
}

async function createJiraComment(
  issueKey: string,
  commentBody: string
): Promise<string> {
  if (!issueKey || !/^[A-Z]+-\d+$/.test(issueKey.trim())) {
    throw new Error(
      `Invalid issue key "${issueKey}". Expected format: PROJECT-123`
    );
  }

  if (!commentBody || commentBody.trim().length === 0) {
    throw new Error("Comment body must not be empty.");
  }

  // Jira Cloud REST API v3 requires Atlassian Document Format for comment body.
  const adfBody = {
    version: 1,
    type: "doc",
    content: [
      {
        type: "paragraph",
        content: [
          {
            type: "text",
            text: commentBody.trim(),
          },
        ],
      },
    ],
  };

  const response = await jiraRequest<JiraAddCommentResponse>(
    `issue/${issueKey.trim()}/comment`,
    "POST",
    { body: adfBody }
  );

  const result = {
    success: true,
    commentId: response.id,
    issueKey: issueKey.trim(),
    created: response.created,
    message: `Comment successfully added to ${issueKey.trim()}.`,
  };

  return JSON.stringify(result, null, 2);
}

/**
 * Recursively extracts plain text from a Jira ADF (Atlassian Document Format)
 * node. Returns an empty string for null or non-text nodes.
 */
function extractPlainText(
  node: unknown,
  depth: number = 0
): string {
  if (!node || typeof node !== "object") {
    return "";
  }

  const n = node as Record<string, unknown>;

  if (n.type === "text" && typeof n.text === "string") {
    return n.text;
  }

  if (Array.isArray(n.content)) {
    const childText = (n.content as unknown[])
      .map((child) => extractPlainText(child, depth + 1))
      .join("");

    // Add a newline after block-level nodes for readability.
    const blockTypes = new Set([
      "paragraph",
      "heading",
      "bulletList",
      "orderedList",
      "listItem",
      "blockquote",
      "codeBlock",
    ]);

    if (typeof n.type === "string" && blockTypes.has(n.type) && depth > 0) {
      return childText + "\n";
    }

    return childText;
  }

  return "";
}

// ---------------------------------------------------------------------------
// Tool definitions
// ---------------------------------------------------------------------------

const TOOLS: Tool[] = [
  {
    name: "get_jira_issue",
    description: [
      "Retrieve a Jira issue by its key and return its summary, status, assignee, priority, labels, and description.",
      "Use this tool when asked about a specific Jira ticket.",
      "Examples: get_jira_issue('PROJ-123'), get_jira_issue('BACKEND-456')",
    ].join(" "),
    inputSchema: {
      type: "object",
      properties: {
        issue_key: {
          type: "string",
          description:
            "The Jira issue key in the format PROJECT-NUMBER, e.g. PROJ-123 or BACKEND-456.",
        },
      },
      required: ["issue_key"],
    },
  },
  {
    name: "create_jira_comment",
    description: [
      "Add a comment to an existing Jira issue.",
      "Use this tool when asked to comment on, update, or reply to a Jira ticket.",
      "The comment is posted as plain text and will appear in the issue's comment thread.",
      "Examples: create_jira_comment('PROJ-123', 'Investigated and confirmed the root cause is X.')",
    ].join(" "),
    inputSchema: {
      type: "object",
      properties: {
        issue_key: {
          type: "string",
          description:
            "The Jira issue key in the format PROJECT-NUMBER, e.g. PROJ-123.",
        },
        comment_body: {
          type: "string",
          description:
            "The plain-text body of the comment to add. Keep it concise and factual.",
        },
      },
      required: ["issue_key", "comment_body"],
    },
  },
];

// ---------------------------------------------------------------------------
// MCP Server setup
// ---------------------------------------------------------------------------

const server = new Server(
  {
    name: "jira-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools: TOOLS };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result: string;

    switch (name) {
      case "get_jira_issue": {
        const issueKey = (args as Record<string, string>).issue_key;
        result = await getJiraIssue(issueKey);
        break;
      }
      case "create_jira_comment": {
        const { issue_key, comment_body } = args as Record<string, string>;
        result = await createJiraComment(issue_key, comment_body);
        break;
      }
      default:
        throw new Error(`Unknown tool: "${name}"`);
    }

    return {
      content: [
        {
          type: "text",
          text: result,
        },
      ],
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ error: message }, null, 2),
        },
      ],
      isError: true,
    };
  }
});

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  // MCP servers communicate over stdio; do not write to stdout after connecting.
  process.stderr.write("Jira MCP server running on stdio.\n");
}

main().catch((error) => {
  process.stderr.write(`Fatal error: ${error}\n`);
  process.exit(1);
});
