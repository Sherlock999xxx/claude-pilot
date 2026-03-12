---
sidebar_position: 3
title: Pilot Console
description: Local web dashboard at localhost:41777 — monitor and manage your sessions
---

# Pilot Console

Local web dashboard at `localhost:41777` — monitor and manage your sessions.

The Console runs locally as a Bun/Express server with a React web UI. It's automatically started when you launch Pilot and stopped when all sessions close. All data — memories, sessions, usage — is stored in a local SQLite database. Nothing leaves your machine.

```bash
$ open http://localhost:41777
```

## 8 Views

| View | Description |
|------|-------------|
| **Dashboard** | Workspace status, active sessions, spec progress, git info, recent activity. Your real-time command center. |
| **Specifications** | All spec plans with task progress (checkboxes), phase tracking (PENDING/COMPLETE/VERIFIED), and iteration history. |
| **Memories** | Browsable observations — decisions, discoveries, bugfixes — with type filters, search, and timeline view. |
| **Sessions** | Active and past sessions with observation counts, duration, and the ability to browse session context. |
| **Usage** | Daily token costs, model routing breakdown (Opus vs Sonnet distribution), and usage trends over time. |
| **Share** | Browse, edit, rename, and delete all assets (skills, rules, commands, agents). Filter by scope and type. Push/pull to git remotes. Markdown preview. |
| **Settings** | Model selection per command and sub-agent (Sonnet 4.6 vs Opus 4.6), extended context toggle (1M tokens). |
| **Help** | Embedded documentation from pilot-shell.com — full technical reference without leaving the Console. |

## Smart Notifications via SSE

The Console sends real-time alerts via Server-Sent Events when Claude needs your input or a significant phase completes. You don't need to watch the terminal constantly — the Console notifies you.

- Plan requires your approval — review and respond in the terminal or via notification
- Spec phase completed — implementation done, verification starting
- Clarification needed — Claude is waiting for design decisions before proceeding
- Session ended — completion summary with observation count

:::info Settings tab
Configure model selection per component — Planning (Opus), Implementation (Sonnet), Verification (Sonnet), each sub-agent independently. Enable the **Extended Context (1M)** toggle to use the 1M token context window across all models simultaneously. *Requires Max 20x or Enterprise subscription.*
:::
