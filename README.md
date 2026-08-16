# Agent Skills Catalog (`skills-catalog`)

Production-grade Agent Skills Monorepo adhering to the open **Agent Skills Standard**, engineered for cross-runtime compatibility with **Google Antigravity 2.x**, **Claude Code**, and **OpenAI Codex**.

---

## 🚀 Runtime Compatibility Matrix

| Runtime Environment | Target Location | Trigger Mechanism | Status |
| :--- | :--- | :--- | :--- |
| **Google Antigravity 2.x** | `~/.antigravity/skills/` | `/brd`, Slash Command, Natural Language | **Tier 1 Supported** |
| **Claude Code** | `~/.claude/skills/` | `/brd`, Prompt Invocation | **Tier 1 Supported** |
| **OpenAI Codex** | `~/.codex/skills/` | `/brd`, Prompt Invocation | **Tier 1 Supported** |
| **Standalone / CI** | Native CLI (`python3`) | `scripts/validate_brd.py` | **Supported (Python >= 3.9)** |

---

## 📁 Monorepo Architecture

The repository adheres to the standard Agent Skills schema defined in [`registry.json`](file:///Users/skakumanu/practice/skills-catalog/registry.json):

```text
skills-catalog/
├── registry.json                    # Machine-readable Agent Skills manifest
├── install.sh                       # Cross-platform multi-runtime installer
├── README.md                        # Catalog documentation and reference guide
└── skills/
    └── brd/                         # Autonomous Principal Product Owner Skill
        ├── SKILL.md                 # Agent persona, directives, and cognitive protocol
        ├── assets/
        │   └── BRD_SCHEMA.md        # Standard 7-section BABOK/IEEE 29148 BRD schema
        └── scripts/
            └── validate_brd.py      # Standalone zero-dependency Python BRD linter
```

---

## 📦 Installation & Deployment

Deploy skills to your local AI agent runtimes using the automated installer script [`install.sh`](file:///Users/skakumanu/practice/skills-catalog/install.sh).

### Quick Install (All Platforms)

```bash
# Symlink all skills into Antigravity, Claude Code, and Codex runtimes
./install.sh
```

### Targeted Installations

```bash
# Install exclusively for Antigravity 2.x
./install.sh --target antigravity

# Install exclusively for Claude Code
./install.sh --target claude

# Install exclusively for OpenAI Codex
./install.sh --target codex

# Install via file copying instead of symlinks
./install.sh --target all --mode copy

# Force overwrite existing installations
./install.sh --force
```

---

## 🧠 Featured Skill: `brd` (Principal Product Owner)

The [`brd`](file:///Users/skakumanu/practice/skills-catalog/skills/brd/SKILL.md) skill operates as an autonomous **Principal Product Owner & Requirements Engineer (AI-PO)**. It transforms unstructured product concepts into verified, pure **Business Requirements Documents (`BRD.md`)** compliant with **BABOK v3** and **IEEE 29148:2018**.

### Key Capabilities

1. **Strict Pure Functional Scope**: Excludes technical architectures, SQL schemas, API routes, and cloud infrastructure to produce an unambiguous business foundation for downstream engineering.
2. **Multi-Phase Cognitive Protocol**:
   - **Phase 1: Chain of Thought (CoT)**: Elicits a 360° persona ecosystem (End-Users, Ops, Support, Risk/Compliance, Admins) and quantifiable KPIs.
   - **Phase 2: Tree of Thoughts (ToT)**: Evaluates 2–3 competing domain decomposition paths to select the model with minimal functional coupling.
   - **Phase 3: MoSCoW & Flow Synthesis**: Maps use cases with nominal paths, alternate/exception flows, and formal Gherkin Given-When-Then criteria while strictly isolating Phase 1 MVP boundaries.
   - **Phase 4: ReAct Critique Loop**: Self-corrects boundary collisions, orphaned personas, unhandled exceptions, and scope creep.
   - **Phase 5: Markdown Compilation**: Emits [`BRD_SCHEMA.md`](file:///Users/skakumanu/practice/skills-catalog/skills/brd/assets/BRD_SCHEMA.md)-compliant markdown.

### 7 Mandatory BRD Sections

1. **Executive Summary & Business Intent**
2. **Stakeholder, Persona & Actor Ecosystem**
3. **Functional Domain Taxonomy & Boundaries**
4. **Comprehensive Business Use Case Catalog**
5. **MVP Scoping & Phased Rollout Matrix**
6. **Business Constraints & Governance Guardrails**
7. **Refinement & Validation Changelog**

### Invocation Triggers

In Antigravity, Claude Code, or Codex, invoke the skill with:

```text
/brd Create a customer onboarding and identity verification platform
```
or
```text
generate brd for an automated expense reconciliation workflow
```

---

## 🔍 Automated Verification & Linting

Validate any generated `BRD.md` against BABOK and IEEE 29148 standards using the bundled Python 3 linter:

```bash
# Standard validation
python3 skills/brd/scripts/validate_brd.py BRD.md

# Strict validation (fails on any technical scope leakage)
python3 skills/brd/scripts/validate_brd.py BRD.md --strict

# Machine-readable JSON output for CI/CD
python3 skills/brd/scripts/validate_brd.py BRD.md --json
```

---

## 🤝 Contributing New Skills

To add a new skill to `skills-catalog`:
1. Create a new directory under `skills/<skill_name>/`.
2. Add `SKILL.md` with valid YAML frontmatter (`name`, `description`, `license`, `compatibility`).
3. Add any schema specifications under `skills/<skill_name>/assets/`.
4. Add any validation tools or helpers under `skills/<skill_name>/scripts/`.
5. Register the skill in [`registry.json`](file:///Users/skakumanu/practice/skills-catalog/registry.json).

---

## 📄 License

Apache-2.0 © Srikanth Kakumanu
