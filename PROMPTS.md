You are an expert Systems Architect and Agent Engineering Specialist.
Scaffold and initialize this repository as a production-grade Agent Skills Monorepo named `skills-catalog`, fully compatible with Antigravity 2.x, Claude Code, and OpenAI Codex following the open Agent Skills standard.

Create the exact directory structure and all necessary files with full, production-ready implementation details (no placeholders, no abbreviations, no omissions) for our primary skill: `brd`.

### Context & Requirements
1. Skill Identity: `brd` (located at `skills/brd/`).
2. Supported Runtimes: Antigravity 2.x (`~/.antigravity/skills`), Claude Code (`~/.claude/skills`), and OpenAI Codex (`~/.codex/skills`).
3. Role & Persona: Act as a Principal Product Owner & Requirements Engineer (AI-PO).
4. Pure Business & Functional Scope: The generated output must be STRICTLY restricted to business, functional, and user requirements. Technical architectures, database schemas, API routes, and cloud infrastructure stacks must be excluded to produce an unambiguous baseline for downstream design.
5. Delivery Scope Boundaries (`prototype` | `mvp` | `full`):
   - The skill must support choosing between three explicit delivery scope levels (default: `mvp`):
     - **`prototype`**: Rapid concept validation & feasibility. 1–2 essential personas, 1–2 happy-path use cases, basic input validation, explicit prototype assumptions, deferred enterprise SLAs.
     - **`mvp`** (Default): Day-1 production-ready release viability. 3–4 core operational personas, full nominal flows + primary exception flows (`E1`, `E2`), formal Given-When-Then criteria, strict Day-1 Must Haves vs. Day-1 Out-of-Scope guardrails.
     - **`full`**: Comprehensive enterprise multi-phase specification. 360° persona ecosystem (5+ roles with RACI), exhaustive L1/L2 capability trees, edge and disaster recovery exception flows, multi-phase roadmap, and enterprise regulatory/SLA compliance matrices.
   - Skill must support CLI/prompt flags: `/brd --scope prototype`, `/brd --scope mvp`, `/brd --scope full`, `/brd --prototype`, `/brd --mvp`, `/brd --full`.
6. Multi-Phase Cognitive Reasoning:
   - Phase 1 (Chain of Thought): Elicit scope-calibrated persona ecosystem and business JTBD/KPIs.
   - Phase 2 (Tree of Thoughts): Explore 2-3 domain decomposition paths; select the one with minimal functional coupling into L1 Capabilities and L2 Business Modules.
   - Phase 3 (Chain of Thought & MoSCoW): Exhaustively map use cases (Nominal flow, Exceptions, Given-When-Then criteria) and strictly isolate scope boundaries.
   - Phase 4 (ReAct Critique Loop): Self-evaluate against boundary collisions, orphaned personas, unhandled exceptions, and scope bleed before final compilation.
   - Phase 5: Markdown compilation adhering to BABOK and IEEE 29148 standards with explicit `Scope Level` metadata.
7. Model Selection & Cost Optimization:
   - Skills must implement a two-tier model routing strategy across supported model families (Google Gemini, Anthropic Claude, OpenAI Codex/GPT).
   - Trivial / mechanical tasks (linter execution, schema verification, table formatting, regex scanning, minor text fixes) MUST use cheap, ultra-low-cost, fast models (e.g. `gemini-2.5-flash` / `gemini-2.0-flash-lite`, `claude-3-5-haiku`, `gpt-4o-mini`).
   - Deep cognitive reasoning tasks (Phases 1-4: persona elicitation, ToT domain decomposition, use case & Gherkin formulation, ReAct critique) MUST use capable reasoning models (e.g. `gemini-2.5-pro` / `gemini-3.7-flash` (High), `claude-3-7-sonnet` / `claude-3-5-sonnet`, `gpt-4o` / `o3-mini`).
   - Skills must NOT randomly invoke expensive high-reasoning models for routine tasks.
8. Context Window Management & Token Efficiency:
   - Managing the agent's context window efficiently is essential to maintain reasoning fidelity and prevent token bloat across multi-step workflows.
   - Progressive Loading (Lazy Loading): Keep `SKILL.md` entrypoints compact; load extensive schema templates (`assets/*.md`) only when entering final document compilation phases.
   - Subagent Context Isolation: Offload heavy tool executions (such as running `validate_brd.py` linters, regex audits, or checking references) to ephemeral subagents or local CLI scripts, returning only compact summaries to the main orchestrator.
   - Line-Bounded Slicing: Use line-sliced file reads and targeted replacement chunks rather than dumping multi-hundred-line documents into context.
   - Intermediate Checkpointing: Persist state to disk or structured sections rather than accumulating sprawling chat history.

---

### Files to Generate or Update

1. `README.md` (Root Catalog Guide)
   - Master catalog documentation containing all information that applies universally across all skills.
   - Monorepo architecture, Agent Skills standard directory anatomy, and runtime compatibility matrix (Antigravity 2.x, Claude Code, Codex, CLI).
   - Model Selection & Cost Optimization Framework documenting the two-tier routing strategy across Gemini, Claude, and Codex runtimes.
   - Context Window Management & Token Efficiency Standard establishing the Four Pillars of context optimization (Progressive Loading, Subagent Isolation, Line-Bounded Slicing, Compact CLI Outputs).
   - Universal installation & deployment guide using `./install.sh` (targets, symlink/copy modes, specific skills).
   - Available Skills table indexing all skills with links to each skill's dedicated `README.md`, scope capabilities, and cost/context profiles.
   - Central registry (`registry.json`) specification, catalog testing conventions, and step-by-step contribution guide for authoring new skills.

2. `registry.json`
   - Machine-readable manifest conforming to `https://agentskills.io/schema/registry.json`.
   - Top-level `context_standards` defining progressive loading, subagent isolation, and targeted file slicing.
   - Register the `brd` skill with path `skills/brd`, entrypoint `SKILL.md`, readme `README.md`, version `1.0.0`, detailed description, triggers (including scope flags), `scopes` metadata (`prototype`, `mvp`, `full`), `context_optimization` configuration, and `models` tiering.

3. `install.sh`
   - Executable bash script supporting targets: `antigravity`, `claude`, `codex`, and `all`.
   - Supports modes: `symlink` (default) and `copy`.
   - Supports installing specific skills via `--skill <name>` or all skills.
   - Handles automated directory creation and clean symlinking/copying to user runtime directories.

4. `skills/brd/SKILL.md`
   - Valid YAML frontmatter:
     ```yaml
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
       supported: ["prototype", "mvp", "full"]
       default: "mvp"
     ---
     ```
   - Comprehensive instructions embodying the Principal Product Owner persona, operational guardrails, Directive 5 (Scope-Bounded Generation for `prototype`, `mvp`, `full`), cost-aware model tiering directive, context window optimization directive (Directive 4), step-by-step cognitive phases (CoT, ToT, ReAct), and self-rectification routines.

5. `skills/brd/README.md` (Skill-Specific Documentation)
   - Dedicated documentation for the `brd` skill.
   - Explains the AI-PO persona, pure functional scope directives (forbidden vs. mandatory boundaries).
   - Dedicated Scope Boundaries section comparing Prototype, MVP, and Full Enterprise scopes with trigger examples and comparison matrix.
   - Dedicated Model Selection & Cost Optimization Guide with cross-runtime model tier matrix and task-to-model routing flowchart.
   - Dedicated Context Window Management & Token Efficiency section detailing lazy asset loading, subagent context isolation sequence diagram, and line-bounded slicing.
   - Visual Mermaid flowchart and details for the 5-Phase Cognitive Protocol.
   - Reference for the 7 mandatory BRD sections compliant with BABOK v3 and IEEE 29148.
   - Skill-specific installation commands, invocation triggers (`/brd`), validation CLI usage with `--scope` flag, and unit testing instructions.

6. `skills/brd/assets/BRD_SCHEMA.md`
   - Strict standard Business Requirements Document schema with all 7 mandatory sections and `Scope Level` metadata header attribute:
     1. Executive Summary & Business Intent
     2. Stakeholder, Persona & Actor Ecosystem
     3. Functional Domain Taxonomy & Boundaries
     4. Comprehensive Business Use Case Catalog
     5. MVP Scoping & Phased Rollout Matrix
     6. Business Constraints & Governance Guardrails
     7. Refinement & Validation Changelog

7. `skills/brd/scripts/validate_brd.py`
   - Standalone Python 3 linter (using only standard libraries: `re`, `sys`, `pathlib`, `argparse`, `json`) that:
     - Verifies presence of all 7 mandatory sections.
     - Detects and validates Scope Level (`prototype`, `mvp`, `full`).
     - Scans for and warns about technical scope leakage (e.g., SQL, HTTP verbs, container/cloud keywords).
     - Checks for orphaned personas lacking mapped use cases.
     - Validates Given-When-Then Gherkin acceptance criteria in use cases.
     - Supports CLI flags: `--scope {prototype,mvp,full}`, `--strict`, `--json`, and `--quiet`.
     - Exits with status code 0 on success or 1 on structural failure.

8. `tests/test_validate_brd.py`
   - Automated unit test suite verifying `validate_brd.py` across prototype, mvp, and full scope documents, strict mode enforcement, and JSON reporting.

9. `tests/test_registry.py`
   - Automated unit test suite verifying `registry.json` schema validity, skill directory paths, mandatory metadata fields, model configuration structures, context optimization settings, and scope configurations.

Ensure all scripts (`install.sh` and `skills/brd/scripts/validate_brd.py`) are created with executable permissions (`chmod +x`). Execute the creation now.
