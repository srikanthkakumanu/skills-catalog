# Agent Skills Catalog (`skills-catalog`)

[![Standard](<https://img.shields.io/badge/Standard-Agent%20Skills%20Spec-blue.svg>)](file:///Users/skakumanu/practice/skills-catalog/registry.json)
[![Runtimes](<https://img.shields.io/badge/Runtimes-Antigravity%20%7C%20Claude%20%7C%20Codex-purple.svg>)](#-runtime-compatibility-matrix)
[![Cost Optimization](<https://img.shields.io/badge/Model%20Routing-Cost%20Tiered-brightgreen.svg>)](#-model-selection--cost-optimization-framework)
[![Context Management](<https://img.shields.io/badge/Context%20Window-Optimized%20Budget-orange.svg>)](#-context-window-management--token-efficiency-standard)
[![License](<https://img.shields.io/badge/License-Apache%202.0-green.svg>)](file:///Users/skakumanu/practice/skills-catalog/LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](#-testing--quality-assurance)

A curated, production-grade monorepo of modular **Agent Skills** engineered for cross-runtime execution across **Google Antigravity 2.x**, **Claude Code**, and **OpenAI Codex**, complying with the open **Agent Skills Standard**.

---

## 📑 Table of Contents

- [Overview &amp; Architecture](#-overview--architecture)
- [Runtime Compatibility Matrix](#-runtime-compatibility-matrix)
- [Available Skills](#-available-skills)
- [⚡ Model Selection &amp; Cost Optimization Framework](#-model-selection--cost-optimization-framework)
- [🧠 Context Window Management &amp; Token Efficiency Standard](#-context-window-management--token-efficiency-standard)
- [Installation &amp; Deployment](#-installation--deployment)
- [Agent Skills Standard Specification](#-agent-skills-standard-specification)
- [Central Registry (`registry.json`)](#-central-registry-registryjson)
- [Testing &amp; Quality Assurance](#-testing--quality-assurance)
- [Authoring &amp; Contributing Skills](#-authoring--contributing-skills)
- [License](#-license)

---

## 🧭 Overview & Architecture

The **Agent Skills Catalog** provides a standardized, runtime-agnostic collection of domain-expert AI agent skills. Each skill encapsulates autonomous cognitive workflows, prime directives, output schemas, validation linters, model tier routing, and verification test suites.

### Monorepo Structure

```text
skills-catalog/
├── registry.json                    # Central catalog manifest & machine-readable registry
├── install.sh                       # Multi-runtime CLI installer (symlink / copy modes)
├── README.md                        # Catalog-wide overview and documentation (this file)
├── skills/                          # Modular agent skills directory
│   └── <skill_name>/                # Individual skill package
│       ├── SKILL.md                 # Agent persona, directives, and cognitive execution protocol
│       ├── README.md                # Dedicated skill documentation, model guide, and context specs
│       ├── assets/                  # Templates, output schemas, and reference assets
│       └── scripts/                 # Standalone validation linters and helper utilities
└── tests/                           # Catalog-wide automated test suite
    ├── test_registry.py             # Manifest, context standards, and skill metadata validation
    └── test_validate_<skill>.py     # Unit tests for skill validators
```

---

## 🚀 Runtime Compatibility Matrix

All skills in this catalog are designed for zero-friction cross-runtime compatibility:

| Runtime Environment              | Target Installation Path                                          | Discovery & Trigger Mechanism                                   | Status                              |
| :------------------------------- | :---------------------------------------------------------------- | :-------------------------------------------------------------- | :---------------------------------- |
| **Google Antigravity 2.x** | `~/.antigravity/skills/<skill>/` or `.agents/skills/<skill>/` | Slash commands (`/<skill>`), Natural Language, Auto-Discovery | **Tier 1 Supported**          |
| **Claude Code**            | `~/.claude/skills/<skill>/`                                     | Slash commands (`/<skill>`), Prompt Invocation                | **Tier 1 Supported**          |
| **OpenAI Codex**           | `~/.codex/skills/<skill>/`                                      | Slash commands (`/<skill>`), Prompt Invocation                | **Tier 1 Supported**          |
| **Standalone / CI**        | Native CLI (`python3`)                                          | Direct script execution, GitHub Actions / CI runners            | **Supported (Python >= 3.9)** |

---

## 📚 Available Skills

Each skill in the catalog is self-contained and documented with its own dedicated `README.md`:

| Skill                                                                                                       | Version   | Description                                                                                                                                                                                                                                                                                                  | Target Runtimes            | Cost & Context Profile                                                 | Dedicated Documentation                                                                                                                         |
| :---------------------------------------------------------------------------------------------------------- | :-------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------- | :--------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| [`brd`](file:///Users/skakumanu/practice/skills-catalog/skills/brd/)                                       | `1.0.0` | Produces a compact Business Requirements Document — domain, personas, use cases with happy/negative paths and acceptance criteria, scope boundaries, and self-checks for framing claims, contradictions, and orphaned scope items. Pure functional scope: WHAT and WHO, never HOW.                                                                      | Antigravity, Claude, Codex | Lightweight Single-Pass                     | [**`skills/brd/README.md`**](file:///Users/skakumanu/practice/skills-catalog/skills/brd/README.md)                                       |
| [`req-nfr-analysis`](file:///Users/skakumanu/practice/skills-catalog/skills/req-nfr-analysis/)             | `1.0.0`   | Normalizes a BRD's functional requirements and tags NFRs across 10 categories (Performance & Scalability, Reliability & Recovery, Security, Compliance & Data Governance, Usability & Accessibility, Maintainability & Portability, Observability, Transparency/Explainability, Cost, Other), flags contradictions and unsupported claims, prioritizes as hard-constraint or nice-to-have.       | Antigravity, Claude, Codex | Lightweight Single-Pass | [**`skills/req-nfr-analysis/README.md`**](file:///Users/skakumanu/practice/skills-catalog/skills/req-nfr-analysis/README.md)             |
| [`architecture-decisions`](file:///Users/skakumanu/practice/skills-catalog/skills/architecture-decisions/) | `1.0.0` | Decides architecture style and agentic-AI fitness from normalized requirements, produces MADR-formatted ADRs, gated behind mandatory confirmation checkpoint. "Not applicable" is valid when no agentic capability is evidenced. | Antigravity, Claude, Codex | Lightweight Single-Pass + Checkpoint Gate       | [**`skills/architecture-decisions/README.md`**](file:///Users/skakumanu/practice/skills-catalog/skills/architecture-decisions/README.md) |
| [`detailed-design`](file:///Users/skakumanu/practice/skills-catalog/skills/detailed-design/)               | `1.0.0` | Turns confirmed architecture decisions into bounded contexts, design pattern selection, data architecture, API contracts, and security model. Traces every hard-constraint NFR to a design decision or flags it unaddressed. Refuses to run against unconfirmed ADRs. | Antigravity, Claude, Codex | Lightweight Single-Pass + Checkpoint Guard | [**`skills/detailed-design/README.md`**](file:///Users/skakumanu/practice/skills-catalog/skills/detailed-design/README.md)                 |
| [`tech-stack`](file:///Users/skakumanu/practice/skills-catalog/skills/tech-stack/)                       | `1.0.0` | Selects full-stack technology choices per bounded context from detailed design, citing catalog playbooks where they fit or presenting tradeoff options with a mandatory confirmation checkpoint. Never decides off-catalog stacks unilaterally. | Antigravity, Claude, Codex | Lightweight Single-Pass + Playbook-First | [**`skills/tech-stack/README.md`**](file:///Users/skakumanu/practice/skills-catalog/skills/tech-stack/README.md)                           |
| [`prd`](file:///Users/skakumanu/practice/skills-catalog/skills/prd/)                                   | `1.0.0` | Assembles a Product Requirements Document by pulling confirmed sections from all five upstream documents per a section manifest. No new judgments — pure assembly only. Aggregates all unresolved items (pending, open questions, structural findings) into one Open Items section. | Antigravity, Claude, Codex | Lightweight Single-Pass + Assembly | [**`skills/prd/README.md`**](file:///Users/skakumanu/practice/skills-catalog/skills/prd/README.md)                                       |

*(Additional skills can be authored and added following the [Contribution Guide](#-authoring--contributing-skills).)*

---

## ⚡ Design Principles: Lightweight Single-Pass & Assembly-Based Workflows

The six-phase pipeline prioritizes **focused decision-making** over heavyweight multi-phase reasoning. Each skill is designed as a **single-pass, lightweight process** that:

1. **Consumes upstream outputs** — Takes confirmed decisions from prior phases as input
2. **Produces focused output** — Delivers one specific artifact per skill
3. **Enforces checkpoints** — Uses mandatory confirmation gates for pending decisions
4. **Avoids redundant reasoning** — Each phase builds on prior work, never re-decides
5. **Stays in scope** — Executes only the directives it's responsible for

### Cost & Context Efficiency

- **No multi-scope complexity** — Each skill is a single, focused workflow (not minimal/prototype/mvp/full variants)
- **No model tiering** — Skills are designed to be efficient regardless of model tier
- **Single-pass execution** — No re-derivation loops or costly re-reasoning cycles
- **Assembly-based thinking** — Phases 1-5 make decisions; Phase 6 assembles them (no new judgments)

This approach minimizes cognitive load on both AI and human stakeholders, reducing decision fatigue and token expenditure.

---

## 🧠 Context Window Management & Token Efficiency Standard

Each skill is designed to minimize context overhead:

- **Compact SKILL.md** — Directives fit on one screen; references are links, not inlined
- **Clear input/output** — Each skill knows exactly what it consumes and produces
- **No re-reading** — Upstream decisions are trusted; confirmed items are never re-analyzed
- **No optional states** — No scope variants or model-dependent branches; one workflow per skill
- **Checkpoint gates** — Pending decisions stop execution, preventing speculative processing

This results in predictable, low-overhead execution: read upstream output once, apply directives, produce output, move to next phase.

---

## 📦 Installation & Deployment

Deploy skills from this catalog to your local AI agent runtimes using the automated installer script [`install.sh`](file:///Users/skakumanu/practice/skills-catalog/install.sh).

### Quick Start

```bash
# Install all 6 skills to all supported runtimes (symlinks)
./install.sh

# Install all skills via file copy (recommended if symlinks don't work)
./install.sh --mode copy

# Force-reinstall all skills (overwrites existing installations)
./install.sh --force
```

### Targeted Installations

```bash
# Install all skills to a specific runtime
./install.sh --target claude          # Claude Code only
./install.sh --target antigravity     # Google Antigravity only
./install.sh --target codex           # OpenAI Codex only

# Install a single skill (e.g., 'brd') to all runtimes
./install.sh --skill brd

# Install a single skill to a specific runtime
./install.sh --skill brd --target claude

# Force-reinstall a specific skill (overwrites)
./install.sh --skill brd --force

# Install via file copy to a specific runtime
./install.sh --skill detailed-design --target claude --mode copy
```

### Common Installation Scenarios

| Scenario                                           | Command                                              |
| :------------------------------------------------- | :--------------------------------------------------- |
| First-time setup (all skills, all runtimes)      | `./install.sh --mode copy`                        |
| Update a single skill after edits                 | `./install.sh --skill <name> --force`             |
| Reinstall everything from scratch                 | `./install.sh --force --mode copy`                |
| Install only for Claude Code                      | `./install.sh --target claude`                    |
| Troubleshoot: use copy mode instead of symlinks   | `./install.sh --mode copy --force`                |

### CLI Installer Options Reference

| Flag                 | Argument                                              | Description                                            | Default     |
| :------------------- | :---------------------------------------------------- | :----------------------------------------------------- | :---------- |
| `-t`, `--target` | `antigravity` \| `claude` \| `codex` \| `all` | Target runtime environment                             | `all`     |
| `-m`, `--mode`   | `symlink` \| `copy`                               | Installation method (symlink or file copy)             | `symlink` |
| `-s`, `--skill`  | `<skill_name>` \| `all`                           | Specific skill to deploy or `all`                      | `all`     |
| `-f`, `--force`  | (None)                                                | Force-overwrite existing installations                 | `false`   |
| `-h`, `--help`   | (None)                                                | Display full help and usage details                    |             |

### Installation Locations

Skills are installed to these standard locations:

- **Claude Code**: `~/.claude/skills/<skill_name>/`
- **Google Antigravity**: `~/.antigravity/skills/<skill_name>/` or `.agents/skills/<skill_name>/`
- **OpenAI Codex**: `~/.codex/skills/<skill_name>/`

---

## 📐 Agent Skills Standard Specification

Each skill in `skills/<skill_name>/` follows the standardized Agent Skills anatomy:

1. **`SKILL.md` (Required Entrypoint)**:
   - Contains YAML frontmatter metadata (`name`, `description`, `license`, `compatibility`).
   - Defines agent persona, behavioral boundaries, and prime directives.
   - Skills are intentionally simplified: one workflow per skill, no scopes/models/context_optimization variants.
2. **`README.md` (Required Documentation)**:
   - Complete reference manual for the specific skill, explaining role, input/output, process steps, and when to use it.
3. **`assets/` (Optional Resources)**:
   - Houses templates, schemas, reference examples, and architectural diagrams (loaded on-demand by skills).
4. **`scripts/` (Optional Tooling)**:
   - Standalone utilities and validators (e.g., zero-dependency Python scripts).

### Standard YAML Frontmatter Example (Simplified)

```yaml
---
name: sample-skill
description: What the skill does and when to trigger it.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
```

**Note:** The current catalog skills use this simplified frontmatter. Optional extensions like `models`, `scopes`, or `context_optimization` can be added to individual skills when needed, but are not required.

---

## 🗂️ Central Registry (`registry.json`)

The catalog maintains a centralized, machine-readable manifest at [`registry.json`](file:///Users/skakumanu/practice/skills-catalog/registry.json) for automated indexing, tooling, and package discovery:

```json
{
  "$schema": "https://agentskills.io/schema/registry.json",
  "name": "skills-catalog",
  "version": "1.0.0",
  "compatibility": {
    "antigravity": ">=2.0.0",
    "claude_code": ">=1.0.0",
    "codex": ">=1.0.0",
    "python": ">=3.9"
  },
  "context_standards": {
    "progressive_loading": true,
    "subagent_isolation": true,
    "targeted_file_slicing": true,
    "compact_tool_outputs": true
  },
  "skills": [
    {
      "name": "brd",
      "version": "1.0.0",
      "path": "skills/brd",
      "entrypoint": "SKILL.md",
      "readme": "README.md",
      "description": "Produces a compact Business Requirements Document — domain, personas, use cases with happy/negative paths and acceptance criteria, and in/out-of-scope boundaries — with a mandatory self-check for unsupported framing claims, contradictions, and orphaned scope items. Pure functional scope: WHAT and WHO, never HOW.",
      "triggers": ["/brd", "generate brd", "create business requirements", "draft brd", "business requirements document", "requirements analysis"],
      "runtimes": ["antigravity", "claude", "codex"],
      "tags": ["requirements-engineering", "product-management", "bakok", "ieee-29148", "business-analysis", "pure-functional-spec"],
      "license": "Apache-2.0"
    }
  ]
}
```

---

## 🧪 Testing & Quality Assurance

All skills, registry schemas, and validators within the catalog are tested and linted. You can use the **`uv` package manager** or standard Python:

### Using `uv` (Recommended)

```bash
# Run full test suite with pytest via uv
uv run pytest

# Run fast code linting via ruff
uv run ruff check .

# Run native unittest discovery via uv
uv run python -m unittest discover tests
```

### Using Native Python CLI

```bash
# Run all unit test suites across the catalog
python3 -m unittest discover tests

# Run registry and context validation tests
python3 -m unittest tests/test_registry.py
```

---

## 🤝 Authoring & Contributing Skills

To contribute or add a new skill to `skills-catalog`:

1. **Create Skill Directory**:
   ```bash
   mkdir -p skills/<new_skill>/assets skills/<new_skill>/scripts
   ```

2. **Author `SKILL.md`**:
   - Add YAML frontmatter: `name`, `description`, `license`, `compatibility`
   - Define directives (behavioral rules) and the skill's execution process
   - Keep it focused: one workflow per skill, no scope variants
   - Example:
     ```yaml
     ---
     name: my-skill
     description: What this skill does and when to invoke it.
     license: Apache-2.0
     compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
     ---
     # My Skill
     
     ## Directives
     1. [directive 1]
     2. [directive 2]
     ...
     
     ## Process
     [step 1] → [step 2] → ... → Output
     ```

3. **Author `README.md`**:
   - Comprehensive reference: Overview, What It Does, Input/Output, How It Works, When to Use
   - Include installation instructions with skill-specific examples
   - Link to upstream/downstream skills in the pipeline

4. **Add Assets & Schemas** (optional):
   - Place templates and schemas under `skills/<new_skill>/assets/`
   - Load on-demand in the skill, not inline in SKILL.md

5. **Add Tests** (optional):
   - Standalone validators under `skills/<new_skill>/scripts/`
   - Unit tests in `tests/test_validate_<new_skill>.py`

6. **Register in `registry.json`**:
   - Add skill entry with: name, version, path, entrypoint, readme, description, triggers, runtimes, tags, license
   - Example:
     ```json
     {
       "name": "my-skill",
       "version": "1.0.0",
       "path": "skills/my-skill",
       "entrypoint": "SKILL.md",
       "readme": "README.md",
       "description": "...",
       "triggers": ["/my-skill", "invoke my skill"],
       "runtimes": ["antigravity", "claude", "codex"],
       "tags": ["tag1", "tag2"],
       "license": "Apache-2.0"
     }
     ```

7. **Update This Catalog**:
   - Add a row for the new skill in the [Available Skills](#-available-skills) table above
   - Run tests to ensure everything passes: `python3 -m unittest discover tests`

---

## 📄 License

Apache-2.0 © [Srikanth Kakumanu](https://github.com/srikanthkakumanu)
