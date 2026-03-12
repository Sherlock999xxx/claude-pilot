#!/usr/bin/env python3
"""Hook to block built-in WebSearch/WebFetch and warn on general Agent sub-agent calls.

Agent calls for /spec workflow reviewers (pilot:plan-reviewer, pilot:spec-reviewer)
pass through silently. Other Agent calls get a warning but are NOT blocked.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib.util import pre_tool_use_context, pre_tool_use_deny

BLOCKS: dict[str, dict[str, str]] = {
    "WebSearch": {
        "message": "WebSearch is blocked (use MCP alternative)",
        "alternative": "Use ToolSearch to load mcp__plugin_pilot_web-search__search, then call it directly",
        "example": 'ToolSearch(query="+web-search search") then mcp__plugin_pilot_web-search__search(query="...")',
    },
    "WebFetch": {
        "message": "WebFetch is blocked (truncates at ~8KB)",
        "alternative": "Use ToolSearch to load mcp__plugin_pilot_web-fetch__fetch_url, then call it directly",
        "example": 'ToolSearch(query="+web-fetch fetch") then mcp__plugin_pilot_web-fetch__fetch_url(url="...")',
    },
}

AGENT_WARNING = (
    "Prefer doing work directly with Probe CLI, Grep/Glob, and Bash instead of sub-agents. "
    "Sub-agents waste tokens duplicating work you can do yourself. "
    "Exception: /spec reviewer agents (pilot:plan-reviewer, pilot:spec-reviewer) are fine."
)

# Agent sub-agent types that pass through without any warning
SILENT_AGENT_TYPES: set[str] = {"pilot:plan-reviewer", "pilot:spec-reviewer"}


def run_tool_redirect() -> int:
    """Block WebSearch/WebFetch. Warn (don't block) on general Agent calls."""
    try:
        hook_data = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0

    tool_name = hook_data.get("tool_name", "")

    # Agent: silent pass for /spec reviewers, warning for everything else
    if tool_name == "Agent":
        subagent_type = hook_data.get("tool_input", {}).get("subagent_type", "")
        if subagent_type in SILENT_AGENT_TYPES:
            return 0
        sys.stderr.write(f"\033[0;33m[Pilot] Agent sub-agent warning: prefer direct tools\033[0m\n")
        print(pre_tool_use_context(AGENT_WARNING))
        return 0

    # WebSearch/WebFetch: hard block
    if tool_name in BLOCKS:
        info = BLOCKS[tool_name]
        reason = f"{info['message']}\n-> {info['alternative']}\nExample: {info['example']}"
        sys.stderr.write(f"\033[0;31m[Pilot] {info['message']}\033[0m\n")
        print(pre_tool_use_deny(reason))
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(run_tool_redirect())
