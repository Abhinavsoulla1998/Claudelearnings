---
name: daily-standup
description: Generate a standup summary from the last 24 hours of git activity and open TODOs. Output is formatted as Done / In Progress / Blockers and kept under 150 words.
---

You are helping the developer run their daily standup. Follow these steps exactly:

1. Run `git log --oneline --since="24 hours ago" --author="$(git config user.name)" 2>/dev/null` to get commits made in the last 24 hours. If the directory is not a git repo or the command fails, note that and skip git steps.

2. Run `git status --short 2>/dev/null` to identify any uncommitted work in progress.

3. Run `grep -rn "TODO\|FIXME\|HACK" --include="*.py" --include="*.ts" --include="*.js" --include="*.go" . 2>/dev/null | head -10` to find open TODO comments in the codebase.

4. Based on the above, produce a standup summary in this exact format:

**Done**
- [list completed commits as short action phrases, one per line]

**In Progress**
- [list any WIP commits (containing "wip", "WIP", "draft", or uncommitted changes) and open TODOs that appear actively worked on]

**Blockers**
- [list anything that appears stuck, failing, or flagged as FIXME/HACK; write "None" if there are no blockers]

Rules:
- Keep the entire output under 150 words.
- Use past tense for Done items and present continuous for In Progress items.
- Do not include file paths in the output unless they are essential to understanding a blocker.
- Do not add any preamble or conclusion outside the three sections above.
