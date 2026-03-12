---
sidebar_position: 4
title: Pilot CLI
description: Full command reference for the pilot binary at ~/.pilot/bin/pilot
---

# Pilot CLI

Full command reference for the pilot binary at `~/.pilot/bin/pilot`.

The `pilot` binary manages sessions, worktrees, licensing, and context. Run `pilot` or `ccp` with no arguments to start Claude with Pilot enhancements. All commands support `--json` for structured output. Multiple sessions can run in parallel on the same project — each tracks its own worktree and context state independently.

## Session & Context

| Command | Description |
|---------|-------------|
| `pilot` | Start Claude with Pilot enhancements, auto-update, and license check |
| `pilot run [args...]` | Same as above, with optional flags (`--skip-update-check`) |
| `ccp` | Alias for pilot — shorter to type |
| `pilot check-context --json` | Get current context usage percentage (informational) |
| `pilot register-plan <path> <status>` | Associate a plan file with the current session for statusline display |
| `pilot sessions [--json]` | Show count of active Pilot sessions |

## Worktree Isolation

| Command | Description |
|---------|-------------|
| `pilot worktree create --json <slug>` | Create isolated git worktree for safe experimentation |
| `pilot worktree detect --json <slug>` | Check if a worktree already exists |
| `pilot worktree diff --json <slug>` | List changed files in the worktree |
| `pilot worktree sync --json <slug>` | Squash merge worktree changes back to base branch |
| `pilot worktree cleanup --json <slug>` | Remove worktree and branch when done |
| `pilot worktree status --json` | Show active worktree info for current session |

## License & Auth

| Command | Description |
|---------|-------------|
| `pilot activate <key>` | Activate a license key on this machine |
| `pilot deactivate` | Deactivate license on this machine |
| `pilot status [--json]` | Show current license status and tier |
| `pilot verify [--json]` | Verify license validity (used by hooks) |
| `pilot trial --check [--json]` | Check trial eligibility for this machine |
| `pilot trial --start [--json]` | Start a trial (one-time per machine) |

:::info Slug format
The `<slug>` parameter for worktree commands is the plan filename without the date prefix and `.md` extension. For example, `docs/plans/2026-02-22-add-auth.md` → `add-auth`.
:::
