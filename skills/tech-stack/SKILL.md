---
name: tech-stack
description: Selects a full-stack technology choice per bounded context from detailed-design.md, citing a catalog playbook where one fits or presenting tradeoff options and stopping for confirmation when it doesn't. Never decides an off-catalog stack unilaterally.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
metadata:
  tier_policy: "lightweight tier for constraint listing and a clean catalog match; reasoning tier only when no catalog entry fits and tradeoff options must be weighed"
---
# Tech Stack Skill

## Directives
1. One decision per bounded context — different contexts may land on different stacks; that's expected, not inconsistent.
2. Catalog match first — cite the playbook directly, no re-derivation, no checkpoint needed.
3. No catalog fit → present 2–3 tradeoff options, `status: pending`, stop. Never pick unilaterally.
4. A stack must satisfy every data/API/security constraint `detailed-design.md` set for that context — disqualify before weighing tradeoffs.
5. Deliverable isn't valid while any context is still `pending`.
6. **Cost control** — listing constraints and citing a clean catalog match is lightweight lookup; escalate to reasoning tier only when the catalog doesn't fit and tradeoffs must actually be weighed.
7. **Context** — read `detailed-design.md` once per context; don't re-read the whole file per constraint field.

## Process
1. Per context, list binding constraints (data model, API protocol, security, any NFR performance figure) *(lightweight)*.
2. **Catalog check** *(lightweight if a clean match exists)* — if a `stacks/*.md` playbook fits with no conflict, cite it: `status: confirmed`.
3. **No fit / conflict** *(reasoning)* — 2–3 full-stack options (frontend to database), one-line tradeoff each (familiarity, ecosystem, cost, hiring — only the relevant ones), no ranking beyond stating tradeoffs: `status: pending`.
4. Present pending contexts, wait for selection, update to `confirmed` with the chosen option retained (not the alternatives) *(lightweight bookkeeping)*.

## Output: `tech-stack.md`
Table: Context | Stack | Source/Rationale | Status. Flag any context left `under-constrained` by missing upstream detail.

> **Consumer tier hint:** `confirmed` rows are lightweight-lookup for the PRD assembler. `pending` or `under-constrained` rows must route to Open Items, never be treated as decided.

## Out of Scope
Design patterns and bounded contexts (earlier phase). Test/deploy plans. Ranking off-catalog options beyond stating tradeoffs.
