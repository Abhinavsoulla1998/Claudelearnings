# Exercise: Set Up Project Memory with CLAUDE.md

## Goal
Create a CLAUDE.md in a real project so Claude understands your codebase without repeated prompting.

## Steps

### Step 1: Copy the template

```bash
cp path/to/claude-curriculum/levels/02-core-features/templates/CLAUDE.md.template /your/project/CLAUDE.md
```

### Step 2: Fill in your project details

Open `CLAUDE.md` and replace all `[placeholder]` sections with real values:
- Tech stack (runtime, framework, database, test runner)
- Commands (test, lint, build, start)
- Code conventions (naming, error handling, imports)
- Architecture overview (main directories and their purpose)
- Off-limits directories

### Step 3: Verify Claude reads it

Start a new Claude session from your project root:

```bash
cd /your/project
claude "What do you know about this project? Summarize the tech stack and main commands."
```

**Check:** Does Claude mention your actual tech stack? Does it know your test command?

### Step 4: Test convention adherence

Ask Claude to write a small new function or route. Without giving any extra instructions, check:
- Does the naming follow your documented convention?
- Does error handling match your documented pattern?
- Does it use the right imports?

### Step 5: Commit it

```bash
git add CLAUDE.md
git commit -m "Add CLAUDE.md project memory for Claude Code"
```

## Success Criterion

Claude generates code matching your documented conventions without you repeating them in the prompt.

## Troubleshooting

- If Claude does not reference CLAUDE.md, check that you started Claude from the project root (not a subdirectory)
- If Claude references outdated conventions, re-read and update CLAUDE.md — it gets stale
- CLAUDE.md is case-sensitive on Linux — ensure the filename is exactly `CLAUDE.md`
