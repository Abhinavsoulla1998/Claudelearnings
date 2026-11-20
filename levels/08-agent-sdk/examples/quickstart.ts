/**
 * quickstart.ts — Claude Code Agent SDK: minimal working TypeScript example.
 *
 * Demonstrates:
 *   - Importing from @anthropic-ai/claude-code
 *   - Configuring ClaudeCodeOptions (model, permissionMode, systemPrompt)
 *   - Streaming a response using for await
 *   - Handling message types: text, tool_use, result
 *   - Basic error handling and process exit
 *
 * Usage:
 *   export ANTHROPIC_API_KEY=your-key-here
 *   npx ts-node quickstart.ts
 *   # or compile and run:
 *   npx tsc quickstart.ts && node quickstart.js
 */

import { ClaudeCodeOptions, query } from "@anthropic-ai/claude-code";

async function main(): Promise<void> {
  // Validate environment before making any API calls.
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    console.error("Error: ANTHROPIC_API_KEY is not set.");
    console.error("Set it with: export ANTHROPIC_API_KEY=your-key-here");
    process.exit(1);
  }

  // ClaudeCodeOptions configures the agent session.
  const options: ClaudeCodeOptions = {
    // Model to use. claude-sonnet-4-6 is a good balance of capability and cost.
    // Use claude-haiku-4-5 for faster, cheaper responses in automated pipelines.
    model: "claude-sonnet-4-6",

    // permissionMode controls how Claude handles tool calls.
    // 'auto' allows safe operations without prompting — appropriate for scripts.
    permissionMode: "auto",

    // systemPrompt scopes Claude's behavior for this session.
    systemPrompt:
      "You are a helpful developer assistant. " +
      "When asked about files, run shell commands to get accurate information. " +
      "Be concise and precise.",
  };

  const prompt =
    "List the 5 most recently modified files in the current directory.";

  console.log(`Prompt: ${prompt}`);
  console.log("-".repeat(60));

  try {
    // query() returns an async iterable. Each iteration yields one message event.
    // The for await loop drives the full agentic loop: Claude thinks, calls tools,
    // processes tool results, and continues until it has a final answer.
    for await (const message of query({ prompt, options })) {
      switch (message.type) {
        case "text":
          // Claude is generating text output. Print it as it streams.
          process.stdout.write(message.text);
          break;

        case "tool_use":
          // Claude is about to call a tool (e.g., Bash, Read, Glob).
          // message.name is the tool name; message.input is the tool parameters.
          process.stdout.write(`\n[Tool call: ${message.name}]`);
          if (message.input) {
            const input = message.input as Record<string, unknown>;
            const cmd = input["command"];
            if (typeof cmd === "string" && cmd) {
              process.stdout.write(`\n  Command: ${cmd}`);
            }
          }
          process.stdout.write("\n");
          break;

        case "tool_result":
          // The tool has returned a result. Claude will process this before
          // continuing. Skip printing to keep output clean.
          break;

        case "result":
          // The session has ended.
          console.log("\n\n[Session complete]");
          console.log(`  Stop reason: ${message.stop_reason}`);
          if (message.cost_usd != null) {
            console.log(`  Cost: $${message.cost_usd.toFixed(4)} USD`);
          }
          if (message.duration_ms != null) {
            console.log(`  Duration: ${message.duration_ms}ms`);
          }
          break;

        case "system":
          // System messages from the SDK (initialization, warnings).
          // Usually safe to ignore, but useful for debugging.
          break;

        default:
          // Forward compatibility: ignore unknown message types.
          break;
      }
    }
  } catch (error: unknown) {
    if (error instanceof Error && error.message.includes("interrupted")) {
      console.log("\n\nInterrupted by user.");
      process.exit(0);
    }
    console.error(
      "\n\nError during agent session:",
      error instanceof Error ? error.message : String(error)
    );
    process.exit(1);
  }
}

main();
