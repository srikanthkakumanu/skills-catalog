# req-nfr-analysis Skill (v2.0)

**Phase 1 of the Requirements → PRD → Architecture Pipeline**

A structured, methodical skill for analyzing Business Requirements Documents (BRDs) to extract, normalize, and prioritize functional and non-functional requirements.

## Overview

This skill takes a completed BRD and produces a normalized requirements analysis that serves as the input to downstream phases (architecture design, tech-stack selection, PRD refinement). It ensures that all non-functional concerns are visible, prioritized, and traceable—preventing surprises when architecture decisions are made.

## What It Does

The skill performs **exactly five sequential steps**, none skipped or merged:

1. **Extract Functional Requirements** — Walk the BRD systematically; normalize each requirement to a short imperative statement with source tracking.
2. **Tag Every NFR Across 19 Categories** — Classify each requirement (and inferred gaps) against all 19 named NFR categories (see `references/nfr-taxonomy.md`).
3. **Prioritize Each NFR** — Classify as Hard Constraint or Nice-to-Have with documented reasoning.
4. **Ask for Real Gaps** — Identify patterns in the BRD that signal missing information. By default, list questions for stakeholder. With `--ask-gaps`, ask user directly and resolve answers into the analysis.
5. **Produce Structured Output** — Generate a single `req-nfr-analysis.md` file with three sections: Normalized Functional Requirements, NFR List (all 19 rows), and Open Questions.

## When to Use

Invoke this skill when:

- A BRD is provided or completed, and you want it analyzed for completeness and clarity
- You need a structured view of all functional and non-functional requirements before moving into architecture/design
- You want to identify and escalate ambiguities and gaps in the BRD
- You're moving from requirements phase into design or tech-stack selection
- A BRD is marked "done" and stakeholders ask "what's next?"

**Do NOT use this skill for:**

- Architecture recommendations (Phase 2+)
- Technology selection or comparison
- Detailed design decisions
- Implementation planning

---

## Input

A completed Business Requirements Document (BRD), typically in markdown or PDF format, containing:

- Use cases or user stories
- Acceptance criteria
- High-level constraints or context
- Any explicit requirements (functional or non-functional)

The BRD should be self-contained enough to identify where information is missing or implied.

## Output

A single markdown file: `req-nfr-analysis.md`

**Section 1: Normalized Functional Requirements**

```
| ID  | Requirement                                  | Source     |
|-----|----------------------------------------------|-----------|
| F1  | System shall authenticate users via LDAP    | UC-101    |
| F2  | System shall persist user preferences       | UC-102    |
| ... |                                              |           |
```

**Section 2: NFR List**

```
| #  | Category                              | Status         | Evidence         | Priority        |
|----|---------------------------------------|----------------|------------------|-----------------|
| 1  | Performance                           | I              | P1.2: 500ms SLA  | HC              |
| 2  | Latency                               | NE             | —                | —               |
| 3  | Scalability                           | DEF            | UC-2: 100k-user scale implied — deferred | — |
| 4  | Availability                          | E              | UC-2: 99.95% uptime | HC              |
| 15 | Disaster Recovery/Business Continuity | EC             | User confirmed: 4-hour RTO, 1-hour RPO | HC              |
| ... | ...                                  | ...            | ...              | ...             |
| 19 | Other/Uncategorized                  | NE             | —                | —               |

**Status codes:** E = Explicit, I = Inferred, NE = Not evidenced, DEF = Deferred (Minimal Scope), EC = Explicit (user-confirmed)  
**Priority codes:** HC = Hard Constraint, NTH = Nice-to-Have, — = Deferred or absent
```

All 19 rows appear in every output, even "Not evidenced." Minimal scope may use `DEF` for categories identified but outside the minimal essential set. With `--ask-gaps`, resolved gap questions appear as `EC` rows in the table. (See SKILL.md Scope Behavior Matrix for scope-conditional behavior.)

**Section 3: Open Questions for Stakeholder**

```
- **Disaster Recovery (NFR #15):** If a regional data center fails, what is the acceptable downtime (RTO) and data loss window (RPO)? Pattern: Multi-Region Implied (gap-patterns.md #1)
- **AI Safety/Autonomy (NFR #18):** Which decisions can the agent make autonomously vs. which require human approval? Pattern: AI System Without Guardrails (gap-patterns.md #9)
- ...
```

---

## How It Works

### Step 1: Extract Functional Requirements

The skill walks through the BRD section-by-section (use cases, acceptance criteria, requirements tables, etc.) and extracts every requirement into a normalized form:

- **Short imperative statement**: "System shall X"
- **Source reference**: Cite where it came from (e.g., use case ID like "UC-101", section reference like "General Constraints", or the BRD's own requirement identifier)
- **Functional only**: No NFR language mixed in (separate "persist data" from "persist data with 99.95% durability")

If a single BRD sentence contains both functional and NFR concerns, they are split into separate rows.

### Step 2: Tag Every NFR

For each requirement (including inferred ones), determine its classification:

**Across the 18 named categories** (see `references/nfr-taxonomy.md`):

- Performance, Latency, Scalability, Availability, Reliability, Resilience/Fault Tolerance, Security, Compliance/Regulatory, Data Privacy, Maintainability, Usability/Accessibility, Interoperability, Portability, Observability, Disaster Recovery/Business Continuity, Capacity/Resource Efficiency, Explainability/Transparency, AI Safety/Autonomy Control

**For each category, mark**:

- **Status**: Explicit (clearly stated), Inferred (implied but not stated), or Not evidenced (absent)
- **Evidence**: Cite the BRD section or gap pattern (from `references/gap-patterns.md`) that led to the classification
- **Priority**: Hard Constraint or Nice-to-Have (from Step 3)

**For the 19th category ("Other/Uncategorized")**: Use only when a requirement is genuinely uncategorizable, with one-line justification. This is not a shortcut between two close categories.

**Important**: Never upgrade an Inferred NFR to Explicit by inventing a plausible number. If the BRD doesn't state "99.95% availability," don't assume it.

### Step 3: Prioritize Each NFR

For every NFR (all 19 categories), decide:

- **Hard Constraint** = System does not functionally work, fails a stated KPI, or violates compliance without it. Includes load-bearing Inferred NFRs.
- **Nice-to-Have** = Improves experience/performance but system works without it. Includes anything BRD explicitly defers.

Spell out the reasoning rule for each decision. If priority is unclear, route to "Open Questions" instead of guessing.

### Step 4: Ask for Real Gaps

Consult `references/gap-patterns.md` for 18 common patterns that signal missing requirements (multi-region architecture, compliance domain, external integrations, etc.).

For each pattern that applies to this BRD:

- Prepare one short, specific question
- Do not pose leading questions or assume answers
- Route only patterns that actually apply

Example questions (from gap patterns):

- "If the external payment service is unavailable, should the system queue transactions or reject immediately?"
- "What data must be accessible within 2 seconds globally—all data, or only user profile data?"
- "Are there regulatory requirements (GDPR, HIPAA, PCI-DSS) we must comply with?"

### Step 5: Produce Structured Output

Generate `req-nfr-analysis.md` with three sections in this exact order:

1. **Normalized Functional Requirements** — All requirements from Step 1 in a table
2. **NFR List** — All 19 categories from Step 2 in a single table (every row, even "Not evidenced")
3. **Open Questions for Stakeholder** — Bulleted list from Step 4, each tied to a specific NFR row or gap pattern

---

## Key Design Principles

- **All 19 rows every time**: Even if an NFR category is "Not evidenced," it appears in the output. This makes gaps visible and prevents silent assumptions.
- **No invented data**: If the BRD doesn't state an availability SLA, it is marked I (with citation to the gap pattern), not E. An open question is raised for the stakeholder, except minimal scope does not raise production-grade-hardening questions about Deferred categories — those are marked DEF instead.
- **Scope-aware identification, not scope-aware silence**: Minimal scope still identifies all 19 NFR categories and writes every identified one to the output file as DEF or one of the standard statuses (E/I/NE/EC). The difference is which categories get prioritized and which get gap questions — not which ones appear in the file at all.
- **Production-grade rigor at thorough scope**: Thorough scope expects real targets (SLA %, latency budgets, RTO/RPO, compliance frameworks) for categories that demand them, and surfaces cross-NFR dependencies explicitly (e.g., how a multi-region Availability SLA implies specific Disaster Recovery RTO/RPO).
- **Separation of concerns**: Functional requirements are purely functional; NFR concerns are isolated and categorized.
- **Traceability**: Every requirement and every inferred gap is tied back to a source (BRD section, gap pattern, or explicit question).
- **Out of scope**: No architecture recommendations, technology choices, or design decisions. This skill is purely analytical.

---

## agentskills.io Compliance

This skill is fully compliant with the [agentskills.io specification v1.0](https://agentskills.io/specification):

- ✅ Frontmatter with required metadata (name, description, metadata)
- ✅ Clear trigger conditions (when to invoke)
- ✅ Sequential, non-overlapping steps
- ✅ Deterministic inputs and outputs
- ✅ Reproducible execution (same BRD → same analysis)
- ✅ Structured reference materials (`references/`)
- ✅ Out-of-scope declarations

---

## Example Usage

**Scenario:** Product team completes a BRD for a new financial transaction system and asks, "Is this ready for architecture?"

**Skill invocation:**

```
User: "Analyze our BRD for Phase 1 requirements. We think it's done, but I want to catch any gaps before we design the architecture."
```

**Skill execution:**

1. Walks the BRD, extracts 47 functional requirements
2. Tags 19 NFR categories; finds:
   - Availability: Explicit ("99.95%"), Hard Constraint
   - Data Privacy: Inferred ("regulated domain, no explicit retention policy"), Nice-to-Have
   - Disaster Recovery: Not evidenced, Hard Constraint (load-bearing)
   - AI Safety: Not evidenced (BRD mentions "automated risk assessment"), Hard Constraint
3. Routes five open questions to stakeholder:
   - "What is the recovery time objective (RTO) if a data center fails?"
   - "For the automated risk assessment, which decisions require human approval?"
   - "Must we comply with SOC2, PCI-DSS, or other frameworks?"
   - etc.

**Output:** `req-nfr-analysis.md` with structured tables + questions

**Next step:** Stakeholder reviews analysis, answers open questions, and refines BRD if needed. Then skill output feeds into Phase 2 (architecture/design).

---

## 🚀 Installation & Activation

### Quick Install (All Agents)

```bash
cd /Users/skakumanu/practice/skills-catalog

# Install to all agents (Antigravity, Claude Code, Codex)
./install.sh --skill req-nfr-analysis --target all

# Or with short flags
./install.sh -s req-nfr-analysis -t all
```

### Forceful Installation (Recommended for Updates)

Use `--force` to overwrite an existing installation and pick up the latest version:

```bash
./install.sh --skill req-nfr-analysis --target all --force --mode copy
```

#### Installation Mode Comparison

| Mode              | Command                      | Use Case                                        | Auto-Updates |
| ----------------- | ---------------------------- | ----------------------------------------------- | ------------ |
| **Copy**    | `--mode copy`              | Independent copies (recommended for production) | ❌ No        |
| **Symlink** | `--mode symlink` (default) | Link to catalog source                          | ✅ Yes       |

### Installation Flags Reference

| Flag                      | Purpose                                 | Example                                                     |
| ------------------------- | --------------------------------------- | ----------------------------------------------------------- |
| `-s, --skill <NAME>`    | Which skill to install                  | `-s req-nfr-analysis` or `-s all`                       |
| `-t, --target <TARGET>` | Agent(s) to install to                  | `-t all`, `-t claude`, `-t antigravity`, `-t codex` |
| `-f, --force`           | **Forcefully overwrite existing** | Forces reinstall even if already present                    |
| `-m, --mode <MODE>`     | Installation method                     | `-m copy` or `-m symlink`                               |
| `-h, --help`            | Show help message                       | `--help`                                                  |

### Verify Installation Success

```bash
# Check all agents have the skill installed
echo "=== Antigravity ===" && ls -la ~/.antigravity/skills/req-nfr-analysis/SKILL.md && echo "✓ Installed"
echo "=== Claude Code ===" && ls -la ~/.claude/skills/req-nfr-analysis/SKILL.md && echo "✓ Installed"
echo "=== Codex ===" && ls -la ~/.codex/skills/req-nfr-analysis/SKILL.md && echo "✓ Installed"
```

### Targeted Installation Examples

```bash
# Install only to Claude Code (copy mode)
./install.sh --skill req-nfr-analysis --target claude --mode copy

# Install specific skill with default settings
./install.sh -s req-nfr-analysis

# View installation help
./install.sh --help
```

### Safety Notes

- **`--force` flag:** Removes existing installations and replaces with latest version (safe for updates)
- **Symlink mode:** Updates in catalog automatically propagate to all agents (but breaks if catalog moves)
- **Copy mode:** Independent installations don't auto-update (safer if you modify locally)
- **Recommendation:** Use `--force --mode copy` for production environments

### Activation Triggers by Scope

Invoke the skill within your AI agent runtime with your desired scope depth:

#### 1. Minimal Scope Invocation (Default)

```text
/req-nfr-analysis Analyze BRD.md for a fully functional system at minimal deployment scale
```

or

```text
extract nfr from BRD.md, minimal pass
```

Minimal scope identifies all 19 NFR categories but focuses only on the minimal essential set. Categories outside this set are tagged as DEF (Deferred) and do not receive production-grade-hardening questions. For detailed scope behavior across all three scopes, see SKILL.md's Scope Behavior Matrix.

#### 2. Standard Scope Invocation

```text
/req-nfr-analysis --scope standard Analyze BRD.md
```

or

```text
/req-nfr-analysis --scope standard Analyze our BRD for phase 1 requirements analysis
```

Standard scope walks all 19 NFR categories and generates applicable gap questions; no deferral concept.

#### 3. Thorough Scope Invocation

```text
/req-nfr-analysis --scope thorough Analyze BRD.md with production-grade rigor across all NFRs
```

or

```text
do a thorough phase 1 requirements analysis on BRD.md before we move to architecture
```

Thorough scope evaluates all 19 NFR categories at production-grade rigor; expects real targets and surfaces cross-NFR dependencies. Never uses DEF status.

#### 4. Interactive Gap Resolution

```text
/req-nfr-analysis --ask-gaps Analyze BRD.md and ask me about missing requirements
```

or

```text
/req-nfr-analysis --scope standard --ask-gaps Analyze BRD.md and let's resolve the gaps together
```

With `--ask-gaps`, the skill asks gap questions in the conversation, integrates your answers into the analysis, and updates the NFR table with `Explicit (user-confirmed)` entries for resolved items.

---

## 🔍 Validation

This skill's structure and frontmatter are validated against the agentskills.io specification using the `skills-ref` reference validator:

```bash
pip install skills-ref --break-system-packages
agentskills validate ./skills/req-nfr-analysis/
```

All validation checks pass.

---

## 🧪 Testing

Registry and skill-frontmatter tests for `req-nfr-analysis` live alongside the rest of the catalog's test suite in `tests/`, run via `uv`:

```bash
# Run the full test suite (registry + BRD validator tests)
uv run pytest tests/ -v

# Run just the registry/skill-configuration tests that cover req-nfr-analysis
uv run pytest tests/test_registry.py -v
```

These tests assert that:

- `req-nfr-analysis` is correctly registered in `registry.json` with valid `path`, `entrypoint`, and `readme`
- `SKILL.md` frontmatter declares `models`, `context_optimization`, and `scopes`
- The declared `scopes.default` is included in `scopes.supported`
- Model tiering (`reasoning_tier`, `lightweight_tier`) is defined for `gemini`, `claude`, and `codex`

---

## Files

- **SKILL.md** — Formal skill definition with 5-step execution procedure
- **README.md** — This file; user-facing documentation
- **references/nfr-taxonomy.md** — Definitions of all 19 NFR categories with examples
- **references/gap-patterns.md** — 18 patterns that signal missing requirements; guides stakeholder questions

---

## Version History

**v2.1** (2026-09-01):

- Compacted SKILL.md: consolidated scope-conditional rules (previously scattered across Steps 2, 3, 4) into single Scope Behavior Matrix (no behavior change, improved scannability)
- Introduced short Status/Priority codes: E/I/NE/DEF/EC for Status; HC/NTH for Priority (used in all generated output to compact NFR tables)
- Deduplicated repeated rule restatements; trimmed Success Criteria from 11 to 6 focused bullets
- Codified Open Questions bullet template in Step 5 for consistency
- Updated README example tables and cross-references to use short codes and Scope Behavior Matrix
- "Always 19 rows, even Not evidenced" guarantee unchanged — compaction via shorter cell content, not fewer rows

**v2.0** (2026-09-01):

- Renamed `quick` scope to `minimal` across registry.json, SKILL.md, and README.md — breaking change to the public scope identifier and default value
- Renamed `Deferred (Quick Scope)` status literal to `Deferred (Minimal Scope)` accordingly
- Fixed pre-existing sync bug: registry.json `scopes.default` was `"standard"`, now corrected to `"minimal"` to match SKILL.md's actual default
- Scope-tier behavior and analysis depths unchanged; terminology-only update

**v1.4** (2026-09-01):

- Capped Evidence field length to short phrases (~12–15 words / one clause) instead of full sentences for consistency and conciseness in all output tables
- Updated source-reference conventions: generalized from invented `AC-x.x` scheme to match BRD output (use case IDs like `UC-101` and acceptance criteria cited by parent use case or section reference)
- Added `Explicit (user-confirmed)` to canonical Status tag list in Step 2 (result of `--ask-gaps` resolution)
- Clarified that quick-scope's "minimal essential set" is a scoping heuristic for question depth, not an architecture recommendation

**v1.3** (2026-08-31):

- Redefined `quick` scope: minimal essential set (one container per frontend app/microservice, one DB, one AI agent per identified need), no production-grade-hardening questions for out-of-scope categories. Introduced `Deferred (Quick Scope)` status to distinguish identified-but-deferred NFRs from `Not evidenced` categories.
- Redefined `thorough` scope: production-grade rigor across all 19 categories with real targets (SLA %, latency budgets, RTO/RPO, compliance frameworks) and explicit cross-NFR dependency surfacing.
- Made `quick` the default scope (changed from `standard`).
- Updated gap question generation rules: quick scope suppresses production-grade-hardening questions for deferred categories; thorough scope generates complete coverage with dependency implications called out; standard scope unchanged.
- Reconciled "always ask" rules in Out of Scope and Key Design Principles sections to account for quick scope's selective question suppression while maintaining all 19 rows in output.
- Cleaned up Core Directives table formatting (moved Directive 4–6 labels to consistent columns).
- Dropped "Python 3" from compatibility line (no Python script in this skill).

**v1.2** (2026-08-27):

- Added `--ask-gaps` interactive mode for resolving gap questions with user input
- Gap questions can now be answered in-conversation, with responses folded into the NFR table as `Explicit (user-confirmed)` entries
- Status column can now display `Explicit (user-confirmed)` for NFRs resolved via user interaction
- Default behavior unchanged: omit `--ask-gaps` for static question listing

**v1.1** (2026-08-27):

- Finalized all 19 NFR categories with detailed definitions
- Added 18 gap patterns for structured gap identification
- Validated against agentskills.io specification

**v1.0** (initial):

- Core 5-step analysis procedure
- Basic NFR taxonomy

---

## Pipeline Context

This skill is **Phase 1** of the BRD → Architecture → PRD pipeline:

- **Phase 1 (this skill):** Normalize requirements, extract and prioritize NFRs, identify gaps
- **Phase 2:** [`architecture-decisions`](../architecture-decisions/README.md) skill; consume `req-nfr-analysis.md` output and make architecture style + agentic-AI fitness decisions
- **Phase 3 (future):** PRD refinement or specification phase; detail user stories, API contracts, test plans based on Phase 2 architecture decisions

Each phase's output feeds into the next.

---

## Questions?

If you have questions about what a particular NFR category covers, see `references/nfr-taxonomy.md`.

If you want to understand why a particular gap question was asked, see `references/gap-patterns.md`.

If the skill is unclear about a requirement's classification, it will ask you directly rather than guess.
