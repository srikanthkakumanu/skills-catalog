---
name: messaging
description: >
  Messaging and edge-routing reference for Spring Boot 4: Kafka/RabbitMQ/Pulsar/JMS event-driven messaging and Spring Cloud Gateway 5 edge routing. Covers 2 topic(s): event-driven-messaging, spring-cloud-gateway.
  Resolved by the implementation-guide skill for confirmed Spring Boot 4.x / Java 27
  contexts, cited from tech-stack playbooks by topic name; each topic can also be read directly.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# Messaging Skill

Messaging and edge-routing reference for Spring Boot 4: Kafka/RabbitMQ/Pulsar/JMS event-driven messaging and Spring Cloud Gateway 5 edge routing.

## Topics

| Topic | Use when |
|---|---|
| [`event-driven-messaging/`](event-driven-messaging/SKILL.md) | Kafka/RabbitMQ/Pulsar/JMS producers and consumers; event contracts, idempotency, dead letters, outbox delivery. |
| [`spring-cloud-gateway/`](spring-cloud-gateway/SKILL.md) | Gateway 5 routes (WebFlux or Web MVC), edge auth, trusted headers, rate limits, resilience. |

## How to Use

1. Identify which topic above matches the current task.
2. Read that topic's `SKILL.md` for the specific directive and trigger conditions.
3. Check its `examples/` folder for a bad-vs-good comparison, and `templates/` (where present)
   for a copy-paste starting point. Some topics also carry `agents/openai.yaml` for Codex.

## Out of Scope

- Anything outside the 2 topic(s) listed above — this skill covers only Spring Boot 4.x / Java 27 messaging concerns.
- Choosing whether a project uses this stack at all — that's `tech-stack`'s decision, cited via its playbooks' "Implementation detail" lines.
- Inlining topic content elsewhere — the topic's own `SKILL.md` is the reference; point to it, don't copy it.
