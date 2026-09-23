---
name: resilience
description: >
  Resilience reference for Spring Boot 4 / Spring Framework 7: native retry/concurrency-limit support and idempotency patterns for retried operations. Covers 2 topic(s): resilience-retry, idempotency-patterns.
  Resolved by the implementation-guide skill for confirmed Spring Boot 4.x / Java 27
  contexts, cited from tech-stack playbooks by topic name; each topic can also be read directly.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# Resilience Skill

Resilience reference for Spring Boot 4 / Spring Framework 7: native retry/concurrency-limit support and idempotency patterns for retried operations.

## Topics

| Topic | Use when |
|---|---|
| [`resilience-retry/`](resilience-retry/SKILL.md) | Core @Retryable/@ConcurrencyLimit support, backoff, proxy limits, behavior after retries are exhausted. |
| [`idempotency-patterns/`](idempotency-patterns/SKILL.md) | Database-backed idempotency keys for retried commands/messages; payload conflicts and concurrent retries. |

## How to Use

1. Identify which topic above matches the current task.
2. Read that topic's `SKILL.md` for the specific directive and trigger conditions.
3. Check its `examples/` folder for a bad-vs-good comparison, and `templates/` (where present)
   for a copy-paste starting point. Some topics also carry `agents/openai.yaml` for Codex.

## Out of Scope

- Anything outside the 2 topic(s) listed above — this skill covers only Spring Boot 4.x / Java 27 resilience concerns.
- Choosing whether a project uses this stack at all — that's `tech-stack`'s decision, cited via its playbooks' "Implementation detail" lines.
- Inlining topic content elsewhere — the topic's own `SKILL.md` is the reference; point to it, don't copy it.
