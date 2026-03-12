## Skill Sharing

Share skills, rules, commands, and agents across machines and teams using **Skillshare** and a Git repository.

### Two Modes

| Mode | Source Directory | Scope | Shared Via |
|------|-----------------|-------|------------|
| **Global** (`-g`) | `~/.config/skillshare/skills/` | All projects | Git remote (Team Remote) |
| **Project** (`-p`) | `.skillshare/skills/` | This repo only | Committed to repo |

Skills in the **source** are synced to the **target** (`~/.claude/skills/`) where Claude uses them. The sync button only appears when source and target differ.

### Sharing Tiers

| Tier | Feature | License |
|------|---------|---------|
| **All paid users** | Install, sync, cross-machine push/pull | Solo, Team, Trial |
| **Team/Trial only** | Team Remote, tracked repos, organization features | Team, Trial |

### Primary Interface

**Use the Share page in the Pilot Shell Console dashboard** (`http://localhost:41777/#/share`):

- **Source & Sync card** — shows Project (first) and Global sections with source → target arrows, per-section sync buttons (only when out of sync), and Collect button for local-only skills
- **Team Remote card** — manage multiple git remotes for global skills (Team/Trial plan). Push uploads current global state; Pull downloads from remote
- **Skills grid** — merged view of all global + project skills with scope badges
- **Install from URL** — paste a GitHub URL to install globally or to a project
- **How does this work?** — collapsed help section with explanations and documentation links
- **CLI Reference** — collapsed section with global and project commands side by side

### Key Concepts

- **Sync**: Distributes skills from source to target. **Must run after every mutation** (`install`, `uninstall`, `update`, `collect`).
- **Collect**: Imports skills that exist only in Claude's directory (e.g., from `/learn`) back into the source directory so they can be pushed/shared.
- **Team Remote**: Git remotes for **global skills only**. Project skills are shared by committing `.skillshare/` to the project repo instead.
- **Push**: Uploads current global skills to remote. Skills removed locally will also be removed from the remote.
- **Audit**: Security scan on install — blocks CRITICAL findings by default. Use `--skip-audit` to bypass, `--force` to override.
- **Trash**: `uninstall` moves to trash (7-day retention), not permanent deletion. Recover with `skillshare trash restore <name>`.
- **Hub**: Curated skill catalogs. `skillshare hub add <url>` to subscribe, `skillshare hub index` to build one.

### Cross-Machine Sync and Organization Sharing

Two complementary mechanisms — use both for personal skills + team/org standards:

**Personal remote** (`push`/`pull`) — your own skills across your machines:

```bash
skillshare init --remote git@github.com:you/my-skills.git  # First machine
skillshare push -m "Add skill"                              # Push changes
# On another machine:
skillshare init --remote git@github.com:you/my-skills.git  # Auto-pulls existing skills
skillshare pull                                             # Sync updates
```

**Tracked repos** (`install --track`) — team/org repos, multiple repos supported:

```bash
# Install team and org repos as tracked sources
skillshare install github.com/my-team/team-skills --track --name team-skills
skillshare install github.com/my-org/org-standards --track --name org-standards
skillshare sync

# Update all tracked repos at once
skillshare update --all && skillshare sync
```

**How they coexist:**

```
~/.config/skillshare/skills/
├── my-personal-skill/        ← your skills (push/pull via personal remote)
├── _team-skills/             ← tracked repo (update --all)
│   ├── react-patterns/
│   └── ui-guidelines/
└── _org-standards/           ← another tracked repo
    ├── security-audit/
    └── code-review/
```

`push`/`pull` syncs everything including tracked repos. Tracked repos also update independently via `skillshare update --all`. Collision detection warns if skills from different repos share the same `name` field.

### Tool Portability in Skills

Skills are shared with users who may not have Pilot Shell. **Only reference built-in Claude Code tools** in skill content:

| Use This (Built-in) | NOT This (Pilot-specific) |
|---------------------|--------------------------|
| `Grep`, `Glob` | `probe search/extract/query` |
| `Bash` + `npx playwright` | `playwright-cli` |
| `WebFetch`, `WebSearch` | Pilot MCP servers (`web-fetch`, `web-search`, `mem-search`, `context7`, `grep-mcp`) |
| `Bash` + standard CLI | `pilot` CLI, `skillshare` CLI |

If a skill requires a non-standard tool, list it as a prerequisite — never silently assume it exists.

### /learn and /sync Integration

Both `/learn` and `/sync` create skills in `.skillshare/skills/` **if it exists** in the project. Otherwise they fall back to `.claude/skills/`. When creating in `.skillshare/`, they run `skillshare sync -p` afterward to make the skill available to Claude. This works independently — if Skillshare isn't used, skills go directly to `.claude/skills/` as before.

### When to Use

| Situation | Action |
|-----------|--------|
| User says "share", "push", "sync skills" | Direct to Share page in Console |
| After `/learn` captures a new skill | Use Collect to import to source, then push |
| User wants skills on another machine | Set up Team Remote, push from source, pull on target |
| New team member onboarding | `skillshare install -p && skillshare sync -p` |
| Org-wide skill distribution | `skillshare install <url> --track` (Team plan) |

### Extras — Sharing Rules, Commands, and Agents

Skillshare can sync non-skill resources (rules, commands, agents) via **extras**. Configured automatically by the Pilot installer.

**Source directories** (global only):

```
~/.config/skillshare/
├── skills/       ← skill source
├── rules/        ← rules to share across machines
├── commands/     ← commands to share across machines
└── agents/       ← agents to share across machines
```

**How it works:** Files placed in extras source directories are synced to Claude's directories via `skillshare sync -g --all`. Merge mode preserves existing local files — only symlinks from extras source are managed.

**Sync:** `skillshare sync -g --all` syncs skills + extras in one command. `skillshare sync extras` syncs only extras. Extras are global only — not available in project mode.

**Cross-machine:** Extras source directories are part of the same git repo as skills. `skillshare push` / `pull` includes them automatically.

| To share | Place file in | Syncs to |
|----------|---------------|----------|
| Rule | `~/.config/skillshare/rules/my-rule.md` | `~/.claude/rules/my-rule.md` |
| Command | `~/.config/skillshare/commands/my-cmd.md` | `~/.claude/commands/my-cmd.md` |
| Agent | `~/.config/skillshare/agents/my-agent.md` | `~/.claude/agents/my-agent.md` |

**Note:** Pilot-managed rules/commands (installed by the Pilot installer) are tracked via manifest and should NOT be placed in extras. Extras are for user-created assets you want to share across machines.

### Non-Interactive Usage (for Claude)

Claude cannot answer interactive prompts. Always use non-interactive flags:

| Action | Flags |
|--------|-------|
| Install without prompts | `--all` or `-s name1,name2` or `--yes` |
| Uninstall without confirmation | `--force` |
| Collect without confirmation | `--force` |
| Override audit block | `--force` or `--skip-audit` |
| Preview changes | `--dry-run` |
| Structured output | `--json` |

**Always sync after mutations:** `install`, `uninstall`, `update`, `collect`, and `target` all modify source only — run `skillshare sync` to propagate to targets.

### CLI Quick Reference

```bash
# Global commands
skillshare status -g              # Global status
skillshare list -g                # List global skills
skillshare sync -g                # Sync global source → Claude
skillshare sync -g --all          # Sync skills + extras (rules, commands, agents)
skillshare install <url> -g       # Install to global
skillshare collect -g             # Import local-only skills to source
skillshare diff -g                # Show pending changes

# Project commands
skillshare init -p                # Initialize project mode
skillshare status -p              # Project status
skillshare list -p                # List project skills
skillshare sync -p                # Sync project source → Claude
skillshare install <url> -p       # Install to project
skillshare collect -p             # Import local-only skills
skillshare diff -p                # Show pending changes

# Skill management
skillshare new my-skill -p        # Create new skill (project)
skillshare new my-skill -g        # Create new skill (global)
skillshare uninstall my-skill     # Remove (moves to trash)
skillshare trash restore my-skill # Recover deleted skill
skillshare update --all           # Update all tracked repos
skillshare check                  # Check for available updates

# Cross-machine sync (global only)
skillshare init --remote <url>    # Set up git remote
skillshare push -m "Add skill"    # Commit and push to remote
skillshare pull                   # Pull from remote and sync

# Organization (Team/Trial)
skillshare install <url> --track  # Install tracked org repo
skillshare audit                  # Security audit of skills
skillshare doctor                 # Diagnose issues
skillshare hub add <url>          # Subscribe to a skill hub
skillshare hub index --full       # Build hub index from source
```

### Setup

Skillshare is installed automatically by the Pilot installer. For cross-machine sync, add a Team Remote via the Console Share page, or:

```bash
skillshare init --remote git@github.com:you/my-skills.git
```

### Project Mode

Project-level skills live in `.skillshare/skills/` and are committed to the repo:

```bash
skillshare init -p                    # Initialize project config
skillshare install <url> -p           # Install skill at project level
skillshare sync -p                    # Sync project skills to target
```

New team members get all project skills with:
```bash
git clone <repo> && cd <repo> && skillshare install -p && skillshare sync -p
```

### Documentation

- [Quick Start](https://skillshare.runkids.cc/docs/learn/with-claude-code)
- [Cross-Machine Sync](https://skillshare.runkids.cc/docs/how-to/sharing/cross-machine-sync)
- [Project Setup](https://skillshare.runkids.cc/docs/how-to/sharing/project-setup)
- [Organization Sharing](https://skillshare.runkids.cc/docs/how-to/sharing/organization-sharing)
- [Full Command Reference](https://skillshare.runkids.cc/docs/reference/commands)
