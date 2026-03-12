---
sidebar_position: 1
title: /sync — Codebase Sync
description: Learn your existing codebase and sync rules with it
---

# /sync — Codebase Sync

Learn your existing codebase and sync rules with it.

Run `/sync` to explore your project structure, discover your conventions and undocumented patterns, update project documentation, and create new custom skills. This is how Pilot adapts to your project — not the other way around. Run it once initially, then any time your codebase changes significantly.

```bash
$ pilot
> /sync
```

## What /sync Does

13 phases (zero-indexed):

| Phase | Action |
|-------|--------|
| 0 | Load reference guidelines, recommended directory structure, error handling |
| 1 | Read existing rules (including nested subdirectories), detect structure and path-scoping |
| 2 | Migrate unscoped assets to `{slug}`-prefixed names |
| 3 | Quality audit against best practices (size, specificity, path-scoping enforcement) |
| 4 | Explore codebase with Probe CLI/Grep to find patterns |
| 5 | Compare discovered vs documented patterns |
| 6 | Sync project rule, nested directories, and generate rules README |
| 7 | Sync MCP server documentation |
| 8 | Update existing custom skills that have changed |
| 9 | Discover new rules, place in correct directory by scope |
| 10 | Create new skills via `/learn` command |
| 11 | Cross-check: validate references, README, path-scoping |
| 12 | Report summary of all changes made |

## When to Run /sync

- After installing Pilot in a new project
- After making significant architectural changes
- When adding new MCP servers to `.mcp.json`
- Before starting a complex `/spec` task on an unfamiliar codebase
- After onboarding to a project you didn't write
