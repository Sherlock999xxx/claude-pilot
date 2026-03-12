"""Tests for tool_redirect hook — blocks WebSearch/WebFetch, warns on general Agent calls."""

from __future__ import annotations

import json
from io import StringIO
from unittest.mock import patch

from tool_redirect import run_tool_redirect


def _run_with_input(tool_name: str, tool_input: dict | None = None) -> tuple[int, str]:
    """Simulate hook invocation. Returns (exit_code, stdout_output)."""
    hook_data: dict = {"tool_name": tool_name}
    if tool_input is not None:
        hook_data["tool_input"] = tool_input
    stdin = StringIO(json.dumps(hook_data))
    with patch("sys.stdin", stdin), patch("sys.stdout", new_callable=StringIO) as stdout:
        code = run_tool_redirect()
        return code, stdout.getvalue()


class TestBlockedTools:
    """Tests for tools that should be hard-blocked (exit code 2)."""

    def test_blocks_web_search(self):
        code, _ = _run_with_input("WebSearch", {"query": "python tutorial"})
        assert code == 2

    def test_blocks_web_fetch(self):
        code, _ = _run_with_input("WebFetch", {"url": "https://example.com"})
        assert code == 2


class TestAgentWarning:
    """General Agent calls are warned (not blocked) — exit code 0 with context."""

    def test_warns_agent_explore(self):
        code, output = _run_with_input("Agent", {"subagent_type": "Explore", "prompt": "find files"})
        assert code == 0
        assert "additionalContext" in output

    def test_warns_agent_general_purpose(self):
        code, output = _run_with_input("Agent", {"subagent_type": "general-purpose", "prompt": "research"})
        assert code == 0
        assert "additionalContext" in output

    def test_warns_agent_without_subagent_type(self):
        code, output = _run_with_input("Agent", {"prompt": "do something"})
        assert code == 0
        assert "additionalContext" in output

    def test_warns_agent_plan(self):
        code, output = _run_with_input("Agent", {"subagent_type": "Plan", "prompt": "plan impl"})
        assert code == 0
        assert "additionalContext" in output


class TestAllowedSpecReviewerAgents:
    """/spec reviewer agents pass through silently — no warning."""

    def test_allows_plan_reviewer(self):
        code, output = _run_with_input("Agent", {"subagent_type": "pilot:plan-reviewer", "prompt": "review plan"})
        assert code == 0
        assert output == ""

    def test_allows_spec_reviewer(self):
        code, output = _run_with_input("Agent", {"subagent_type": "pilot:spec-reviewer", "prompt": "review code"})
        assert code == 0
        assert output == ""


class TestAllowedTools:
    """Tests for tools that should pass through."""

    def test_allows_read(self):
        code, _ = _run_with_input("Read", {"file_path": "/foo.py"})
        assert code == 0

    def test_allows_write(self):
        code, _ = _run_with_input("Write", {"file_path": "/foo.py"})
        assert code == 0

    def test_allows_edit(self):
        code, _ = _run_with_input("Edit", {"file_path": "/foo.py"})
        assert code == 0

    def test_allows_bash(self):
        code, _ = _run_with_input("Bash", {"command": "ls"})
        assert code == 0

    def test_allows_grep(self):
        code, _ = _run_with_input("Grep", {"pattern": "where is config loaded"})
        assert code == 0

    def test_allows_task_create(self):
        code, _ = _run_with_input("TaskCreate", {"subject": "test"})
        assert code == 0

    def test_allows_enter_plan_mode(self):
        code, _ = _run_with_input("EnterPlanMode")
        assert code == 0


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
