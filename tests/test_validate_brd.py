#!/usr/bin/env python3
"""
Unit tests for validate_brd.py
"""

import subprocess
import tempfile
import unittest
from pathlib import Path

SAMPLE_VALID_BRD = """# Business Requirements Document: Automated Expense Reconciliation

| Document Attribute | Specification Value |
| :--- | :--- |
| **Document Version** | `1.0.0` |
| **Status** | `Approved` |
| **Author / Lead AI-PO** | Principal Requirements Engineer (`brd` skill) |
| **Business Sponsor** | Finance Operations Group |
| **Last Updated** | 2026-08-16 |
| **Standard Compliance** | BABOK v3, IEEE 29148:2018 |
| **Scope Boundary** | Pure Functional & Business Scope (Zero Technical Leakage) |

## 1. Executive Summary & Business Intent

### 1.1 Problem Statement & Market Opportunity
Manual expense auditing creates severe processing bottlenecks and delays employee reimbursements by an average of 14 business days.

### 1.2 Strategic Alignment & Business Objectives
Streamline financial review workflows, reduce audit cycle times, and enforce automated expense policy compliance.

### 1.3 Key Performance Indicators (KPIs) & Success Metrics

| Metric Identifier | Metric Name | Baseline Value | Target Milestone (MVP) | Target Milestone (Mature) | Measurement Method |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `KPI-001` | Reimbursement Cycle Time | 14 Days | < 48 Hours | < 2 Hours | Timestamp delta from submission to approval |
| `KPI-002` | Audit Discrepancy Rate | 18% | < 5% | < 0.5% | Disputed expense submissions / Total submissions |

## 2. Stakeholder, Persona & Actor Ecosystem

### 2.1 Persona Matrix

| Persona ID | Persona Name | Role Classification | Business JTBD | Primary Pain Points | Authority Level |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PER-001` | Employee Claimant | Primary External | Submit expense claims quickly with digital receipts | Slow reimbursement and unclear rejection reasons | Standard Employee |
| `PER-002` | Expense Auditor | Internal Ops | Review flagged claims and reconcile line items | High volume of repetitive manual verification | Operational Reviewer |
| `PER-003` | Finance Supervisor | Governance & Risk | Approve high-value expense exceptions and oversee budgets | Inadequate audit trail and policy visibility | Management Approver |

## 3. Functional Domain Taxonomy & Boundaries

### 3.1 Domain Decomposition
```text
Domain: Expense Lifecycle
├── L1 Capability 1: Claim Intake & Verification
│   └── L2 Module 1.1: Receipt Ingestion & Data Extraction
└── L1 Capability 2: Audit & Approval Workflow
    └── L2 Module 2.1: Policy Rule Evaluation & Approval Routing
```

### 3.2 Business In-Scope vs. Out-of-Scope Guardrails

| Scope Area | In-Scope (Business Obligations) | Out-of-Scope (Strict Boundaries) | Strategic Rationale |
| :--- | :--- | :--- | :--- |
| **Functional Bounds** | Digital receipt intake, automated policy evaluation | Physical check printing | Focus on digital disbursements |

## 4. Comprehensive Business Use Case Catalog

### UC-101: Submit Expense Claim

| Attribute | Specification |
| :--- | :--- |
| **Use Case ID** | `UC-101` |
| **L1 / L2 Domain** | Claim Intake -> Receipt Ingestion |
| **Primary Actor** | `PER-001` (Employee Claimant) |
| **Secondary Actors** | `PER-002` (Expense Auditor) |
| **Business Priority** | `Must Have` |

#### A. Nominal Business Flow
1. The `PER-001` submits an expense receipt with category and amount.
2. The system verifies claim eligibility against per-diem limits.
3. The claim transitions to `Approved` or routes to `PER-002` if thresholds exceed policy.

#### B. Given-When-Then Acceptance Criteria

```gherkin
Feature: UC-101 - Submit Expense Claim
  Scenario: Claimant submits compliant claim within limits
    Given Claimant PER-001 is an active corporate employee
    And The receipt total is under the single-item policy limit
    When The claimant submits the expense report
    Then The system records the claim in Pending Approval status
```

### UC-102: Conduct Audit Review & Exception Approval

| Attribute | Specification |
| :--- | :--- |
| **Use Case ID** | `UC-102` |
| **L1 / L2 Domain** | Audit Workflow -> Policy Rule Evaluation |
| **Primary Actor** | `PER-002` (Expense Auditor) |
| **Secondary Actors** | `PER-003` (Finance Supervisor) |
| **Business Priority** | `Must Have` |

#### A. Nominal Business Flow
1. `PER-002` reviews flagged items and approves or escalates to `PER-003`.
2. `PER-003` provides final executive authorization.

#### B. Given-When-Then Acceptance Criteria

```gherkin
Feature: UC-102 - Conduct Audit Review
  Scenario: Auditor resolves policy discrepancy
    Given A claim submitted by PER-001 has been flagged for audit
    When Auditor PER-002 reviews and approves the exception with supervisor PER-003
    Then The claim status is updated to Cleared For Payment
```

## 5. MVP Scoping & Phased Rollout Matrix

### 5.1 MoSCoW Feature Allocation Table

| Requirement ID | Capability Description | Persona Beneficiary | MoSCoW Tier | Target Milestone |
| :--- | :--- | :--- | :--- | :--- |
| `REQ-101` | Receipt intake and OCR extraction | `PER-001` | **Must Have** | Phase 1 (MVP) |
| `REQ-102` | Automated policy boundary checking | `PER-002` | **Must Have** | Phase 1 (MVP) |

## 6. Business Constraints & Governance Guardrails

### 6.1 Regulatory & Compliance Constraints
- Adherence to SOX financial auditing and corporate taxation compliance.

### 6.2 Risk Management & Mitigation Matrix

| Risk ID | Identified Business Risk | Severity | Probability | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| `RSK-001` | Inaccurate receipt data extraction | Medium | Low | Human-in-the-loop manual review for ambiguous receipts |

## 7. Refinement & Validation Changelog

### 7.1 Traceability & Persona Coverage Validation
- 100% persona traceability confirmed across all defined use cases.

### 7.2 Version Changelog

| Revision | Date | Author | Summary | Approved By |
| :--- | :--- | :--- | :--- | :--- |
| `1.0.0` | 2026-08-16 | AI-PO (`brd` skill) | Baselined pure business requirements document | Product Council |
"""


class TestBRDValidator(unittest.TestCase):
    def setUp(self):
        self.script_path = Path(__file__).parent.parent / "skills" / "brd" / "scripts" / "validate_brd.py"

    def test_valid_brd_passes_strict(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(SAMPLE_VALID_BRD)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", str(self.script_path), temp_path, "--strict", "--json"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"Validator failed: {result.stdout} {result.stderr}")
        finally:
            Path(temp_path).unlink()

    def test_missing_section_fails(self):
        invalid_brd = SAMPLE_VALID_BRD.replace("## 1. Executive Summary & Business Intent", "## Intro")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(invalid_brd)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", str(self.script_path), temp_path, "--json"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Missing mandatory section", result.stdout)
        finally:
            Path(temp_path).unlink()

    def test_technical_leakage_detected_in_strict(self):
        leaked_brd = SAMPLE_VALID_BRD + "\n\nData is saved in PostgreSQL database via POST /api/v1/expenses"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(leaked_brd)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", str(self.script_path), temp_path, "--strict", "--json"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("technical scope leakage", result.stdout.lower())
        finally:
            Path(temp_path).unlink()


if __name__ == "__main__":
    unittest.main()
