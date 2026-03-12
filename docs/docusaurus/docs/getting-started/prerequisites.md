---
sidebar_position: 1
title: Prerequisites
description: What you need before installing Pilot Shell
---

# Prerequisites

What you need before installing Pilot Shell.

## Claude Code (Auto-Installed)

Pilot Shell installs **on top of Claude Code**. If Claude Code is not already installed, the Pilot Shell installer will install it automatically via the [native installer](https://docs.anthropic.com/en/docs/claude-code/setup).

## Claude Subscription

Pilot enhances Claude Code — it doesn't replace it. You need an active Claude subscription. Solo developers, teams, and enterprise organizations are all supported.

| Plan | Audience | Notes |
|------|----------|-------|
| **Max 5x** | Solo — moderate usage | Good for part-time or focused coding sessions |
| **Max 20x** | Solo — heavy usage | Recommended for full-time AI-assisted development |
| **Team Premium** | Teams | 6.25x usage per member + SSO, admin tools, billing management |
| **Enterprise** | Companies | For organizations with compliance, procurement, or security requirements |

## System Requirements

Pilot installs once and works across all your projects. Each project can have its own `.claude/` rules and skills.

| Platform | Notes |
|----------|-------|
| **macOS** | 10.15 Catalina or later, Apple Silicon and Intel |
| **Linux** | Debian, Ubuntu, RHEL-based distros, and most others |
| **Windows** | WSL2 required — native Windows not supported |

:::tip Windows users
Install WSL2 first (`wsl --install -d Ubuntu`), then run the installer inside Ubuntu.
:::
