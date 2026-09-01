# Minimal Business Requirements Document (BRD) Schema

This specification defines the minimal, lightweight 4-section structure for Business Requirements Documents produced under the `brd` Agent Skill using the **`minimal` scope**. Minimal BRDs focus on rapid, lean requirements without KPIs, RACI matrices, MoSCoW phasing, governance matrices, or regulatory compliance detail — suitable for throwaway prototypes, quick concept validation, or internal workflow documentation. Generated documents must strictly adhere to this 4-section structure while maintaining pure business/functional scope in accordance with BABOK Guide v3 and IEEE 29148:2018 principles.

---

## Document Metadata Header

Every minimal BRD markdown file must begin with the following metadata header table:

```markdown
# Business Requirements Document: [Product / Initiative Name]

| Document Attribute | Specification Value |
| :--- | :--- |
| **Document Version** | `1.0.0` (or semantic version) |
| **Status** | `Draft` \| `In Review` \| `Approved` |
| **Scope Level** | `Minimal` |
| **Author / Lead AI-PO** | Principal Requirements Engineer (`brd` skill) |
| **Business Sponsor / Owner** | [Target Business Unit / Executive Sponsor] |
| **Last Updated** | [YYYY-MM-DD] |
| **Standard Compliance** | BABOK v3, IEEE 29148:2018 (Lightweight Mode) |
| **Scope Boundary** | Pure Functional & Business Scope (Zero Technical Leakage) |
```

---

## 1. Domain & Module Taxonomy

### 1.1 Domain Decomposition (Lightweight Hierarchy)
A lightweight hierarchical decomposition of the business domain into logical domains, modules, and submodules without explicit L1/L2 capability identification or KPI mappings.

```text
Domain: [Core Business Ecosystem]
├── Module 1: [e.g., User Onboarding]
│   ├── Submodule 1.1: [e.g., Profile Creation]
│   └── Submodule 1.2: [e.g., Credential Validation]
└── Module 2: [e.g., Transaction Processing]
    ├── Submodule 2.1: [e.g., Request Submission]
    └── Submodule 2.2: [e.g., Confirmation & Notification]
```

### 1.2 Functional Scope Boundaries (In-Scope vs. Out-of-Scope)

| Area | In-Scope | Out-of-Scope | Rationale |
| :--- | :--- | :--- | :--- |
| [e.g., User Authentication] | [Explicit features included] | [Explicit features excluded] | [Why this boundary is drawn] |

---

## 2. Personas

### 2.1 Actor / Persona Roster

| Persona ID | Persona Name | Role | Jobs-To-Be-Done (JTBD) | Pain Points | Authority Level |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PER-001` | [e.g., Direct User] | Primary | [Core goal to accomplish] | [Current friction/blocker] | [Access level] |
| `PER-002` | [e.g., Support Agent] | Support | [Back-office goal] | [Operational challenge] | [Access level] |

---

## 3. Use Case Catalog

Every use case must follow a minimal, standardized specification template.

### Specification Template for Use Cases:

```markdown
### UC-[XXX]: [Descriptive Action-Oriented Title]

| Attribute | Specification |
| :--- | :--- |
| **Use Case ID** | `UC-[XXX]` (e.g., `UC-101`) |
| **Primary Actor** | `PER-[XXX]` ([Persona Name]) |
| **Module / Submodule** | [Parent Module → Submodule] |

#### Main Flow (Happy Path) — 3 Steps Max
1. [Actor initiates]; system validates conditions.
2. System executes core action; records outcome.
3. System confirms completion and notifies actor.

#### Exception Flows — One Line Each
- **E1: [Exception Name]** — [Trigger] → [Behavior outcome]
- **E2: [Exception Name]** — [Trigger] → [Behavior outcome]

#### Acceptance Criteria (Gherkin) — 3 Lines Per Scenario

```gherkin
Feature: UC-[XXX] - [Title]

  Scenario: Nominal execution
    Given [Preconditions], When [Actor initiates], Then [System transitions to success state]

  Scenario: Exception handling
    Given [Out-of-bounds input], When [Validation fails], Then [System rejects; no state change]
```
```

---

## 4. Mapping Matrix

A single traceability table linking Personas, Domains/Modules, and Use Cases to ensure coverage and identify orphaned actors or disconnected capabilities.

| Domain / Module | Persona ID | Persona Name | Primary Use Case | Supporting Use Cases | Coverage Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [Module 1] | `PER-001` | [Name] | `UC-101` | `UC-102`, `UC-103` | Primary workflow |
| [Module 1] | `PER-002` | [Name] | `UC-104` | — | Exception handling only |
| [Module 2] | `PER-001` | [Name] | `UC-105` | — | Secondary flow |

### Validation Notes
- **Persona Coverage**: Verify every declared persona in Section 2 maps to at least one use case.
- **Module Coverage**: Verify every module/submodule in Section 1 is referenced in at least one use case.
- **Use Case Traceability**: Verify every use case in Section 3 is mapped to at least one persona and one module.

---
