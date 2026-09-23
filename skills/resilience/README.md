# Resilience Skill

**Resilience reference for Spring Boot 4 / Spring Framework 7: native retry/concurrency-limit support and idempotency patterns for retried operations.**

## Overview

A Spring Boot 4.x / Java 27 reference collection for resilience concerns, promoted from
`implementation-guide`'s internal guide catalog into a standalone, directly-triggerable skill.
It groups 2 topic(s), each its own self-contained reference with a directive
`SKILL.md`, bad-vs-good `examples/`, and (where applicable) copy-paste `templates/`.

## What It Covers

| Topic | What it covers | Path |
|---|---|---|
| `resilience-retry` | Core @Retryable/@ConcurrencyLimit support, backoff, proxy limits, behavior after retries are exhausted. | `resilience-retry/` |
| `idempotency-patterns` | Database-backed idempotency keys for retried commands/messages; payload conflicts and concurrent retries. | `idempotency-patterns/` |

## When to Use

Invoke this skill directly when working on a Spring Boot 4.x / Java 27 project and the task
matches one of the topics above. It is also resolved automatically by the `implementation-guide`
skill: once `tech-stack.md` confirms a context's stack, `implementation-guide` cites the matching
topic path here (`skills/resilience/<topic>/`) when generating project conventions.

**Do NOT use this skill for:**

- Deciding whether a project should use this stack at all — that's `tech-stack`'s job.
- Non-Spring Boot / non-Java 27 contexts — see the Python conventions under
  `skills/implementation-guide/conventions/python/` instead.

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes (symlinks)
./install.sh --skill resilience

# Install via file copy
./install.sh --skill resilience --mode copy

# Install to a specific runtime
./install.sh --skill resilience --target claude

# Force-reinstall
./install.sh --skill resilience --force
```

For general installation details and troubleshooting, see the
[**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README.

### Invocation

Use natural language or a slash command:

```text
/resilience resilience retry spring boot

resilience retry spring boot
idempotency patterns
```

## Files

- **`SKILL.md`** — Entrypoint; topic index and how-to-use pointer
- **`README.md`** — This file; user-facing reference documentation
- **`resilience-retry/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`idempotency-patterns/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present

## Out of Scope

- Architecture, stack, or requirement decisions — those belong to the upstream pipeline
  (`brd` → `req-nfr-analysis` → `architecture-decisions` → `detailed-design` → `tech-stack` → `prd`).
- Merging or rewriting topic content into one document — each topic stays independently
  addressable and citable by name from `tech-stack`'s playbooks.
