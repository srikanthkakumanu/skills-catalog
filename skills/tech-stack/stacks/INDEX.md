# Stacks Index

Read this file first. Match a bounded context's binding constraints against the rows below, then
open at most the one playbook that matches — per `tech-stack/SKILL.md` Directive 5, cite it by
path and stop; don't read further playbooks once one fits.

Every **Spring Boot** playbook here inherits `java-baseline.md` (Java 27). It isn't a row below
because it isn't a choice — it's a prerequisite. `python-ai-agentic.md` is the one exception: it's
a Python playbook, not a Spring Boot one, so it doesn't inherit this baseline.

| Constraint | Playbook |
|---|---|
| Synchronous HTTP/REST, relational data, standard CRUD/transactional workload | `springboot4-webmvc-jpa-postgres.md` |
| High-concurrency I/O-bound, streaming, backpressure-sensitive, non-blocking end-to-end | `springboot4-webflux-reactive.md` |
| Async integration, event sourcing, CQRS, cross-context coordination, audit/replay | `springboot4-event-driven-kafka.md` |
| Large-volume scheduled/bulk processing, restartable/checkpointed jobs | `springboot4-batch.md` |
| Multiple backend services needing unified edge routing, rate limiting, auth | `springboot4-gateway.md` |
| LLM/agent integration, RAG, tool-calling, exposing capabilities via MCP | `python-ai-agentic.md` (default) — or `springboot4-ai-mcp.md` only when deliberately hosting inside an existing Spring service |
| Single team, single deploy cadence, explicit "avoid over-engineering" signal, wants module boundaries without microservices ops cost | `springboot4-modulith.md` |
| Browser-based UI (web app/dashboard/portal) confirmed as a bounded context's consumer — evidence-gated, see `SKILL.md` Directive 1; additive alongside any backend row above, not a mutually-exclusive alternative to them | `frontend-nextjs-react-typescript.md` |

## Disqualifiers worth checking before matching

- **Architecture style ADR says microservices with independent per-context scaling** →
  `springboot4-modulith.md` does not fit regardless of other constraints; that ADR already ruled
  out a single-deployable shape.
- **Agentic-AI ADR says "Not applicable"** → neither `python-ai-agentic.md` (the default) nor
  `springboot4-ai-mcp.md` (the rare Spring-hosted fallback) fits; don't select either on an FR
  alone if the confirmed ADR already closed that door — route back to `architecture-decisions`
  instead of overriding it here.
- **Constraint calls for reactive (WebFlux) AND heavy JPA/Hibernate use** → no clean fit; the two
  playbooks are mutually exclusive at the persistence layer (Hibernate is blocking). Present as
  `pending` with the conflict named, per Directive 3 — don't force one.
- **No UI/browser-facing consumer evidenced for a context** (pure API/service-to-service) → don't
  attach `frontend-nextjs-react-typescript.md`; the evidence gate at decomposition (Directive 1)
  already said no frontend layer exists here — this isn't a playbook mismatch to route around.

## Cross-cutting — not a playbook of its own

- **Observability** (Actuator, Micrometer, OpenTelemetry) — baseline expectation across every
  playbook, not a differentiator; don't spend a bounded-context decision on it.
- **Container/native packaging** (Docker, Kubernetes, GraalVM native image) — a deployment
  attribute of the chosen playbook's Stack row, not a separate axis.
- **Security** (OAuth2 resource server vs. first-party JWT) — stated inside each playbook's Stack
  row where relevant; depends on whether tokens are issued by an external IdP or first-party.
- **Architectural patterns** (DDD, hexagonal, layered) — selected at `detailed-design` (Phase 4),
  not here; any Spring Boot playbook can carry any of them. Implementation guidance lives in Phase
  7 regardless of which stack playbook was chosen.
