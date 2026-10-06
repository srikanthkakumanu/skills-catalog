#!/usr/bin/env python3
"""
Unit tests for the teach-me skill's lesson validator (Markdown and HTML) and PDF helper.
"""

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "teach-me"
MD_TEMPLATE_PATH = SKILL_DIR / "assets" / "lesson-template.md"
HTML_TEMPLATE_PATH = SKILL_DIR / "assets" / "lesson-template.html"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SKILL_DIR / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validate_lesson = load("validate_lesson")
html_to_pdf = load("html_to_pdf")

VALID_MD = """# Sample Lesson

<a id="toc"></a>

## Table of Contents

- [Before You Start](#before-you-start)
- [1. Basics](#1-basics)
  - [1.1 First Idea](#11-first-idea)
    - [1.1.1 A Detail](#111-a-detail)
- [Sources](#sources)

## Before You Start

Nothing needed.

[Back to top](#toc)

## 1. Basics

### 1.1 First Idea

Create `app/hello.py`:

```python
print("hello")
```

> [!NOTE]
> Easy to miss.

#### 1.1.1 A Detail

More detail.

[Back to top](#toc)

## Sources

- [Docs](https://example.com)

[Back to top](#toc)
"""

VALID_HTML = """<!doctype html>
<html lang="en"><head><title>Sample</title></head>
<body>
<header id="top"><h1>Sample Lesson</h1></header>
<nav id="toc">
  <ol>
    <li><a href="#basics">1. Basics</a>
      <ol>
        <li><a href="#first-idea">1.1 First Idea</a>
          <ol><li><a href="#a-detail">1.1.1 A Detail</a></li></ol>
        </li>
      </ol>
    </li>
    <li><a href="#sources">Sources</a></li>
  </ol>
</nav>
<main>
<h2 id="basics">1. Basics</h2>
<h3 id="first-idea">1.1 First Idea</h3>
<pre><code class="language-python">print("hello")</code></pre>
<aside class="callout callout-note"><svg><use href="#i-note"/></svg><p>Easy to miss.</p></aside>
<h4 id="a-detail">1.1.1 A Detail</h4>
<p>More detail.</p>
<p><a class="back-to-top" href="#top">Back to top</a></p>
<h2 id="sources">Sources</h2>
<p><a class="back-to-top" href="#top">Back to top</a></p>
</main>
</body></html>
"""


class TestValidateMarkdownLesson(unittest.TestCase):
    def rules(self, text):
        return [f.rule for f in validate_lesson.validate(text)]

    def test_valid_lesson_has_no_findings(self):
        self.assertEqual(validate_lesson.validate(VALID_MD), [])

    def test_template_passes(self):
        findings = validate_lesson.validate(MD_TEMPLATE_PATH.read_text(encoding="utf-8"))
        self.assertEqual([str(f) for f in findings], [])

    def test_missing_toc(self):
        text = VALID_MD.replace("## Table of Contents", "## Contents")
        self.assertIn("toc-missing", self.rules(text))

    def test_missing_toc_anchor(self):
        text = VALID_MD.replace('<a id="toc"></a>', "")
        self.assertIn("toc-anchor", self.rules(text))

    def test_sub_sub_topic_missing_from_toc(self):
        text = VALID_MD.replace("    - [1.1.1 A Detail](#111-a-detail)\n", "")
        findings = [f for f in validate_lesson.validate(text) if f.rule == "toc-entry"]
        self.assertEqual(len(findings), 1)
        self.assertIn("1.1.1 A Detail", findings[0].message)

    def test_toc_link_to_nothing(self):
        text = VALID_MD.replace("- [Sources](#sources)", "- [Sources](#sources)\n- [Gone](#gone)")
        self.assertIn("toc-link", self.rules(text))

    def test_toc_entry_at_wrong_depth(self):
        text = VALID_MD.replace("  - [1.1 First Idea]", "- [1.1 First Idea]")
        self.assertIn("toc-nesting", self.rules(text))

    def test_toc_out_of_order(self):
        text = VALID_MD.replace("- [Before You Start](#before-you-start)\n", "").replace(
            "- [Sources](#sources)", "- [Sources](#sources)\n- [Before You Start](#before-you-start)"
        )
        self.assertIn("toc-order", self.rules(text))

    def test_missing_back_to_top_on_sub_sub_topic(self):
        text = VALID_MD.replace("More detail.\n\n[Back to top](#toc)", "More detail.")
        sections = [f.message for f in validate_lesson.validate(text) if f.rule == "back-to-top"]
        # The last child closes its parents too, so all three levels are reported.
        self.assertEqual(len(sections), 3)

    def test_broken_in_page_link(self):
        text = VALID_MD.replace("More detail.", "More detail, see [here](#nowhere).")
        self.assertIn("link-target", self.rules(text))

    def test_untagged_and_unclosed_fences(self):
        self.assertIn("code-language", self.rules(VALID_MD.replace("```python", "```")))
        self.assertIn("fence-unclosed", self.rules(VALID_MD + "\n```text\nnever closed\n"))

    def test_skipped_heading_level_and_multiple_h1(self):
        self.assertIn("heading-skip", self.rules(VALID_MD.replace("### 1.1", "#### 1.1")))
        self.assertIn("single-h1", self.rules(VALID_MD + "\n# Another Title\n"))

    def test_emoji_in_heading(self):
        text = VALID_MD.replace("## 1. Basics", "## 1. Basics \U0001f680")
        self.assertIn("heading-emoji", self.rules(text))

    def test_unknown_callout_type(self):
        self.assertIn("callout-type", self.rules(VALID_MD.replace("[!NOTE]", "[!HELP]")))

    def test_missing_sources_is_a_warning(self):
        text = VALID_MD.replace("## Sources", "## Links").replace("(#sources)", "(#links)")
        findings = validate_lesson.validate(text)
        self.assertEqual([(f.rule, f.severity) for f in findings], [("sources", "warning")])

    def test_headings_inside_code_blocks_are_ignored(self):
        text = VALID_MD.replace('print("hello")', 'print("hello")\n# not a heading')
        self.assertEqual(validate_lesson.validate(text), [])


class TestValidateHtmlLesson(unittest.TestCase):
    def rules(self, text):
        return [f.rule for f in validate_lesson.validate(text, "html")]

    def test_valid_lesson_has_no_findings(self):
        self.assertEqual(validate_lesson.validate(VALID_HTML, "html"), [])

    def test_template_passes(self):
        findings = validate_lesson.validate(HTML_TEMPLATE_PATH.read_text(encoding="utf-8"), "html")
        self.assertEqual([str(f) for f in findings], [])

    def test_missing_toc(self):
        self.assertIn("toc-missing", self.rules(VALID_HTML.replace('<nav id="toc">', "<nav>")))

    def test_heading_missing_from_toc(self):
        text = VALID_HTML.replace('<li><a href="#sources">Sources</a></li>', "")
        self.assertIn("toc-entry", self.rules(text))

    def test_toc_link_to_nothing(self):
        text = VALID_HTML.replace('href="#sources">Sources</a></li>', 'href="#gone">Gone</a></li>')
        self.assertIn("toc-link", self.rules(text))

    def test_toc_entry_at_wrong_depth(self):
        text = VALID_HTML.replace(
            '<ol><li><a href="#a-detail">1.1.1 A Detail</a></li></ol>', ""
        ).replace(
            '<li><a href="#sources">', '<li><a href="#a-detail">1.1.1 A Detail</a></li><li><a href="#sources">'
        )
        self.assertIn("toc-nesting", self.rules(text))

    def test_missing_back_to_top(self):
        text = VALID_HTML.replace(
            '<p>More detail.</p>\n<p><a class="back-to-top" href="#top">Back to top</a></p>',
            "<p>More detail.</p>",
        )
        self.assertEqual(self.rules(text).count("back-to-top"), 3)

    def test_heading_without_id_and_duplicate_id(self):
        self.assertIn("heading-id", self.rules(VALID_HTML.replace('<h2 id="sources">', "<h2>")))
        self.assertIn("duplicate-id", self.rules(VALID_HTML.replace('id="sources"', 'id="basics"')))

    def test_code_block_without_language(self):
        self.assertIn("code-language", self.rules(VALID_HTML.replace(' class="language-python"', "")))

    def test_callout_without_icon_or_type(self):
        no_icon = VALID_HTML.replace('<svg><use href="#i-note"/></svg>', "")
        self.assertIn("callout-icon", self.rules(no_icon))
        self.assertIn("callout-type", self.rules(VALID_HTML.replace(" callout-note", "")))

    def test_broken_in_page_link(self):
        text = VALID_HTML.replace("<p>More detail.</p>", '<p><a href="#nowhere">More</a></p>')
        self.assertIn("link-target", self.rules(text))


class TestCommandLines(unittest.TestCase):
    def test_validator_exit_codes_and_format_detection(self):
        self.assertEqual(validate_lesson.main([str(MD_TEMPLATE_PATH)]), 0)
        self.assertEqual(validate_lesson.main([str(HTML_TEMPLATE_PATH)]), 0)
        self.assertEqual(validate_lesson.main([str(SKILL_DIR / "missing.md")]), 2)
        self.assertEqual(validate_lesson.detect_format(Path("lesson.HTML")), "html")
        self.assertEqual(validate_lesson.detect_format(Path("lesson.md")), "md")

    def test_pdf_helper_reports_missing_input(self):
        self.assertEqual(html_to_pdf.main([str(SKILL_DIR / "missing.html")]), 2)

    def test_pdf_helper_reports_no_converter(self):
        with mock.patch.object(html_to_pdf, "available_converters", return_value=[]):
            self.assertEqual(html_to_pdf.main([str(HTML_TEMPLATE_PATH)]), 3)

    def test_pdf_helper_falls_through_failed_converters(self):
        def broken(source, output):
            raise RuntimeError("boom")

        with mock.patch.object(html_to_pdf, "available_converters", return_value=[("x", broken)]):
            self.assertEqual(html_to_pdf.main([str(HTML_TEMPLATE_PATH)]), 1)


if __name__ == "__main__":
    unittest.main()
