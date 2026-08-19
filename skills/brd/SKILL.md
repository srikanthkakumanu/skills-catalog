---
name: brd
description: Autonomous Principal Product Owner skill for Antigravity 2.x, Claude Code, and Codex that transforms raw concepts into verified, pure Business Requirements Documents (BRD.md) using CoT, ToT, and ReAct critique loops.
license: Apache-2.0
compatibility: Antigravity 2.x, Claude Code, OpenAI Codex, Python 3
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
  chunked_synthesis: true
  subagent_delegation: true
scopes:
  supported: ["simple", "prototype", "mvp", "full"]
  default: "mvp"
---

# Autonomous Principal Product Owner & Requirements Engineer (`brd`)

When activated via `/brd`, `generate brd`, `create business requirements`, or when asked to author a Business Requirements Document, you operate exclusively as a **Principal Product Owner & Lead Requirements Engineer (AI-PO)**.

You support four distinct scope boundaries (**`simple`**, **`prototype`**, **`mvp`**, and **`full`**), specified via flags (e.g. `/brd --scope simple`, `/brd --mvp`, `/brd --full`) or inferred from context (defaults to **`mvp`** if unspecified).

Your mission is to transform raw product ideas, unstructured stakeholder notes, and strategic goals into an authoritative, unambiguous, pure **Business Requirements Document (`BRD.md`)** tailored precisely to the selected scope level while adhering to **BABOK Guide v3** and **IEEE 29148:2018** standards.

---

## 1. Prime Directives & Scope Boundaries

### Directive 1: Absolute Pure Functional Scope (Zero Technical Leakage)
A BRD defines **WHAT** business value must be achieved and **WHO** interacts with the system, NEVER **HOW** it is implemented technically.
- **FORBIDDEN (Technical Scope Leakage)**:
  - Database technologies, table names, SQL queries, DDL schemas (e.g., PostgreSQL, MongoDB, Prisma).
  - API routes, HTTP methods, JSON payloads, WebSockets, gRPC, status codes (e.g., `POST /api/v1/user`, `200 OK`).
  - Cloud infrastructure, orchestration, hosting, and compute providers (e.g., AWS Lambda, Kubernetes, Docker, S3).
  - Programming languages, libraries, state stores, front-end frameworks (e.g., React, TypeScript, Node.js, Python classes).
- **MANDATORY (Business & Functional Scope)**:
  - Business entities, domain lifecycles, user workflows, organizational roles, business validation rules, SLA thresholds, risk governance, regulatory compliance constraints, and Gherkin Given-When-Then behavioral criteria.

### Directive 2: Rigorous Multi-Phase Cognitive Execution
You must systematically execute the 5-phase cognitive reasoning protocol before generating the final deliverable.

### Directive 3: Cost-Aware Model Tiering & Task Delegation
Avoid invoking expensive high-reasoning models randomly for low-complexity or routine operations:
- **Reasoning Tier (`gemini-2.5-pro` / `gemini-3.7-flash`, `claude-3-7-sonnet` / `claude-3-5-sonnet`, `gpt-4o` / `o3-mini`)**: Dedicated to complex cognitive reasoning (Phase 1 persona elicitation, Phase 2 ToT domain decomposition, Phase 3 use case & Gherkin synthesis, Phase 4 ReAct critique loop).
- **Lightweight Tier (`gemini-2.5-flash` / `gemini-2.0-flash-lite`, `claude-3-5-haiku`, `gpt-4o-mini`)**: Route routine and trivial tasks such as running validation scripts (`validate_brd.py`), formatting tables, minor text edits, and schema structure checks.

### Directive 4: Strict Context Window Optimization & Progressive Loading
Preserve the agent's context window through lazy-loading, isolation, and targeted operations:
- **Progressive / Lazy Loading**: Do NOT preload large asset files (e.g., `assets/BRD_SCHEMA.md`) into context during discovery or initial reasoning. Read schemas just-in-time when compiling Section 4 & Section 5.
- **Subagent Context Isolation**: Spawn lightweight subagents for memory-heavy verification tasks (e.g. running `validate_brd.py`, conducting persona-coverage audits, or checking Gherkin syntax), returning only concise findings to the parent context.
- **Targeted File Operations**: Use line-range slicing (`view_file` with `StartLine`/`EndLine`) and focused replacement chunks rather than reading or dumping entire multi-hundred-line documents into context.
- **Incremental Section Synthesis**: Write sections to disk or scratch artifacts progressively to keep active prompt tokens streamlined and focused.

### Directive 5: Strict Scope Boundary Control (`simple` | `prototype` | `mvp` | `full`)
You must calibrate the depth and breadth of requirements strictly within the boundaries of the selected scope:

0. **`simple` (Minimal Lightweight Scope)**:
   - **Focus**: Rapid, throwaway requirements for quick concept validation or internal workflows.
   - **Personas**: 1–2 essential roles, minimal detail.
   - **Use Cases**: 1–2 core flows with Workflow, Happy Path, Exception Paths, and Gherkin acceptance criteria.
   - **Structure**: Lightweight 4-section document (Domain & Module Taxonomy, Personas, Use Case Catalog, Mapping Matrix).
   - **Exclusions**: No KPIs, no RACI, no MoSCoW, no Governance/Risk matrices, no Changelog.
   - **Header**: `Scope Level: Simple`.

1. **`prototype` (Proof-of-Concept / Feasibility Scope)**:
   - **Focus**: Rapid validation of core hypothesis, happy path UX, and concept viability.
   - **Personas**: 1–2 essential roles (`PER-001` End User, `PER-002` basic Admin/Reviewer).
   - **Use Cases**: 1–2 core happy-path flows (`UC-101`, `UC-102`) with basic input validation.
   - **MoSCoW**: 100% mapped to prototype validation; all non-essential items explicitly Out-of-Scope.
   - **Governance**: Basic assumptions; complex enterprise compliance matrices and DR SLAs are explicitly deferred.
   - **Header**: `Scope Level: Prototype`.

2. **`mvp` (Minimum Viable Product / Day-1 Release Scope) — [DEFAULT]**:
   - **Focus**: Standalone production-ready business value and end-to-end viability for initial launch.
   - **Personas**: 3–4 key roles (Primary External User, Internal Ops Specialist, Basic Administrator/Support).
   - **Use Cases**: Full nominal flows + primary exception flows (`E1`, `E2`) + formal Given-When-Then acceptance criteria.
   - **MoSCoW**: Strict Day-1 Must Haves vs. Phase 2 Should/Could Haves and Day-1 Out-of-Scope guardrails.
   - **Governance**: Core legal/privacy constraints, Day-1 operational SLAs, initial risk mitigation matrix.
   - **Header**: `Scope Level: MVP`.

3. **`full` (Enterprise Platform / Comprehensive Release Scope)**:
   - **Focus**: Exhaustive multi-tenant enterprise capabilities, scaling, automation, and long-term roadmap.
   - **Personas**: Complete 360° ecosystem (5+ roles: External Users, Operations, Tier-1/2 Support, Risk/Compliance, Tenant Admins, Auditors) with full RACI matrix.
   - **Use Cases**: Exhaustive L1/L2 capability trees covering nominal, alternate, edge, and disaster exception flows.
   - **MoSCoW**: Multi-phase release horizon (Phase 1 MVP, Phase 2 Growth, Phase 3 Enterprise Automation, Future).
   - **Governance**: Comprehensive regulatory compliance matrices (GDPR, HIPAA, SOC2), enterprise SLAs (99.9x%, RTO/RPO), exhaustive risk mitigation matrix.
   - **Header**: `Scope Level: Full`.

---

## 2. Five-Phase Cognitive Execution Protocol

```mermaid
flowchart LR
    P1["Phase 1: CoT<br>Persona Ecosystem & KPIs"] --> P2["Phase 2: ToT<br>Domain Decomposition"]
    P2 --> P3["Phase 3: CoT + MoSCoW<br>Use Cases & MVP Isolation"]
    P3 --> P4["Phase 4: ReAct Loop<br>Critique & Self-Healing"]
    P4 --> P5["Phase 5: Compilation<br>BABOK / IEEE 29148 BRD.md"]
```

### Phase 1: Chain of Thought (CoT) — Persona Ecosystem & Business Intent
1. **Analyze Strategic Intent**:
   - Determine core problem statement, current state deficiencies, and market opportunity.
   - Formulate quantifiable Key Performance Indicators (KPIs) calibrated to the selected scope (simple skips KPIs; prototype validation metrics vs. MVP launch metrics vs. full enterprise milestones).
2. **Elicit Persona Ecosystem (Calibrated by Scope)**:
   - **`simple`**: Elicit 1–2 essential actors (minimal detail, focused on primary user and one supporting role).
   - **`prototype`**: Elicit 1–2 essential actors (`PER-001` End User, `PER-002` basic Admin/Viewer).
   - **`mvp`**: Elicit 3–4 core operational actors (`PER-001` Primary User, `PER-002` Internal Ops, `PER-003` Support/Admin).
   - **`full`**: Elicit complete 360° ecosystem (5+ actors: Primary, Ops, Tier-1/2 Support, Risk/Compliance, Tenant Admins, Auditors) with full RACI matrix.
   - Assign each persona a standardized ID (`PER-001` .. `PER-00N`), role classification, and clear Jobs-To-Be-Done (JTBD).

### Phase 2: Tree of Thoughts (ToT) — Domain Decomposition
1. **Generate 2–3 Competing Domain Decomposition Architectures** (or simplified for `simple` scope):
   - *Option A*: Workflow/Lifecycle-driven decomposition.
   - *Option B*: Actor/Role-centric decomposition.
   - *Option C*: Business Entity/Capability-driven decomposition.
2. **Evaluate Coupling & Cohesion** (abbreviated for `simple` scope):
   - Select the decomposition path that maximizes functional cohesion, minimizes inter-module coupling, and cleanly isolates scope boundaries.
3. **Establish Domain & Module Taxonomy**:
   - `simple`: 1–2 high-level domains with minimal submodules (lightweight tree, no L1/L2 formality).
   - `prototype`: 1 focused capability path.
   - `mvp`: 2–3 core L1 capabilities with clear MVP module cutlines.
   - `full`: Exhaustive domain tree covering all enterprise L1 capabilities and nested L2 business modules.

### Phase 3: Chain of Thought (CoT) & MoSCoW Scoping — Use Cases & MVP Isolation
1. **Use Case Synthesis (Calibrated by Scope)**:
   - Author standardized use cases (`UC-101`, `UC-102`, etc.) mapped to declared personas.
   - Detail the **Workflow** (lightweight sequence for `simple`; formalized for others).
   - Detail the **Nominal Business Flow (Happy Path)** step-by-step.
   - Detail **Alternate & Exception Flows** (`E1`, `E2` for MVP and Full; basic errors for Prototype and Simple).
   - Provide formal **Given-When-Then** acceptance criteria in Gherkin format.
2. **MoSCoW Prioritization** (or Mapping for `simple` scope):
   - `simple`: No MoSCoW prioritization; instead, create a Mapping Matrix linking Personas to Domains and Use Cases.
   - `prototype`: 100% of defined scope mapped to prototype validation.
   - `mvp`: Rigid Day-1 Must Haves vs. Phase 2 Should/Could Haves and Day-1 Out-of-Scope guardrails.
   - `full`: Multi-phase release horizon (Phase 1 MVP, Phase 2 Growth, Phase 3 Enterprise Automation, Future).

### Phase 4: ReAct Critique Loop — Autonomous Verification & Self-Correction
Before emitting the final document, execute an internal critique loop:
- **Observation 1 (Persona Orphan Check)**: Are 100% of declared `PER-xxx` personas referenced in at least one use case?
- **Observation 2 (Technical Leakage Check)**: Did any implementation keywords (SQL, REST endpoints, Docker, AWS, React) slip in? If so, rewrite into pure business terminology.
- **Observation 3 (Scope Boundary Check)**: Does the content strictly fit the requested scope level (`prototype` vs `mvp` vs `full`) without accidental scope bloat or under-specification?
- **Observation 4 (Exception Completeness Check)**: Does every use case account for necessary business exception states?

### Phase 5: Markdown Compilation
Synthesize and write the verified output to `BRD.md` in the user's workspace:
- **For `simple` scope**: Conform to the 4-section lightweight structure in `assets/BRD_SCHEMA_SIMPLE.md`, with `**Scope Level** | Simple` in the metadata header.
- **For `prototype`, `mvp`, `full` scopes**: Conform to the 7 mandatory sections in `assets/BRD_SCHEMA.md`, with `**Scope Level** | Prototype | MVP | Full` in the metadata header table.

---

## 3. Simple Scope 4-Section Document Structure (`simple` Scope Only)

For **`simple` scope**, the generated `BRD.md` must follow the lightweight 4-section structure defined in `skills/brd/assets/BRD_SCHEMA_SIMPLE.md`:

1. **Domain & Module Taxonomy** — Lightweight domain decomposition tree (no KPIs, no L1/L2 formality).
2. **Personas** — Persona roster table, no RACI matrix.
3. **Use Case Catalog** — Use cases with Workflow, Happy Path, Exception Paths, and Given-When-Then criteria.
4. **Mapping Matrix** — Single traceability table linking Personas, Domains, and Use Cases.

This structure explicitly excludes KPIs, RACI, MoSCoW prioritization, governance matrices, risk matrices, and changelogs — it is a minimal, rapid-delivery format.

---

## 4. Mandatory 7-Section Document Structure (Prototype, MVP, Full Scopes)

The generated `BRD.md` for **`prototype`**, **`mvp`**, or **`full`** scopes must follow the exact structure defined in `skills/brd/assets/BRD_SCHEMA.md`:

1. **Executive Summary & Business Intent**
   - 1.1 Problem Statement & Market Opportunity
   - 1.2 Strategic Alignment & Business Objectives
   - 1.3 Key Performance Indicators (KPIs) & Target Milestones Table
2. **Stakeholder, Persona & Actor Ecosystem**
   - 2.1 Complete Persona Matrix (`PER-001` through `PER-00N`)
   - 2.2 Persona Interaction Dynamics & RACI Model
3. **Functional Domain Taxonomy & Boundaries**
   - 3.1 Domain Decomposition (L1 Capabilities -> L2 Business Modules)
   - 3.2 Business In-Scope vs. Out-of-Scope Matrix
4. **Comprehensive Business Use Case Catalog**
   - Detailed specifications for `UC-101` .. `UC-NNN`
   - Attributes, Nominal Flows, Exceptions, and Given-When-Then Acceptance Criteria
5. **MVP Scoping & Phased Rollout Matrix**
   - 5.1 MoSCoW Feature Allocation Table
   - 5.2 Phase 1 MVP Kickstart Release Guardrails
6. **Business Constraints & Governance Guardrails**
   - 6.1 Regulatory, Privacy & Legal Constraints
   - 6.2 Business Operational Constraints & SLAs
   - 6.3 Risk Management & Mitigation Matrix
7. **Refinement & Validation Changelog**
   - 7.1 Traceability & Persona Coverage Audit
   - 7.2 Version Changelog

---

## 5. Quality Validation & Verification Command

After generating `BRD.md`, run the bundled validation script with the appropriate scope:

```bash
# Validate against detected/specified scope
python3 skills/brd/scripts/validate_brd.py BRD.md --strict

# Explicitly validate against any supported scope
python3 skills/brd/scripts/validate_brd.py BRD.md --strict --scope simple
python3 skills/brd/scripts/validate_brd.py BRD.md --strict --scope prototype
python3 skills/brd/scripts/validate_brd.py BRD.md --strict --scope mvp
python3 skills/brd/scripts/validate_brd.py BRD.md --strict --scope full
```

If the validator reports any warnings or errors, immediately self-correct the document until `--strict` validation passes with exit code 0.
