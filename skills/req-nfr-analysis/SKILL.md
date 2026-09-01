---
name: req-nfr-analysis
description: Normalizes a BRD's functional requirements and tags NFRs across a compact 10-category taxonomy, flags inferred NFRs and any contradictions or unsupported claims the BRD's self-check may have missed, and prioritizes each as hard-constraint or nice-to-have. Consumes BRD.md, produces req-nfr-analysis.md.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# Req & NFR Analysis Skill

## Directives

1. Functional requirements stay functional — split out any NFR language mixed into a requirement.
2. Tag all 10 NFR categories every time, even "Not evidenced" — never omit a row.
3. Inferred ≠ stated. Always mark source; cite the trigger in ≤10 words.
4. If `BRD.md`'s Self-Check Findings section is missing or looks incomplete, re-run that check here — don't assume it was done.
5. Unclear priority → Open Question. Never guessed.

## NFR Taxonomy (10 categories)

Performance & Scalability · Reliability & Recovery · Security · Compliance & Data Governance · Usability & Accessibility · Maintainability & Portability · Observability · Transparency/Explainability (incl. AI) · Cost · Other

## Process

1. **Extract FRs** — table: ID | Requirement | Source (use case ref).
2. **Tag NFRs** — table: # | Category | Status (E/I/NE) | Evidence (≤10 words) | Priority (HC/NTH/—). All 10 rows, always.
3. **Structural check** — contradiction / unsupported framing claim / orphaned scope row. Reuse BRD's findings if present; otherwise derive directly. Table: Type | Description | Ref.
4. **Open Questions** — only unresolved items, one line each, tied to a category or finding.

## Output: `req-nfr-analysis.md`

- `## Functional Requirements` — table
- `## NFR Table` — 10 rows, always
- `## Structural Findings` — table; "None" is valid
- `## Open Questions` — list, may be empty

## Out of Scope

- Architecture, stack, pattern, or design decisions (later phase).
- Inventing thresholds or resolving structural findings unilaterally.
