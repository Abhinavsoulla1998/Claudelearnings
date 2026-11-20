---
name: changelog
description: Generate a CHANGELOG.md entry from recent git commits in Keep a Changelog format (Added, Changed, Fixed, Removed sections).
---

You are helping the developer write a changelog entry. Follow these steps exactly:

1. Run `git log --oneline --since="$(git describe --tags --abbrev=0 2>/dev/null || echo '30 days ago')" 2>/dev/null` to get commits since the last tag. If no tags exist, fall back to the last 30 days.

2. Run `git describe --tags --abbrev=0 2>/dev/null` to find the most recent version tag. If no tags exist, use `Unreleased` as the version label.

3. Run `git log --format="%s|%b" --since="$(git describe --tags --abbrev=0 2>/dev/null || echo '30 days ago')" 2>/dev/null` to get full commit subjects and bodies for categorization.

4. Categorize commits into Keep a Changelog sections using these rules:
   - **Added**: new features, new commands, new files, new endpoints (keywords: add, feat, new, introduce, implement)
   - **Changed**: modifications to existing behavior (keywords: update, change, refactor, improve, rename, move)
   - **Fixed**: bug fixes (keywords: fix, resolve, correct, repair, patch)
   - **Removed**: deleted features or files (keywords: remove, delete, drop, deprecate)
   - **Security**: security-related changes (keywords: security, cve, vulnerability, auth)
   - Omit any section that has no entries.

5. Determine today's date using the `date +%Y-%m-%d` command.

6. Output the changelog entry in this exact format:

```
## [VERSION] - YYYY-MM-DD

### Added
- [entry]

### Changed
- [entry]

### Fixed
- [entry]

### Removed
- [entry]
```

Rules:
- Write each entry as a short imperative sentence (e.g., "Add user authentication endpoint").
- Do not include commit hashes or author names.
- Do not include merge commits or version bump commits.
- Do not include entries for test file changes unless the change is significant.
- If a commit message is ambiguous, use judgment to place it in the most appropriate section.
- Print only the formatted changelog block. Do not add any explanation before or after it.
