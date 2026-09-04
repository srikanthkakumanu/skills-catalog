---
name: detailed-design
description: Turns confirmed architecture decisions into bounded contexts, microservice/design pattern selection, data architecture, API contracts, and a security model. Refuses to run against unconfirmed ADRs; traces every hard-constraint NFR to a design decision or flags it unaddressed.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
metadata:
  tier_policy: "lightweight tier for deriving context names and stating API protocol lines; reasoning tier for pattern selection, data architecture, security model, and NFR traceability"
---
# Detailed Design Skill

## Directives
1. Never run against an `architecture-decisions.md` with any `status: pending` ADR — block, route back.
2. Smallest sufficient pattern set — every pattern traces to a named coordination problem, not general practice.
3. Bounded contexts follow the confirmed style ADR's own split; don't re-derive from scratch.
4. Any human-in-loop gate from the agentic-AI ADR must show up as a concrete API/permission boundary, not a narrative note.
5. Every Hard-Constraint NFR maps to a design decision, or is flagged unaddressed.
6. **Cost control** — naming contexts directly from the ADR and stating a protocol/versioning line is lightweight lookup. Choosing patterns, data architecture, and the security model, plus the NFR traceability check, need reasoning-tier judgment.
7. **Context** — read `architecture-decisions.md` once to confirm status and pull the split; don't re-evaluate the style or fitness verdicts themselves.

## Process
1. **Bounded contexts** *(lightweight)* — derive from the style ADR; name + one-line responsibility each.
2. **Patterns** *(reasoning)* — one microservice/integration pattern plus at most 1–2 design patterns per non-trivial context, each with the specific problem it solves. No named problem → no pattern.
3. **Data architecture** *(reasoning)* — DB-per-context vs shared, driven by Hard-Constraint NFRs; event sourcing/CQRS only where an explicit audit/replay/read-write-mismatch need exists.
4. **API contracts** *(lightweight for the protocol/versioning line; reasoning for where a human-in-loop gate sits)* — one line per context boundary: protocol + versioning. Gates shown as a separate endpoint/step, not folded into the main path.
5. **Security model** *(reasoning)* — authn/authz per context; agentic capability's autonomous-vs-gated actions stated explicitly, matching the API contract exactly.
6. **NFR traceability** *(reasoning)* — walk every Hard-Constraint NFR, name the design decision addressing it or flag unaddressed.

## Output: `detailed-design.md`
`## Bounded Contexts` · `## Pattern Selection` · `## Data Architecture` · `## API Contracts` · `## Security Model` · `## NFR Traceability` (table: NFR | Addressed by / Unaddressed)

> **Consumer tier hint:** Bounded Contexts and API Contracts are lightweight-lookup for the tech-stack skill. Any "Unaddressed" row in NFR Traceability needs reasoning-tier attention — it's an open risk, not a settled design fact.

## Out of Scope
Tech stack selection. Re-deciding architecture style or agentic-AI fitness. Test/deploy plans.
