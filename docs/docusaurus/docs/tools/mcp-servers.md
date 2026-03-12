---
sidebar_position: 1
title: MCP Servers
description: External context always available to every session
---

# MCP Servers

External context always available to every session.

Five MCP servers are pre-configured and always available. They're lazy-loaded via `ToolSearch` to keep context lean — discovered and called on demand. Add your own in `.mcp.json`, then run `/sync` to generate documentation.

## lib-docs (Context7)

**Library documentation lookup**

Get up-to-date API docs and code examples for any library or framework. Two-step: resolve the library ID, then query for specific documentation.

```
resolve-library-id(libraryName="react")
query-docs(libraryId="/npm/react", query="useEffect cleanup")
```

## mem-search

**Persistent memory search**

Recall decisions, discoveries, and context from past sessions. Three-layer workflow: search → timeline → get_observations for token efficiency.

```
search(query="authentication flow", limit=5)
timeline(anchor=22865, depth_before=3)
get_observations(ids=[22865, 22866])
```

## web-search

**Web search + article fetching**

Web search via DuckDuckGo, Bing, and Exa (no API keys needed). Also fetches GitHub READMEs, Linux.do articles, and other content sources.

```
search(query="React Server Components 2026", limit=5)
fetchGithubReadme(url="https://github.com/org/repo")
```

## grep-mcp

**GitHub code search**

Find real-world code examples from 1M+ public repositories. Search by literal code patterns, filter by language, repo, or file path. Supports regex.

```
searchGitHub(query="useServerAction", language=["TypeScript"])
searchGitHub(query="FastMCP", language=["Python"])
```

## web-fetch

**Full web page fetching**

Fetch complete web pages via Playwright (handles JS-rendered content, no truncation). Fetches single or multiple URLs in one call.

```
fetch_url(url="https://docs.example.com/api")
fetch_urls(urls=["https://a.com", "https://b.com"])
```

:::info Tool selection
Rules specify the preferred order — Probe CLI first for codebase questions, lib-docs for library API lookups, grep-mcp for production code examples, web-search for current information. The `tool_redirect.py` hook blocks the built-in WebSearch/WebFetch and redirects to these MCP alternatives.
:::
