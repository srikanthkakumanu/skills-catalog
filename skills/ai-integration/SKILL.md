---
name: ai-integration
description: >
  Spring AI 2.0 reference for Spring Boot 4: LLM/ChatClient integration, RAG/embeddings, and exposing application capabilities as MCP tools. Covers 2 topic(s): spring-ai-integration, mcp-server.
  Resolved by the implementation-guide skill for confirmed Spring Boot 4.x / Java 27
  contexts, cited from tech-stack playbooks by topic name; each topic can also be read directly.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# AI Integration Skill

Spring AI 2.0 reference for Spring Boot 4: LLM/ChatClient integration, RAG/embeddings, and exposing application capabilities as MCP tools.

## Topics

| Topic | Use when |
|---|---|
| [`spring-ai-integration/`](spring-ai-integration/SKILL.md) | ChatClient, prompt templates, embeddings, vector stores, structured output. |
| [`mcp-server/`](mcp-server/SKILL.md) | Exposing app capabilities via Model Context Protocol tools/resources/prompts; Spring AI 2.0 MCP annotations and the standalone MCP Java SDK 2.x. |

## How to Use

1. Identify which topic above matches the current task.
2. Read that topic's `SKILL.md` for the specific directive and trigger conditions.
3. Check its `examples/` folder for a bad-vs-good comparison, and `templates/` (where present)
   for a copy-paste starting point. Some topics also carry `agents/openai.yaml` for Codex.

## Out of Scope

- Anything outside the 2 topic(s) listed above — this skill covers only Spring Boot 4.x / Java 27 ai integration concerns.
- Choosing whether a project uses this stack at all — that's `tech-stack`'s decision, cited via its playbooks' "Implementation detail" lines.
- Inlining topic content elsewhere — the topic's own `SKILL.md` is the reference; point to it, don't copy it.
