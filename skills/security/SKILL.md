---
name: security
description: >
  Spring Boot 4 / Spring Security 7 reference for first-party JWT authentication and OAuth2 resource-server validation. Covers 2 topic(s): spring-security-jwt, oauth2-resource-server.
  Resolved by the implementation-guide skill for confirmed Spring Boot 4.x / Java 27
  contexts, cited from tech-stack playbooks by topic name; each topic can also be read directly.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# Security Skill

Spring Boot 4 / Spring Security 7 reference for first-party JWT authentication and OAuth2 resource-server validation.

## Topics

| Topic | Use when |
|---|---|
| [`spring-security-jwt/`](spring-security-jwt/SKILL.md) | First-party JWT issuance/validation, auth filters, password encoding, RBAC, method security. |
| [`oauth2-resource-server/`](oauth2-resource-server/SKILL.md) | Validating externally-issued JWTs (Keycloak, Auth0, Okta, Cognito), claims extraction, scope-based authorization. |

## How to Use

1. Identify which topic above matches the current task.
2. Read that topic's `SKILL.md` for the specific directive and trigger conditions.
3. Check its `examples/` folder for a bad-vs-good comparison, and `templates/` (where present)
   for a copy-paste starting point. Some topics also carry `agents/openai.yaml` for Codex.

## Out of Scope

- Anything outside the 2 topic(s) listed above — this skill covers only Spring Boot 4.x / Java 27 security concerns.
- Choosing whether a project uses this stack at all — that's `tech-stack`'s decision, cited via its playbooks' "Implementation detail" lines.
- Inlining topic content elsewhere — the topic's own `SKILL.md` is the reference; point to it, don't copy it.
