# Architecture Styles: Decision Reference

This reference defines the 5 candidate architecture styles evaluated in Architecture Decisions. Each entry includes the definition, driver signals that favor or disfavor the style, and the common failure mode when misapplied.

---

## 1. Monolith

**Definition:** Single deployable unit; all business logic, data access, and APIs co-located in one codebase and runtime. Shared database typically. No service-to-service network calls.

**Driver Signals (Favorable):**

- **Team size:** ≤ 8 people (single team, shared ownership minimal overhead)
- **Deployment cadence:** Low (weekly or less frequent; deployment orchestration overhead not justified)
- **Scaling shape:** "Scales uniformly" — all features grow in traffic together (no subsystems require independent scaling)
- **Data consistency:** Strict/transactional required across many entities (monolith's shared DB simplifies ACID guarantees)

**Driver Signals (Unfavorable):**

- **Team size:** > 12 people (coordination overhead grows quadratically)
- **Deployment cadence:** Multiple times per day (monolith deployment blocks all teams; CI/CD bottleneck)
- **Scaling shape:** Heterogeneous (video processing subsystem scales 100x; API layer scales 5x; monolith forces both)
- **Data consistency:** Eventual OK (independent subsystems can tolerate async replication; monolith's coupling overhead wasted)

**Common Failure Mode:** Monolith forced to support heterogeneous scaling or multiple independent teams → database hotspot, deployment-conflict Hell, team blocking.

---

## 2. Modular Monolith

**Definition:** Single deployable unit, but codebase organized into separate business modules/domains with explicit interfaces. Shared database or federated databases per module. Deployment still monolithic, but internal coupling reduced via clear boundaries.

**Driver Signals (Favorable):**

- **Team size:** 8–15 people (modules can have clear ownership, but deployment still centralized)
- **Deployment cadence:** Low-to-moderate (weekly-to-daily; acceptable to coordinate one deployment, but multiple teams need clear responsibilities)
- **Scaling shape:** Mostly uniform with 1–2 subsystems growing differently (module separation allows some independent optimization without full microservices cost)
- **Data consistency:** Mixed (some strict/transactional, others eventual; module boundaries + federated DB schema provide isolation without service-to-service complexity)

**Driver Signals (Unfavorable):**

- **Team size:** ≤ 5 people (overhead of module contracts unjustified for small team)
- **Deployment cadence:** Multiple times per day, independent services (monolith deployment still blocks; modular internal structure doesn't help external throughput)
- **Scaling shape:** Highly heterogeneous (video processing 100x, search 20x, API 5x; still one deployment = all features re-deployed together, still one database = contention)
- **Data consistency:** Purely eventual (module contracts enforced at deployment time only; runtime isolation lost vs. microservices)

**Common Failure Mode:** Modular monolith boundaries eroded over time → modules make synchronous calls, shared DB schema creeps across module lines, deployment coordination reverts to chaos.

---

## 3. Microservices

**Definition:** Multiple independently deployable services, each owning a bounded business domain, data store, and API. Service-to-service communication via network (REST, gRPC, events). Decentralized data ownership.

**Driver Signals (Favorable):**

- **Team size:** 15+ people (each service owned by 1–2 team(s); independent deployment velocity justified by team autonomy)
- **Deployment cadence:** Multiple times per day, per service (independent deployment gates; one team's changes don't block others)
- **Scaling shape:** Highly heterogeneous (video processor, search index, API gateway scale independently; justify per-service resource allocation)
- **Data consistency:** Eventual (services own databases; cross-service consistency via events/choreography/sagas; distributed transactions avoided)

**Driver Signals (Unfavorable):**

- **Team size:** ≤ 10 people (operational complexity overhead — debugging, observability, inter-service contracts — not justified; coordination cost still high)
- **Deployment cadence:** Low (monolith or modular monolith simpler; distributed tracing, chaos testing, service discovery overhead wasted)
- **Scaling shape:** Uniform (all subsystems grow uniformly; microservices' independent scaling benefit not realized; per-service deployment/testing cost unjustified)
- **Data consistency:** Strict/transactional across many entities (microservices' eventual consistency contradicts requirement; distributed transaction complexity high)

**Common Failure Mode:** Microservices chosen for tech trend reasons, not drivers → 20+ services for a 3-person team; debugging cross-service failures impossible; latency increases; deployment speed decreases.

---

## 4. Event-Driven

**Definition:** Services (or subsystems) communicate via asynchronous events published to a broker (Kafka, Redis, cloud pub/sub). Decoupled in time and space. No direct service-to-service calls; all coordination through events.

**Driver Signals (Favorable):**

- **Deployment cadence:** High (services can deploy asynchronously without coordinating request/response pairs; eventual consistency model fits)
- **Scaling shape:** Heterogeneous, with bursty/spiking demand patterns (event broker naturally buffers load; subscribers scale independently without backpressure)
- **Data consistency:** Eventual (event ordering per partition sufficient; strong consistency across services not required)
- **Team size:** 10+ (operationally complex; justifies investment for fast-moving teams)

**Driver Signals (Unfavorable):**

- **Deployment cadence:** Low (event infrastructure overhead — broker setup, topic management, DLQ handling — not justified for low deployment frequency)
- **Scaling shape:** Uniform (no heterogeneous scaling benefit; monolith or modular monolith simpler)
- **Data consistency:** Strict/transactional (events cannot guarantee strong consistency across systems; saga pattern adds latency/complexity)
- **Team size:** ≤ 5 people (broker operations, event replay, partition rebalancing — too complex for small team)

**Common Failure Mode:** Event-driven chosen for "modern architecture" reasons; lack of domain experience → runaway event storms, partition hot-spots, message ordering bugs, events lost due to misconfigured retention.

---

## 5. Serverless

**Definition:** Functions or containers deployed on managed cloud platforms (AWS Lambda, Google Cloud Functions, Azure Functions); no server provisioning, auto-scale per request, pay-per-invocation. Stateless, ephemeral execution; coordinated via cloud services (queues, databases, event buses).

**Driver Signals (Favorable):**

- **Scaling shape:** Highly bursty/spiky (sudden traffic spikes → automatic scale without capacity planning; dormant periods → zero cost)
- **Deployment cadence:** Continuous (individual function deploy ≈ 1 min; no orchestration overhead; natural fit for DevOps/small teams)
- **Team size:** 3–5 people (managed infrastructure removes ops burden; developers focus on code)
- **Data consistency:** Eventual (functions are ephemeral; distributed coordination via cloud services; strong consistency difficult by design)

**Driver Signals (Unfavorable):**

- **Scaling shape:** Uniform/sustained (always-on traffic → underutilizes serverless; monolith cheaper per request)
- **Deployment cadence:** Low (no continuous deployment pressure; serverless complexity overhead not justified)
- **Data consistency:** Strict/transactional (distributed transactions across functions impossible; monolith's ACID guarantees lost)
- **Team size:** 15+ with diverse skillsets (cold-start latency problems; billing surprises; vendor lock-in; need cloud ops expertise)

**Common Failure Mode:** Serverless chosen for "low-ops" narrative; poor latency/cost analysis → cold-start timeouts for long-running workflows; bill shock from unexpected invocation patterns.

---

## Summary: Driver Decision Tree

| Team Size | Cadence        | Scaling        | Consistency | Recommended                | Rationale                                                    |
| :-------- | :------------- | :------------- | :---------- | :------------------------- | :----------------------------------------------------------- |
| ≤ 5      | Low            | Uniform        | Strict      | **Monolith**         | Simplest, ACID native, deployment overhead unjustified       |
| ≤ 5      | High           | Bursty         | Eventual    | **Serverless**       | Ops-managed, auto-scale, pay-per-use                         |
| 5–8      | Low–Moderate  | Uniform        | Mixed       | **Monolith**         | Single team, no scaling heterogeneity                        |
| 8–12     | Moderate       | Mostly-Uniform | Mixed       | **Modular Monolith** | Module boundaries, single deployment, centralized control    |
| 10–15    | Moderate–High | Heterogeneous  | Eventual    | **Microservices**    | Team autonomy, independent scaling, eventual-consistency fit |
| 15+       | High           | Heterogeneous  | Eventual    | **Microservices**    | Multiple teams, continuous deployment, scaling freedom       |
| 3–5      | Continuous     | Bursty         | Eventual    | **Serverless**       | Minimal ops, auto-scale, startup speed priority              |

*Note: This table is a heuristic, not a prescription. Always ground decisions in the 4 driver facts for the specific system, not in team size or trends alone.*
