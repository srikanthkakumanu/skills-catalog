---
name: batch
description: >
  Spring Batch 6 reference for Spring Boot 4: chunk-oriented batch jobs, ETL pipelines, and restartability. Covers 1 topic(s): spring-batch.
  Resolved by the implementation-guide skill for confirmed Spring Boot 4.x / Java 27
  contexts, cited from tech-stack playbooks by topic name; each topic can also be read directly.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# Batch Skill

Spring Batch 6 reference for Spring Boot 4: chunk-oriented batch jobs, ETL pipelines, and restartability.

## Topics

| Topic | Use when |
|---|---|
| [`spring-batch/`](spring-batch/SKILL.md) | Spring Batch 6 / Boot 4 builder API, job repositories, restartability, idempotent job parameters, reader/writer/processor patterns. |

## How to Use

1. Identify which topic above matches the current task.
2. Read that topic's `SKILL.md` for the specific directive and trigger conditions.
3. Check its `examples/` folder for a bad-vs-good comparison, and `templates/` (where present)
   for a copy-paste starting point. Some topics also carry `agents/openai.yaml` for Codex.

## Out of Scope

- Anything outside the 1 topic(s) listed above — this skill covers only Spring Boot 4.x / Java 27 batch concerns.
- Choosing whether a project uses this stack at all — that's `tech-stack`'s decision, cited via its playbooks' "Implementation detail" lines.
- Inlining topic content elsewhere — the topic's own `SKILL.md` is the reference; point to it, don't copy it.
