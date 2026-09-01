---
name: detailed-design
description: Turns confirmed architecture decisions into bounded contexts, microservice/design pattern selection, data architecture, API contracts, and a security model. Refuses to run against unconfirmed ADRs; traces every hard-constraint NFR to a design decision or flags it unaddressed.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# Detailed Design Skill

## Directives
1. Never run against an `architecture-decisions.md` with any `status: pending` ADR — block, route back.
2. Smallest sufficient pattern set — every pattern traces to a named coordination problem, not general practice.
3. Bounded contexts follow the confirmed style ADR's own split; don't re-derive from scratch.
4. Any human-in-loop gate from the agentic-AI ADR must show up as a concrete API/permission boundary, not a narrative note.
5. Every Hard-Constraint NFR maps to a design decision, or is flagged unaddressed.

## Process
1. **Bounded contexts** — derive from the style ADR; name + one-line responsibility each.
2. **Patterns** — one microservice/integration pattern plus at most 1–2 design patterns per non-trivial context, each with the specific problem it solves. No named problem → no pattern.
3. **Data architecture** — DB-per-context vs shared, driven by Hard-Constraint NFRs; event sourcing/CQRS only where an explicit audit/replay/read-write-mismatch need exists.
4. **API contracts** — one line per context boundary: protocol + versioning. Human-in-loop gates shown as a separate endpoint/step, not folded into the main path.
5. **Security model** — authn/authz per context; agentic capability's autonomous-vs-gated actions stated explicitly, matching the API contract exactly.
6. **NFR traceability** — walk every Hard-Constraint NFR, name the design decision addressing it or flag unaddressed.

## Output: `detailed-design.md`
`## Bounded Contexts` · `## Pattern Selection` · `## Data Architecture` · `## API Contracts` · `## Security Model` · `## NFR Traceability` (table: NFR | Addressed by / Unaddressed)

## Out of Scope
Tech stack selection. Re-deciding architecture style or agentic-AI fitness. Test/deploy plans.
