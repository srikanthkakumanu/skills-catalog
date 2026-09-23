> **Historical planning document — superseded.** This describes an earlier approach (copying
> spring-boot-skills content verbatim into `tech-stack/refs/` and embedding it directly in
> `tech-stack.md`) that was reconsidered before implementation. What was actually built:
>
> - `skills/tech-stack/stacks/` — seven playbooks that can disqualify a fit, plus `INDEX.md` and
>   `java-baseline.md` (Java 26). `tech-stack.md` cites a playbook by path in ≤2 lines; it never
>   embeds content (see `tech-stack/SKILL.md` Directive 5).
> - `skills/implementation-guide/` — the full 31-topic migration, organized by concern under
>   `guides/`, consumed only after `PRD.md` (Phase 7), never inlined upstream.
>
> Kept here for the record of how the design evolved, not as current guidance.

# Tech-Stack Skill: Spring Boot 4.x Reference Files Consolidation

**Date:** September 13, 2026  
**Project:** Consolidate spring-boot-skills into tech-stack skill reference playbooks  
**Status:** Prototype Complete (1 of 31 files)

---

## Overview

This document captures the complete planning, design, and prototype creation for consolidating 33 Spring Boot 4.x skill topics from the `spring-boot-skills` repo into focused, self-contained reference markdown files for the `tech-stack` skill in `skills-catalog`.

### Key Objective

When the tech-stack skill identifies that a bounded context requires Spring Data JPA (or any other Spring Boot 4 pattern), it will:
1. **Cite the relevant reference markdown file** (e.g., `SpringBoot-4-Spring-Data-JPA.md`)
2. **Embed the file's content directly** into the generated `tech-stack.md` output
3. **Provide developers** with complete, actionable instructions—no external research needed

---

## Conversation Flow

### Phase 1: Initial Requirements

**User Request:**
- Analyze the spring-boot-skills project
- Identify files/folders applicable for Spring Boot 4.x and Java versions
- Create reference/instruction markdown files in `skills-catalog/skills/tech-stack/refs/`
- These files will be used by the tech-stack skill to generate tech-stack.md

### Phase 2: Clarifications

#### Clarification 1: Only Gradle
**User:** "I only use Gradle Groovy format and not the Kotlin."

**Decision:** All examples use **Gradle Groovy DSL** (build.gradle syntax), never Kotlin DSL (build.gradle.kts).

#### Clarification 2: Java 26 Only
**User:** "We only use Java 26."

**Decision:** Reference files focus exclusively on **Java 26** as the runtime, with forward-looking context (Java 26 has not shipped; using best-effort based on Java 25 LTS + known JEPs).

#### Clarification 3: 1:1 Skill Mapping
**User:** "33 skills should be available as 33 markdown files under refs directory... tech-stack skill will use them whenever relevant requirement arises."

**Decision:** Mirror spring-boot-skills structure: **1 skill topic = 1 reference markdown file** (31 files total; skip multi-module-maven and spring-boot-migration).

#### Clarification 4: Self-Contained Instructions
**User:** "Each reference file should have all the information so that it is referenced by tech-stack skill... all the information so that it is referenced by tech-stack skill."

**Decision:** Each file is **comprehensive and embeddable**:
- Complete Gradle Groovy build configuration
- Code examples with Java 26 features
- Configuration snippets (application.yml)
- Testing strategies
- Common pitfalls and solutions
- No external lookups required

#### Clarification 5: Direct Embedding in Tech-Stack Output
**User:** "My objective is tech-stack skill uses relevant markdown file as instructions and those instructions will be copied/mentioned in tech-stack.md file whenever such/matching requirement is arised."

**Example:** If a bounded context needs relational data + JPA, tech-stack embeds the SpringBoot-4-Spring-Data-JPA.md content directly into tech-stack.md output.

---

## Design: Reference File Template

Each reference file follows this structure:

```
# Spring Boot 4: [Topic Name]

[One paragraph: what it solves, when it's standard practice]

## Fits
- [Use case 1 with constraints]
- [Use case 2 with constraints]
- [5–8 total]

## Does NOT fit
- [When this pattern doesn't apply / alternative to use]
- [Incompatibility or tradeoff]

## Gradle Build
### build.gradle
[Gradle Groovy DSL example with Spring Boot 4 starters]

### application.yml
[Configuration specific to this pattern]

### Java 26 Toolchain
[Gradle toolchain setup for Java 26]

## Implementation
### Configuration Example
[application.yml or properties snippet]

### Code Pattern Example
[Java code using Java 26 features: records, sealed classes, pattern matching, virtual threads, etc.]

### Spring Boot Conventions
[How pattern integrates with Boot 4 auto-configuration]

## Testing Approach
[Unit + integration test strategy]

## Tradeoffs
- [Pro/con analysis]

## Common Pitfalls
- [Mistake + how to avoid it]

## Further Reading
[Links to Spring Boot 4, Spring Framework 7 docs]
```

---

## Skill Mapping: 33 Skills → 31 Reference Files

| # | Skill Topic | Reference File | Status |
|----|---|---|---|
| 1 | rest-api-conventions | SpringBoot-4-Rest-Api-Conventions.md | TODO |
| 2 | api-versioning | SpringBoot-4-Api-Versioning.md | TODO |
| 3 | hateoas | SpringBoot-4-HATEOAS.md | TODO |
| 4 | openapi-first | SpringBoot-4-OpenAPI-First.md | TODO |
| 5 | problem-details-rfc9457 | SpringBoot-4-Problem-Details.md | TODO |
| 6 | http-interface-clients | SpringBoot-4-HTTP-Interface-Clients.md | TODO |
| 7 | oauth2-resource-server | SpringBoot-4-OAuth2-Resource-Server.md | TODO |
| 8 | spring-security-jwt | SpringBoot-4-Spring-Security-JWT.md | TODO |
| 9 | spring-data-jpa | SpringBoot-4-Spring-Data-JPA.md | ✅ DONE |
| 10 | spring-data-redis | SpringBoot-4-Spring-Data-Redis.md | TODO |
| 11 | flyway-migrations | SpringBoot-4-Flyway-Migrations.md | TODO |
| 12 | transactional-patterns | SpringBoot-4-Transactional-Patterns.md | TODO |
| 13 | null-safety | SpringBoot-4-Null-Safety.md | TODO |
| 14 | event-driven-messaging | SpringBoot-4-Event-Driven-Messaging.md | TODO |
| 15 | spring-cloud-gateway | SpringBoot-4-Spring-Cloud-Gateway.md | TODO |
| 16 | domain-driven-design | SpringBoot-4-Domain-Driven-Design.md | TODO |
| 17 | hexagonal-architecture | SpringBoot-4-Hexagonal-Architecture.md | TODO |
| 18 | layered-architecture | SpringBoot-4-Layered-Architecture.md | TODO |
| 19 | spring-modulith | SpringBoot-4-Spring-Modulith.md | TODO |
| 20 | multi-tenancy | SpringBoot-4-Multi-Tenancy.md | TODO |
| 21 | testing-pyramid | SpringBoot-4-Testing-Pyramid.md | TODO |
| 22 | production-observability | SpringBoot-4-Production-Observability.md | TODO |
| 23 | ai-observability | SpringBoot-4-AI-Observability.md | TODO |
| 24 | spring-batch | SpringBoot-4-Spring-Batch.md | TODO |
| 25 | spring-ai-integration | SpringBoot-4-Spring-AI-Integration.md | TODO |
| 26 | mcp-server | SpringBoot-4-MCP-Server.md | TODO |
| 27 | resilience-retry | SpringBoot-4-Resilience-Retry.md | TODO |
| 28 | idempotency-patterns | SpringBoot-4-Idempotency-Patterns.md | TODO |
| 29 | webflux-reactive-patterns | SpringBoot-4-WebFlux-Reactive-Patterns.md | TODO |
| 30 | configuration-properties | SpringBoot-4-Configuration-Properties.md | TODO |
| 31 | container-native-deployment | SpringBoot-4-Container-Native-Deployment.md | TODO |
| - | multi-module-maven | *(skip: Maven-only)* | SKIP |
| - | spring-boot-migration | *(skip: migration content excluded)* | SKIP |

---

## Prototype: SpringBoot-4-Spring-Data-JPA.md

### File Details
- **Location:** `/Users/skakumanu/practice/skills-catalog/skills/tech-stack/refs/SpringBoot-4-Spring-Data-JPA.md`
- **Size:** 17 KB, 516 lines
- **Source:** `spring-boot-skills/skills/spring-boot-4/spring-data-jpa/SKILL.md`

### Key Sections
1. **Fits** — Relational data, CRUD, complex relationships, N+1 prevention, pagination, batch writes
2. **Does NOT fit** — NoSQL, event-sourcing, analytics, schemaless
3. **Gradle Build** — Spring Boot 4 starter, PostgreSQL driver, Java 26 toolchain
4. **application.yml** — JPA/Hibernate config, JDBC batching
5. **Entity Model** — Full Order/OrderItem/Money example with Jakarta Persistence 3.2
6. **Repository** — Derived queries, JPQL, entity graphs, keyset pagination
7. **Response DTOs** — Records mapping entities to API responses
8. **Patterns** — Many-to-one lazy loading, N+1 prevention, batch writes
9. **Testing** — Testcontainers + PostgreSQL integration test
10. **Pitfalls** — 13 common mistakes with fixes
11. **Flyway** — DDL migration example
12. **References** — Spring Boot 4, Jakarta Persistence, Hibernate docs

### Validation Checkpoints
- ✅ Gradle Groovy (build.gradle) syntax correct
- ✅ Java 26 features used (UUID IDs, record DTOs, pattern matching)
- ✅ Jakarta Persistence 3.2 imports (not javax.*)
- ✅ Self-contained: Gradle examples, configuration, code, testing, pitfalls included
- ✅ Embeddable: Ready to copy directly into tech-stack.md
- ✅ No Maven references
- ✅ No Kotlin DSL

---

## Next Steps

### To Scale to All 31 Files

1. **Read** each of the 30 remaining `spring-boot-4/*/SKILL.md` files
2. **Extract** key information (constraints, patterns, Gradle starters, code examples)
3. **Convert** Maven examples → Gradle Groovy DSL
4. **Rewrite** for Java 26 context (forward-looking, pre-release guidance)
5. **Validate** against playbook template and source SKILL.md
6. **Deliver** all 31 files to `skills-catalog/skills/tech-stack/refs/`

### Estimated Effort
- **6–8 hours** (31 files × 150–250 lines each = ~4500–7500 total lines)
- **Per-file:** Extract source, design, write, validate (~12–15 minutes per file)

### Approval Needed
Does the SpringBoot-4-Spring-Data-JPA.md prototype validate the approach? If yes, proceed to create all 30 remaining files.

---

## Key Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| 1:1 skill-to-file mapping | Mirrors spring-boot-skills structure; enables granular tech-stack citations |
| Gradle Groovy only | User standard; no Kotlin DSL; build.gradle format throughout |
| Java 26 focus | User's target runtime; forward-looking (pre-release context noted) |
| Self-contained files | Tech-stack embeds them directly into output; no external lookups |
| 516-line prototype | Comprehensive enough for developers; template scalable to 30 remaining files |
| Jakarta Persistence 3.2 | Boot 4 standard; explicit javax → jakarta migration guidance |
| Gradle toolchain config | Java 26 as primary; explicit `JavaLanguageVersion.of(26)` |
| Testcontainers examples | Production-grade integration testing pattern |
| Pitfalls section | Prevents 13 common mistakes documented in spring-boot-skills |

---

## File Locations

**Source Skills:**
- `spring-boot-skills/skills/spring-boot-4/*/SKILL.md` (33 skills, 31 applicable)

**Target Reference Files:**
- `skills-catalog/skills/tech-stack/refs/SpringBoot-4-*.md` (31 files)

**Supporting Files (Existing):**
- `skills-catalog/skills/tech-stack/SKILL.md` (Tech-stack skill directives)
- `skills-catalog/skills/tech-stack/README.md` (Tech-stack skill documentation)

---

## Appendix: Key Constraints & Features

### Spring Boot 4.x Stack
- **Framework:** Spring Boot 4.1.x, Spring Framework 7
- **Security:** Spring Security 7
- **Data:** Spring Data JPA (Hibernate 7), Spring Data Redis, Flyway
- **Batch:** Spring Batch 6
- **Messaging:** Spring Cloud Stream, Spring Cloud Gateway 5.0
- **AI:** Spring AI 2.0, MCP Java SDK 2.0
- **Testing:** JUnit 5, Mockito, Testcontainers
- **Build:** Gradle 8.x (Groovy DSL)

### Java 26 Context
- **Baseline:** Java 26 (non-LTS, expected March 2026)
- **Features:** Records, sealed classes, pattern matching, virtual threads, structured concurrency, scoped values
- **Toolchain:** `JavaLanguageVersion.of(26)` in Gradle
- **Caveat:** Pre-release; details subject to change before final GA

### Tech-Stack Skill Integration
- Reads bounded context constraints from detailed-design.md
- Matches constraints to reference files (Fits section)
- Embeds matched reference file content into tech-stack.md output
- Provides developers with complete, actionable instructions

---

## Document History

| Date | Event |
|------|-------|
| 2026-09-13 | Initial requirements & planning phase |
| 2026-09-13 | Clarifications: Gradle Groovy, Java 26, 1:1 mapping, self-contained files, embedding |
| 2026-09-13 | Prototype created: SpringBoot-4-Spring-Data-JPA.md (516 lines) |
| 2026-09-13 | Conversation saved as tech-stack-merge-refactor.md |

---

## Contact & Questions

- **User Email:** kakumanu.srik@gmail.com
- **Spring Boot Skills Repo:** `/Users/skakumanu/practice/spring-boot-skills`
- **Skills Catalog Repo:** `/Users/skakumanu/practice/skills-catalog`
- **Tech-Stack Skill:** `skills-catalog/skills/tech-stack/`

---

*End of document. Ready to scale to all 31 reference files upon approval of prototype.*
