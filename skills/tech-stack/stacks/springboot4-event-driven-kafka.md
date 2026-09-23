# Spring Boot 4 · Event-Driven (Kafka/RabbitMQ)

Async integration and cross-context coordination. Not a default — select only when a real
decoupling, audit, or replay need exists.

## Fits
- **Data model:** event-sourced, CQRS read/write split, append-only audit trail
- **API protocol:** async events (Kafka, RabbitMQ, Pulsar, JMS), not synchronous request/response
- **Reliability:** at-least-once delivery as the working assumption; consumers own idempotency,
  producers use an outbox when atomicity with a local write matters

## Does NOT fit
- Simple synchronous request/response with no cross-context decoupling need — adds latency and
  operational surface for no payoff; use `springboot4-webmvc-jpa-postgres.md`
- Low-latency user-facing calls where the caller needs an immediate result — a broker round-trip
  doesn't fit that shape
- A single deployable with nothing else to coordinate with

## Stack
| Component | Choice |
|---|---|
| Language | Java 27 (see `java-baseline.md`) |
| Messaging | Spring Cloud Stream on Boot 4's own messaging/test starters (not Boot 3 transitive deps) |
| Broker | Kafka or RabbitMQ, per existing platform standard |
| Delivery pattern | Outbox for atomicity with a local DB write; consumer-side idempotency always, regardless of any broker transaction guarantee |
| Contract | Stable, versioned event schema — never a framework entity serialized directly |

## Prerequisites
- Idempotency enforced at the consumer regardless of broker-level "exactly once" claims
- Failure classification before retrying — not every exception is transient
- Idempotency keys enforced by a database uniqueness constraint, not a JVM map or Redis TTL alone

## Tradeoffs
- Operational cost: a broker is new infrastructure to run, monitor, and reason about — justify it
  against the coordination problem it solves, per `detailed-design`'s pattern-selection directive
- Debuggability: async flows are harder to trace than a synchronous call stack; tracing is not
  optional here

## Implementation detail
`implementation-guide` (Phase 7) — event-driven-messaging, idempotency-patterns.
