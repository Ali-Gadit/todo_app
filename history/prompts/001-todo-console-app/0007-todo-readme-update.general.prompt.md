---
id: 0007
title: todo-readme-update
stage: general
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-console-app
branch: master
user: n/a
command: documentation update
labels: ["docs", "readme", "uv"]
links:
  spec: specs/001-todo-console-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - README.md
tests:
  - N/A (Manual documentation check)
---

## Prompt

update the readme.md file because the command are not properly mentioned there and the error which came to me was because of that

## Response snapshot

Updated the `README.md` to use `uv run todo <command>` across all examples.

**Changes Summary**:
- Updated **Setup** section to show `uv run todo list` and `python -m todo_app.cli.main list`.
- Prefixed all **Usage** examples with `uv run todo`.
- Updated **Command Reference** to show the correct usage format.
- Explained that `uv sync` installs the `todo` command alias.

## Outcome

- ✅ Impact: README now provides working, copy-pasteable commands matching the current project configuration.
- 🧪 Tests: N/A
- 📁 Files: 1 file updated.
- 🔁 Next prompts: N/A
