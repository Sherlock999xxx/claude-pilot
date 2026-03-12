---
sidebar_position: 2
title: Hooks Pipeline
description: 15 hooks across 7 lifecycle events — fire automatically at every stage
---

# Hooks Pipeline

15 hooks across 7 lifecycle events — fire automatically at every stage.

Hooks are the enforcement layer. They run at each stage of Claude's work cycle — automatically, without prompting. Blocking hooks can reject an action or force a fix. Non-blocking hooks warn without interrupting. Async hooks run in the background.

## SessionStart

*On startup, clear, or after compaction*

| Hook | Type | Description |
|------|------|-------------|
| Memory loader | Blocking | Loads persistent context from Console memory into the session |
| `post_compact_restore.py` | Blocking | Re-injects active plan, task state, and key context after compaction |
| Session tracker | Async | Initializes user message tracking for the session |

## UserPromptSubmit

*When the user sends a message*

| Hook | Type | Description |
|------|------|-------------|
| Session initializer | Async | Registers the session with the Console worker daemon on first message |

## PreToolUse

*Before search, web, or task tools*

| Hook | Type | Description |
|------|------|-------------|
| `tool_redirect.py` | Blocking | Redirects to MCP alternatives, blocks plan mode conflicts, hints Probe CLI for search |

## PostToolUse

*After every Write / Edit / MultiEdit*

| Hook | Type | Description |
|------|------|-------------|
| `file_checker.py` | Blocking | Python (ruff + basedpyright), TypeScript (Prettier + ESLint + tsc), Go (gofmt + golangci-lint). Auto-fixes formatting. |
| `tdd_enforcer.py` | Non-blocking | Warns when implementation files are edited without a failing test first |
| `context_monitor.py` | Non-blocking | Tracks context usage 0–100%. Warns at ~80%, caution at ~90%+ |
| Memory observer | Async | Captures decisions, discoveries, and bugfixes to persistent memory |

## PreCompact

*Before auto-compaction fires*

| Hook | Type | Description |
|------|------|-------------|
| `pre_compact.py` | Blocking | Snapshots active plan, task list, and key decisions to memory |

## Stop

*When Claude tries to finish*

| Hook | Type | Description |
|------|------|-------------|
| `spec_stop_guard.py` | Blocking | Blocks stopping if an active spec hasn't completed verification |
| `spec_plan_validator.py` | Blocking | Verifies plan file was created with required sections |
| `spec_verify_validator.py` | Blocking | Verifies plan status was updated to VERIFIED |
| Session summarizer | Async | Saves session observations to memory for future sessions |

## SessionEnd

*When the session closes*

| Hook | Type | Description |
|------|------|-------------|
| `session_end.py` | Blocking | Stops worker daemon if no other sessions active. Sends dashboard notification. |

:::info Closed loop
When compaction fires, **PreCompact** captures your active plan, task list, and key decisions to persistent memory. **SessionStart** restores everything afterward — work continues exactly where it left off. No progress lost, no manual intervention.
:::
