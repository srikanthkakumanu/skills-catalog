#!/usr/bin/env python3
"""
Unit tests for the tutorial-author skill's TUTORIAL.md structural validator.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "tutorial-author"
VALIDATOR_PATH = SKILL_DIR / "scripts" / "validate_tutorial.py"
TEMPLATE_PATH = SKILL_DIR / "assets" / "tutorial-template.md"

spec = importlib.util.spec_from_file_location("validate_tutorial", VALIDATOR_PATH)
validate_tutorial = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validate_tutorial
spec.loader.exec_module(validate_tutorial)

VALID = """# Sample Tutorial

<a id="toc"></a>

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Step 1: Add the Endpoint](#step-1-add-the-endpoint)
  - [1.1 Create the Handler](#11-create-the-handler)

## Overview

A short concept.

[Back to top](#toc)

## Prerequisites

- Python 3.11

[Back to top](#toc)

## Step 1: Add the Endpoint

### 1.1 Create the Handler

**Where:** new file `app/handler.py`

```python
def handle():
    return "ok"
```

```bash
python -m app
```

[Back to top](#toc)
"""


class TestValidateTutorial(unittest.TestCase):
    def rules(self, text):
        return [f.rule for f in validate_tutorial.validate(text)]

    def test_valid_tutorial_has_no_findings(self):
        self.assertEqual(validate_tutorial.validate(VALID), [])

    def test_template_passes(self):
        findings = validate_tutorial.validate(TEMPLATE_PATH.read_text(encoding="utf-8"))
        self.assertEqual([str(f) for f in findings], [])

    def test_slugify_matches_github_rules(self):
        self.assertEqual(validate_tutorial.slugify("1.1 Create the Handler"), "11-create-the-handler")
        self.assertEqual(validate_tutorial.slugify("Step 1: Add `foo` & Bar"), "step-1-add-foo--bar")

    def test_missing_toc(self):
        text = VALID.replace("## Table of Contents", "## Contents")
        self.assertIn("toc-missing", self.rules(text))

    def test_missing_toc_anchor(self):
        text = VALID.replace('<a id="toc"></a>', "")
        self.assertIn("toc-anchor", self.rules(text))

    def test_heading_missing_from_toc(self):
        text = VALID.replace("- [Overview](#overview)\n", "")
        self.assertIn("toc-entry", self.rules(text))

    def test_toc_link_to_nothing(self):
        text = VALID.replace("- [Overview](#overview)", "- [Overview](#overview)\n- [Gone](#gone)")
        self.assertIn("toc-link", self.rules(text))

    def test_missing_back_to_top(self):
        text = VALID.replace("- Python 3.11\n\n[Back to top](#toc)", "- Python 3.11")
        findings = [f for f in validate_tutorial.validate(text) if f.rule == "back-to-top"]
        self.assertEqual(len(findings), 1)
        self.assertIn("Prerequisites", findings[0].message)

    def test_untagged_fence(self):
        text = VALID.replace("```bash", "```")
        self.assertIn("fence-language", self.rules(text))

    def test_unclosed_fence(self):
        self.assertIn("fence-unclosed", self.rules(VALID + "\n```text\nnever closed\n"))

    def test_skipped_heading_level(self):
        text = VALID.replace("### 1.1 Create the Handler", "#### 1.1 Create the Handler")
        self.assertIn("heading-skip", self.rules(text))

    def test_multiple_h1(self):
        self.assertIn("single-h1", self.rules(VALID + "\n# Another Title\n"))

    def test_missing_prerequisites_and_steps(self):
        text = VALID.replace("## Prerequisites", "## Requirements").replace("## Step 1:", "## Part 1:")
        rules = self.rules(text)
        self.assertIn("prerequisites", rules)
        self.assertIn("steps", rules)

    def test_headings_inside_code_blocks_are_ignored(self):
        text = VALID.replace('return "ok"', 'return "ok"\n# not a heading')
        self.assertEqual(validate_tutorial.validate(text), [])

    def test_code_change_without_file_label_is_a_warning(self):
        text = VALID.replace("**Where:** new file `app/handler.py`", "Add this code:")
        findings = [f for f in validate_tutorial.validate(text) if f.rule == "file-label"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "warning")

    def test_cli_exit_codes(self):
        self.assertEqual(validate_tutorial.main([str(TEMPLATE_PATH)]), 0)
        self.assertEqual(validate_tutorial.main([str(SKILL_DIR / "missing.md")]), 2)


if __name__ == "__main__":
    unittest.main()
