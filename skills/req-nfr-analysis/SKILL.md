---
name: req-nfr-analysis
description: Requirements analysis skill that normalizes functional or business requirements, extracts and tags every requirement across 19 NFR categories (18 named plus "Other"), flags inferred NFRs the BRD implies but never states, and prioritizes each NFR as hard constraint vs nice-to-have for downstream architecture/design phases. Consumes BRD output, produces requirements-to-architecture input with complete gap analysis and stakeholder questions.
license: Apache-2.0
compatibility: Antigravity 2.x, Claude Code, OpenAI Codex
models:
  reasoning_tier:
    gemini: gemini-2.5-pro / gemini-3.7-flash
    claude: claude-3-7-sonnet / claude-3-5-sonnet
    codex: gpt-4o / o3-mini
  lightweight_tier:
    gemini: gemini-2.5-flash / gemini-2.0-flash-lite
    claude: claude-3-5-haiku
    codex: gpt-4o-mini
context_optimization:
  progressive_loading: true
  chunked_synthesis: false
  subagent_delegation: false
  state_saving_split: false
scopes:
  supported: ["minimal", "standard", "thorough"]
  default: "minimal"
flags:
  ask_gaps:
    invocation: "--ask-gaps"
    default: false
    description: >
      When set, Step 4 gap questions are asked directly to the user in the conversation
      and answers are resolved into the NFR table (Section 2) instead of only being
      listed as Open Questions.
---
# Phase 1: Requirements & NFR Analysis

## Core Directives

1. **Pure Requirements Analysis** — No architecture or tech recommendations
2. **Five-Step Sequential Execution** — Steps 1–5 in order; none skipped or merged
3. **Complete NFR Coverage** — All 19 categories in every output, even "Not evidenced"
4. **Progressive Reference Loading** — Inline category names; reference taxonomy/patterns for details
5. **Scope Boundary Control** — Three scopes; see Scope Behavior Matrix below
6. **Gap Resolution** — `--ask-gaps` asks stakeholders and resolves into NFR table; omit for static questions

---

## Scope Behavior Matrix

| Scope | Step 2: Tagging | Step 3: Priority | Step 4: Gap Questions |
|---|---|---|---|
| **Minimal (default)** | Outside minimal essential set (one container per app/microservice, one DB, one AI agent per need) → `Deferred (DEF)` | Deferred rows: Priority `—` | Essential-set categories only; skip Deferred |
| **Standard** | All 19 resolve to E/I/NE; no deferral | All 19 prioritized | Applicable patterns only; no deferral concept |
| **Thorough** | All 19 resolve to E/I/NE; never `Deferred` | DR/Compliance/Security near-always Hard Constraint | Every I/NE category gets a question; surface cross-NFR dependencies |

---

## Overview

Analyzes completed BRDs to extract, normalize, and prioritize functional and non-functional requirements. Serves as the bridge between requirements definition and architecture/design phases. **Does not recommend architecture, patterns, or tech stacks.**

## When to Use

- BRD provided and needs normalization or NFR extraction
- User asks for "requirement analysis" or declares BRD "done"
- Incomplete BRD needs structured gap identification

## Execution Steps (Sequential—None Skipped or Merged)

### Step 1: Extract Functional Requirements

Walk systematically through use cases, acceptance criteria, and requirement rows.

**Rules:**
- One normalized imperative statement per requirement
- Format: "System shall X" with source reference (e.g., use case ID like UC-101, section reference, or BRD-provided identifier)
- Functional only—separate from NFR language (split "persist data with 99.95% durability" into functional requirement + NFR tag)

**Output:** Table: ID, Requirement, Source

### Step 2: Tag Every NFR Across 19 Categories

For every requirement, determine NFR classification across 18 named categories (see `references/nfr-taxonomy.md`) plus "Other/Uncategorized."

**Tags (Status column codes below; output uses short codes):**
- **Explicit (E)** — Stated clearly in BRD
- **Inferred (I)** — Implied but not stated (cite gap pattern from `references/gap-patterns.md`)
- **Not evidenced (NE)** — Absent
- **Deferred (DEF)** — Identified but outside minimal essential set (minimal scope only)
- **Explicit (user-confirmed) (EC)** — Resolved from `--ask-gaps` stakeholder answers (Step 4)

**Rules:**
- Never invent thresholds; mark "99.95% availability" as Inferred if unstated
- Use "Other/Uncategorized" only for genuinely uncategorizable requirements (not a shortcut between close categories); one-line justification required
- **Evidence field is a short phrase, not a sentence** — cap at ~12–15 words / one clause (e.g., `"UC-2: multi-region implied — deferred"`, not a full sentence). Cite the source tersely; don't restate reasoning in prose.
- **Scope-conditional tagging:** See Scope Behavior Matrix for minimal/standard/thorough differences

**Output:** Table: #, Category, Status (using codes: E, I, NE, DEF, EC), Evidence, Priority — always 19 rows (Directive 3)

### Step 3: Prioritize Each NFR

Classify all 19 categories as **Hard Constraint** or **Nice-to-Have.**

**Definitions (Priority column codes below; output uses short codes):**
- **Hard Constraint (HC)** — System doesn't work, fails a KPI, or violates compliance without it; includes load-bearing Inferred NFRs
- **Nice-to-Have (NTH)** — Improves experience but system works without it

**Rules:**
- Spell out reasoning for each priority decision
- If priority is unclear, route to Open Questions instead of guessing
- **Scope-conditional prioritization:** See Scope Behavior Matrix for minimal/standard/thorough differences

### Step 4: Ask for Real Gaps

Identify patterns in the BRD suggesting missing requirements. Consult `references/gap-patterns.md` (18 patterns) and build specific gap questions.

**Rules:**
- Only questions for patterns that actually apply
- Tied to specific BRD sections
- Not leading; ask what's genuinely missing

**Scope-specific filtering:** See Scope Behavior Matrix (Step 4 column) for minimal/standard/thorough differences.

**Default (no `--ask-gaps`):** Route questions to "Open Questions for Stakeholder" section (Step 5). Do not ask user directly.

**With `--ask-gaps`:** Ask batched questions in one concise round. For each answer:
- Status → `Explicit (user-confirmed)`
- Evidence → one-line paraphrase (not verbatim)
- Priority → re-apply Step 3 rule
- Update Step 2 NFR table; remove from Open Questions
- If answer is ambiguous/partial, keep in Open Questions rather than forcing resolution

### Step 5: Produce Structured Output

Generate single file: `req-nfr-analysis.md` with three sections in order:

1. **Normalized Functional Requirements** — Table: ID, Requirement, Source
2. **NFR List** — Table: #, Category, Status (E/I/NE/DEF/EC), Evidence, Priority (HC/NTH/—) — always 19 rows (Directive 3); Evidence kept to a short phrase, not a full sentence
3. **Open Questions for Stakeholder** — Template: `**Category (NFR #N):** <question> — Pattern: <name> (gap-patterns.md #N)` — tied to NFR rows or gap patterns

With `--ask-gaps`: Section 2 includes EC rows; Section 3 contains only unresolved items (may be empty).

## Deliverable

Single markdown file: `req-nfr-analysis.md` with three self-contained sections (see Step 5).

## Out of Scope

- Architecture recommendations, patterns, or technology stack suggestions
- Design decisions or trade-off analysis (Phase 2+)
- Inventing missing information (always ask stakeholders; except minimal scope suppresses production-grade questions for Deferred (DEF) categories—they're still identified and written to output, just without a stakeholder question)

## Success Criteria

- ✅ All 19 categories present in output; Deferred (DEF) distinct from Not evidenced (NE) (Directive 3)
- ✅ Every Inferred (I) NFR cites gap pattern; no invented thresholds
- ✅ Functional requirements are functional (no NFR language mixed in); Evidence kept to short phrases (~12–15 words)
- ✅ Priorities (HC/NTH) grounded in BRD or routed to Open Questions
- ✅ With `--ask-gaps`: Explicit (user-confirmed) (EC) rows traced to user answers; Section 3 contains only unresolved items
- ✅ Scope-tier behavior conforms to Scope Behavior Matrix (no production-grade questions in Minimal scope; cross-NFR dependencies surfaced in Thorough scope)
