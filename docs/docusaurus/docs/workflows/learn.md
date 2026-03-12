---
sidebar_position: 4
title: /learn — Online Learning
description: Capture non-obvious discoveries as reusable skills
---

# /learn — Online Learning

Capture non-obvious discoveries as reusable skills.

When Pilot solves a non-obvious problem — a tricky debugging session, an undocumented API pattern, a workaround for a framework quirk — `/learn` extracts that knowledge into a reusable skill. Future sessions load and apply it automatically. Triggered automatically when relevant, or invoked manually after significant investigations.

## Automatic Trigger Conditions

- Non-obvious debugging solution discovered after 10+ minutes
- Misleading errors — error pointed the wrong direction, found the real cause
- Workaround for a library limitation found during work
- Undocumented tool or API integration pattern
- Trial-and-error — multiple approaches tried before finding the solution
- Multi-step workflow that will likely recur
- External service query pattern (Jira, GitHub, Confluence)
- User-facing automation — reports or status checks user will ask for again

## What Gets Extracted Into a Skill

- The problem context and why standard approaches failed
- Step-by-step solution with exact commands and code
- When to apply this knowledge in future sessions
- Edge cases and caveats to watch out for

## Manual Invocation

```bash
> /learn "Extract the debugging workflow we used for the race condition"
> /learn "Save the PostgreSQL connection pooling pattern we discovered"
```

:::info
Skills are plain markdown files stored in `.claude/skills/`. They're loaded on-demand when relevant, created by `/learn`, and shareable across your team via the **Share dashboard**. Skills follow a frontmatter format that describes when they apply.
:::
