"""Tests for tool_redirect hook — blocks WebSearch/WebFetch and Agent."""

from __future__ import annotations

import json
from io import StringIO
from unittest.mock import patch

from tool_redirect import run_tool_redirect


def _run_with_input(tool_name: str, tool_input: dict | None = None) -> int:
    """Simulate hook invocation with the given tool name and optional input."""
    hook_data: dict = {"tool_name": tool_name}
    if tool_input is not None:
        hook_data["tool_input"] = tool_input
    stdin = StringIO(json.dumps(hook_data))
    with patch("sys.stdin", stdin):
        return run_tool_redirect()


class TestBlockedTools:
    """Tests for tools that should be blocked (exit code 2)."""

    def test_blocks_web_search(self):
        assert _run_with_input("WebSearch", {"query": "python tutorial"}) == 2

    def test_blocks_web_fetch(self):
        assert _run_with_input("WebFetch", {"url": "https://example.com"}) == 2

    def test_blocks_agent_explore(self):
        assert _run_with_input("Agent", {"subagent_type": "Explore", "prompt": "find files"}) == 2

    def test_blocks_agent_general_purpose(self):
        assert _run_with_input("Agent", {"subagent_type": "general-purpose", "prompt": "research"}) == 2

    def test_blocks_agent_without_subagent_type(self):
        assert _run_with_input("Agent", {"prompt": "do something"}) == 2

    def test_blocks_agent_plan(self):
        assert _run_with_input("Agent", {"subagent_type": "Plan", "prompt": "plan impl"}) == 2


class TestAllowedTools:
    """Tests for tools that should pass through."""

    def test_allows_read(self):
        assert _run_with_input("Read", {"file_path": "/foo.py"}) == 0

    def test_allows_write(self):
        assert _run_with_input("Write", {"file_path": "/foo.py"}) == 0

    def test_allows_edit(self):
        assert _run_with_input("Edit", {"file_path": "/foo.py"}) == 0

    def test_allows_bash(self):
        assert _run_with_input("Bash", {"command": "ls"}) == 0

    def test_allows_grep(self):
        assert _run_with_input("Grep", {"pattern": "where is config loaded"}) == 0

    def test_allows_task_create(self):
        assert _run_with_input("TaskCreate", {"subject": "test"}) == 0

    def test_allows_enter_plan_mode(self):
        assert _run_with_input("EnterPlanMode") == 0


class TestEdgeCases:
    """Tests for malformed input and edge cases."""

    def test_handles_invalid_json(self):
        stdin = StringIO("not json")
        with patch("sys.stdin", stdin):
            assert run_tool_redirect() == 0

    def test_handles_empty_stdin(self):
        stdin = StringIO("")
        with patch("sys.stdin", stdin):
            assert run_tool_redirect() == 0

    def test_handles_missing_tool_name(self):
        stdin = StringIO(json.dumps({"tool_input": {}}))
        with patch("sys.stdin", stdin):
            assert run_tool_redirect() == 0
