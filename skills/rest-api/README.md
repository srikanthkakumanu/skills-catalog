# REST API Skill

**Spring Boot 4 / Spring Framework 7 REST API reference covering controller conventions, versioning, hypermedia, OpenAPI-first generation, RFC 9457 error responses, and declarative HTTP interface clients.**

## Overview

A Spring Boot 4.x / Java 27 reference collection for rest api concerns, promoted from
`implementation-guide`'s internal guide catalog into a standalone, directly-triggerable skill.
It groups 6 topic(s), each its own self-contained reference with a directive
`SKILL.md`, bad-vs-good `examples/`, and (where applicable) copy-paste `templates/`.

## What It Covers

| Topic | What it covers | Path |
|---|---|---|
| `rest-api-conventions` | REST controllers, DTOs, success response contracts, pagination, HTTP status mapping. | `rest-api-conventions/` |
| `api-versioning` | Built-in Spring Framework 7 mapping-version API, request version resolution, deprecation headers. | `api-versioning/` |
| `hateoas` | Spring HATEOAS hypermedia links — EntityModel, CollectionModel, RepresentationModel. | `hateoas/` |
| `openapi-first` | Generating controller interfaces, DTOs, and clients from an OpenAPI spec. | `openapi-first/` |
| `problem-details-rfc9457` | RFC 9457 exception mapping and error responses. | `problem-details-rfc9457/` |
| `http-interface-clients` | Declarative @HttpExchange outbound clients; RestClient vs WebClient selection. | `http-interface-clients/` |

## When to Use

Invoke this skill directly when working on a Spring Boot 4.x / Java 27 project and the task
matches one of the topics above. It is also resolved automatically by the `implementation-guide`
skill: once `tech-stack.md` confirms a context's stack, `implementation-guide` cites the matching
topic path here (`skills/rest-api/<topic>/`) when generating project conventions.

**Do NOT use this skill for:**

- Deciding whether a project should use this stack at all — that's `tech-stack`'s job.
- Non-Spring Boot / non-Java 27 contexts — see the Python conventions under
  `skills/implementation-guide/conventions/python/` instead.

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes (symlinks)
./install.sh --skill rest-api

# Install via file copy
./install.sh --skill rest-api --mode copy

# Install to a specific runtime
./install.sh --skill rest-api --target claude

# Force-reinstall
./install.sh --skill rest-api --force
```

For general installation details and troubleshooting, see the
[**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README.

### Invocation

Use natural language or a slash command:

```text
/rest-api rest api conventions

rest api conventions
spring boot rest api
```

## Files

- **`SKILL.md`** — Entrypoint; topic index and how-to-use pointer
- **`README.md`** — This file; user-facing reference documentation
- **`rest-api-conventions/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`api-versioning/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`hateoas/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`openapi-first/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`problem-details-rfc9457/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present
- **`http-interface-clients/`** — `SKILL.md` (directive), `examples/` (bad vs good), `templates/`/`agents/` where present

## Out of Scope

- Architecture, stack, or requirement decisions — those belong to the upstream pipeline
  (`brd` → `req-nfr-analysis` → `architecture-decisions` → `detailed-design` → `tech-stack` → `prd`).
- Merging or rewriting topic content into one document — each topic stays independently
  addressable and citable by name from `tech-stack`'s playbooks.
