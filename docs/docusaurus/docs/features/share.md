---
sidebar_position: 1
title: Customize & Share
description: Create your own rules, commands, and skills — then share them across machines, projects, and organizations
---

# Customize & Share

Create your own rules, commands, and skills — then share them across machines, projects, and organizations.

## Create Your Own Assets

All assets are plain markdown files in your project's `.claude/` directory. Your project-level assets load alongside Pilot's built-in defaults and take precedence when they overlap.

| Asset | Location | When it loads | Best for |
|-------|----------|---------------|----------|
| **Rules** | `.claude/rules/` | Every session, or conditionally by file type | Guidelines Claude should always follow |
| **Commands** | `.claude/commands/` | On demand via `/command-name` | Specific workflows or multi-step tasks |
| **Skills** | `.claude/skills/` | Automatically when relevant | Reusable knowledge from past sessions |
| **Agents** | `.claude/agents/` | Spawned as sub-agents for specialized tasks | Code review, security audits, domain experts |

### How to create assets

- **Rules** — Create `.claude/rules/my-rule.md`. Add `paths: ["*.py"]` frontmatter to activate only for specific file types. Rules without `paths` load every session.
- **Commands** — Create `.claude/commands/my-command.md`. Invoke with `/my-command` in any session.
- **Skills** — Create `.claude/skills/my-skill.md` with a `description` frontmatter. Claude loads skills automatically when their description matches the current task.

### Auto-generation

- `/sync` explores your codebase and generates project-specific rules based on your tech stack, conventions, and patterns.
- `/learn` captures non-obvious debugging discoveries, workarounds, and tool integrations as reusable skills.

### Monorepo support

Organize rules in nested subdirectories by product and team (e.g. `.claude/rules/my-product/team-x/`). Team-level rules must use `paths` frontmatter to scope to the right files. `/sync` validates the structure, enforces path-scoping, and generates a `README.md` to document the organization.

### MCP servers

Add custom MCP servers in `.mcp.json`, then run `/sync` to generate documentation so Claude knows how to use them.

## Share Across Boundaries

Share all four asset types across machines, projects, and organizations using [Skillshare](https://github.com/runkids/skillshare). Skillshare is installed automatically by the Pilot installer and works with **50+ AI coding tools** — Claude Code, Cursor, Codex, Windsurf, Copilot, and more. One central source of truth for all your AI assets.

Use the `skillshare` CLI for operations and the Console Share page for browsing, editing, and managing assets.

### Getting Started

```bash
# Global mode — available in all projects
skillshare init --targets claude

# Project mode — skills committed to this repo
skillshare init -p --targets claude

# Cross-machine sync — add a git remote
skillshare init --remote git@github.com:you/my-skills.git
```

### Project Mode — team sharing via git

Commit `.skillshare/skills/` to your repo. Team members get all assets on `git clone` — no extra setup.

```bash
skillshare init -p --targets claude     # Initialize project mode
skillshare install <url> -p             # Install a skill to the project
skillshare install -p                   # Install all from registry.yaml
skillshare sync -p                      # Sync to Claude's directory
skillshare status -p                    # Check project status
```

New team members onboard with:

```bash
git clone <repo> && cd <repo> && skillshare install -p && skillshare sync -p
```

[Project Setup Guide →](https://skillshare.runkids.cc/docs/how-to/sharing/project-setup)

### Global Mode — personal cross-machine sync

Skills in `~/.config/skillshare/skills/` sync to `~/.claude/skills/` on every machine. Add a git remote to push/pull between devices.

```bash
skillshare init --remote git@github.com:you/my-skills.git   # First machine
skillshare push -m "Add skill"                               # Push changes
# On another machine:
skillshare init --remote git@github.com:you/my-skills.git   # Auto-pulls
skillshare pull                                              # Sync updates
```

```bash
skillshare status -g            # Global status
skillshare list -g              # List global skills
skillshare install <url> -g     # Install to global
skillshare sync -g --all        # Sync skills + extras → Claude
skillshare collect -g           # Import local-only skills to source
skillshare diff -g              # Show pending changes
```

[Cross-Machine Sync Guide →](https://skillshare.runkids.cc/docs/how-to/sharing/cross-machine-sync)

### Extras — rules, commands, agents

Share non-skill assets across machines via extras (global only). Place files in `~/.config/skillshare/{rules,commands,agents}/` and sync with `skillshare sync -g --all`.

| To share | Place file in | Syncs to |
|----------|---------------|----------|
| Rule | `~/.config/skillshare/rules/my-rule.md` | `~/.claude/rules/my-rule.md` |
| Command | `~/.config/skillshare/commands/my-cmd.md` | `~/.claude/commands/my-cmd.md` |
| Agent | `~/.config/skillshare/agents/my-agent.md` | `~/.claude/agents/my-agent.md` |

Extras are included when you push/pull — they sync across machines automatically. The Pilot installer configures extras automatically.

### Organization Mode — org-wide distribution

Track shared repos to distribute curated assets across your organization.

```bash
skillshare install github.com/org/skills --track   # Install tracked repo
skillshare update --all && skillshare sync -g       # Update all tracked repos
```

[Organization Sharing Guide →](https://skillshare.runkids.cc/docs/how-to/sharing/organization-sharing)

### Console Share Page

The Share page in the Pilot Console provides a full management interface:

- **Source & Sync** — asset counts (skills, rules, commands, agents) for both project and global scopes
- **Team Remote** — connected git remotes with **Push** and **Pull** buttons for one-click sync
- **Assets Grid** — all assets with type and scope badges, filterable by scope (Project / Global / All) and type (Skill / Rule / Command / Agent), plus text search
- **Asset Detail** — click any asset to:
  - **Preview** rendered markdown or view raw source
  - **Edit** markdown in-place with a Save button
  - **Rename** the asset file
  - **Delete** with confirmation prompt
  - View metadata (source, version, install date, repository URL) and file list

### CLI Quick Reference

| Command | Description |
|---------|-------------|
| `skillshare init --targets claude` | Initialize global mode |
| `skillshare init -p --targets claude` | Initialize project mode |
| `skillshare init --remote <url>` | Set up git remote |
| `skillshare status -g` / `-p` | Check status |
| `skillshare list -g` / `-p` | List skills |
| `skillshare install <url> -g` / `-p` | Install a skill |
| `skillshare sync -g --all` | Sync skills + extras |
| `skillshare sync -p` | Sync project skills |
| `skillshare collect -g` | Import local-only skills |
| `skillshare update --all` | Update tracked repos |
| `skillshare push -m "msg"` | Push to remote |
| `skillshare pull` | Pull from remote |
| `skillshare diff -g` / `-p` | Show pending changes |
| `skillshare audit --json -g` | Security audit |

### Documentation

- [Quick Start](https://skillshare.runkids.cc/docs/learn/with-claude-code) — Get started with Skillshare
- [Commands Reference](https://skillshare.runkids.cc/docs/reference/commands) — All CLI commands
- [Cross-Machine Sync](https://skillshare.runkids.cc/docs/how-to/sharing/cross-machine-sync) — Sync via git push/pull
- [Project Setup](https://skillshare.runkids.cc/docs/how-to/sharing/project-setup) — Commit skills to your repo
- [Organization Sharing](https://skillshare.runkids.cc/docs/how-to/sharing/organization-sharing) — Tracked repos for teams
