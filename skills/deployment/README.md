# Deployment Skill

**Container-native deployment reference for Spring Boot 4: OCI images, buildpacks, AOT, and GraalVM native executables.**

## Overview

A Spring Boot 4.x / Java 27 reference collection for deployment concerns, promoted from
`implementation-guide`'s internal guide catalog into a standalone, directly-triggerable skill.
It groups 1 topic(s), each its own self-contained reference with a directive
`SKILL.md`, bad-vs-good `examples/`, and (where applicable) copy-paste `templates/`.

## What It Covers

| Topic | What it covers | Path |
|---|---|---|
| `container-native-deployment` | Buildpacks, layers, runtime hints, probes, security, and verification for OCI/JVM/native images. | `container-native-deployment/` |

## When to Use

Invoke this skill directly when working on a Spring Boot 4.x / Java 27 project and the task
matches one of the topics above. It is also resolved automatically by the `implementation-guide`
skill: once `tech-stack.md` confirms a context's stack, `implementation-guide` cites the matching
topic path here (`skills/deployment/<topic>/`) when generating project conventions.

**Do NOT use this skill for:**

- Deciding whether a project should use this stack at all — that's `tech-stack`'s job.
- Non-Spring Boot / non-Java 27 contexts — see the Python conventions under
  `skills/implementation-guide/conventions/python/` instead.

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes (symlinks)
./install.sh --skill deployment

# Install via file copy
./install.sh --skill deployment --mode copy

# Install to a specific runtime
./install.sh --skill deployment --target claude

# Force-reinstall
./install.sh --skill deployment --force
```

For general installation details and troubleshooting, see the
[**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README.

### Invocation

Use natural language or a slash command:

```text
/deployment container native deployment

container native deployment
graalvm native executable
```

## Files

- **`SKILL.md`** — Entrypoint; topic index and how-to-use pointer
- **`README.md`** — This file; user-facing reference documentation
- **`container-native-deployment/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present

## Out of Scope

- Architecture, stack, or requirement decisions — those belong to the upstream pipeline
  (`brd` → `req-nfr-analysis` → `architecture-decisions` → `detailed-design` → `tech-stack` → `prd`).
- Merging or rewriting topic content into one document — each topic stays independently
  addressable and citable by name from `tech-stack`'s playbooks.
