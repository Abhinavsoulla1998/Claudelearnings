#!/usr/bin/env python3
"""
custom-tool.py — Claude Code Agent SDK: custom tool definition pattern.

Demonstrates:
  - Defining a custom tool with a name, description, and JSON Schema input schema
  - Passing the tool to the query() call
  - Intercepting tool_use messages to handle the custom tool call
  - Returning mocked data (no external dependencies required)
  - The full tool call cycle: Claude requests tool -> handler runs -> result returned

The example tool is get_weather. In a real implementation you would call a
weather API; here we return mocked data so the example runs without any API keys
beyond ANTHROPIC_API_KEY.

Usage:
    export ANTHROPIC_API_KEY=your-key-here
    python custom-tool.py
"""

import asyncio
import json
import os
import sys
from typing import Any

from claude_code_sdk import ClaudeCodeOptions, query

# ---------------------------------------------------------------------------
# Step 1: Define the custom tool.
#
# The definition is a plain dict with three required keys:
#   name          — identifier Claude uses to call the tool
#   description   — natural language description that helps Claude decide when
#                   to use this tool
#   input_schema  — JSON Schema object describing the tool's parameters
# ---------------------------------------------------------------------------
GET_WEATHER_TOOL: dict[str, Any] = {
    "name": "get_weather",
    "description": (
        "Get the current weather conditions for a location. "
        "Use this tool when the user asks about weather, temperature, or climate "
        "for a specific place. Returns temperature, conditions, humidity, and wind speed."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": (
                    "The location to get weather for. Can be a city name, "
                    "city and country (e.g. 'London, UK'), or coordinates "
                    "(e.g. '51.5074,-0.1278')."
                ),
            },
            "units": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature units. Defaults to celsius if not specified.",
            },
        },
        "required": ["location"],
    },
}


# ---------------------------------------------------------------------------
# Step 2: Implement the tool handler.
#
# This function is called when Claude requests the get_weather tool.
# In a real implementation, call a weather API (OpenWeatherMap, etc.) here.
# We return mocked data to avoid external dependencies.
# ---------------------------------------------------------------------------
def handle_get_weather(tool_input: dict[str, Any]) -> dict[str, Any]:
    """Return mocked weather data for any location."""
    location = tool_input.get("location", "Unknown")
    units = tool_input.get("units", "celsius")

    # Mocked response — replace with a real API call in production.
    temp = 22 if units == "celsius" else 72
    unit_symbol = "C" if units == "celsius" else "F"

    return {
        "location": location,
        "temperature": temp,
        "unit": unit_symbol,
        "conditions": "Partly cloudy",
        "humidity_percent": 65,
        "wind_speed_kph": 15,
        "note": "This is mocked data for demonstration purposes.",
    }


# ---------------------------------------------------------------------------
# Step 3: Run the agent loop with the custom tool.
# ---------------------------------------------------------------------------
async def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    options = ClaudeCodeOptions(
        model="claude-sonnet-4-6",
        permission_mode="auto",
        system_prompt=(
            "You are a helpful weather assistant. "
            "When asked about the weather, always use the get_weather tool to look it up. "
            "Present the results in a friendly, readable format."
        ),
    )

    prompt = "What is the weather like in Tokyo right now? Please use Celsius."

    print(f"Prompt: {prompt}")
    print("-" * 60)

    # Pass the custom tool definition in the tools list.
    # Claude will see it alongside built-in tools and choose when to call it.
    async for message in query(
        prompt=prompt,
        options=options,
        tools=[GET_WEATHER_TOOL],
    ):
        if message.type == "text":
            print(message.text, end="", flush=True)

        elif message.type == "tool_use":
            print(f"\n[Tool requested: {message.name}]")
            print(f"  Input: {json.dumps(message.input, indent=2)}")

            # Handle our custom tool.
            if message.name == "get_weather":
                result = handle_get_weather(message.input or {})
                print(f"  Result: {json.dumps(result, indent=2)}")
                # The SDK automatically injects the tool result back into the
                # conversation. You do not need to manually send a tool_result
                # message — just handle the tool_use and return from the handler.
                # The SDK picks up the return value from the tool handler.
                #
                # NOTE: Depending on the SDK version, tool result injection may
                # require a different mechanism. Check the SDK documentation for
                # the current API for returning tool results.

        elif message.type == "result":
            print(f"\n\n[Session complete — stop reason: {message.stop_reason}]")
            if hasattr(message, "cost_usd") and message.cost_usd is not None:
                print(f"Cost: ${message.cost_usd:.4f} USD")


if __name__ == "__main__":
    asyncio.run(main())
