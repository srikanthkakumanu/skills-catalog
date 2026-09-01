---
name: brd
description: Produces a compact Business Requirements Document — domain, personas, use cases with happy/negative paths and acceptance criteria, and in/out-of-scope boundaries — with a mandatory self-check for unsupported framing claims, contradictions, and orphaned scope items. Pure functional scope: WHAT and WHO, never HOW.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# BRD Skill

## Directives
1. Functional only — no tech/architecture leakage.
2. Every in-scope item maps to ≥1 use case, or it's flagged — never asserted as covered without checking.
3. Every capability named in the title/domain (e.g. "AI," "automated," "integrated") maps to ≥1 use case, or it's flagged.
4. No two requirements may silently contradict; if they do, flag both.
5. Lean by default: 3-step happy paths, 1-line exceptions, 3-line Gherkin max.

## Process
1. **Domain** — one name, 2–4 modules.
2. **Personas** — table: ID, name, role, top JTBD, top pain point. 1–2 personas unless the concept clearly needs more.
3. **Use cases** — one per persona-critical flow: ID, actor, happy path (≤3 steps), exceptions (1 line: trigger → behavior), acceptance criteria (Gherkin, ≤3 lines).
4. **Scope** — table: module | in-scope | out-of-scope | 1-line reason.
5. **Self-check** (mandatory, before output):
   - *Framing:* title/domain implies a capability no use case delivers? → flag.
   - *Contradiction:* any two flows/rules conflict? → flag both, name each.
   - *Coverage:* every in-scope row traces to a use case? → flag orphans.

## Output: `BRD.md`
- `## Domain` — name + modules
- `## Personas` — table
- `## Use Cases` — per use case, as above
- `## Scope` — in/out table
- `## Self-Check Findings` — table: Type | Description | Ref. Always present; "None" is a valid result.

## Out of Scope
- Architecture, tech stack, patterns, test/deploy plans.
- Resolving a self-check finding by itself — flag it, don't fix it silently.
