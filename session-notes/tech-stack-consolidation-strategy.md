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

# Tech-Stack Consolidation Strategy: Spring Boot 4.x Migration into Skills-Catalog

**Date:** September 13, 2026  
**Status:** Strategic Design Complete — Ready for Implementation  
**Next Session:** Implementation Planning & Execution

---

## Executive Summary

**Objective:** Migrate all relevant skills from `spring-boot-skills` (31 applicable topics) into `skills-catalog` as a self-contained, independent knowledge base that powers the organizational skills pipeline without bloating outputs.

**Key Insight:** skills-catalog must be organizationally independent and self-sufficient, not dependent on external spring-boot-skills repository.

**Approach:** Create an internal **reference-library/** that consolidates all Spring Boot 4.x knowledge, organized by concern area, which powers lean skill outputs (tech-stack.md, architecture-decisions.md, prd.md) without duplication.

---

## Strategic Evolution: Session Conversation

### Phase 1: Initial Requirements (Start)

**User Request:**
- Analyze spring-boot-skills project
- Identify Spring Boot 4.x + Java 26 applicable content
- Create reference files for tech-stack skill

### Phase 2: First Clarifications

1. **Gradle Only**: "I only use Gradle Groovy format and not the Kotlin."
   - Decision: All examples use `build.gradle` (Groovy DSL), never `build.gradle.kts`

2. **Java 26 Only**: "We only use Java 26."
   - Decision: Focus exclusively on Java 26 (forward-looking, pre-release context noted)

3. **1:1 Skill Mapping**: "33 skills should be available as 33 markdown files"
   - Decision: Create 31 reference files (skip multi-module-maven, spring-boot-migration)

4. **Self-Contained Files**: "Each reference file should have all the information"
   - Decision: Files include Gradle examples, code patterns, configuration, testing, gotchas
   - Prototype created: `SpringBoot-4-Spring-Data-JPA.md` (516 lines, 17KB)

### Phase 3: Architectural Shift (Critical)

**User Challenge:** "What do you think about spring-boot-skills and tech-stack skill? How can tech-stack best utilize spring-boot-skills?"

**Root Issues Identified:**
- ❌ Embedding full spring-boot-skills into tech-stack.md creates bloat
- ❌ tech-stack.md is consumed by prd skill (assembler of all skills)
- ❌ Bloated tech-stack.md → Bloated prd.md
- ❌ No single source of truth if content is duplicated

**Recommended Separation of Concerns:**
- tech-stack.md: Decision-focused (brief, why we chose this tech)
- prd.md: Assembled from multiple skills (concise, org-wide)
- spring-boot-skills: Implementation authority (detailed, developer-focused)
- **Link, don't embed**: Reference spring-boot-skills from skills-catalog outputs

### Phase 4: Independence Requirement (Final)

**User Clarification:** "spring-boot-skills is a project created by someone else. But I want to migrate the relevant content into my own skills-catalog so that my skills-catalog stay independent and self-sufficient."

**Key Insight:**
- ✅ Not just linking to external repo
- ✅ Full migration of knowledge INTO skills-catalog
- ✅ skills-catalog becomes autonomous and complete
- ✅ NOT 31 separate files, but organized by concern

**Final Decision:** Create internal **reference-library/** that consolidates all 31 skills organized by architectural concern, powering the skills pipeline independently.

---

## Final Architecture: Three-Layer Knowledge System

### Layer 1: Internal Knowledge Base (Reference-Library)

**Purpose:** Comprehensive Spring Boot 4.x knowledge, organized by concern  
**Location:** `skills-catalog/reference-library/`  
**Audience:** Internal reference for skills, templates, and developers  
**Ownership:** Fully owned by user; independent from spring-boot-skills

**Structure:**

```
reference-library/
├── README.md (Master index of all topics)
├── guides/
│   ├── 01-Rest-API-Design/
│   │   ├── conventions.md
│   │   ├── versioning.md
│   │   ├── hateoas.md
│   │   ├── openapi-first.md
│   │   ├── problem-details.md
│   │   └── http-interface-clients.md
│   ├── 02-Data-Persistence/
│   │   ├── spring-data-jpa.md (COMPREHENSIVE: 516+ lines)
│   │   ├── spring-data-redis.md
│   │   ├── flyway-migrations.md
│   │   ├── transactional-patterns.md
│   │   └── null-safety.md
│   ├── 03-Security/
│   │   ├── oauth2-resource-server.md
│   │   └── spring-security-jwt.md
│   ├── 04-Architecture/
│   │   ├── domain-driven-design.md
│   │   ├── hexagonal-architecture.md
│   │   ├── layered-architecture.md
│   │   ├── spring-modulith.md
│   │   └── multi-tenancy.md
│   ├── 05-Async-Messaging/
│   │   ├── event-driven-messaging.md
│   │   └── spring-cloud-gateway.md
│   ├── 06-Testing/
│   │   └── testing-pyramid.md
│   ├── 07-Observability/
│   │   ├── production-observability.md
│   │   └── ai-observability.md
│   ├── 08-Batch-Processing/
│   │   └── spring-batch.md
│   ├── 09-AI-Integration/
│   │   ├── spring-ai-integration.md
│   │   └── mcp-server.md
│   ├── 10-Resilience/
│   │   ├── resilience-retry.md
│   │   └── idempotency-patterns.md
│   ├── 11-Configuration/
│   │   └── configuration-properties.md
│   └── 12-Deployment/
│       ├── container-native-deployment.md
│       └── webflux-reactive-patterns.md
├── patterns/
│   ├── gradle-build-patterns.md
│   ├── gradle-dependencies.md
│   ├── java-26-features.md
│   └── common-gotchas.md
└── cross-cutting/
    ├── http-interface-clients.md
```

**Key Characteristics:**
- ✅ Comprehensive (516+ lines per major topic)
- ✅ Organized by concern (12 categories)
- ✅ Gradient Groovy examples
- ✅ Java 26 features highlighted
- ✅ No external dependencies
- ✅ Cross-references within library
- ✅ Single source of truth for Spring Boot 4.x knowledge

### Layer 2: Skills Pipeline (Lean Outputs)

**Purpose:** Generate lean, decision-focused documents for organizational use  
**Consumers:** tech-stack.md → prd skill → prd.md

**Skills using reference-library internally:**

| Skill | Uses Reference-Library For | Output Size |
|-------|----------------------------|------------|
| tech-stack | Technology choices per context | 1-2 pages |
| architecture-decisions | Architecture patterns per design | 1-2 pages |
| detailed-design | Design constraints per context | 2-3 pages |
| req-nfr-analysis | NFR mappings to tech choices | 1 page |

**Example: tech-stack.md (Lean Output)**

```markdown
# Technology Stack: [Project Name]

| Context | Stack | Rationale | Key Constraints |
|---------|-------|-----------|-----------------|
| Relational Data | Spring Data JPA | ACID + complex relationships needed | Use UUID IDs (not IDENTITY) for batch performance; lazy-load to-one relationships |
| Cache Layer | Spring Data Redis | Hot-path read optimization | Use Caffeine for L1 cache, Redis for L2 |
| REST APIs | Spring MVC + OpenAPI | Stateless, scalable APIs | Use records for DTOs; never expose entities |

[1-2 pages total, decision-focused]

See project CLAUDE.md and reference-library/guides/ for implementation details.
```

### Layer 3: Project Templates

**Purpose:** Onboard new projects with conventions and guidance  
**Location:** `skills-catalog/templates/spring-boot-4/`

**Contents:**

```
templates/spring-boot-4/
├── CLAUDE.md (30-50 lines: conventions + links to reference-library/)
├── AGENTS.md (Agent guidance for Codex/Claude)
├── build.gradle (Groovy template: Boot 4, Java 26 toolchain)
├── application.yml (Configuration template)
└── settings.gradle (Multi-module template if needed)
```

**Example: CLAUDE.md**

```markdown
# Spring Boot 4 + Java 26 Project Instructions

## Quick Reference

**Build**: Gradle 8.x (Groovy DSL) — see build.gradle template  
**Runtime**: Java 26 with toolchain configuration  
**Framework**: Spring Boot 4.1.x, Spring Framework 7  
**Database**: PostgreSQL + Flyway migrations

## Key Conventions

- Entities: Import `jakarta.persistence.*` (not `javax.*`)
- IDs: Use `UUID` for batch insert performance
- DTOs: Use Java records; never expose entities from REST controllers
- Testing: Use Testcontainers for integration tests
- Gradle: Use Groovy DSL; no Kotlin DSL

## Pattern Reference

For detailed implementation guidance, see:
- **REST APIs**: reference-library/guides/01-Rest-API-Design/
- **Data Persistence**: reference-library/guides/02-Data-Persistence/
- **Security**: reference-library/guides/03-Security/
- **Architecture**: reference-library/guides/04-Architecture/
- **Testing**: reference-library/guides/06-Testing/
- **And more**: reference-library/README.md

## Gradle Build Example

See `build.gradle` in this template. Key points:
- Spring Boot 4.1.1 (managed by dependency management)
- Java 26 toolchain
- Starter dependencies (no explicit Hibernate, JPA, validator versions)
```

---

## Migration Strategy: 31 Skills → 12 Organized Guides

### Skill-to-Category Mapping

| # | Category | Skills (31 total) |
|----|----------|-------------------|
| 1 | REST API Design | rest-api-conventions, api-versioning, hateoas, openapi-first, problem-details, http-interface-clients (6) |
| 2 | Data Persistence | spring-data-jpa, spring-data-redis, flyway-migrations, transactional-patterns, null-safety (5) |
| 3 | Security | oauth2-resource-server, spring-security-jwt (2) |
| 4 | Architecture | domain-driven-design, hexagonal-architecture, layered-architecture, spring-modulith, multi-tenancy (5) |
| 5 | Async Messaging | event-driven-messaging, spring-cloud-gateway (2) |
| 6 | Testing | testing-pyramid (1) |
| 7 | Observability | production-observability, ai-observability (2) |
| 8 | Batch Processing | spring-batch (1) |
| 9 | AI Integration | spring-ai-integration, mcp-server (2) |
| 10 | Resilience | resilience-retry, idempotency-patterns (2) |
| 11 | Configuration | configuration-properties (1) |
| 12 | Deployment | container-native-deployment, webflux-reactive-patterns (2) |
| — | SKIP | multi-module-maven (Maven-only), spring-boot-migration (no migration content) |

### Migration Process Per Category

**For each category (12 total):**

1. **Extract content** from 2-6 related spring-boot-4 SKILL.md files
2. **Consolidate** into ONE comprehensive guide (reference-library/guides/[category]/)
3. **Convert** Maven examples → Gradle Groovy DSL
4. **Enhance** with Java 26 features (records, pattern matching, virtual threads, etc.)
5. **Add** cross-references to related guides within reference-library
6. **Verify** self-contained (no external dependencies on spring-boot-skills)

**Output:** 12 comprehensive guides covering all 31 skills, organized by concern, fully owned by skills-catalog.

---

## Data Flow: From Migration to PRD

```
Step 1: Migration
  spring-boot-skills/[31 skills] → reference-library/[12 guides]
  
Step 2: Skills Use Internal Knowledge
  tech-stack skill → queries reference-library/ → generates tech-stack.md
  architecture-decisions → queries reference-library/ → generates architecture-decisions.md
  
Step 3: Lean Outputs
  tech-stack.md (1-2 pages, decisions)
  architecture-decisions.md (1-2 pages, patterns)
  
Step 4: Assembly
  prd skill → assembles tech-stack.md + architecture-decisions.md + others → prd.md (3-5 pages)
  
Step 5: Implementation
  Developer reads prd.md (org decisions)
  → Opens CLAUDE.md template (project conventions)
  → References reference-library/guides/[category]/ (detailed implementation)
  → Codes using Spring Boot 4 patterns
```

---

## Current Status

### Completed
- ✅ Strategic analysis of spring-boot-skills vs. skills-catalog
- ✅ Identified bloat problem in current approach
- ✅ Designed three-layer knowledge system
- ✅ Created skill-to-category mapping (31 skills → 12 guides)
- ✅ Defined migration strategy
- ✅ Prototype (SpringBoot-4-Spring-Data-JPA.md) validates structure

### To Be Done Tomorrow

1. **Create reference-library/ directory structure** in skills-catalog
2. **Begin migration: Category 01 (REST API Design)** — consolidate 6 skills → 1 guide
3. **Create reference-library/README.md** — master index
4. **Update templates/spring-boot-4/CLAUDE.md** — link to reference-library
5. **Establish conventions document** — how to cross-reference within library
6. **Plan phases** — tackle 2-3 categories per session

---

## Questions for Tomorrow Morning

Before starting implementation, clarify:

1. **Parallel vs. Sequential?**
   - Migrate all 12 categories in parallel? Or sequential (1-2 per session)?

2. **Naming Convention?**
   - Keep skill names as-is (spring-data-jpa.md) or shorten (jpa.md)?
   - Category folder naming: `01-Rest-API-Design` vs. `rest-api`?

3. **Consolidation Depth?**
   - Merge 5-6 related skills into ONE guide (516+ lines)?
   - Or keep them separate but cross-referenced (150-200 lines each)?

4. **Gradle Patterns?**
   - Create `reference-library/patterns/gradle-build-patterns.md` (shared across all guides)?
   - Or embed Gradle examples in each guide?

5. **Java 26 Coverage?**
   - Highlight Java 26 features throughout each guide?
   - Create separate `java-26-features.md` reference?

6. **Reference Updates?**
   - If spring-boot-skills updates, do we re-sync reference-library periodically?
   - Or fully own it now (no future sync)?

---

## Files Created This Session

1. ✅ `tech-stack-merge-refactor.md` — Conversation summary (session 1)
2. ✅ `tech-stack-consolidation-strategy.md` — THIS DOCUMENT (session 1 continuation)
3. ✅ `SpringBoot-4-Spring-Data-JPA.md` — Prototype reference file (in refs/)

---

## Key Takeaways

| Principle | Implementation |
|-----------|-----------------|
| **Self-Sufficiency** | Migrate knowledge INTO skills-catalog; don't reference external repo |
| **Lean Outputs** | tech-stack.md, prd.md stay concise (decision-focused, not tutorial) |
| **Rich Internal** | reference-library/ contains comprehensive Spring Boot 4.x knowledge |
| **Organization** | Group 31 skills by concern (12 categories) not individual files |
| **Single Source** | reference-library/ is org's canonical Spring Boot 4 knowledge base |
| **Gradual Adoption** | Developers: prd → CLAUDE.md → reference-library/ (progressive detail) |

---

## Appendix: Spring Boot 4 Stack Summary

**Baseline (Managed by Spring Boot 4 BOM):**
- Framework: Spring Boot 4.1.x, Spring Framework 7
- Jakarta EE 11, Servlet 6.1
- Hibernate ORM 7.x
- Jackson 3
- Spring Security 7
- Spring Data JPA

**Build & Runtime:**
- Build Tool: Gradle 8.x (Groovy DSL)
- Language/Runtime: Java 26 (forward-looking, non-LTS)
- Toolchain: Explicit Java 26 via `JavaLanguageVersion.of(26)`

**Verified Baseline (as of Aug 2026):**
- Spring Boot 4.1.x
- Spring Cloud 2025.1
- Spring AI 2.0.x
- MCP Java SDK 2.0.x
- Spring Cloud Gateway 5.0.x
- GraalVM 25.x+ for native compilation

---

## Next Session Agenda

**Tomorrow Morning:**

1. **Confirm approach** — Any changes to three-layer architecture?
2. **Answer clarification questions** (above)
3. **Create reference-library/ directory structure**
4. **Migrate Category 01 (REST API Design)** — First guide as template
5. **Establish quality standards** — Length, structure, cross-references

---

*Document saved for continuation tomorrow. Status: Ready for implementation.*

*Last updated: September 13, 2026 — End of Session 1*
