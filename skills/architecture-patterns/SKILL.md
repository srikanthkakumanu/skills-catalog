---
name: architecture-patterns
description: >
  Architectural pattern reference for Spring Boot 4 projects: domain-driven design, hexagonal architecture, layered architecture, multi-tenancy, and Spring Modulith. Covers 5 topic(s): domain-driven-design, hexagonal-architecture, layered-architecture, multi-tenancy, spring-modulith.
  Resolved by the implementation-guide skill for confirmed Spring Boot 4.x / Java 27
  contexts, cited from tech-stack playbooks by topic name; each topic can also be read directly.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# Architecture Patterns Skill

Architectural pattern reference for Spring Boot 4 projects: domain-driven design, hexagonal architecture, layered architecture, multi-tenancy, and Spring Modulith.

## Topics

| Topic | Use when |
|---|---|
| [`domain-driven-design/`](domain-driven-design/SKILL.md) | Domain models, aggregates, value objects, domain events, repositories. |
| [`hexagonal-architecture/`](hexagonal-architecture/SKILL.md) | Ports & adapters — keeping domain code free of Spring/JPA dependencies. |
| [`layered-architecture/`](layered-architecture/SKILL.md) | Strict controller/service/repository layer separation. |
| [`multi-tenancy/`](multi-tenancy/SKILL.md) | Tenant resolution, DB/schema isolation, Hibernate 7 tenancy, reactive tenant context. |
| [`spring-modulith/`](spring-modulith/SKILL.md) | Modular monolith verification — module APIs, dependency rules, reliable module events. |

## How to Use

1. Identify which topic above matches the current task.
2. Read that topic's `SKILL.md` for the specific directive and trigger conditions.
3. Check its `examples/` folder for a bad-vs-good comparison, and `templates/` (where present)
   for a copy-paste starting point. Some topics also carry `agents/openai.yaml` for Codex.

## Out of Scope

- Anything outside the 5 topic(s) listed above — this skill covers only Spring Boot 4.x / Java 27 architecture patterns concerns.
- Choosing whether a project uses this stack at all — that's `tech-stack`'s decision, cited via its playbooks' "Implementation detail" lines.
- Inlining topic content elsewhere — the topic's own `SKILL.md` is the reference; point to it, don't copy it.
