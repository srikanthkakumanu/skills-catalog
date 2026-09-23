# Architecture Patterns Skill

**Architectural pattern reference for Spring Boot 4 projects: domain-driven design, hexagonal architecture, layered architecture, multi-tenancy, and Spring Modulith.**

## Overview

A Spring Boot 4.x / Java 27 reference collection for architecture patterns concerns, promoted from
`implementation-guide`'s internal guide catalog into a standalone, directly-triggerable skill.
It groups 5 topic(s), each its own self-contained reference with a directive
`SKILL.md`, bad-vs-good `examples/`, and (where applicable) copy-paste `templates/`.

## What It Covers

| Topic | What it covers | Path |
|---|---|---|
| `domain-driven-design` | Domain models, aggregates, value objects, domain events, repositories. | `domain-driven-design/` |
| `hexagonal-architecture` | Ports & adapters — keeping domain code free of Spring/JPA dependencies. | `hexagonal-architecture/` |
| `layered-architecture` | Strict controller/service/repository layer separation. | `layered-architecture/` |
| `multi-tenancy` | Tenant resolution, DB/schema isolation, Hibernate 7 tenancy, reactive tenant context. | `multi-tenancy/` |
| `spring-modulith` | Modular monolith verification — module APIs, dependency rules, reliable module events. | `spring-modulith/` |

## When to Use

Invoke this skill directly when working on a Spring Boot 4.x / Java 27 project and the task
matches one of the topics above. It is also resolved automatically by the `implementation-guide`
skill: once `tech-stack.md` confirms a context's stack, `implementation-guide` cites the matching
topic path here (`skills/architecture-patterns/<topic>/`) when generating project conventions.

**Do NOT use this skill for:**

- Deciding whether a project should use this stack at all — that's `tech-stack`'s job.
- Non-Spring Boot / non-Java 27 contexts — see the Python conventions under
  `skills/implementation-guide/conventions/python/` instead.

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes (symlinks)
./install.sh --skill architecture-patterns

# Install via file copy
./install.sh --skill architecture-patterns --mode copy

# Install to a specific runtime
./install.sh --skill architecture-patterns --target claude

# Force-reinstall
./install.sh --skill architecture-patterns --force
```

For general installation details and troubleshooting, see the
[**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README.

### Invocation

Use natural language or a slash command:

```text
/architecture-patterns domain driven design

domain driven design
hexagonal architecture
```

## Files

- **`SKILL.md`** — Entrypoint; topic index and how-to-use pointer
- **`README.md`** — This file; user-facing reference documentation
- **`domain-driven-design/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`hexagonal-architecture/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`layered-architecture/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`multi-tenancy/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`spring-modulith/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present

## Out of Scope

- Architecture, stack, or requirement decisions — those belong to the upstream pipeline
  (`brd` → `req-nfr-analysis` → `architecture-decisions` → `detailed-design` → `tech-stack` → `prd`).
- Merging or rewriting topic content into one document — each topic stays independently
  addressable and citable by name from `tech-stack`'s playbooks.
