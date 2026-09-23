# Spring Boot 4 · Spring Cloud Gateway

Edge routing for multiple backend services. Not a client library, not for internal
service-to-service calls, and not a place for domain logic.

## Fits
- **Topology:** several backend services need a single edge for routing, rate limiting, and
  authentication
- **Concern:** cross-cutting edge policy (auth, rate limits, timeouts) applied once instead of
  per-service

## Does NOT fit
- A single monolith or single service — nothing to route between; every other playbook in this
  catalog already exposes its own API
- Internal service-to-service calls — use declarative `@HttpExchange` clients
  (`http-interface-clients`) from the calling context instead, not a gateway hop
- Domain orchestration of any kind — filters are edge-only; business logic belongs downstream

## Stack
| Component | Choice |
|---|---|
| Language | Java 27 (see `java-baseline.md`) |
| Gateway | Spring Cloud Gateway 5 on Boot 4, WebFlux or Web MVC server starter — matched to the exact Boot 4 line via the compatibility matrix; Cloud trains aren't interchangeable |

## Prerequisites
- Identity derived after authentication, never trusted from a caller-supplied header
- POST/non-idempotent requests never auto-retried
- Response timeouts always set — an unbounded upstream can exhaust gateway resources

## Tradeoffs
- Another moving part to operate and version against the exact Boot 4 line in use

## Implementation detail
`implementation-guide` (Phase 7) — spring-cloud-gateway.
