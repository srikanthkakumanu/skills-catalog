# Req & NFR Analysis Skill

**Normalizes a BRD's functional requirements and extracts non-functional requirements across 10 categories, flags contradictions and unsupported claims, prioritizes constraints.**

A structured skill for consuming Business Requirements Documents (BRDs) and producing a normalized requirements analysis — functional requirements extracted with source tracking, all non-functional concerns visible and categorized, contradictions surfaced, and priorities documented for downstream architecture/design phases.

## Overview

This skill takes a completed BRD and produces `req-nfr-analysis.md` — a reference document that normalizes all stated and inferred functional/non-functional requirements, flags any structural gaps or contradictions the BRD's self-check may have missed, and prioritizes each NFR as a hard constraint or nice-to-have. This output feeds directly into architecture decisioning.

## What It Does

The skill executes exactly four sequential steps:

1. **Extract Functional Requirements** — Walk the BRD systematically; extract each functional requirement as a short imperative statement with source tracking (cite the use case or section).
2. **Tag Every NFR Across 10 Categories** — Classify each requirement (and any inferred NFRs) against all 10 named NFR categories: Performance & Scalability, Reliability & Recovery, Security, Compliance & Data Governance, Usability & Accessibility, Maintainability & Portability, Observability, Transparency/Explainability, Cost, Other.
3. **Structural Check** — Detect contradictions (two flows conflict), unsupported framing claims (title implies capabilities the BRD doesn't deliver), and orphaned scope items (in-scope modules with no use cases). Re-run the BRD's self-check if its findings section is missing or incomplete.
4. **Open Questions** — List only unresolved items (each ≤1 line, tied to an NFR category or structural finding). May be empty.

Output is always `req-nfr-analysis.md` with four sections: Functional Requirements, NFR Table (10 rows), Structural Findings, Open Questions. "None" is valid for Findings and Questions.

## Key Design Principles

- **Pure requirements, pure NFRs** — Functional statements stay functional; any NFR language mixed in is split out.
- **All 10 rows every time** — Even if an NFR category is "Not evidenced," it appears in the output. Gaps are visible, not silent.
- **Inferred ≠ stated** — Always mark source; distinguish explicit requirements from inferred needs with a citation (≤10 words).
- **Contradiction detection** — If two flows or rules silently conflict (e.g., "must be offline-capable" + "real-time sync required"), both are flagged with their source.
- **No invented thresholds** — Unclear priority or unstated details become Open Questions, not guesses. Never invent an SLA the BRD didn't state.

## Input

A completed Business Requirements Document (BRD), such as output from the `/brd` skill, containing:

- Domain, personas, use cases
- Happy paths, exception flows, acceptance criteria
- Scope boundaries (in-scope / out-of-scope)
- Self-check findings (if any)

The BRD should be self-contained enough to extract both stated and implied requirements.

## Output: `req-nfr-analysis.md`

```markdown
# Requirements & NFR Analysis: [BRD Name]

## Functional Requirements

| ID  | Requirement | Source |
|-----|-------------|--------|
| FR1 | System shall authenticate users via LDAP | UC-101 |
| FR2 | System shall persist user preferences | UC-102 |
| ... | ... | ... |

## NFR Table

| # | Category | Status | Evidence | Priority |
|---|----------|--------|----------|----------|
| 1 | Performance & Scalability | E | UC-2: 100k concurrent users | HC |
| 2 | Reliability & Recovery | I | Multi-region implied but not explicit | NTH |
| 3 | Security | E | UC-1: LDAP auth required | HC |
| 4 | Compliance & Data Governance | NE | — | — |
| 5 | Usability & Accessibility | E | Use case flows assume web UI | NTH |
| 6 | Maintainability & Portability | NE | — | — |
| 7 | Observability | I | "Debug mode" mentioned once in Scope | NTH |
| 8 | Transparency/Explainability | NE | — | — |
| 9 | Cost | NE | — | — |
| 10 | Other | NE | — | — |

**Status codes:** E = Explicit, I = Inferred, NE = Not evidenced  
**Priority codes:** HC = Hard Constraint, NTH = Nice-to-Have, — = Not applicable/deferred

## Structural Findings

| Type | Description | Reference |
|------|-------------|-----------|
| Contradiction | "Must support offline" (Scope) vs "Real-time sync required" (UC-2) | UC-2, Scope row 3 |
| Unsupported Claim | Domain claims "AI-driven" but no use case delivers automated decisions | Domain name vs UC-101/102/103 |
| Orphaned Scope | "Reporting" module in-scope but no use case exercises it | Scope table row 4 |

Empty finding → `| None | | |` (always one row at minimum)

## Open Questions

- **Performance (NFR #1):** Does "100k concurrent" mean peak load or sustained?
- **Compliance (NFR #4):** Are there PCI-DSS, GDPR, or HIPAA requirements given the domain involves payment data?
- **Transparency (NFR #8):** For the "AI-driven" claim, which decisions should be explainable to users vs admins?
```

Every section is always present. Functional Requirements may be 0 rows (if BRD is purely non-functional, rare). NFR Table is always 10 rows. Findings and Questions may be "None" if none exist.

## How It Works

### Step 1: Extract Functional Requirements

Walk through the BRD section by section (Domain, Personas, Use Cases, Scope). For each use case happy path, exception, or explicit requirement:

- Write a short imperative statement (e.g., "System shall authenticate users via LDAP")
- Cite the source (e.g., "UC-101") — do not invent general capabilities
- Normalize similar requirements into one row (e.g., multiple UCs mentioning "audit logging" → one FR)

### Step 2: Tag Every NFR Across 10 Categories

For each stated and inferred requirement (and the BRD as a whole), classify against the 10 NFR categories:

1. **Performance & Scalability** — Throughput, latency, concurrent user capacity, data volume handling
2. **Reliability & Recovery** — MTBF, error handling, retry logic, recovery procedures
3. **Security** — Authentication, authorization, encryption, threat model, attack surface
4. **Compliance & Data Governance** — Regulatory (GDPR, HIPAA, PCI-DSS), data retention, audit trails
5. **Usability & Accessibility** — UI responsiveness, a11y, help systems, error messages
6. **Maintainability & Portability** — Code quality, testability, deployment targets, tech-stack choices
7. **Observability** — Logging, metrics, tracing, debugging, dashboards
8. **Transparency/Explainability** — Model explainability (for AI/ML), decision reasoning, rationale visibility
9. **Cost** — Infrastructure, licensing, operational expense targets
10. **Other** — Anything genuinely uncategorizable (rare; use only with justification)

For each category, mark:

- **Status:** E (Explicit), I (Inferred), or NE (Not evidenced)
- **Evidence:** Source or gap pattern (≤10 words)
- **Priority:** HC (Hard Constraint — system fails without it), NTH (Nice-to-Have — improves but not load-bearing), or — (not applicable/deferred)

### Step 3: Structural Check

Detect three classes of issues:

- **Contradiction:** Two flows, rules, or acceptance criteria conflict. E.g., "offline-capable" + "must sync in real-time." Flag both with their sources.
- **Unsupported Framing:** Domain/title names a capability (e.g., "AI-driven," "fully automated") that no use case actually delivers. Flag the claim and the gap.
- **Orphaned Scope:** A module in the Scope table's "in-scope" column has no use case exercising it. Flag module name and suggest whether it should be deferred or added to a UC.

If the BRD's Self-Check Findings section is present and complete, you may reuse it (cite it). If missing, incomplete, or the skill identifies *additional* issues, add them here.

### Step 4: Open Questions

List unresolved items only — one line each, tied to an NFR category or structural finding. Examples:

- `Performance (NFR #1): Does "100k concurrent" mean peak or sustained load?`
- `Compliance (NFR #4): Are we subject to GDPR, HIPAA, or PCI-DSS given the data domain?`
- `Contradiction (Scope vs UC-2): Should offline sync be deferred or added to scope?`

Do not invent answers or "nice-to-have" refinements. Only surface genuine gaps.

## When to Use

Invoke this skill when:

- A BRD is completed and you need to extract and normalize all requirements before architecture/design
- You want a structured, traceable view of all functional and non-functional concerns
- You need to identify ambiguities, contradictions, or scope gaps in the BRD
- You're moving from requirements phase into architecture decisioning
- Stakeholders ask "what are we actually building and what quality attributes must we meet?"

**Do NOT use this skill for:**

- Architecture recommendations or tech-stack selection (Phase 2+)
- Detailed design decisions or implementation planning
- Resolving contradictions or filling gaps unilaterally — flag them, don't fix them
- Inventing requirements the BRD didn't state or imply

## Installation & Activation

### Install

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all runtimes (symlinks)
./install.sh --skill req-nfr-analysis

# Install via file copy
./install.sh --skill req-nfr-analysis --mode copy

# Install to a specific runtime
./install.sh --skill req-nfr-analysis --target claude

# Force-reinstall
./install.sh --skill req-nfr-analysis --force

# Full reinstall via copy
./install.sh --skill req-nfr-analysis --force --mode copy
```

For general installation details and troubleshooting, see the [**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README.

### Invocation

Use natural language or a slash command:

```text
/req-nfr-analysis Analyze our BRD for phase 1 requirements

analyze requirements from BRD.md

/req-nfr-analysis Extract NFRs and flag contradictions before architecture phase

nfr analysis
```

The skill reads the BRD and produces `req-nfr-analysis.md` with all four sections and structural findings.

## Files

- **SKILL.md** — Persona directives and 4-step execution protocol
- **README.md** — This file; user-facing reference documentation

## Out of Scope

- **Architecture, stack, or design decisions** — No "use Kubernetes," "pick PostgreSQL," or "microservices architecture." Pure requirements only.
- **Resolving findings unilaterally** — If the analysis flags a contradiction or unsupported claim, the skill flags it; fixing it is a stakeholder decision, not part of this skill's output.
- **Inventing thresholds or SLAs** — If the BRD doesn't state "99.95% uptime," the skill marks it Inferred or Not Evidenced, not guessed.
- **Implementation planning, test plans, or deployment strategies** — Those are downstream artifacts.
