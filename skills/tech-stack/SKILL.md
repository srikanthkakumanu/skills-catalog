
---
name: tech-stack
description: Selects a full-stack technology choice per bounded context, decomposed by layer, against a standing defaults policy (Java/Spring Boot for microservice layers, Python/uv for AI/agentic layers, common infra, pattern-based messaging). Shows a per-layer comparison table (decision, why, cross-stack alternatives), batch-confirms policy-backed rows, and asks individually for anything the policy doesn't resolve.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
metadata:
  tier_policy: "lightweight tier for policy-matched rows (stacks/defaults.md lookup) and batch confirmation; reasoning tier only for rows the policy doesn't resolve — database choice, an ambiguous messaging pattern, or true off-catalog"
---
# Tech Stack Skill

## Directives

1. Decompose each bounded context into its actual layers (microservice/business-logic, AI/agentic, data, messaging, common infra) — only the ones present, not a fixed checklist applied blindly.
2. Check `stacks/defaults.md` first, per layer. A policy match is lookup, not a fresh decision — cite it directly.
3. Always show the full per-context comparison table before asking anything: Layer/Component | Decision (brief why) | Alternatives (Python / Java / DB, common-across-stacks flagged).
4. Confirmation is two-speed: every policy-backed row in a context is batch-confirmed in one question ("confirm these, or override any row"). Any row — or sub-decision within a row — the policy doesn't resolve is asked individually, one at a time: database choice, an ambiguous messaging pattern, true off-catalog, and AI/agentic framework composition (runtime/build tool is policy-backed; which of LangChain/LangGraph/OpenAI SDK/Claude SDK applies is not).
5. A stack must satisfy every data/API/security constraint `detailed-design.md` set for that context — disqualify before presenting alternatives, not after.
6. Deliverable isn't valid while any row is still `status: pending`.
7. **Cost control** — policy lookups and batch confirmation stay lightweight. Escalate to reasoning tier only for the rows directive 4 calls out individually.
8. **Context** — read `detailed-design.md` and `stacks/defaults.md` once per context; don't re-read either per row.

## Process

1. **Decompose** *(lightweight)* — split the context into its present layers.
2. **Policy match** *(lightweight)* — microservice/business-logic layer → Java/Spring Boot 4.x/Gradle (Groovy DSL); AI/agentic layer → Python/uv runtime settled, framework composition deferred to step 6; common-infra rows → Docker, Kubernetes, GitHub Actions, Redis.
3. **Messaging** *(lightweight if the pattern is clear from `detailed-design.md`; reasoning if ambiguous)* — event-streaming/log-style/event-sourcing → Kafka; task/work-queue → RabbitMQ; unclear → mark for individual ask, don't assume.
4. **Database** *(lightweight if a `stacks/*.md` catalog entry matches the context's data-architecture constraints with no conflict; reasoning otherwise)* — matched: cite it. Unmatched: 2–3 full options with one-line tradeoffs each, marked for individual ask.
5. **Build the table** *(lightweight)* — one row per layer, `status: pending` throughout, for the whole context at once.
6. **Ask** — batch-confirm all policy-backed rows in one question per context. Then ask individually, one row at a time, for each row directive 4 flagged (database, ambiguous messaging, off-catalog, AI framework composition — present LangChain/LangGraph/OpenAI SDK/Claude SDK with a one-line note on when each fits, then ask; LangSmith is a separate additive question, not part of that choice).
7. **Update status** *(lightweight)* — `confirmed` per response, chosen option retained (not the alternatives).

## Output: `tech-stack.md`

One table per bounded context: Layer/Component | Decision (why) | Alternatives (Python/Java/DB, common flagged) | Source (`defaults.md` / `detailed-design`-derived / off-catalog, user-selected) | Status.

> **Consumer tier hint:** any row at `status: confirmed` is lightweight-lookup for the PRD assembler, regardless of how it was resolved. A `status: pending` row must not be consumed — block and route back rather than assuming a default.

## Out of Scope

Design patterns and bounded contexts (earlier phase). Test/deploy plans. Ranking off-catalog options beyond stating tradeoffs. Re-deciding a messaging or database pattern that `detailed-design.md` already settled.
