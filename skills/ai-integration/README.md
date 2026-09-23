# AI Integration Skill

**Spring AI 2.0 reference for Spring Boot 4: LLM/ChatClient integration, RAG/embeddings, and exposing application capabilities as MCP tools.**

## Overview

A Spring Boot 4.x / Java 27 reference collection for ai integration concerns, promoted from
`implementation-guide`'s internal guide catalog into a standalone, directly-triggerable skill.
It groups 2 topic(s), each its own self-contained reference with a directive
`SKILL.md`, bad-vs-good `examples/`, and (where applicable) copy-paste `templates/`.

## What It Covers

| Topic | What it covers | Path |
|---|---|---|
| `spring-ai-integration` | ChatClient, prompt templates, embeddings, vector stores, structured output. | `spring-ai-integration/` |
| `mcp-server` | Exposing app capabilities via Model Context Protocol tools/resources/prompts; Spring AI 2.0 MCP annotations and the standalone MCP Java SDK 2.x. | `mcp-server/` |

## When to Use

Invoke this skill directly when working on a Spring Boot 4.x / Java 27 project and the task
matches one of the topics above. It is also resolved automatically by the `implementation-guide`
skill: once `tech-stack.md` confirms a context's stack, `implementation-guide` cites the matching
topic path here (`skills/ai-integration/<topic>/`) when generating project conventions.

**Do NOT use this skill for:**

- Deciding whether a project should use this stack at all — that's `tech-stack`'s job.
- Non-Spring Boot / non-Java 27 contexts — see the Python conventions under
  `skills/implementation-guide/conventions/python/` instead.

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes (symlinks)
./install.sh --skill ai-integration

# Install via file copy
./install.sh --skill ai-integration --mode copy

# Install to a specific runtime
./install.sh --skill ai-integration --target claude

# Force-reinstall
./install.sh --skill ai-integration --force
```

For general installation details and troubleshooting, see the
[**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README.

### Invocation

Use natural language or a slash command:

```text
/ai-integration spring ai integration

spring ai integration
mcp server spring boot
```

## Files

- **`SKILL.md`** — Entrypoint; topic index and how-to-use pointer
- **`README.md`** — This file; user-facing reference documentation
- **`spring-ai-integration/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`mcp-server/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present

## Out of Scope

- Architecture, stack, or requirement decisions — those belong to the upstream pipeline
  (`brd` → `req-nfr-analysis` → `architecture-decisions` → `detailed-design` → `tech-stack` → `prd`).
- Merging or rewriting topic content into one document — each topic stays independently
  addressable and citable by name from `tech-stack`'s playbooks.
