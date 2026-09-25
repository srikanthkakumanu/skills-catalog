# Implementation Guide (Phase 7)

Project-invariant Spring Boot 4.x / Java 27 implementation knowledge, plus Python 3.11.x /
AI-agentic implementation knowledge.

**Scope:** Spring Boot 4.x + Java 27 (Spring Boot 3.x was never read or migrated), Python 3.11.x
for the AI-agentic layer (`stacks/python-ai-agentic.md`), and Next.js 16.x / React 19 /
TypeScript 5.9.x for the frontend/presentation layer (`stacks/frontend-nextjs-react-typescript.md`)
when that layer was evidence-gated in for a context. No other language or framework.

## Why this exists

`tech-stack` (Phase 5) decides *which* technology a bounded context gets, and cites a
`stacks/*.md` playbook by path — it never inlines implementation detail (`SKILL.md` Directive 5).
This skill resolves the detail those citations point to. It runs *after* `PRD.md` (Phase 6), resolves
each confirmed context's playbook citation to the reference skills/conventions below, and produces project
conventions (`CLAUDE.md`/`AGENTS.md`) — never a PRD section, never read by any upstream phase. It is
not part of the six-phase decision pipeline (`brd` → `prd`); it's a stack-specific extension that
only applies when `tech-stack` selected a Spring Boot 4.x context, a Python AI-agentic context, or
an evidence-gated frontend/presentation context.

## Spring Boot 4.x reference skills

All 31 applicable topics from `spring-boot-4` are grouped by concern into 13 standalone,
directly-triggerable catalog skills under top-level `skills/<category>/`, each keeping its
topics' original `SKILL.md`, `examples/`, `templates/`, and `agents/` unchanged:

| Category (`skills/<category>/`) | Topics |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rest-api/`              | rest-api-conventions, api-versioning, hateoas, openapi-first, problem-details-rfc9457, http-interface-clients                                       |
| `persistence/`           | spring-data-jpa (includes this catalog's Gradle/Testcontainers addendum), spring-data-redis, flyway-migrations, transactional-patterns, null-safety |
| `security/`              | oauth2-resource-server, spring-security-jwt                                                                                                         |
| `architecture-patterns/` | domain-driven-design, hexagonal-architecture, layered-architecture, spring-modulith, multi-tenancy                                                  |
| `messaging/`             | event-driven-messaging, spring-cloud-gateway                                                                                                        |
| `testing/`               | testing-pyramid                                                                                                                                     |
| `observability/`         | production-observability, ai-observability                                                                                                          |
| `batch/`                 | spring-batch                                                                                                                                        |
| `ai-integration/`        | spring-ai-integration, mcp-server                                                                                                                   |
| `resilience/`            | resilience-retry, idempotency-patterns                                                                                                              |
| `configuration/`         | configuration-properties                                                                                                                            |
| `deployment/`            | container-native-deployment                                                                                                                         |
| `reactive/`              | webflux-reactive-patterns                                                                                                                           |

Excluded on purpose: `multi-module-maven` (Maven-only, this catalog is Gradle Groovy) and
`spring-boot-migration` (no migration content applicable).

Each category has its own `SKILL.md`/`README.md` (frontmatter: `name`, `description`,
`license: Apache-2.0`, `compatibility: Claude Code, OpenAI Codex, Google Antigravity 2`),
registered in `registry.json` and listed in the root README's Available Skills table — so each
is independently triggerable, not just resolved through this skill. A topic itself has no
`README.md`, only `SKILL.md` plus `examples/` and, where applicable, `templates/`/`agents/`.

Each `stacks/*.md` playbook in `tech-stack` points back here by topic name under its
"Implementation detail" line — e.g. `springboot4-webmvc-jpa-postgres.md` cites
`spring-data-jpa, flyway-migrations, ...`. Resolve those names against the table above, at
`skills/<category>/<topic>/`.

## Frontend reference skills

All 8 topics live under one new top-level catalog skill, `skills/frontend/`, resolved the same way
the 13 Spring Boot categories above are — evidence-gated, not default-applied (see `tech-stack`
Directive 1):

| Category (`skills/<category>/`) | Topics |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frontend/` | react-component-patterns, nextjs-app-router, state-management, data-fetching, forms-validation, styling-tailwind, testing-frontend, performance-accessibility |

`stacks/frontend-nextjs-react-typescript.md`'s "Implementation detail" line cites these 8 topic
names.

## Java baseline mini-skills

`java-language-conventions/` and `spring-boot-conventions/` sit directly under
`implementation-guide/` (siblings of this `SKILL.md`/`README.md`) — the same tier as a
`skills/<category>/<topic>/` topic (lightweight `name`+`description` frontmatter only, not the
full top-level package frontmatter, not independently registered in `registry.json`), but nested
here instead of promoted to top-level because they're cross-cutting baselines rather than a
citable topic owned by one category:

- `java-language-conventions/SKILL.md` — Java 27 version/toolchain/build facts (stated identically
  to `tech-stack/stacks/java-baseline.md`) plus language-feature usage (records, sealed interfaces,
  pattern matching, virtual threads, structured concurrency) with good/bad examples
- `spring-boot-conventions/SKILL.md` — project conventions (layered structure, DTOs-as-records,
  Flyway naming, git conventions); consistently Java 27 throughout

Both are loaded unconditionally for every Java context — never resolved per-context the way
`skills/<category>/<topic>/` topics are.

## Frontend baseline mini-skills

`typescript-language-conventions/` and `nextjs-project-conventions/` sit directly under
`implementation-guide/` (siblings of this `SKILL.md`/`README.md`) — the same tier as a
`skills/<category>/<topic>/` topic (lightweight `name`+`description` frontmatter only, not the
full top-level package frontmatter, not independently registered in `registry.json`), nested here
instead of promoted to top-level because they're cross-cutting baselines rather than a citable
topic owned by one category:

- `typescript-language-conventions/SKILL.md` — TypeScript 5.9.x version/toolchain facts (strict
  mode flags, target/module resolution) plus language-feature usage guidance (discriminated
  unions, `satisfies`, template literal types, utility types) with good/bad examples
- `nextjs-project-conventions/SKILL.md` — project conventions (App Router folder structure,
  Server/Client Component boundary rules, environment variable handling, git conventions);
  consistently Next.js 16.x / React 19 throughout

Both are loaded unconditionally for every frontend context — never resolved per-context the way
`skills/frontend/<topic>/` topics are.

## `conventions/`

- `compatibility-baseline.md` — verified version pins (Spring Boot/Cloud/AI, GraalVM) as of Aug 2026, loaded unconditionally for every Java context alongside the two mini-skills above; also now carries React/Next.js/TypeScript/TanStack Query/Zod/React Hook Form/Tailwind/Vitest/Playwright/RTL/Node/pnpm pins, loaded unconditionally for every frontend context alongside the two frontend mini-skills above

## `conventions/python/`

Plain reference files (no `SKILL.md` frontmatter — not independently-triggerable skills, not even
at the lightweight topic tier) for the Python AI-agentic layer, resolved by
`python-ai-agentic.md`'s "Implementation detail" citation:

- `language-conventions.md` — Python 3.11.x baseline (uv, type hints, Pydantic v2, Ruff, async
  discipline) — loaded unconditionally for every Python context, the same role
  `java-language-conventions/SKILL.md` plays for Java
- `mcp-server.md`, `langgraph-orchestration.md`, `langchain-integration.md`, `ai-observability.md`
  — capability-specific, resolved per-context by citation only (the same mechanism as
  `skills/<category>/<topic>/` topics for Java, just as plain files instead of skill folders)

Generated `CLAUDE.md`/`AGENTS.md` open with a provenance header citing `PRD.md` as the source and
`implementation-guide` as the generating skill, before the language-matching baseline and the
per-context resolved pointers.

## Registration

Registered in `registry.json` as `implementation-guide`, `SKILL.md` written. Triggerable via
`/implementation-guide` or natural language once installed. Each of the 13 Spring Boot 4.x
reference skills and the 1 Frontend reference skill above is separately registered too (see the
root README's Available Skills table), so they can be triggered directly without going through
this skill.
