
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

1. Decompose each bounded context into its actual layers (microservice/business-logic, AI/agentic, data, messaging, common infra) — only the ones present, not a fixed checklist applied blindly. A frontend/presentation layer is evidence-gated, not default-applied: only decompose it in when the context's upstream requirements (BRD personas/use-cases, or `detailed-design.md`'s API Contracts naming a browser/UI-facing consumer) actually evidence a UI need. When that evidence is genuinely ambiguous — neither a clear UI signal nor a clear API-only/service-to-service signal — stop and ask the user directly per Process step 2 (Frontend evidence check); never silently include or omit the layer.
2. Check `stacks/defaults.md` first, per layer. A policy match is lookup, not a fresh decision — cite it directly.
3. Always show the full per-context comparison table before asking anything: Layer/Component | Decision (brief why) | Alternatives (Python / Java / DB, common-across-stacks flagged).
4. Confirmation is two-speed: every policy-backed row in a context is batch-confirmed in one question ("confirm these, or override any row"). Any row — or sub-decision within a row — the policy doesn't resolve is asked individually, one at a time: database choice, an ambiguous messaging pattern, true off-catalog, AI/agentic framework composition (runtime/build tool is policy-backed; which of LangChain/LangGraph/OpenAI SDK/Claude SDK applies is not), and — per step 2 — the frontend/presentation layer's very inclusion for a context, asked before that context's table is built, the same never-assumed-either-way rule as an ambiguous messaging pattern.
5. A stack must satisfy every data/API/security constraint `detailed-design.md` set for that context — disqualify before presenting alternatives, not after.
6. Deliverable isn't valid while any row is still `status: pending`.
7. **Cost control** — policy lookups and batch confirmation stay lightweight. Escalate to reasoning tier only for the rows directive 4 calls out individually.
8. **Context** — read `detailed-design.md` and `stacks/defaults.md` once per context; don't re-read either per row.

## Process

1. **Decompose** *(lightweight)* — split the context into its present layers, including frontend/presentation only where evidenced; when ambiguous, flag for the individual ask in step 2 rather than guessing.
2. **Frontend evidence check** *(lightweight)* — before finalizing layer decomposition, scan `detailed-design.md`'s API Contracts and the originating `BRD.md` for a UI/browser-facing consumer signal (a named end-user persona, "web UI"/"dashboard"/"portal", or an API Contracts line describing a browser client rather than a service-to-service call).
   - **Clear signal present** → include frontend/presentation as a layer for that context; proceed to Policy match (step 3).
   - **Clear signal absent** (context is explicitly service-to-service, batch, or internal-API-only) → omit it, state why in one line.
   - **Ambiguous** → ask the user directly, one question per context, before building that context's table: *"This context's requirements don't clearly state whether `<context name>` needs a frontend/UI layer. Should I generate a frontend/presentation stack for it, or is this API/service-only?"* Do not proceed with that context's comparison table until answered — this mirrors Directive 6's "deliverable isn't valid while any row is `status: pending`," applied one level up, at the layer-existence question itself.
3. **Policy match** *(lightweight)* — microservice/business-logic layer → Java/Spring Boot 4.x/Gradle (Groovy DSL); AI/agentic layer → Python/uv runtime settled, framework composition deferred to step 7; frontend/presentation layer (once confirmed present at step 2) → Next.js 16.x / React 19 / TypeScript 5.9.x, see `frontend-nextjs-react-typescript.md`; common-infra rows → Docker, Kubernetes, GitHub Actions, Redis.
4. **Messaging** *(lightweight if the pattern is clear from `detailed-design.md`; reasoning if ambiguous)* — event-streaming/log-style/event-sourcing → Kafka; task/work-queue → RabbitMQ; unclear → mark for individual ask, don't assume.
5. **Database** *(lightweight if a `stacks/*.md` catalog entry matches the context's data-architecture constraints with no conflict; reasoning otherwise)* — matched: cite it. Unmatched: 2–3 full options with one-line tradeoffs each, marked for individual ask.
6. **Build the table** *(lightweight)* — one row per layer, `status: pending` throughout, for the whole context at once.
7. **Ask** — batch-confirm all policy-backed rows in one question per context. Then ask individually, one row at a time, for each row directive 4 flagged (database, ambiguous messaging, off-catalog, AI framework composition — present LangChain/LangGraph/OpenAI SDK/Claude SDK with a one-line note on when each fits, then ask; LangSmith is a separate additive question, not part of that choice; frontend layer inclusion is asked earlier, at step 2, not here).
8. **Update status** *(lightweight)* — `confirmed` per response, chosen option retained (not the alternatives).

## Output: `tech-stack.md`

One table per bounded context: Layer/Component | Decision (why) | Alternatives (Python/Java/DB, common flagged) | Source (`defaults.md` / `detailed-design`-derived / off-catalog, user-selected) | Status.

> **Consumer tier hint:** any row at `status: confirmed` is lightweight-lookup for the PRD assembler, regardless of how it was resolved. A `status: pending` row must not be consumed — block and route back rather than assuming a default.

## Out of Scope

Design patterns and bounded contexts (earlier phase). Test/deploy plans. Ranking off-catalog options beyond stating tradeoffs. Re-deciding a messaging or database pattern that `detailed-design.md` already settled.
