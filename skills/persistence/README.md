# Persistence Skill

**Spring Boot 4 persistence reference covering JPA/Hibernate 7 entities, Redis caching, Flyway migrations, transactional patterns, and JSpecify null-safety.**

## Overview

A Spring Boot 4.x / Java 27 reference collection for persistence concerns, promoted from
`implementation-guide`'s internal guide catalog into a standalone, directly-triggerable skill.
It groups 5 topic(s), each its own self-contained reference with a directive
`SKILL.md`, bad-vs-good `examples/`, and (where applicable) copy-paste `templates/`.

## What It Covers

| Topic | What it covers | Path |
|---|---|---|
| `spring-data-jpa` | Jakarta Persistence 3.2 entities, repositories, projections, N+1 prevention, Hibernate 7 mappings. | `spring-data-jpa/` |
| `spring-data-redis` | Caching, session storage, rate limiting; cache-aside pattern, key naming, TTL strategy. | `spring-data-redis/` |
| `flyway-migrations` | DB migration naming, versioning, and safe migration patterns. | `flyway-migrations/` |
| `transactional-patterns` | @Transactional propagation, isolation levels, read-only optimization, common pitfalls. | `transactional-patterns/` |
| `null-safety` | JSpecify nullability annotations, Kotlin interop, NullAway build-time checks. | `null-safety/` |

## When to Use

Invoke this skill directly when working on a Spring Boot 4.x / Java 27 project and the task
matches one of the topics above. It is also resolved automatically by the `implementation-guide`
skill: once `tech-stack.md` confirms a context's stack, `implementation-guide` cites the matching
topic path here (`skills/persistence/<topic>/`) when generating project conventions.

**Do NOT use this skill for:**

- Deciding whether a project should use this stack at all — that's `tech-stack`'s job.
- Non-Spring Boot / non-Java 27 contexts — see the Python conventions under
  `skills/implementation-guide/conventions/python/` instead.

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes (symlinks)
./install.sh --skill persistence

# Install via file copy
./install.sh --skill persistence --mode copy

# Install to a specific runtime
./install.sh --skill persistence --target claude

# Force-reinstall
./install.sh --skill persistence --force
```

For general installation details and troubleshooting, see the
[**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README.

### Invocation

Use natural language or a slash command:

```text
/persistence spring data jpa

spring data jpa
flyway migrations
```

## Files

- **`SKILL.md`** — Entrypoint; topic index and how-to-use pointer
- **`README.md`** — This file; user-facing reference documentation
- **`spring-data-jpa/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`spring-data-redis/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`flyway-migrations/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`transactional-patterns/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`null-safety/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present

## Out of Scope

- Architecture, stack, or requirement decisions — those belong to the upstream pipeline
  (`brd` → `req-nfr-analysis` → `architecture-decisions` → `detailed-design` → `tech-stack` → `prd`).
- Merging or rewriting topic content into one document — each topic stays independently
  addressable and citable by name from `tech-stack`'s playbooks.
