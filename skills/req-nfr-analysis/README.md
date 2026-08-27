# req-nfr-analysis Skill (v1.2)

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
| F1  | System shall authenticate users via LDAP    | UC-3.2    |
| F2  | System shall persist user preferences       | AC-5.1    |
| ... |                                              |           |
```

**Section 2: NFR List**

```
| #  | Category                              | Status         | Evidence         | Priority        |
|----|---------------------------------------|----------------|------------------|-----------------|
| 1  | Performance                           | Inferred       | P1.2: 500ms SLA  | Hard Constraint |
| 2  | Latency                               | Not evidenced  | —                | —               |
| 3  | Scalability                           | Explicit       | UC-2: 100k users | Hard Constraint |
| 15 | Disaster Recovery/Business Continuity | Explicit (user-confirmed) | User confirmed: 4-hour RTO, 1-hour RPO | Hard Constraint |
| ... | ...                                  | ...            | ...              | ...             |
| 19 | Other/Uncategorized                  | Not evidenced  | —                | —               |
```

All 19 rows appear in every output, even "Not evidenced." With `--ask-gaps`, resolved gap questions appear as `Explicit (user-confirmed)` rows in the table.

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
- **Source reference**: Cite where it came from (e.g., "UC-3.2", "AC-5.1", "General Constraints")
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
- **No invented data**: If the BRD doesn't state an availability SLA, it is marked Inferred (with citation to the gap pattern), not Explicit. An open question is raised for the stakeholder.
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

#### 1. Quick Scope Invocation

```text
/req-nfr-analysis --scope quick Analyze BRD.md for the 5 key NFRs before we scope architecture
```

or

```text
extract nfr from BRD.md, quick pass
```

#### 2. Standard Scope Invocation (Default)

```text
/req-nfr-analysis --scope standard Analyze BRD.md
```

or

```text
/req-nfr-analysis Analyze our BRD for phase 1 requirements analysis
```

#### 3. Thorough Scope Invocation

```text
/req-nfr-analysis --scope thorough Analyze BRD.md with full dependency reasoning across NFRs
```

or

```text
do a thorough phase 1 requirements analysis on BRD.md before we move to architecture
```

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

This skill is **Phase 1** of the BRD → PRD → Architecture pipeline:

- **Phase 1 (this skill):** Normalize requirements, extract and prioritize NFRs, identify gaps
- **Phase 2 (future):** Architecture & design phase; consume `req-nfr-analysis.md` output and make technology/pattern decisions
- **Phase 3 (future):** PRD refinement or specification phase; detail user stories, API contracts, test plans

Each phase's output feeds into the next.

---

## Questions?

If you have questions about what a particular NFR category covers, see `references/nfr-taxonomy.md`.

If you want to understand why a particular gap question was asked, see `references/gap-patterns.md`.

If the skill is unclear about a requirement's classification, it will ask you directly rather than guess.
