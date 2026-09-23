# Spring Boot 4 · WebFlux Reactive

Non-blocking end-to-end. Choose this only when the full request path benefits from it — not from
a general preference for "reactive."

## Fits
- **Data model:** reactive relational (R2DBC) or a reactive document store; not standard blocking JPA
- **API protocol:** streaming, backpressure-sensitive, real-time/high-fan-out HTTP or WebSocket
- **Concurrency:** high-concurrency I/O-bound workload where thread-per-request would exhaust the
  pool even with virtual threads

## Does NOT fit
- Any call path that still uses blocking JDBC/Hibernate — wrapping a blocking call in `Mono.just`
  still blocks the event loop; if JPA is required, use `springboot4-webmvc-jpa-postgres.md`
  instead, don't force both stacks into one context
- Simple CRUD with low/moderate concurrency — added complexity with no throughput payoff; the
  default playbook already covers this
- Heavy multi-step transactional workflows — the JPA/Hibernate transactional ecosystem is far more
  mature than reactive transaction management

## Stack
| Component | Choice |
|---|---|
| Language | Java 27 (see `java-baseline.md`) |
| Web | Spring WebFlux (`spring-boot-starter-webflux`) |
| Persistence | R2DBC (reactive relational) or reactive Spring Data Mongo — never mixed with JPA in the same context |
| Outbound calls | Declarative `@HttpExchange` clients via `@ImportHttpServices`, `WEB_CLIENT` explicitly selected |
| Security | Spring Security 7 reactive filter chain |

## Prerequisites
- No `block()`/`subscribe()` inside application flow — subscription stays with the runtime
- Tenant/trace context via Reactor `Context`, never `ThreadLocal`
- `flatMap` concurrency bounded from downstream limits, never unbounded

## Tradeoffs
- Team familiarity: reactive programming has a real learning curve; this should be driven by a
  genuine throughput/streaming NFR, not adopted speculatively
- Ecosystem: narrower than the blocking-JPA path — fewer libraries assume a reactive pipeline

## Implementation detail
`implementation-guide` (Phase 7) — webflux-reactive-patterns, http-interface-clients.
