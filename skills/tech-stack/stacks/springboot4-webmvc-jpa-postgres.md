# Spring Boot 4 · Web MVC + JPA + PostgreSQL

The default: synchronous, relational, transactional. Start here unless a specific constraint
rules it out.

## Fits
- **Data model:** relational, ACID, standard transactional workload (Spring Data JPA + Hibernate 7,
  Jakarta Persistence 3.2)
- **API protocol:** synchronous HTTP/REST (Spring MVC)
- **Concurrency:** standard request-per-thread load; virtual threads (available from Java 21, so
  present here) cover most throughput needs without moving to WebFlux
- **Caching:** read-heavy hot paths → Spring Data Redis, cache-aside, mandatory TTL
- **Security:** OAuth2 resource server (external IdP — Keycloak/Auth0/Okta/Cognito) or first-party
  JWT issuance, either via Spring Security 7's lambda DSL

## Does NOT fit
- Reactive/non-blocking requirement end-to-end — conflicts with Hibernate's blocking model; route
  to `springboot4-webflux-reactive.md` instead, don't mix the two in one context
- Event-sourced or CQRS data model with cross-context coordination needs —
  `springboot4-event-driven-kafka.md`
- Large-volume scheduled/bulk processing — `springboot4-batch.md`

## Stack
| Component | Choice |
|---|---|
| Language | Java 27 (see `java-baseline.md`) |
| Web | Spring MVC (`spring-boot-starter-webmvc`) |
| Persistence | Spring Data JPA + Hibernate 7 (`jakarta.persistence.*`) |
| Migrations | Flyway (`spring-boot-starter-flyway` — no longer pulled in transitively by JPA/JDBC starters in Boot 4) |
| Cache (only where a read-heavy NFR exists) | Spring Data Redis, cache-aside |
| Security | Spring Security 7 — `spring-boot-starter-security-oauth2-resource-server` (external IdP) or a first-party JWT filter chain |
| API contract | REST conventions + RFC 9457 Problem Details for errors; native Boot 4 API versioning (`version` mapping attribute) over hand-rolled `/v1` prefixes |
| Testing | JUnit 5 + `@MockitoBean` + Testcontainers (Boot 4 dropped `@MockBean`) |

## Prerequisites
- `jakarta.*` imports, never `javax.*`
- UUID or pooled-sequence IDs — not `GenerationType.IDENTITY` — on any table under a write-throughput NFR (IDENTITY disables JDBC insert batching)
- `@Version` as nullable `Long`, not primitive, on user-editable aggregates

## Tradeoffs
- Ecosystem/hiring: strongest in the JVM world — default choice unless a constraint says otherwise
- Vendor lock-in: none — pure Apache 2.0/Spring stack, cloud-agnostic

## Implementation detail
`implementation-guide` (Phase 7) — spring-data-jpa, flyway-migrations, transactional-patterns,
spring-data-redis, rest-api-conventions, problem-details-rfc9457, api-versioning, hateoas,
openapi-first, http-interface-clients, oauth2-resource-server, spring-security-jwt,
layered-architecture, null-safety, testing-pyramid, resilience-retry, configuration-properties.
