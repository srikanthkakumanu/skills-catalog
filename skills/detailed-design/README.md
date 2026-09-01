# Detailed Design Skill

**Turns confirmed architecture decisions into bounded contexts, design patterns, data architecture, API contracts, and security model. Every hard-constraint NFR must be addressed or explicitly flagged unaddressed.**

A systematic skill for consuming confirmed architecture decisions (from `/architecture-decisions`) and translating them into detailed design specifications — bounded context decomposition, pattern selection (microservice/integration/design patterns), data architecture choices, API contract definitions, and security model — with rigorous traceability of every hard-constraint NFR to a design decision.

## Overview

This skill takes a confirmed `architecture-decisions.md` (with both ADRs locked at `status: confirmed`) and produces `detailed-design.md` — a reference document that operationalizes the architecture by defining bounded contexts, selecting only necessary patterns (each tied to a specific problem), choosing data strategies per context, defining API contracts with human-in-the-loop gates explicitly modeled, and building a security model. Every hard-constraint NFR is walked and either addressed by a design decision or flagged unaddressed for later resolution.

**Critical guard:** If any ADR in architecture-decisions.md is still `status: pending`, this skill refuses to run and routes back — design is locked only to confirmed architecture.

## What It Does

The skill executes exactly six sequential steps:

1. **Bounded Contexts** — Derive from the confirmed style ADR's topology (monolith splits into modules, microservices defines service boundaries). Name each context and state its one-line responsibility.
2. **Pattern Selection** — Choose one microservice/integration pattern per context, plus at most 1–2 design patterns (e.g., CQRS, saga, event sourcing). Each pattern must trace to a **named coordination problem**, not general best practice.
3. **Data Architecture** — For each context: DB-per-context vs shared? Driven by hard-constraint NFRs (scalability, consistency, audit needs). Event sourcing/CQRS only where an explicit audit/replay/read-write-mismatch requirement exists.
4. **API Contracts** — One line per context boundary: protocol + versioning. Human-in-loop gates from the agentic-AI ADR are shown as separate endpoints/steps, not folded into the main flow.
5. **Security Model** — Authentication/authorization per context; agentic capability's autonomous vs. gated actions stated explicitly, matching API contracts.
6. **NFR Traceability** — Walk every hard-constraint NFR. Name the design decision that addresses it, or flag it unaddressed.

Output is always `detailed-design.md` with six sections. Every HC NFR is accounted for (addressed or flagged).

## Key Design Principles

- **Design is locked to confirmed architecture** — If any ADR is `pending`, this skill blocks and returns you to architecture decisions. No design without confirmation.
- **Smallest sufficient pattern set** — Every pattern exists because a named coordination problem requires it. "It's a best practice" is not a sufficient reason. No patterns without problems.
- **Bounded contexts follow the style** — Don't re-derive from requirements. If the style ADR says "modular monolith with three modules," derive contexts from those three modules. If it says "two microservices," design two bounded contexts.
- **Human-in-loop gates are design facts** — If the agentic-AI ADR says decisions need human approval, that shows up as a concrete API endpoint (e.g., `/approve-transaction`), not a comment. Gates are part of the contract.
- **Every HC NFR is addressed or flagged** — No silent gaps. If an NFR is hard-constraint, it either traces to a design decision (e.g., "persistence via PostgreSQL per-context, addressing Reliability HC #2") or is flagged as unaddressed (e.g., "Compliance HC #4: GDPR audit trail — deferred to Phase 4 implementation").

## Input

A completed architecture decision set with both ADRs confirmed:

- **architecture-decisions.md** — Architecture Style and Agentic-AI Fitness ADRs, both at `status: confirmed`
- **req-nfr-analysis.md** — Normalized FRs, NFR table (10 categories with HC priorities), structural findings
- **BRD.md** — Domain, personas, use cases, scope boundaries (for context and success criteria)

All ADRs must be confirmed (`status: confirmed`). If any are pending, the skill refuses to proceed.

## Output: `detailed-design.md`

```markdown
# Detailed Design: [System Name]

## Bounded Contexts

| Context | Responsibility | Microservice Pattern |
|---------|-----------------|----------------------|
| Expense Submission | Accept and validate receipt uploads | Async task queue (bursty load) |
| Policy Engine | Evaluate expenses against corporate policy | Sync, read-heavy cache layer (performance HC) |
| Approvals | Route expenses to approvers, track state | Saga (distributed transaction across Submission + Policy) |
| Audit Log | Record all decisions for compliance | Event sourcing (Compliance HC: immutable audit trail) |

## Pattern Selection

**Async Task Queue (Expense Submission)**
- **Problem:** Receipt uploads are I/O-bound (image processing, OCR downstream); blocking requests = poor user experience and wasted web server threads.
- **Solution:** Queue uploads, process async, notify user when ready.
- **Implementation:** Message queue (e.g., RabbitMQ, SQS) + worker pool.

**Read-Heavy Cache (Policy Engine)**
- **Problem:** Policy rules change infrequently but are queried on every expense. Direct DB queries = latency HC (#1: <500ms per request).
- **Solution:** Cache rules in memory/Redis; invalidate on policy update.
- **Implementation:** Cache-aside pattern + TTL.

**Saga (Approvals)**
- **Problem:** Expense approval spans two contexts (Submission validates format, Policy Engine evaluates amount). Need distributed transaction (Reliability HC: atomic across contexts).
- **Solution:** Choreography saga (context-to-context events) or orchestration saga (Approvals Service coordinates).
- **Implementation:** Event-driven (context publishes `ExpenseReady`, Policy Engine responds with `PolicyPass`/`PolicyFail`).

**Event Sourcing (Audit Log)**
- **Problem:** Compliance HC requires immutable audit trail, full decision history, ability to replay all decisions for forensics.
- **Solution:** Store all events in append-only log; rebuild state from events.
- **Implementation:** Event store (e.g., EventStoreDB) or log-based DB (PostgreSQL `JSONB`).

## Data Architecture

| Context | Primary Store | Pattern | Rationale |
|---------|---|---|---|
| Expense Submission | PostgreSQL (per-context) | Standard OLTP | Transactional integrity for receipts + metadata. HC: single-context consistency (Reliability). |
| Policy Engine | PostgreSQL + Redis cache | Read-cache-aside | Infrequent writes (policy updates), frequent reads. HC: <500ms latency (Performance). |
| Approvals | PostgreSQL + event log | CQRS (optional read model) | State machine (pending → approved → paid). Event log for audit. HC: atomic cross-context (Reliability) + audit trail (Compliance). |
| Audit Log | Event Store (PostgreSQL JSON log) | Event sourcing | Append-only immutability. HC: non-repudiable audit trail (Compliance). |

**Shared DB?** No. Each context has its own PostgreSQL instance + optional Redis. Cross-context sync via events/APIs. Justification: Reliability HC ("no silent data loss") requires per-context backups + failover; Compliance HC ("immutable audit trail") requires Audit Log isolation.

**CQRS?** Approvals context only (optional): write model is state machine; read model is materialized decision history. Justified by: Compliance HC (need to query decision history efficiently) + Reliability HC (need to handle concurrent approvals without lost updates).

## API Contracts

| Boundary | Endpoint | Method | Input/Output | Agentic Gate |
|----------|----------|--------|---|---|
| Submission → Policy | `POST /policies/evaluate` | HTTP/JSON | Expense JSON → `{ passed: bool, reason: string }` | No gate (deterministic) |
| Policy → Approvals | `POST /approvals/route` | Event (Kafka) | `ExpensePolicyPass` event | No gate (event-driven) |
| Approvals → Audit | `POST /audit/record` | Event (Kafka) | `ExpenseApproved` / `ExpenseRejected` | No gate (side effect only) |
| External (User) → Submission | `POST /expenses/submit` | HTTP multipart | Receipt file + metadata → `{ expenseId, status }` | No gate (user-initiated) |
| External (Approver) → Approvals | `GET /approvals/{id}` / `POST /approvals/{id}/approve` | HTTP/JSON | Decision form → approval confirmation | **Human gate**: Approver explicitly clicks "approve"; no auto-action. |

**Agentic capability gates:**
- Expense categorization (Policy Engine) — **autonomous** (rule-based, deterministic)
- Policy matching (Policy Engine) — **autonomous** (threshold-based, human reviews edge cases async)
- Approval routing (Approvals) — **gated** (human must review and click approve; no auto-approval)

## Security Model

### Authentication
- **External users (expense submitters)**: OAuth 2.0 via company identity provider
- **External users (approvers)**: OAuth 2.0 + role check (group membership: "expense-approvers")
- **Internal (context-to-context)**: Service-to-service mTLS (mutual TLS); each context has a certificate

### Authorization
- **Expense Submission**: Users can submit their own expenses; can read their own submission history
- **Policy Engine**: Internal service only (no external callers); read-only access to policy database
- **Approvals**: Approvers can only see expenses assigned to them (by department/cost center)
- **Audit Log**: Read-only access; only Finance and Compliance roles can query

### Agentic Actions
- **Policy Engine evaluations** (autonomous): Logged to audit trail; do not require human approval before storage
- **Approval routing** (gated): System suggests approver based on amount threshold; actual approval is a human click (traces to `/approvals/{id}/approve` endpoint)
- **Rejection** (gated): System can auto-reject expenses that fail policy thresholds; human can override via `/approvals/{id}/appeal` (future)

### Sensitive Data
- Receipts (PII, payment method): Encrypted at rest (AES-256) in Submission context; encryption key managed by KMS
- Policy rules: Not sensitive; can be cached in memory
- Approval decisions: Logged to Audit Log; immutable (no delete/update)

## NFR Traceability

| HC NFR | Category | Requirement | Addressed By | Design Decision |
|--------|----------|-------------|---|---|
| #1 | Performance | <500ms per request p95 | **Addressed** | Read-cache-aside (Policy Engine); connection pooling (all contexts) |
| #2 | Reliability | Atomic cross-context (no lost approvals) | **Addressed** | Saga + event-driven coordination + persistent event log |
| #3 | Security | No payment method in logs | **Addressed** | Encryption at rest (KMS) + field masking in audit trail |
| #4 | Compliance | Immutable audit trail (GDPR Article 5) | **Addressed** | Event sourcing in Audit Log context; append-only design |
| #5 | Maintainability | Clear module boundaries | **Addressed** | Bounded contexts per style ADR (modular monolith); explicit API contracts |
| #6 | Scalability | 100k concurrent users (Reliability) | **Addressed** | Async task queue (non-blocking); per-context DBs allow independent scaling |
| #7 | Observability | Trace all decisions end-to-end | **Addressed** | Correlation IDs in all event headers; structured logging (JSON) |
| #8 | Transparency | Human approvals logged + visible | **Addressed** | Approvals context logs all decisions; audit trail shows approver ID + timestamp |

**Unaddressed NFRs:** None.

---

## Example: Expense Reconciliation System

**Confirmed Style ADR:** Modular Monolith (three modules: submission, policy engine, approvals)

**Confirmed Agentic-AI ADR:** Partial fit (policy auto-evaluation autonomous; approval routing gated)

### Bounded Contexts (from style)

1. **Expense Submission** — Accept receipt uploads, store metadata
2. **Policy Engine** — Evaluate against corporate spend limits and category rules
3. **Approvals** — Route to department heads, track approval state, publish decisions to Audit Log

### Patterns (one per context + HC problems)

- **Async task queue** (Submission): I/O-bound image processing doesn't block HTTP requests (Performance HC)
- **Read-cache-aside** (Policy): Infrequent policy updates, frequent queries (Performance HC <500ms)
- **Saga** (Approvals): Coordinating policy eval + approval across contexts (Reliability HC: atomic)
- **Event sourcing** (Audit Log): Immutable decision history (Compliance HC: GDPR Article 5)

### Data Architecture

- Submission: PostgreSQL, ACID transactional
- Policy Engine: PostgreSQL + Redis (cache rules)
- Approvals: PostgreSQL state machine + Kafka events
- Audit Log: Event store (append-only, never update/delete)

Each context owns its DB (per Reliability HC); cross-context sync via events/APIs.

### API Contracts

- Submission → Policy: `POST /policies/evaluate` (sync, <500ms)
- Policy → Approvals: Event `ExpensePolicyPass` (async)
- Approvals: `GET /approvals/{id}` (read), `POST /approvals/{id}/approve` (write, human gate)

### Security Model

- OAuth 2.0 for external users; mTLS for internal services
- Approvers see only their assigned expenses (RBAC by department)
- Agentic decisions (policy eval) logged but not gated; approval routing is gated

### NFR Traceability

All 8 HC NFRs traced to design decisions. No gaps.

```

Every section is always present. NFR Traceability table shows all HC NFRs; empty traceability is not valid (all HCs must be addressed or explicitly flagged).

## How It Works

### Step 1: Bounded Contexts

Read the confirmed style ADR. If it says:

- **Monolith**: Derive contexts from the natural module boundaries in the BRD's domain or the ADR's own proposed split
- **Modular Monolith**: Use the ADR's named modules as contexts
- **Microservices**: Use the ADR's named services as contexts
- **Event-Driven**: Use the ADR's event sources/sinks as contexts
- **Serverless**: Derive contexts from the ADR's function definitions

Name each context (one noun), state its one-line responsibility, and note which microservice pattern it uses (e.g., "Async task queue," "Saga," "CQRS," "Event sourcing," or "None" for simple sync request/response).

### Step 2: Pattern Selection

For each context, ask: **What coordination problem exists?**

Examples of named problems:

- I/O-bound work blocking HTTP → async task queue
- Infrequent writes, frequent reads → read-cache-aside
- Distributed transaction across services → saga
- Need full history and replay capability → event sourcing
- Different read/write models → CQRS
- Long-running async flow → workflow/orchestration

If you can't name a problem, **don't add a pattern**. "It's a best practice" is not a problem.

Select at most 1 microservice/integration pattern + at most 1–2 design patterns per context. Each pattern must include:

- **Problem**: The coordination challenge it solves
- **Solution**: The pattern name and brief mechanism
- **Implementation**: Concrete tool/technology (e.g., RabbitMQ, Redis, Kafka, event store)

### Step 3: Data Architecture

For each context, decide:

**Own DB or shared?**

- Own DB if: Hard-constraint NFRs demand per-context failover (Reliability), per-context scaling (Scalability), or data isolation (Compliance/Security)
- Shared DB if: No HC NFR requires isolation; operational simplicity wins
- **Default: own DB** (safer for reliability and scalability)

**Sync or async replication?**

- Sync: Immediate consistency, higher latency
- Async: Lower latency, eventual consistency
- Decide based on HC NFRs (consistency vs. latency trade-off)

**Event sourcing or CQRS?**

- Event sourcing: Only if an explicit audit/replay/non-repudiation HC NFR exists (e.g., Compliance)
- CQRS: Only if read/write models differ significantly AND performance HC requires separate scaling

### Step 4: API Contracts

For each context boundary (internal or external), define:

| Boundary             | Endpoint                    | Method | Protocol | Input/Output                     | Async? |
| -------------------- | --------------------------- | ------ | -------- | -------------------------------- | ------ |
| Submission → Policy | `POST /policies/evaluate` | JSON   | HTTP     | Expense JSON → verdict + reason | Sync   |
| Policy → Approvals  | `ExpensePolicyPass`       | Event  | Kafka    | event schema                     | Async  |

**Critical for agentic-AI:** If the agentic-AI ADR says an action is gated (requires human approval), show that gate as a separate endpoint or explicit approval step. E.g., don't fold a human approval into a single `/process` endpoint; split into `/process/auto` (system) + `/process/approve` (human).

### Step 5: Security Model

Define per-context:

**Authentication:** How do callers identify themselves?

- OAuth 2.0 for external users?
- mTLS for internal services?
- API keys?

**Authorization:** Who can call which endpoints?

- RBAC (role-based): Approvers only see their assigned expenses
- ABAC (attribute-based): Access based on department, cost center, etc.
- Attribute policies: Can only approve expenses ≤ their approval limit

**Sensitive data:** Which fields need encryption, masking, or special handling?

- PII (personal info): Encrypt at rest, mask in logs
- Payment data: Never log; encrypt in transit + at rest
- Audit logs: Immutable, audit who accessed them

**Agentic actions:** Which autonomous decisions are allowed, and which require human gates?

- Autonomous: Rule-based, deterministic decisions (e.g., expense category rules)
- Gated: Decisions with uncertainty or high business impact (e.g., approval, large refunds)

### Step 6: NFR Traceability

Walk the HC NFRs from the req-nfr-analysis table. For each:

1. **Name the design decision** that addresses it. E.g.:

   - HC Performance #1 ("< 500ms p95") → "Read-cache-aside in Policy Engine context"
   - HC Reliability #2 ("no lost approvals") → "Saga + event-driven coordination"
   - HC Compliance #3 ("GDPR audit trail") → "Event sourcing in Audit Log"
2. **If unaddressed**, flag it clearly:

   - "HC Security #4 (encryption at rest) — deferred to Phase 4 (implementation)"
   - "HC Scalability #5 (100k users) — addressed by async queue, but DBA review needed for DB connection pooling"

Table format:

| HC NFR | Category    | Requirement | Addressed By          | Design Decision                    |
| ------ | ----------- | ----------- | --------------------- | ---------------------------------- |
| #1     | Performance | <500ms p95  | **Addressed**   | Read-cache-aside (Policy Engine)   |
| #2     | Compliance  | Audit trail | **Unaddressed** | Deferred to Phase 4 implementation |

## When to Use

Invoke this skill when:

- You have confirmed architecture decisions (both ADRs at `status: confirmed`)
- You need to translate architecture into concrete design (bounded contexts, patterns, data choices)
- You want to operationalize every hard-constraint NFR into a design decision
- You're ready to hand off to implementation teams (developers, DBAs, security) with clear, unambiguous design specs

**Do NOT use this skill for:**

- Unconfirmed architecture (if any ADR is `pending`, this skill refuses to run)
- Tech stack selection (database brand, ORM framework, etc. — that's Phase 4+)
- Re-deciding architecture or agentic-AI fitness (those are locked in confirmed ADRs)
- Test/deployment plans (separate concern)

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes
./install.sh --skill detailed-design

# Or: install to a specific runtime
./install.sh --skill detailed-design --target claude
```

### Invocation

Use natural language or a slash command:

```text
/detailed-design Turn our confirmed architecture decisions into detailed design

design the system based on the architecture decisions we just confirmed

/detailed-design We have architecture ADRs locked; time to design the bounded contexts and patterns
```

The skill reads the confirmed architecture decisions and produces `detailed-design.md` with all six sections and full NFR traceability.

## Files

- **SKILL.md** — Persona directives and 6-step execution protocol
- **README.md** — This file; user-facing reference documentation

## Out of Scope

- **Tech stack selection** — Database brand, ORM, web framework, deployment platform (Phase 4+)
- **Re-deciding architecture or agentic-AI fitness** — Those are locked in confirmed ADRs
- **Test and deployment strategies** — Separate phase
- **Implementation details** — Code structure, configuration, CI/CD pipelines

## Pipeline Context

This skill is **Phase 3** of the BRD → Requirements → Architecture → Design → Implementation pipeline:

- **Phase 1 (brd):** Product concept → BRD (domain, personas, use cases, scope, self-check)
- **Phase 2 (req-nfr-analysis):** BRD → normalized requirements (FRs, 10 NFR categories, structural findings)
- **Phase 3 (architecture-decisions):** Normalized requirements → confirmed architecture (style + agentic-AI ADRs)
- **Phase 4 (detailed-design - this skill):** Confirmed architecture → detailed design (bounded contexts, patterns, data, APIs, security, NFR traceability)
- **Phase 5 (future):** Detailed design → implementation plan, tech stack, code structure

Each phase's output feeds into the next. Design is locked only to **confirmed** architecture.

## Version History

**v1.0** (2026-09-02):

- Initial skill definition: 6-step process, mandatory checkpoint guard (refuse pending ADRs), full NFR traceability
- Frontmatter: `name`, `description`, `license`, `compatibility` (no `models`, `scopes`, `context_optimization`)
- Focus on smallest-sufficient patterns (every pattern tied to a named problem)
- Bounded contexts derived from confirmed style ADR (not re-derived from scratch)
- Human-in-loop gates from agentic-AI ADR modeled as explicit API endpoints

---
