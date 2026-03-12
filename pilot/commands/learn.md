---
description: Use after significant debugging, workarounds, or multi-step workflows worth standardizing for future sessions
model: opus
---

# /learn - Online Learning System

**Extract reusable knowledge from this session into skills.** Evaluates what was learned, checks for existing skills, creates new ones when valuable.

---

## Phase 0: Reference

### Triggers

| Trigger | Example |
|---------|---------|
| **Non-obvious debugging** | Spent 10+ minutes; solution wasn't in docs |
| **Misleading errors** | Error message pointed wrong direction; found real cause |
| **Workarounds** | Found limitation and creative solution |
| **Tool integration** | Undocumented API/tool usage |
| **Trial-and-error** | Tried multiple approaches before finding what worked |
| **Repeatable workflow** | Multi-step task that will recur |
| **External service queries** | Fetched from Jira, GitHub, Confluence |
| **User-facing automation** | Reports, status checks user will ask for again |

### Quality Criteria

- **Reusable**: Will help future tasks, not just this instance
- **Non-trivial**: Required discovery or is a valuable workflow pattern
- **Verified**: Solution actually worked

**Do NOT extract:** Single-step tasks, one-off fixes, knowledge in official docs.

### Project Slug

Prefix ALL created skills with the project slug to avoid name collisions across repos.

```bash
SLUG=$(basename "$(git remote get-url origin 2>/dev/null | sed 's/\.git$//')" 2>/dev/null || basename "$PWD")
# Result: "pilot-shell", "my-api", "acme-backend"
```

**Skill scope:** Choose project or global based on reusability.

| Scope | When | Create with | After creating |
|-------|------|-------------|----------------|
| **Project** (`.skillshare/skills/` exists) | Skill is specific to this repo | `skillshare new {slug}-{name} -p` | `skillshare sync -p` |
| **Global** (`skillshare` installed) | Skill applies across projects | `skillshare new {slug}-{name} -g` | `skillshare sync -g` |
| **Fallback** (no skillshare) | Direct creation | Write to `.claude/skills/{slug}-{name}/SKILL.md` | Nothing needed |

**Priority:** Project (`-p`) if `.skillshare/skills/` exists → Global (`-g`) if `skillshare` is installed → Fallback.

**Naming rules:** Lowercase with hyphens only. The slug provides context; the name should be 1-3 words max that are descriptive (not generic). Examples: `pilot-shell-lsp-cleaner`, `my-api-auth-flow`, `acme-deploy`. Never use generic names like "helper", "utils", "tools", "handler", "workflow".

**Organizing into folders (requires skillshare):** Use `--into` to group skills into subdirectories. Skillshare auto-flattens folder paths with `__` separators at the target (e.g., `frontend/react/my-skill/` → `frontend__react__my-skill` in `.claude/skills/`). Recommended structure for global skills:

```
~/.config/skillshare/skills/
├── frontend/              # Personal organized skills
│   └── react/
├── utils/                 # Personal utilities
│   └── code-review/
├── _team-skills/          # Tracked repo (auto-updated)
│   ├── deploy/
│   └── security/
└── _org-standards/        # Another tracked repo
    └── compliance/
```

### Skill Complexity Spectrum

Before writing, decide WHERE your skill falls. **Move left whenever possible** — simpler skills are more reliable, cheaper to execute, and work across more models.

| Level | Style | Determinism | Best For |
|-------|-------|-------------|----------|
| **Passive** | Context only | N/A | Background knowledge, coding standards |
| **Instructional** | Rules + guidelines | Medium | Code review, style guides |
| **CLI Wrapper** | Calls a binary/script | **High** | Automation, integrations, data processing |
| **Workflow** | Multi-step with validation | Medium | Deploy pipelines, migrations |
| **Generative** | Asks agent to write code | Low | Scaffolding, code generation |

**Key insight:** A skill that says "run `eslint --fix`" works on any model. A skill that says "analyze the code and suggest improvements" requires expensive reasoning. Prefer commands over descriptions, scripts over instructions, explicit values over judgment.

### Skill Template

Before writing, answer these five questions:

1. **When should this skill activate?** (→ becomes `description`)
2. **What inputs does it need?** (arguments, files, environment state)
3. **What does success look like?** (specific output, files created, commands run)
4. **What should it NOT do?** (explicit exclusions prevent scope creep)
5. **How do you verify it worked?** (include a validation step)

```markdown
---
name: {slug}-descriptive-kebab-case-name
description: |
  [CRITICAL: Describe WHEN to use, not HOW it works. Include trigger conditions, scenarios, exact error messages.]
targets: [claude]
tags: [category, domain]
license: MIT
author: Claude Code
version: 1.0.0
---

# Skill Name

## When to Use
[Specific trigger conditions — be precise]

## Solution
[Steps — ordered, concrete, verifiable. Prefer exact commands over descriptions.]

## Verification
[How to confirm it worked]

## When NOT to Use
[Explicit exclusions — prevents scope creep and misactivation]

## Example
[Concrete input/output example]

## References
```

**Frontmatter fields:**

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Unique identifier — lowercase, hyphens, prefixed with project slug |
| `description` | Yes | Trigger conditions for AI discovery — describe WHEN, not HOW |
| `targets` | No | Restrict sync to specific CLIs (e.g., `[claude]`). Omit to sync everywhere |
| `tags` | No | Categories for hub search and filtering (e.g., `[debugging, python]`) |
| `license` | No | License identifier shown during `skillshare install` (e.g., `MIT`, `Apache-2.0`) |
| `author` | No | Creator attribution |
| `version` | No | Semantic version — bump on updates |

**⚠️ The Description Trap:** If description summarizes the workflow, Claude follows the short description as a shortcut instead of reading SKILL.md. Always describe trigger conditions, not process.

✅ `"Fix for ENOENT errors in npm monorepos. Use when: (1) npm run fails with ENOENT, (2) symlinked deps cause failures."`
❌ `"Extract and organize npm monorepo fixes by analyzing symlinks and paths."`

### Progressive Disclosure

Don't dump everything into SKILL.md. Layer content so the AI loads only what it needs.

| Layer | What | Context Cost |
|-------|------|--------------|
| **Metadata** | `description` in frontmatter | Always loaded (~100 tokens) |
| **Body** | SKILL.md instructions | Loaded on activation |
| **Scripts/Assets** | `scripts/`, `examples/` subdirs | Executed or path-referenced, never loaded |

**Rule of thumb:** "Is this line worth the context tokens it costs?" Don't explain what AI already knows. Only add your project's specific conventions, internal APIs, and domain rules.

**Guidelines:** Concise (Claude is smart). Under 500 lines for body. Examples over explanations. Put detailed reference docs in `references/` subdirectory.

---

## Phase 1: Evaluate

Ask yourself:

1. "What did I learn that wasn't obvious before starting?"
2. "Would future-me benefit from having this documented?"
3. "Was the solution non-obvious from docs alone?"
4. "Is this a multi-step workflow I'd repeat?"
5. "Did I query an external service the user will ask about again?"

**If NO to all → Skip, nothing to learn.** External service queries are almost always worth extracting.

---

## Phase 2: Check Existing

```bash
# Project skills (source + target)
ls .skillshare/skills/ 2>/dev/null
ls .claude/skills/ 2>/dev/null
rg -i "keyword" .skillshare/skills/ .claude/skills/ 2>/dev/null
# Global skills (source + Pilot defaults)
ls ~/.config/skillshare/skills/ 2>/dev/null
ls ~/.claude/pilot/skills/ 2>/dev/null
rg -i "keyword" ~/.config/skillshare/skills/ ~/.claude/pilot/skills/ 2>/dev/null
# Or use skillshare list for a merged view
skillshare list -p 2>/dev/null; skillshare list -g 2>/dev/null
```

| Found | Action |
|-------|--------|
| Nothing related | Create new |
| Same trigger/fix | Update existing (bump version) |
| Partial overlap | Update with new variant |

---

## Phase 3: Create Skill

**Detect environment first:**

```bash
HAS_SKILLSHARE=$(command -v skillshare >/dev/null 2>&1 && echo true || echo false)
HAS_PROJECT_MODE=$([ -d ".skillshare/skills" ] && echo true || echo false)
```

**Create the skill:**

```bash
if [ "$HAS_PROJECT_MODE" = true ]; then
  # Project scope — skill lives in repo, shared via git
  skillshare new {slug}-{name} -p
  # Or into a subfolder: skillshare new {slug}-{name} -p --into {category}
elif [ "$HAS_SKILLSHARE" = true ]; then
  # Global scope — skill applies across all projects
  skillshare new {slug}-{name} -g
else
  # No skillshare — create directly in Claude's skills directory
  mkdir -p .claude/skills/{slug}-{name}
  # Write SKILL.md directly
fi
```

Edit the generated (or manually created) `SKILL.md` with the skill content using the template from Phase 0.

**After creating (only if skillshare is available):** Sync to make the skill available to Claude.

```bash
if [ "$HAS_PROJECT_MODE" = true ]; then
  skillshare sync -p
elif [ "$HAS_SKILLSHARE" = true ]; then
  skillshare sync -g
fi
# No sync needed for fallback — .claude/skills/ is already the target
```

**Portability checklist** — skills are shared with users who may NOT have Pilot Shell:

- **Only use built-in Claude Code tools** in skill instructions: `Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`, `Agent`, `WebFetch`, `WebSearch`, `Notebook`, `LSP`, `TodoRead`/`TodoWrite`
- **Never reference Pilot-specific tools:** `probe search/extract/query`, `playwright-cli`, `skillshare`, `pilot` CLI, Pilot MCP servers (`mem-search`, `context7`, `grep-mcp`, `web-fetch`, `web-search`)
- **Substitute with built-in equivalents:** `probe search` → `Grep`/`Glob`, `playwright-cli` → `Bash` with `npx playwright`, web fetch → `WebFetch`
- If a skill genuinely requires a non-standard tool, document it as a prerequisite in the skill body (not silently assume it exists)

**Determinism checklist** — maximize reliability:

- Prefer exact commands over descriptions (`run prettier --write .` not "format the code")
- Prefer scripts over multi-step instructions (reference `scripts/deploy.sh` not 5 prose steps)
- Use explicit values over judgment (`block files > 100KB` not "block large files")
- For high-risk operations (DB migrations, deploys): exact commands, validation steps, rollback plan
- For low-risk operations (code review, docs): general guidelines, let AI use judgment

**One skill = one purpose.** If the skill handles review AND testing AND deployment, split it.

---

## Phase 4: Quality Gates

- [ ] Description contains specific trigger conditions (not process summary)
- [ ] Includes "When NOT to Use" section with explicit exclusions
- [ ] Solution verified to work
- [ ] Specific enough to be actionable
- [ ] General enough to be reusable
- [ ] No sensitive information (API keys, passwords, internal URLs → use env vars instead)
- [ ] No hardcoded paths (use relative paths or environment variables)
- [ ] Deterministic where possible (commands > descriptions)
- [ ] Context-efficient (no explaining what AI already knows)
- [ ] Includes verification step (how to confirm it worked)

---

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| **Kitchen sink** — skill does too many things | One skill = one purpose. Split it. |
| **Vague instructions** — "properly format the code" | Name the specific tool and command |
| **Explaining AI knowledge** — "React is a JavaScript library..." | Only add what AI doesn't know: YOUR conventions |
| **Too many options** — "use pdfplumber, PyMuPDF, or camelot..." | Give one default, mention alternatives only if needed |
| **No verification** — "deploy to staging" (how do you know it worked?) | Always include a verification command |
| **Hardcoded paths** — `/Users/john/projects/my-app/...` | Relative paths or environment variables |

---

## Example

**Scenario:** Discovered LSP `findReferences` can find dead code by checking if functions have only 1 reference (their definition) or only test references.

**Result:** `.claude/skills/my-project-lsp-cleaner/SKILL.md`

```yaml
name: my-project-lsp-cleaner
description: |
  Find dead/unused code using LSP findReferences. Use when: (1) user asks
  to find dead code, (2) cleaning up codebase, (3) refactoring. Key insight:
  function with only 1 reference (definition) or only test refs is dead code.
targets: [claude]
tags: [refactoring, code-quality]
license: MIT
author: Claude Code
version: 1.0.0
```
