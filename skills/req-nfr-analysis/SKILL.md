
---
name: req-nfr-analysis
description: Normalizes a BRD's functional requirements and tags NFRs across a compact 10-category taxonomy, flags inferred NFRs and any contradictions or unsupported claims the BRD's self-check may have missed, asks the user its open questions directly, and integrates the rephrased answers into the relevant output sections. Consumes BRD.md, produces req-nfr-analysis.md.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
metadata:
  tier_policy: "lightweight tier for explicit-tag extraction, question presentation, and status bookkeeping; reasoning tier for inferred-NFR tagging, priority calls, the structural check, and answer evaluation/integration"
---
# Req & NFR Analysis Skill

## Directives

1. Functional requirements stay functional — split out any NFR language mixed into a requirement.
2. Tag all 10 NFR categories every time, even "Not evidenced" — never omit a row.
3. Inferred ≠ stated. Always mark source; cite the trigger in ≤10 words.
4. If `BRD.md`'s Self-Check Findings section is missing or looks incomplete, re-run that check here — don't assume it was done.
5. Every open question is asked to the user directly, in one batched round — never left silently unresolved when the user is available to answer.
6. An answer is rephrased into evidence-length prose (not pasted verbatim) and written into the specific section it resolves — the NFR row, the FR table, or the structural finding it addresses. A vague or partial answer stays an Open Question rather than being forced into a resolution.
7. **Cost control** — tagging Explicit/Not-evidenced rows and presenting questions is lightweight lookup. Inferred tagging, priority calls, the structural check, and evaluating/placing each answer need reasoning-tier judgment.
8. **Context** — read `BRD.md` once; work from its Self-Check Findings and use case table directly rather than re-deriving facts already stated there.

## NFR Taxonomy (10 categories)

Performance & Scalability · Reliability & Recovery · Security · Compliance & Data Governance · Usability & Accessibility · Maintainability & Portability · Observability · Transparency/Explainability (incl. AI) · Cost · Other

## Process

1. **Extract FRs** *(lightweight)* — table: ID | Requirement | Source (use case ref).
2. **Tag NFRs** *(lightweight for E/NE rows; reasoning for I rows and priority calls)* — table: # | Category | Status (E/I/NE) | Evidence (≤10 words) | Priority (HC/NTH/—). All 10 rows, always.
3. **Structural check** *(reasoning)* — contradiction / unsupported framing claim / orphaned scope row. Reuse BRD's findings if present; otherwise derive directly. Table: Type | Description | Ref.
4. **Ask** *(lightweight)* — batch every question from steps 2–3 into one round, put to the user directly. Don't drip-feed one at a time.
5. **Evaluate & integrate** *(reasoning)* — for each answer: rephrase to an evidence-length phrase (≤15 words, not verbatim); locate the exact row/section it resolves (NFR row → status `EC`, Evidence, re-applied Priority; FR table → new/amended row; Structural Finding → resolution note); write it there. Ambiguous or partial answers are left as Open Questions, unresolved.
6. **Open Questions** *(lightweight)* — only what step 5 left unresolved; may be empty.

## Output: `req-nfr-analysis.md`

- `## Functional Requirements` — table (includes any FR added or amended via user answers)
- `## NFR Table` — 10 rows, always; Status codes E/I/NE/EC (EC = Explicit, user-confirmed)
- `## Structural Findings` — table: Type | Description | Ref | Resolution (blank until answered)
- `## Open Questions` — only unresolved items; may be empty

> **Consumer tier hint:** rows tagged E, NE, or EC are lightweight-lookup for downstream skills — a user-confirmed answer is as settled as a stated one. Rows tagged I, and any Structural Finding with no Resolution, still need reasoning-tier attention downstream.

## Out of Scope

- Architecture, stack, pattern, or design decisions (later phase).
- Inventing thresholds or resolutions on this skill's own judgment — every resolution traces to an actual user answer.
