# Tech Stack Skill

**Selects full-stack technology choices per bounded context from detailed design, citing a catalog playbook where one fits or presenting tradeoff options with a mandatory confirmation checkpoint.**

A decisive skill for consuming detailed design specifications (from `/detailed-design`) and selecting technology stacks (frontend to database) per bounded context. Catalog playbooks are applied first — if a playbook fits with no conflicts, it's confirmed immediately. If no playbook fits, 2–3 full-stack tradeoff options are presented at pending status and require explicit selection before finalization.

## Overview

This skill takes a completed `detailed-design.md` (with bounded contexts, patterns, data architecture, API contracts, and security model all defined) and produces `tech-stack.md` — a reference document that selects concrete technologies per context. The skill enforces a catalog-first approach: if a playbook from `stacks/*.md` fits all constraints (data model, API protocol, security, performance), it's cited directly. If no playbook fits or conflicts exist, full-stack tradeoff options are presented at pending status, and you explicitly choose one. Every context must be confirmed before the document is valid.

**Design principle:** Differ contexts get different stacks. That's not inconsistent; it's expected.

## What It Does

The skill executes exactly four sequential steps:

1. **List Binding Constraints** — For each bounded context, extract constraints from detailed-design: data model (relational/document/event-sourced?), API protocol (HTTP/gRPC/async events?), security requirements (authn/authz method?), any performance/scalability figures.
2. **Catalog Check** — For each context, search `stacks/` playbooks. If one matches all constraints, cite it directly: `status: confirmed`. No re-derivation, no checkpoint needed.
3. **No Fit / Conflict** — If no playbook fits or a conflict exists, present 2–3 full-stack options (frontend framework, backend runtime, database, message broker if needed). State only relevant tradeoffs per context (familiarity, ecosystem, cost, hiring pool). No ranking beyond stating tradeoffs. Set `status: pending`.
4. **Wait for Selection, Update to Confirmed** — Present all pending contexts. You select one option per pending context. Update status to `confirmed` with the chosen option (discard alternatives).

Output is always `tech-stack.md` with a table. No context can remain `pending`; the deliverable is only valid when all are confirmed.

## Key Design Principles

- **One decision per bounded context** — Each context may have a different stack. That's expected, not a bug.
- **Catalog match first** — If a playbook exists and fits, cite it directly. No re-derivation, no second-guessing, no checkpoint gate.
- **No unilateral off-catalog picks** — If no playbook fits, present tradeoff options and stop. Never decide an off-catalog stack alone.
- **Constraints drive disqualification** — A stack must satisfy every data/API/security constraint detailed-design set. Disqualify before weighing tradeoffs.
- **All contexts confirmed before valid** — The deliverable isn't finished while any context is still `pending`. Explicit selection required.

## Input

A completed detailed design with all bounded contexts specified:

- **detailed-design.md** — Bounded contexts (name + responsibility), data architecture (per-context DBs? shared? event sourcing?), API contracts (protocol, versioning), security model (authn/authz per context)
- **req-nfr-analysis.md** — Hard-constraint NFRs (performance latency, scalability throughput, compliance needs)
- **stacks/*.md playbooks** — Catalog of vetted full-stack templates (e.g., `stacks/python-django-postgres.md`, `stacks/node-express-mongodb.md`)

Contexts must have clear data/API/security constraints. If a context is under-constrained (missing detail from earlier phases), flag it as such.

## Output: `tech-stack.md`

```markdown
# Technology Stack Decisions: [System Name]

| Context | Stack | Source/Rationale | Status |
|---------|-------|--|--|
| Expense Submission | Python 3.11 + FastAPI + PostgreSQL 15 + Celery + Redis | Catalog: `stacks/python-fastapi-postgres-async.md` (async task queue + relational model match constraints). Reliability HC: ACID per-context; Performance HC: <500ms response via FastAPI; Compliance: PostgreSQL encryption at rest. | Confirmed |
| Policy Engine | Python 3.11 + FastAPI + PostgreSQL 15 + Redis (cache-aside) | Catalog: `stacks/python-fastapi-postgres-cached.md` (read-heavy cache pattern). Justification: infrequent writes (policy updates), frequent queries (Performance HC: <500ms p95). Redis TTL invalidation on policy change. | Confirmed |
| Approvals | Python 3.11 + FastAPI + PostgreSQL 15 + Kafka | Catalog: `stacks/python-fastapi-postgres-kafka.md` (saga + event-driven). Justification: CQRS read model for approval history (Compliance HC); Kafka for cross-context coordination (Reliability HC: atomic). | Confirmed |
| Audit Log | Python 3.11 + FastAPI + PostgreSQL 15 (JSON log table) | Catalog: `stacks/python-fastapi-postgres-eventlog.md` (event sourcing via JSONB). Justification: append-only immutability (Compliance HC: GDPR audit trail); no deletes/updates. | Confirmed |

**Frontend (all contexts):** React 18 + TypeScript + Vite (per detailed-design API contract: HTTP/JSON). Catalog: `stacks/react-typescript-vite.md`.

**All contexts confirmed. Deliverable valid.**

---

## Alternative Tradeoff Example (Pending Status)

Assume a new context **Analytics** with constraints:
- Data: read-only queries over expense history (large dataset, 1M+ records)
- API: async batch exports (not HTTP sync)
- Performance HC: query latency <5 seconds (analytical, not user-facing)
- No catalog fit for analytical stack → present options at pending:

| Context | Stack | Source/Rationale | Status |
|---------|-------|--|--|
| Analytics | *[Pending]* | No playbook matches analytical + async export combination. Options: <br> **Option 1:** DuckDB + Python (embedded, no server, lightning-fast analytics on Parquet exports from PostgreSQL). Pro: zero ops; Con: not web-accessible, requires Python knowledge. <br> **Option 2:** Redshift + Python API (managed data warehouse, standard SQL). Pro: familiar SQL, built-in scaling; Con: AWS vendor lock-in, cost for small datasets. <br> **Option 3:** BigQuery + Python API (fully managed, serverless analytics). Pro: unlimited scale, SQL standard; Con: Google vendor lock-in, coldstart latency on first query. | Pending |

(After your selection, status updates to `confirmed` with chosen option.)
```

Table structure:
- **Context**: Bounded context name from detailed-design
- **Stack**: Full stack (frontend to database) or `[Pending]` if awaiting selection
- **Source/Rationale**: Playbook name or full tradeoff options with pros/cons
- **Status**: `confirmed` (playbook match or you selected) or `pending` (awaiting your selection)

Every context must be confirmed before the document is valid.

## How It Works

### Step 1: List Binding Constraints

For each bounded context from detailed-design, extract:

**Data Model Constraints:**
- Relational (structured tables)? → SQL database
- Document (flexible schema)? → NoSQL (MongoDB, DynamoDB)
- Event-sourced (audit trail, replay)? → Event store (EventStoreDB, Kafka logs)
- Read-heavy cache needed? → Redis, Memcached
- Shared vs. per-context DB? → Affects deployment topology

**API Protocol Constraints:**
- Synchronous HTTP/REST? → Web framework (Django, FastAPI, Express)
- gRPC (low-latency, binary)? → gRPC framework (specialized)
- Async events (Kafka, RabbitMQ)? → Message broker integration
- Real-time bidirectional (WebSocket)? → Framework with WebSocket support

**Security Constraints:**
- OAuth 2.0 needed? → Framework with OAuth libraries
- mTLS for internal services? → TLS support + certificate management
- Encryption at rest? → Database encryption or app-level (depends on tech choice)
- PII masking in logs? → Logging framework with field masking

**Performance/Scalability Figures:**
- Latency HC (e.g., <500ms p95)? → Frameworks/databases optimized for low latency
- Throughput HC (e.g., 100k concurrent)? → Async frameworks (FastAPI, Node.js), connection pooling
- Data volume (e.g., 1M+ records)? → Database choice (relational vs. columnar for analytics)

### Step 2: Catalog Check

For each context, search the `stacks/` directory for playbooks that match all constraints:

**Playbook Format** (example):
```markdown
# Python + FastAPI + PostgreSQL + Celery (Async Task Queue)

**Fits:**
- Data model: Relational (PostgreSQL)
- API protocol: HTTP/JSON (FastAPI)
- Patterns: Async task queue (Celery + Redis)
- Security: OAuth 2.0 (via Python-Jose), PostgreSQL encryption at rest
- Performance: <500ms latency (FastAPI is fast); scales via Celery workers

**Does NOT fit:**
- Event sourcing (no native event store; can add EventStoreDB but adds complexity)
- Real-time WebSocket (not a core feature; can be added but not built-in)

**Stack:**
- Frontend: React 18 + TypeScript
- Backend: Python 3.11 + FastAPI
- Database: PostgreSQL 15
- Task Queue: Celery + Redis
- Deployment: Docker + Kubernetes (or serverless AWS Lambda for tasks)
```

If a playbook matches all constraints for a context, **cite it directly and mark `status: confirmed`**. No checkpoint needed, no second-guessing.

### Step 3: No Fit / Conflict

If no playbook matches or a conflict exists (e.g., playbook says "relational DB" but detailed-design specifies "event-sourced"), present 2–3 full-stack options:

Each option should include:
- **Tech stack:** Frontend, backend runtime, database, message broker (if needed)
- **Constraints it satisfies:** Which data/API/security constraints this option meets
- **Constraints it violates (if any):** Any conflicts or workarounds needed
- **Tradeoffs (relevant ones only):** Familiarity (is the team experienced?), ecosystem (third-party libraries?), cost (license, hosting), hiring pool (can you hire for this stack?)

**Example (pending options for Analytics context):**

**Option 1: DuckDB + Python**
- Stack: Python 3.11 + DuckDB (embedded) + Parquet files (from PostgreSQL exports)
- Satisfies: Read-only analytical queries, <5s latency for up to 100M rows
- Violates: Not web-accessible; requires Python knowledge for queries
- Tradeoffs: Ecosystem (DuckDB ecosystem growing, not mature); cost (free, zero ops); hiring (hard to find DuckDB experts)

**Option 2: Redshift + Python SDK**
- Stack: AWS Redshift (data warehouse) + Python Boto3 SDK + async exports
- Satisfies: Large-scale analytics, SQL standard, <5s queries on 100M+ rows
- Violates: AWS vendor lock-in; not suitable for real-time OLTP
- Tradeoffs: Ecosystem (mature, AWS integrations); cost (high for small datasets); hiring (SQL expertise common, AWS expertise less so)

**Option 3: BigQuery + Python SDK**
- Stack: Google BigQuery (serverless warehouse) + Python google-cloud-bigquery + async exports
- Satisfies: Unlimited scale, SQL standard, serverless (no ops)
- Violates: Google vendor lock-in; coldstart latency on first query
- Tradeoffs: Ecosystem (mature, Google integrations); cost (pay-per-query, can be expensive); hiring (SQL expertise common, BigQuery expertise less common)

Then set `status: pending` and wait for your selection.

### Step 4: Wait for Selection, Update to Confirmed

Present all contexts with `pending` status. You review tradeoffs and pick one option per pending context (or suggest a different stack if none fit your needs). Once you select:

- Update `Stack` cell with the chosen option
- Update `Source/Rationale` to explain why you chose it (e.g., "Selected Option 1: DuckDB because team knows Python and zero-ops is critical")
- Update `Status` to `confirmed`
- **Delete the alternatives** from the table (only the chosen stack remains)

Once all contexts are confirmed, the deliverable is valid.

## When to Use

Invoke this skill when:

- You have a completed detailed design with all bounded contexts, patterns, data architecture, and security model defined
- You need to select concrete technologies (frontend to database) per context
- You want a catalog-first approach (apply proven playbooks, minimize reinvention)
- You're ready to hand off to implementation teams with clear tech choices locked in

**Do NOT use this skill for:**

- Incomplete detailed design (missing constraints from earlier phases)
- Design pattern selection or data architecture decisions (earlier phase)
- Test/deployment/CI-CD strategy (separate concern)
- Implementation details (code structure, build setup — those come after tech stack is chosen)

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes (symlinks)
./install.sh --skill tech-stack

# Install via file copy
./install.sh --skill tech-stack --mode copy

# Install to a specific runtime
./install.sh --skill tech-stack --target claude

# Force-reinstall
./install.sh --skill tech-stack --force

# Full reinstall via copy
./install.sh --skill tech-stack --force --mode copy
```

For general installation details and troubleshooting, see the [**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README.

### Invocation

Use natural language or a slash command:

```text
/tech-stack Select technologies for each bounded context

choose the tech stack per context from catalog playbooks

/tech-stack We have detailed design; select technologies per context

tech stack selection
```

The skill reads the detailed design and produces `tech-stack.md` with all contexts (some confirmed via playbooks, others at pending status awaiting your selection).

## Files

- **SKILL.md** — Persona directives and 4-step execution protocol
- **README.md** — This file; user-facing reference documentation
- **stacks/*.md** — Catalog playbooks (e.g., `stacks/python-fastapi-postgres.md`)

## Out of Scope

- **Design patterns and bounded contexts** — Those are earlier phase (detailed-design)
- **Test/deployment/CI-CD strategies** — Separate concern, addressed after tech stack is locked
- **Implementation details** — Code structure, build configuration, package choices (Phase 6+)
- **Ranking off-catalog options** — The skill states tradeoffs but doesn't rank them; you choose

## Pipeline Context

This skill is **Phase 5** of the complete BRD → Requirements → Architecture → Design → Stack → Implementation pipeline:

- **Phase 1 (brd):** Product concept → BRD
- **Phase 2 (req-nfr-analysis):** BRD → normalized requirements
- **Phase 3 (architecture-decisions):** Normalized requirements → confirmed architecture
- **Phase 4 (detailed-design):** Confirmed architecture → detailed design (bounded contexts, patterns, data, APIs, security)
- **Phase 5 (tech-stack - this skill):** Detailed design → technology stack choices per context
- **Phase 6 (future):** Tech stack → implementation plan, code structure, deployment architecture

Each phase's output feeds into the next. Tech stacks are locked to detailed design specifications.

## Playbook Catalog Structure

The `stacks/` directory contains vetted full-stack playbooks. Each playbook:

1. **Names the stack** (e.g., "Python + FastAPI + PostgreSQL + Celery")
2. **States what constraints it fits** (data model, API protocol, patterns, security)
3. **States what it does NOT fit** (event sourcing? Real-time WebSocket?)
4. **Provides the full stack** (frontend, backend runtime, database, message broker, deployment pattern)
5. **Cites trade-offs** (ecosystem maturity, hiring, cost, vendor lock-in)
6. **Links to example projects** (optional: references to open-source projects using this stack)

Playbooks are vetted once and reused across many projects — they are the "proven practices" the skill applies.

## Version History

**v1.0** (2026-09-02):

- Initial skill definition: 4-step process, catalog-first approach, pending checkpoint for no-fit cases
- Frontmatter: `name`, `description`, `license`, `compatibility` (no `models`, `scopes`, `context_optimization`)
- Enforces that all contexts must be confirmed before deliverable is valid
- No unilateral off-catalog picks; tradeoff options presented at pending status

---

## Questions?

For details on how constraints drive tech selection or how playbooks are structured, see **SKILL.md**. For how detailed design constraints flow from architecture decisions, see the [`detailed-design` README](../detailed-design/README.md) (Phase 4). For upstream NFR definitions, see the [`req-nfr-analysis` README](../req-nfr-analysis/README.md) (Phase 2).
