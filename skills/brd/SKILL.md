---
name: brd
description: Produces a compact Business Requirements Document — domain, personas, use cases with happy/negative paths and acceptance criteria, and in/out-of-scope boundaries — with a mandatory self-check for unsupported framing claims, contradictions, and orphaned scope items. Pure functional scope: WHAT and WHO, never HOW.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
metadata:
  tier_policy: "reasoning tier for drafting (steps 1-4) and self-check (step 5); lightweight tier for final template formatting only"
---
# BRD Skill

## Directives
1. Functional only — no tech/architecture leakage.
2. Every in-scope item maps to ≥1 use case, or it's flagged — never asserted as covered without checking.
3. Every capability named in the title/domain (e.g. "AI," "automated," "integrated") maps to ≥1 use case, or it's flagged.
4. No two requirements may silently contradict; if they do, flag both.
5. Lean by default: 3-step happy paths, 1-line exceptions, 3-line Gherkin max.
6. **Cost control** — drafting and self-check require reasoning-tier judgment; don't downgrade them. Only the final table/section formatting is lightweight-tier work.
7. **Context** — work from the current raw concept/notes; don't carry forward a superseded draft in full once revised, keep only the latest version.

## Process
1. **Domain** *(reasoning)* — one name, 2–4 modules.
2. **Personas** *(reasoning)* — table: ID, name, role, top JTBD, top pain point. 1–2 personas unless the concept clearly needs more.
3. **Use cases** *(reasoning)* — one per persona-critical flow: ID, actor, happy path (≤3 steps), exceptions (1 line: trigger → behavior), acceptance criteria (Gherkin, ≤3 lines).
4. **Scope** *(reasoning)* — table: module | in-scope | out-of-scope | 1-line reason.
5. **Self-check** *(reasoning, mandatory, before output)*:
   - *Framing:* title/domain implies a capability no use case delivers? → flag.
   - *Contradiction:* any two flows/rules conflict? → flag both, name each.
   - *Coverage:* every in-scope row traces to a use case? → flag orphans.
6. **Format output** *(lightweight)* — lay out the sections below; no new judgment at this step.

## Output: `BRD.md`
- `## Domain` — name + modules
- `## Personas` — table
- `## Use Cases` — per use case, as above
- `## Scope` — in/out table
- `## Self-Check Findings` — table: Type | Description | Ref. Always present; "None" is a valid result.

> **Consumer tier hint:** downstream skills can lightweight-lookup Domain/Personas/Scope tables directly. Self-Check Findings needs reasoning-tier attention if non-empty — an unresolved contradiction or unsupported claim here should block, not pass through, the next phase's judgment calls.

## Out of Scope
- Architecture, tech stack, patterns, test/deploy plans.
- Resolving a self-check finding by itself — flag it, don't fix it silently.
