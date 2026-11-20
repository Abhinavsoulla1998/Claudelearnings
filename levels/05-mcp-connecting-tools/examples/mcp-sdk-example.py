"""
MCP in the Agent SDK — SQLite example

Demonstrates how to use the Claude Code SDK to run a Claude query that
connects to a real database via an MCP server, all from a Python script.

SQLite is used here because it requires no credentials and no running
database server, making this example runnable by anyone.

Prerequisites:
    pip install claude-code-sdk

Run:
    python mcp-sdk-example.py

What this script does:
    1. Creates a sample SQLite database (sample_store.db) with products,
       customers, and orders tables, populated with realistic test data.
    2. Configures a Claude session with the SQLite MCP server attached.
    3. Asks Claude to summarize the data across all three tables.
    4. Streams and prints Claude's response.
    5. Cleans up the temporary database file after the run.
"""

from __future__ import annotations

import asyncio
import os
import sqlite3
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# SDK imports
# ---------------------------------------------------------------------------

try:
    from claude_code_sdk import ClaudeCodeOptions, MCPServerConfig, query
    from claude_code_sdk.types import AssistantMessage, TextBlock
except ImportError:
    sys.stderr.write(
        "Error: claude-code-sdk is not installed.\n"
        "Install it with:  pip install claude-code-sdk\n"
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Database bootstrap
# ---------------------------------------------------------------------------

def create_sample_database(db_path: str) -> None:
    """
    Create and populate a sample SQLite database with three tables:
      - products   : items available for purchase
      - customers  : registered customers
      - orders     : purchase history linking customers to products
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT    NOT NULL,
            category     TEXT    NOT NULL,
            price_cents  INTEGER NOT NULL,
            stock        INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS customers (
            customer_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT    NOT NULL,
            email        TEXT    NOT NULL UNIQUE,
            country      TEXT    NOT NULL,
            created_at   TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
            product_id   INTEGER NOT NULL REFERENCES products(product_id),
            quantity     INTEGER NOT NULL DEFAULT 1,
            ordered_at   TEXT    NOT NULL
        );
    """)

    cursor.executemany(
        "INSERT OR IGNORE INTO products (name, category, price_cents, stock) VALUES (?, ?, ?, ?)",
        [
            ("Wireless Keyboard",  "Electronics", 4999,  120),
            ("Ergonomic Mouse",    "Electronics", 3499,   85),
            ("USB-C Hub 7-in-1",   "Electronics", 2999,  200),
            ("Standing Desk Mat",  "Office",       8999,   45),
            ("Monitor Arm",        "Office",       5499,   30),
            ("Notebook A5",        "Stationery",    699,  500),
            ("Blue Ballpoint Pen", "Stationery",    199, 1000),
            ("Whiteboard Markers", "Stationery",   1299,  250),
            ("Webcam 1080p",       "Electronics", 7499,   60),
            ("Cable Organiser",    "Accessories",  1499,  180),
        ],
    )

    cursor.executemany(
        "INSERT OR IGNORE INTO customers (name, email, country, created_at) VALUES (?, ?, ?, ?)",
        [
            ("Alice Johnson",  "alice@example.com",   "US", "2024-01-15"),
            ("Bob Patel",      "bob@example.com",     "IN", "2024-02-03"),
            ("Clara Schmidt",  "clara@example.com",   "DE", "2024-03-20"),
            ("David Osei",     "david@example.com",   "GH", "2024-04-11"),
            ("Elena Rossi",    "elena@example.com",   "IT", "2024-05-08"),
            ("Frank Tanaka",   "frank@example.com",   "JP", "2024-06-30"),
            ("Grace Williams", "grace@example.com",   "GB", "2024-07-22"),
            ("Hiro Nakamura",  "hiro@example.com",    "JP", "2024-08-14"),
            ("Isla Brown",     "isla@example.com",    "AU", "2024-09-05"),
            ("James Lee",      "james@example.com",   "KR", "2024-10-18"),
        ],
    )

    cursor.executemany(
        "INSERT OR IGNORE INTO orders (customer_id, product_id, quantity, ordered_at) VALUES (?, ?, ?, ?)",
        [
            (1,  1,  1, "2025-01-10"),
            (1,  3,  2, "2025-01-10"),
            (2,  2,  1, "2025-01-14"),
            (3,  4,  1, "2025-01-20"),
            (3,  5,  1, "2025-01-20"),
            (4,  6,  5, "2025-01-25"),
            (5,  9,  1, "2025-02-02"),
            (6,  7, 10, "2025-02-07"),
            (7,  1,  1, "2025-02-12"),
            (7,  2,  1, "2025-02-12"),
            (8,  8,  2, "2025-02-18"),
            (9, 10,  3, "2025-02-22"),
            (10, 3,  1, "2025-03-01"),
            (1,  9,  1, "2025-03-05"),
            (2,  5,  1, "2025-03-10"),
            (3,  1,  2, "2025-03-15"),
            (4,  2,  1, "2025-03-18"),
            (5,  6,  3, "2025-03-22"),
            (6,  4,  1, "2025-03-28"),
            (7,  3,  1, "2025-04-01"),
        ],
    )

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Main script
# ---------------------------------------------------------------------------

PROMPT = """
You have access to a SQLite database with three tables: products, customers, and orders.

Please provide a concise data summary covering:
1. How many rows are in each table.
2. The top 3 best-selling products by total quantity ordered.
3. The top 3 customers by number of orders placed.
4. The revenue breakdown by product category (sum of price_cents * quantity for each category).
5. Any data quality observations (missing values, unusual patterns, potential anomalies).

Format your response with clear section headings and use a table where it aids clarity.
"""


async def main() -> None:
    # Create a temporary SQLite database that is cleaned up after the run.
    db_fd, db_path = tempfile.mkstemp(suffix=".db", prefix="mcp_sdk_sample_")
    os.close(db_fd)

    try:
        print(f"Creating sample SQLite database at: {db_path}")
        create_sample_database(db_path)
        print("Database ready. Starting Claude session with SQLite MCP...\n")

        options = ClaudeCodeOptions(
            model="claude-sonnet-4-6",
            # "auto" lets Claude use MCP tools without asking for confirmation
            # each time. Acceptable here because we are using a read-only SQLite
            # file on a local temp path with no credentials.
            permission_mode="auto",
            mcp_servers=[
                MCPServerConfig(
                    name="sqlite",
                    command="npx",
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-sqlite",
                        db_path,
                    ],
                )
            ],
        )

        print("Claude response:\n" + "=" * 60)

        async for message in query(prompt=PROMPT, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text, end="", flush=True)

        print("\n" + "=" * 60)
        print("\nDone.")

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(0)
    except Exception as exc:
        sys.stderr.write(f"Error: {exc}\n")
        sys.exit(1)
    finally:
        # Always remove the temporary database file.
        try:
            Path(db_path).unlink(missing_ok=True)
            print(f"Cleaned up temporary database: {db_path}")
        except OSError as cleanup_error:
            sys.stderr.write(f"Warning: could not remove {db_path}: {cleanup_error}\n")


if __name__ == "__main__":
    asyncio.run(main())
