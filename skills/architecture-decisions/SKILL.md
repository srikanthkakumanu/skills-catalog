---
name: architecture-decisions
description: Decides architecture style and agentic-AI fitness from a normalized requirement set and NFR analysis, in compact ADR format, gated behind a mandatory confirm/pending checkpoint. "Not applicable" is a valid agentic-AI verdict. Does not select stacks or component-level patterns.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
metadata:
  tier_policy: "reasoning tier for both ADRs (style and agentic-AI fitness); lightweight tier only for status bookkeeping after confirmation"
---
# Architecture Decision Skill

## Directives
1. Two decisions only: architecture style; agentic-AI fitness, per capability.
2. ADR format always: Decision | Why | Alternative(s) | Status (pending/confirmed).
3. No forced verdict — "not applicable" is correct when no real agentic capability exists, even if the BRD's title implies one; name the gap when it does.
4. Deferred / Not-evidenced NFRs don't drive the style decision.
5. An unresolved contradiction or unsupported claim in upstream Open Questions blocks the decision it affects — surface it, don't pick a side.
6. Stop at the checkpoint. Nothing is final until the user confirms; update status in place.
7. **Cost control** — both ADRs are judgment calls end to end; keep them on the reasoning tier. Only recording the confirmed/pending status after the user responds is lightweight.
8. **Context** — read the Hard-Constraint NFR rows and BRD scope/success criteria once; don't re-read Deferred/Not-evidenced rows, they don't factor into either decision.

## Process
1. Read the NFR table's Hard-Constraint rows plus the BRD's scope/success criteria. Ignore Deferred/NE rows.
2. **Style ADR** *(reasoning)* — monolith / modular monolith / microservices / event-driven / serverless, or a named split. Checklist: independent scaling needs? single team/deploy cadence? explicit "avoid over-engineering" signal? bursty/event-triggered work?
3. **Agentic-AI ADR** *(reasoning)* — evaluate per capability that's explicitly automated/AI in the FRs, or flagged upstream as an unsupported claim. Checklist: multi-step autonomous reasoning? tolerant of non-determinism? needs a human-confirmation gate? If none qualify: "Not applicable — no agentic capability in confirmed requirements," naming the gap if the BRD implied otherwise.
4. Present both ADRs at `status: pending`. Wait for confirmation. Update to `confirmed` (or revise and re-present) per the response *(lightweight bookkeeping once a decision is made)*.

## Output: `architecture-decisions.md`
- `## Architecture Style` — ADR(s)
- `## Agentic-AI Fitness` — ADR(s), including the "not applicable" case when it applies

Each ADR: **Decision** / **Why** / **Alternatives** / **Status**

> **Consumer tier hint:** any ADR at `status: confirmed` is a lightweight-lookup fact for downstream skills — read the Decision line, no re-litigating. A `status: pending` ADR must not be consumed at all; block and route back rather than reasoning about what it might become.

## Out of Scope
- Tech stack, component design, patterns, data/API/security detail (later phases).
- Test/deploy plans.
