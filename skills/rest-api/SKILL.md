---
name: rest-api
description: >
  Spring Boot 4 / Spring Framework 7 REST API reference covering controller conventions, versioning, hypermedia, OpenAPI-first generation, RFC 9457 error responses, and declarative HTTP interface clients. Covers 6 topic(s): rest-api-conventions, api-versioning, hateoas, openapi-first, problem-details-rfc9457, http-interface-clients.
  Resolved by the implementation-guide skill for confirmed Spring Boot 4.x / Java 27
  contexts, cited from tech-stack playbooks by topic name; each topic can also be read directly.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# REST API Skill

Spring Boot 4 / Spring Framework 7 REST API reference covering controller conventions, versioning, hypermedia, OpenAPI-first generation, RFC 9457 error responses, and declarative HTTP interface clients.

## Topics

| Topic | Use when |
|---|---|
| [`rest-api-conventions/`](rest-api-conventions/SKILL.md) | REST controllers, DTOs, success response contracts, pagination, HTTP status mapping. |
| [`api-versioning/`](api-versioning/SKILL.md) | Built-in Spring Framework 7 mapping-version API, request version resolution, deprecation headers. |
| [`hateoas/`](hateoas/SKILL.md) | Spring HATEOAS hypermedia links — EntityModel, CollectionModel, RepresentationModel. |
| [`openapi-first/`](openapi-first/SKILL.md) | Generating controller interfaces, DTOs, and clients from an OpenAPI spec. |
| [`problem-details-rfc9457/`](problem-details-rfc9457/SKILL.md) | RFC 9457 exception mapping and error responses. |
| [`http-interface-clients/`](http-interface-clients/SKILL.md) | Declarative @HttpExchange outbound clients; RestClient vs WebClient selection. |

## How to Use

1. Identify which topic above matches the current task.
2. Read that topic's `SKILL.md` for the specific directive and trigger conditions.
3. Check its `examples/` folder for a bad-vs-good comparison, and `templates/` (where present)
   for a copy-paste starting point. Some topics also carry `agents/openai.yaml` for Codex.

## Out of Scope

- Anything outside the 6 topic(s) listed above — this skill covers only Spring Boot 4.x / Java 27 rest api concerns.
- Choosing whether a project uses this stack at all — that's `tech-stack`'s decision, cited via its playbooks' "Implementation detail" lines.
- Inlining topic content elsewhere — the topic's own `SKILL.md` is the reference; point to it, don't copy it.
