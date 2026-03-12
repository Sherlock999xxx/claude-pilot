---
slug: /
sidebar_position: 0
title: Introduction
description: Complete technical reference for Pilot Shell
---

# Pilot Shell Documentation

**Pilot Shell** is the professional development environment for Claude Code. It provides spec-driven development, endless context, persistent memory, quality hooks, online learning, and a modular rules system.

## Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/maxritter/pilot-shell/main/install.sh | bash

# Start
cd your-project && pilot

# Sync with your codebase
> /sync

# Plan and build a feature
> /spec "Add user authentication with OAuth"
```

## What's Inside

| Category | Highlights |
|----------|-----------|
| **[Getting Started](/docs/getting-started/prerequisites)** | Prerequisites, one-command installation |
| **[Workflows](/docs/workflows/sync)** | `/sync`, `/spec`, Quick Mode, `/learn` |
| **[Features](/docs/features/share)** | Customize & share, hooks pipeline, context preservation, rules, model routing |
| **[Tools](/docs/tools/mcp-servers)** | MCP servers, language servers, Console dashboard, CLI reference |
| **[Reference](/docs/reference/open-source)** | Open source compliance |

## Key Commands

| Command | Purpose |
|---------|---------|
| `pilot` or `ccp` | Start Claude with Pilot enhancements |
| `/sync` | Explore codebase and sync rules |
| `/spec "task"` | Plan → Implement → Verify with TDD |
| `/learn` | Extract knowledge into reusable skills |

## Architecture

Pilot enhances Claude Code with:

- **15 hooks** across 7 lifecycle events for automatic quality enforcement
- **5 MCP servers** for library docs, memory, web search, code search, and page fetching
- **3 language servers** (Python, TypeScript, Go) for real-time diagnostics
- **Intelligent model routing** — Opus for planning, Sonnet for implementation
- **Persistent memory** via local SQLite — decisions and context survive across sessions
- **Pilot Console** — local web dashboard for monitoring, configuration, and skill sharing
