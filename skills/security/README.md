# Security Skill

**Spring Boot 4 / Spring Security 7 reference for first-party JWT authentication and OAuth2 resource-server validation.**

## Overview

A Spring Boot 4.x / Java 27 reference collection for security concerns, promoted from
`implementation-guide`'s internal guide catalog into a standalone, directly-triggerable skill.
It groups 2 topic(s), each its own self-contained reference with a directive
`SKILL.md`, bad-vs-good `examples/`, and (where applicable) copy-paste `templates/`.

## What It Covers

| Topic | What it covers | Path |
|---|---|---|
| `spring-security-jwt` | First-party JWT issuance/validation, auth filters, password encoding, RBAC, method security. | `spring-security-jwt/` |
| `oauth2-resource-server` | Validating externally-issued JWTs (Keycloak, Auth0, Okta, Cognito), claims extraction, scope-based authorization. | `oauth2-resource-server/` |

## When to Use

Invoke this skill directly when working on a Spring Boot 4.x / Java 27 project and the task
matches one of the topics above. It is also resolved automatically by the `implementation-guide`
skill: once `tech-stack.md` confirms a context's stack, `implementation-guide` cites the matching
topic path here (`skills/security/<topic>/`) when generating project conventions.

**Do NOT use this skill for:**

- Deciding whether a project should use this stack at all — that's `tech-stack`'s job.
- Non-Spring Boot / non-Java 27 contexts — see the Python conventions under
  `skills/implementation-guide/conventions/python/` instead.

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes (symlinks)
./install.sh --skill security

# Install via file copy
./install.sh --skill security --mode copy

# Install to a specific runtime
./install.sh --skill security --target claude

# Force-reinstall
./install.sh --skill security --force
```

For general installation details and troubleshooting, see the
[**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README.

### Invocation

Use natural language or a slash command:

```text
/security spring security jwt

spring security jwt
oauth2 resource server
```

## Files

- **`SKILL.md`** — Entrypoint; topic index and how-to-use pointer
- **`README.md`** — This file; user-facing reference documentation
- **`spring-security-jwt/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`oauth2-resource-server/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present

## Out of Scope

- Architecture, stack, or requirement decisions — those belong to the upstream pipeline
  (`brd` → `req-nfr-analysis` → `architecture-decisions` → `detailed-design` → `tech-stack` → `prd`).
- Merging or rewriting topic content into one document — each topic stays independently
  addressable and citable by name from `tech-stack`'s playbooks.
