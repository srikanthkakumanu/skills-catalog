---
name: deployment
description: >
  Container-native deployment reference for Spring Boot 4: OCI images, buildpacks, AOT, and GraalVM native executables. Covers 1 topic(s): container-native-deployment.
  Resolved by the implementation-guide skill for confirmed Spring Boot 4.x / Java 27
  contexts, cited from tech-stack playbooks by topic name; each topic can also be read directly.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# Deployment Skill

Container-native deployment reference for Spring Boot 4: OCI images, buildpacks, AOT, and GraalVM native executables.

## Topics

| Topic | Use when |
|---|---|
| [`container-native-deployment/`](container-native-deployment/SKILL.md) | Buildpacks, layers, runtime hints, probes, security, and verification for OCI/JVM/native images. |

## How to Use

1. Identify which topic above matches the current task.
2. Read that topic's `SKILL.md` for the specific directive and trigger conditions.
3. Check its `examples/` folder for a bad-vs-good comparison, and `templates/` (where present)
   for a copy-paste starting point. Some topics also carry `agents/openai.yaml` for Codex.

## Out of Scope

- Anything outside the 1 topic(s) listed above — this skill covers only Spring Boot 4.x / Java 27 deployment concerns.
- Choosing whether a project uses this stack at all — that's `tech-stack`'s decision, cited via its playbooks' "Implementation detail" lines.
- Inlining topic content elsewhere — the topic's own `SKILL.md` is the reference; point to it, don't copy it.
