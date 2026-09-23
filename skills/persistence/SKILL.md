---
name: persistence
description: >
  Spring Boot 4 persistence reference covering JPA/Hibernate 7 entities, Redis caching, Flyway migrations, transactional patterns, and JSpecify null-safety. Covers 5 topic(s): spring-data-jpa, spring-data-redis, flyway-migrations, transactional-patterns, null-safety.
  Resolved by the implementation-guide skill for confirmed Spring Boot 4.x / Java 27
  contexts, cited from tech-stack playbooks by topic name; each topic can also be read directly.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# Persistence Skill

Spring Boot 4 persistence reference covering JPA/Hibernate 7 entities, Redis caching, Flyway migrations, transactional patterns, and JSpecify null-safety.

## Topics

| Topic | Use when |
|---|---|
| [`spring-data-jpa/`](spring-data-jpa/SKILL.md) | Jakarta Persistence 3.2 entities, repositories, projections, N+1 prevention, Hibernate 7 mappings. |
| [`spring-data-redis/`](spring-data-redis/SKILL.md) | Caching, session storage, rate limiting; cache-aside pattern, key naming, TTL strategy. |
| [`flyway-migrations/`](flyway-migrations/SKILL.md) | DB migration naming, versioning, and safe migration patterns. |
| [`transactional-patterns/`](transactional-patterns/SKILL.md) | @Transactional propagation, isolation levels, read-only optimization, common pitfalls. |
| [`null-safety/`](null-safety/SKILL.md) | JSpecify nullability annotations, Kotlin interop, NullAway build-time checks. |

## How to Use

1. Identify which topic above matches the current task.
2. Read that topic's `SKILL.md` for the specific directive and trigger conditions.
3. Check its `examples/` folder for a bad-vs-good comparison, and `templates/` (where present)
   for a copy-paste starting point. Some topics also carry `agents/openai.yaml` for Codex.

## Out of Scope

- Anything outside the 5 topic(s) listed above — this skill covers only Spring Boot 4.x / Java 27 persistence concerns.
- Choosing whether a project uses this stack at all — that's `tech-stack`'s decision, cited via its playbooks' "Implementation detail" lines.
- Inlining topic content elsewhere — the topic's own `SKILL.md` is the reference; point to it, don't copy it.
