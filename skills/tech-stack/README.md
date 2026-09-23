# Tech Stack Skill

**Selects a full-stack technology choice per bounded context, decomposed by layer, against a standing defaults policy — citing a catalog playbook where one fits, or presenting tradeoff options when it doesn't — with a two-speed confirmation checkpoint before anything is final.**

A decisive skill for consuming detailed design specifications (from `/detailed-design`) and selecting technology stacks per bounded context, one layer at a time. `stacks/defaults.md` is checked first — most rows (microservice/business-logic → Java/Spring Boot, AI/agentic runtime → Python/uv, common infra) are a policy lookup, not a fresh decision. What the policy doesn't resolve (database choice, an ambiguous messaging pattern, AI framework composition, true off-catalog) is checked against the `stacks/*.md` playbook catalog next, then presented as tradeoff options if nothing fits. Policy-backed rows are batch-confirmed in one question; everything else is asked individually.

## Overview

This skill takes a completed `detailed-design.md` (with bounded contexts, patterns, data architecture, API contracts, and security model all defined) and produces `tech-stack.md` — a reference document that selects concrete technologies per context, decomposed by layer (microservice/business-logic, AI/agentic, data, messaging, common infra — only the layers actually present in a given context). For each layer: check `stacks/defaults.md` first — a policy match is a lookup, cited directly, no fresh decision. What the policy doesn't resolve (a database choice, an ambiguous messaging pattern, AI framework composition, or true off-catalog) is checked against the `stacks/*.md` playbook catalog, then presented as 2-3 tradeoff options if no playbook fits either. Every row starts `pending`; policy-backed rows are batch-confirmed together in one question per context, everything else is asked individually, one row at a time.

**Design principle:** Different contexts — and different layers within the same context — get different stacks. That's not inconsistent; it's expected.

**Output principle:** `tech-stack.md` cites, it never copies. A playbook's implementation detail belongs to the `implementation-guide` skill (Phase 7), fetched later by whatever consumes `PRD.md` — never frozen into it here. See Directive 5 in `SKILL.md`.

## What It Does

The skill executes seven steps per bounded context:

1. **Decompose** — Split the context into its present layers only (microservice/business-logic, AI/agentic, data, messaging, common infra) — not a fixed checklist applied blindly.
2. **Policy match** — Check `stacks/defaults.md` per layer: microservice/business-logic → Java/Spring Boot 4.x/Gradle (Groovy DSL); AI/agentic → Python/uv (framework composition deferred to step 6); common-infra → Docker, Kubernetes, GitHub Actions, Redis.
3. **Messaging** — Pattern-based against `detailed-design.md`: event-streaming/log-style/event-sourcing → Kafka; task/work-queue → RabbitMQ; unclear → flag for individual ask.
4. **Database** — Check `stacks/*.md` for a matching catalog entry against the context's data-architecture constraints; matched → cite it; unmatched → 2-3 tradeoff options, flagged for individual ask.
5. **Build the table** — One row per layer, `status: pending` throughout, for the whole context at once.
6. **Ask** — Batch-confirm every policy-backed row in one question per context ("confirm these, or override any row"). Then ask individually, one row at a time, for anything the policy didn't resolve.
7. **Update status** — `confirmed` per response, chosen option retained (alternatives discarded).

Output is always `tech-stack.md` with one table per bounded context. No row can remain `pending`; the deliverable is only valid when all are confirmed.

## Key Design Principles

- **Layer decomposition, not one decision per context** — A context's microservice layer, AI layer, data layer, and messaging layer are each their own row, decided independently.
- **Policy first** — `stacks/defaults.md` resolves most rows as a lookup, not a fresh decision. Cite it directly.
- **Catalog match second** — For what the policy doesn't resolve (database, messaging pattern, AI framework), check `stacks/*.md` before presenting tradeoffs.
- **Cite, never copy** — The rationale cell states the policy or playbook and the constraint that drove the match, in ≤2 lines. Code, config, and implementation detail belong to `implementation-guide` (Phase 7), not here.
- **Two-speed confirmation** — Policy-backed rows are batch-confirmed together; anything the policy doesn't resolve is asked individually, one row at a time.
- **No unilateral off-catalog picks** — If no policy or playbook fits, present tradeoff options and stop. Never decide an off-catalog stack alone.
- **Constraints drive disqualification** — A stack must satisfy every data/API/security constraint detailed-design set. Disqualify before weighing tradeoffs.
- **All rows confirmed before valid** — The deliverable isn't finished while any row is still `pending`. Explicit selection required.

## Input

A completed detailed design with all bounded contexts specified:

- **detailed-design.md** — Bounded contexts (name + responsibility), data architecture (per-context DBs? shared? event sourcing?), API contracts (protocol, versioning), security model (authn/authz per context)
- **req-nfr-analysis.md** — Hard-constraint NFRs (performance latency, scalability throughput, compliance needs)
- **architecture-decisions.md** — Architecture style ADR and Agentic-AI fitness ADR, both `status: confirmed`. Several playbooks (`springboot4-modulith.md`, `python-ai-agentic.md`, `springboot4-ai-mcp.md`) are gated directly on these verdicts — read them before matching.
- **stacks/defaults.md** — The standing policy: layer → default stack. Checked first, per layer, before any catalog lookup.
- **stacks/*.md playbooks** — This catalog's vetted playbooks (see `stacks/INDEX.md` for the full matrix): `springboot4-webmvc-jpa-postgres.md` (default, synchronous/relational), `springboot4-webflux-reactive.md`, `springboot4-event-driven-kafka.md`, `springboot4-batch.md`, `springboot4-gateway.md`, `springboot4-modulith.md`, `python-ai-agentic.md` (default AI/agentic layer — LangChain/LangGraph, OpenAI SDK/Claude SDK, MCP Python SDK), `springboot4-ai-mcp.md` (rare fallback — only when deliberately hosting MCP/LLM inside an existing Spring Boot service), plus `java-baseline.md` (Java 27, every Spring Boot playbook's shared prerequisite)

Contexts must have clear data/API/security constraints. If a context is under-constrained (missing detail from earlier phases), flag it as such.

## Output: `tech-stack.md`

```markdown
# Technology Stack Decisions: [System Name]

## Order Management

| Layer/Component | Decision (why) | Alternatives | Source | Status |
|---|---|---|---|---|
| Microservice / business-logic | Java 27 · Boot 4.1 · Spring MVC · Spring Data JPA | Policy default | `stacks/defaults.md` | Confirmed |
| Data | PostgreSQL · Flyway · UUID IDs | — | `stacks/springboot4-webmvc-jpa-postgres.md` — relational + ACID per Reliability HC; UUID IDs (Performance HC: batch writes) | Confirmed |
| Common infra | Docker · Kubernetes · GitHub Actions · Redis | Policy default | `stacks/defaults.md` | Confirmed |

## Order Events

| Layer/Component | Decision (why) | Alternatives | Source | Status |
|---|---|---|---|---|
| Messaging | Kafka · Spring Cloud Stream | RabbitMQ (task-queue pattern, doesn't fit here) | `stacks/springboot4-event-driven-kafka.md` — cross-context coordination + audit trail (Compliance HC: replay) | Confirmed |

## Support Agent

| Layer/Component | Decision (why) | Alternatives | Source | Status |
|---|---|---|---|---|
| AI / agentic (runtime) | Python (uv) | — | `stacks/defaults.md` (policy) | Confirmed |
| AI / agentic (framework) | LangGraph (multi-step tool-calling agent) | LangChain (simpler chain, doesn't fit this capability); direct SDK call (no orchestration need here) | `stacks/python-ai-agentic.md` — Agentic-AI ADR confirmed tool-calling capability for this context | Confirmed |
| AI / agentic (MCP exposure) | MCP Python SDK · Streamable HTTP | — | `stacks/python-ai-agentic.md` | Confirmed |

**All rows confirmed. Deliverable valid.**

---

## Alternative Tradeoff Example (Pending Status)

Assume a new context **Analytics** with constraints:
- Data: read-only queries over order history (large dataset, 50M+ rows)
- API: async batch exports (not HTTP sync)
- Performance HC: query latency <5 seconds (analytical, not user-facing)
- No `stacks/` playbook fits an analytical/columnar workload — present options at pending:

| Layer/Component | Decision (why) | Alternatives | Source | Status |
|---|---|---|---|---|
| Data | *[Pending]* | **Option 1:** ClickHouse + a thin Spring Boot query service. Pro: purpose-built for this query shape; Con: new operational surface, no catalog playbook to fall back on. <br> **Option 2:** PostgreSQL read replica + materialized views (`springboot4-webmvc-jpa-postgres.md` extended). Pro: no new infra, team already knows it; Con: won't hold at 50M+ rows with sub-5s latency. <br> **Option 3:** Managed warehouse (Redshift/BigQuery) + Spring Boot as the orchestration layer. Pro: scales without ops burden; Con: vendor lock-in, cost at this data volume. | No playbook matches analytical + async export combination | Pending |

(After your selection, status updates to `confirmed` with the chosen option — and the rationale cell still stays at ≤2 lines, per Directive 5.)
```

Table structure:
- **Layer/Component**: The decomposed layer within the bounded context (microservice/business-logic, AI/agentic, data, messaging, common infra)
- **Decision (why)**: The chosen stack plus a brief driving reason, or `[Pending]` if awaiting selection
- **Alternatives**: Cross-stack options considered and why they didn't win, or full tradeoff options with pros/cons when pending
- **Source**: `stacks/defaults.md` (policy lookup), a `stacks/*.md` playbook path, or `off-catalog, user-selected`
- **Status**: `confirmed` (policy/playbook match or you selected) or `pending` (awaiting your selection)

Every row must be confirmed before the document is valid.

## How It Works

### Step 1: Decompose

For each bounded context from detailed-design, split it into the layers actually present — not a fixed checklist applied blindly:

- **Microservice / business-logic** — present whenever the context exposes an API or holds domain logic
- **AI / agentic** — present only if the context has a confirmed agentic-AI capability (per `architecture-decisions.md`)
- **Data** — present whenever the context owns persistent state
- **Messaging** — present whenever the context integrates async with another context
- **Common infra** — present in every context (deployment, CI/CD, caching)

### Step 2: Policy Match

Check `stacks/defaults.md` per layer:

- Microservice/business-logic → Java, Spring Boot 4.x, Gradle (Groovy DSL) — see `java-baseline.md` for the Java 27 requirement
- AI/agentic (runtime) → Python, uv — framework composition (LangChain/LangGraph/OpenAI SDK/Claude SDK) is not policy-resolved, deferred to Step 6
- Common infra → Docker, Kubernetes, GitHub Actions, Redis

A policy match is a lookup — cite `stacks/defaults.md` directly, no re-derivation. It still needs confirming in Step 6, just batched rather than asked individually.

### Step 3: Messaging

Check `detailed-design.md` for the integration pattern:

- High-throughput event-streaming / log-style / event-sourcing → Kafka
- Task/work-queue (job dispatch, retry/dead-letter, point-to-point async) → RabbitMQ
- Pattern unclear → don't assume; flag for an individual ask in Step 6

### Step 4: Database

Check `stacks/*.md` for a playbook that matches the context's data-architecture constraints (start with `stacks/INDEX.md`'s constraint matrix, and check its "Disqualifiers worth checking" section — an Architecture Style or Agentic-AI ADR verdict can rule a playbook out before you open it). If matched, cite it directly. If not, present 2-3 full tradeoff options and flag for an individual ask.

**Playbook schema** (every `stacks/*.md` capability file follows this):

```markdown
# <Runtime> · <capability>

## Fits
- Data model / API protocol / concurrency / security constraints this playbook satisfies

## Does NOT fit
- The constraints or ADR verdicts that disqualify it — this is what makes the catalog check real

## Stack
| Component | Choice |
|---|---|
| Language / runtime | ... |
| ... | ... |

## Prerequisites
- Hard requirements

## Tradeoffs
- One or two lines, only where a genuine tradeoff exists

## Implementation detail
`implementation-guide` (Phase 7) — topic names only, never inlined content
```

### Step 5: Build the Table

One row per layer, all at `status: pending`, for the whole context at once — don't ask anything until the full per-context table is visible.

### Step 6: Ask (Two-Speed)

- **Batch:** every policy-backed row (Step 2 matches, unambiguous Step 3 matches) is confirmed together in one question: "confirm these, or override any row."
- **Individual:** anything the policy or catalog didn't resolve is asked one row at a time — database choice, an ambiguous messaging pattern, true off-catalog, and AI framework composition (present LangChain/LangGraph/OpenAI SDK/Claude SDK with a one-line note on when each fits; LangSmith is a separate, additive question, not a competing option).

### Step 7: Update Status

For each response:
- Update `Decision (why)` with the chosen option
- Update `Source` to the driving policy/playbook/off-catalog reason (≤2 lines)
- Update `Status` to `confirmed`
- **Delete the alternatives** from that row (only the chosen stack remains)

Once every row in every context is confirmed, the deliverable is valid.

## When to Use

Invoke this skill when:

- You have a completed detailed design with all bounded contexts, patterns, data architecture, and security model defined
- You need to select concrete technologies per context, per layer
- You want a policy-first, catalog-second approach (apply the standing defaults, fall back to proven playbooks, minimize reinvention)
- You're ready to hand off to implementation teams with clear tech choices locked in

**Do NOT use this skill for:**

- Incomplete detailed design (missing constraints from earlier phases)
- Design pattern selection or data architecture decisions (earlier phase)
- Test/deployment/CI-CD strategy (separate concern)
- Implementation details (entity mapping, migration scripts, security wiring) — that's `implementation-guide` (Phase 7), consumed after `PRD.md`, not here

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

The skill reads the detailed design and produces `tech-stack.md` with all rows (some confirmed via policy/playbook, others at pending status awaiting your selection).

## Files

- **SKILL.md** — Persona directives and 7-step layer-decomposition process
- **README.md** — This file; user-facing reference documentation
- **stacks/INDEX.md** — Constraint → playbook matrix; read this first
- **stacks/defaults.md** — Standing policy: layer → default stack, checked before any catalog lookup
- **stacks/java-baseline.md** — Java 27 baseline, inherited by every Spring Boot playbook
- **stacks/python-ai-agentic.md** — Default AI/agentic layer playbook (LangChain/LangGraph, OpenAI SDK/Claude SDK, MCP Python SDK)
- **stacks/springboot4-*.md** — The Spring Boot capability playbooks, including the rare `springboot4-ai-mcp.md` fallback (see `stacks/INDEX.md` for the full list and what disqualifies each one)

## Out of Scope

- **Design patterns and bounded contexts** — Those are earlier phase (detailed-design)
- **Test/deployment/CI-CD strategies** — Separate concern, addressed after tech stack is locked
- **Implementation details** — Code, config, entity mapping, migration scripts — owned by `implementation-guide` (Phase 7), never inlined here
- **Ranking off-catalog options** — The skill states tradeoffs but doesn't rank them; you choose

## Pipeline Context

This skill is **Phase 5** of the complete BRD → Requirements → Architecture → Design → Stack → Implementation pipeline:

- **Phase 1 (brd):** Product concept → BRD
- **Phase 2 (req-nfr-analysis):** BRD → normalized requirements
- **Phase 3 (architecture-decisions):** Normalized requirements → confirmed architecture
- **Phase 4 (detailed-design):** Confirmed architecture → detailed design (bounded contexts, patterns, data, APIs, security)
- **Phase 5 (tech-stack - this skill):** Detailed design → technology stack choices per context, per layer
- **Phase 6 (prd):** All five upstream artifacts → `PRD.md` — the single source of truth for decisions
- **Phase 7 (implementation-guide):** Runs *after* `PRD.md`, never before — resolves the topic names each playbook cites into project conventions and implementation detail. Not read by `tech-stack` or `prd`.

Each phase's output feeds into the next. Tech stacks are locked to detailed design specifications; implementation detail is resolved later, on demand, by whatever consumes `PRD.md` — never frozen into it upstream.

## Playbook Catalog Structure

`stacks/` contains this catalog's standing policy (`defaults.md`) plus its vetted capability playbooks — Spring Boot 4.x for microservice/business-logic layers, and `python-ai-agentic.md` for the AI/agentic layer (with `springboot4-ai-mcp.md` kept as a rare fallback for hosting MCP/LLM inside an existing Spring Boot service). Each playbook:

1. **States what it fits** (data model, API protocol, concurrency profile, security)
2. **States what it does NOT fit** — the part that makes the catalog check meaningful; several playbooks are gated directly on an `architecture-decisions.md` ADR verdict
3. **Gives the Stack** (backend, persistence, messaging, security — whatever the capability needs)
4. **Names Prerequisites** — hard requirements that would break the playbook if violated
5. **States Tradeoffs** — only where a genuine tradeoff exists, one or two lines
6. **Points to Implementation detail** — topic names in `implementation-guide` (Phase 7), never inlined content

Playbooks are vetted once and reused across many projects — they are this catalog's "proven practices." See `stacks/INDEX.md` for the full constraint matrix.

## Version History

**v1.2** (2026-09-20):

- Rewrote `SKILL.md`'s process from a flat per-context decision into layer decomposition (microservice/business-logic, AI/agentic, data, messaging, common infra), checked first against a new standing policy file, `stacks/defaults.md`
- Introduced two-speed confirmation: policy-backed rows are batch-confirmed together, anything the policy doesn't resolve is asked individually
- Output table shape changed from `Context | Stack | Source/Rationale | Status` to `Layer/Component | Decision (why) | Alternatives | Source | Status`
- Added `stacks/python-ai-agentic.md` as the default AI/agentic layer playbook (LangChain/LangGraph, OpenAI SDK/Claude SDK, MCP Python SDK, LangSmith) — the AI/agentic layer defaults to Python per `defaults.md`, so `springboot4-ai-mcp.md` was reframed as a rare fallback, used only when deliberately hosting MCP/LLM inside an existing Spring Boot service
- This README rewritten to match — the earlier "v1.1" description of a flat 4-step process was left stale after `SKILL.md`'s layer-decomposition rewrite; this entry brings the two back in sync

**v1.1** (2026-09-18):

- `stacks/` populated with seven real Spring Boot 4.x playbooks plus `INDEX.md` and `java-baseline.md` (Java 27); the original omnibus `SpringBoot-4.x.md` prototype fit every constraint and disqualified nothing, so it was split and superseded
- `SKILL.md` Directive 5 added: rationale cites the playbook by path, ≤2 lines, never copies implementation detail — that content moved to the new `implementation-guide` skill (Phase 7)
- Fixed a long-standing path mismatch: `SKILL.md`/`README.md` referenced `stacks/*.md` while the directory was named `refs/`, so the catalog check could never match

**v1.0** (2026-09-02):

- Initial skill definition: 4-step process, catalog-first approach, pending checkpoint for no-fit cases
- Frontmatter: `name`, `description`, `license`, `compatibility` (no `models`, `scopes`, `context_optimization`)
- Enforces that all contexts must be confirmed before deliverable is valid
- No unilateral off-catalog picks; tradeoff options presented at pending status

---

## Questions?

For details on how constraints drive tech selection or how playbooks are structured, see **SKILL.md** and **stacks/INDEX.md**. For how detailed design constraints flow from architecture decisions, see the [`detailed-design` README](../detailed-design/README.md) (Phase 4). For upstream NFR definitions, see the [`req-nfr-analysis` README](../req-nfr-analysis/README.md) (Phase 2). For implementation-level detail once a stack is confirmed, see the [`implementation-guide` README](../implementation-guide/README.md) (Phase 7).
