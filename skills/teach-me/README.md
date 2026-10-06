# Teach Me Skill

**Version:** 1.0.0 | **Status:** Supported | **License:** Apache-2.0

**Researches any topic and teaches it in simple English as one ordered, structurally checked lesson — in HTML, PDF, or Markdown.**

## Overview

Say "teach me <topic>" and this skill produces a single lesson document you can read from top to bottom. It researches the topic first, arranges it into topics, sub-topics, and sub-sub-topics in the order a learner should meet them, and then explains each part with easy examples.

It is built for technical topics (a framework, a protocol, a tool, a language feature) but works for any topic: code, configuration, and file lists appear only where the topic has them.

**How it differs from [`tutorial-author`](../tutorial-author/README.md):** `tutorial-author` walks you through *building one specific thing*, step by step, to a working result. `teach-me` *explains a topic* so you understand it, and uses code and configuration as illustrations along the way.

## What It Does

1. **Researches the topic** — web search and official documentation when the runtime has them, the current repository when the topic is about it. The lesson says when no research was possible, and ends with the sources used.
2. **Builds an ordered outline** — topics, sub-topics, and sub-sub-topics, each relying only on what came before.
3. **Asks you once, before writing** — which of the related topics it found should be included, which format you want (HTML, PDF, or Markdown), and where to save the file (default `docs/<topic-slug>.<ext>`).
4. **Writes in simple English** — short sentences, everyday words, every term explained on first use.
5. **Keeps it the right size** — each sub-topic properly explained, nothing padded; proposes splitting into parts when a topic is too big for one read.
6. **Shows easy examples in order** — code labelled with its file, configuration with file, key, value, and before/after.
7. **Lists the files to create or modify** — per topic, plus one combined "Files at a Glance" table.
8. **Puts best practices where they belong** — inside the relevant topic, each with its own example, never as a list at the end.
9. **Adds Note, Warning, and Help callouts** with icons, only where they help.
10. **Builds a nested table of contents** and a **back-to-top link** at every topic, sub-topic, and sub-sub-topic.
11. **Self-checks** — runs the bundled validator and fixes findings before delivering.

## Input

Any topic, for example:

- A technology or concept ("teach me Kubernetes Ingress")
- A language or tool feature ("explain Java virtual threads")
- Something in the current repository ("teach me how this catalog's registry works")
- A non-technical subject ("help me learn how compound interest works")

Optional: your level, the format, the save location. Anything you give up front is not asked again.

## Output

```text
# Topic Title
> One-line promise · Level · Reading time · Researched

## Table of Contents            (nested: topic → sub-topic → sub-sub-topic)
## Before You Start
   ### What You Will Learn
   ### What You Need
   ### Files at a Glance         (technical topics only)
## 1. <Topic>
   ### 1.1 <Sub-topic>           (explanation, example, files, best practice, callouts)
      #### 1.1.1 <Sub-sub-topic> (only when needed)
## N. <Topic>
## Summary                       (key ideas, where to go next)
## Sources
```

| Format | What you get |
| :-- | :-- |
| **Markdown** | GitHub-flavoured Markdown with `> [!NOTE]`, `> [!TIP]`, `> [!WARNING]` callouts. Skeleton: [`assets/lesson-template.md`](assets/lesson-template.md) |
| **HTML** | One self-contained file: Inter and JetBrains Mono fonts with system fallbacks, inline SVG icons (Lucide), light and dark themes with a toggle, a table of contents that stays in view on wide screens and one tap away on phones, highlighted code blocks with a copy button, and print styles. Skeleton: [`assets/lesson-template.html`](assets/lesson-template.html) |
| **PDF** | Made from the HTML version by [`scripts/html_to_pdf.py`](scripts/html_to_pdf.py), using a Chromium-based browser in headless mode, Playwright, or WeasyPrint — whichever is installed. Table-of-contents and back-to-top links keep working inside the PDF. If no converter is found, you get the HTML and instructions to print it to PDF. |

The HTML file loads its fonts and the code highlighter from a CDN. Offline, it falls back to system fonts and plain code blocks; nothing breaks.

## Validator

[`scripts/validate_lesson.py`](scripts/validate_lesson.py) is a standalone linter (Python ≥ 3.9, no dependencies) for both Markdown and HTML lessons:

```bash
python3 skills/teach-me/scripts/validate_lesson.py docs/kubernetes-ingress.md
python3 skills/teach-me/scripts/validate_lesson.py docs/kubernetes-ingress.html

# Treat warnings as errors
python3 skills/teach-me/scripts/validate_lesson.py docs/kubernetes-ingress.md --strict
```

| Rule | Severity | Checks |
| :-- | :-- | :-- |
| `toc-missing`, `toc-anchor` | error | A table of contents exists (`## Table of Contents` with `<a id="toc"></a>` in Markdown; an element with `id="toc"` in HTML) |
| `toc-entry` | error | Every H2/H3/H4 heading is listed in the TOC |
| `toc-link` | error | Every TOC link resolves to a heading |
| `toc-nesting` | error | Each TOC entry is nested at the depth of its heading |
| `toc-order` | error | TOC entries follow the order of the headings |
| `back-to-top` | error | Every H2/H3/H4 section has a back-to-top link |
| `link-target` | error | Every other in-page link resolves |
| `single-h1`, `heading-skip` | error | Exactly one title; no skipped heading levels |
| `heading-emoji` | error | No emoji or icons in headings |
| `code-language`, `fence-unclosed` | error | Code blocks are language-tagged and closed |
| `callout-type` | error | Callouts use a known type |
| `heading-id`, `duplicate-id`, `callout-icon` | error | HTML only: headings have unique ids; callouts carry an inline SVG icon |
| `sources` | warning | A `Sources` section exists |

Exit codes: `0` no errors, `1` findings, `2` file not found. It is suitable for CI.

## When to Use

- Learning a new technology, concept, or tool from scratch
- Getting an ordered, readable explanation instead of scattered search results
- Producing a lesson to share with a team, as a web page or a PDF

**Do NOT use this skill for:**

- A hands-on build of one specific thing, end to end — use [`tutorial-author`](../tutorial-author/README.md)
- API or configuration reference documentation
- READMEs, changelogs, or release notes
- Deciding architecture or technology — the lesson explains; it does not decide

## Installation & Activation

### Install

```bash
# Install to all runtimes (symlinks)
./install.sh --skill teach-me

# Install via file copy (if symlinks don't work)
./install.sh --skill teach-me --mode copy

# Install to a specific runtime
./install.sh --skill teach-me --target claude
```

For general installation details, see the [**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README. Install `arch-diagram-generator` as well if you want generated diagrams.

### Invocation

```text
/teach-me Kubernetes Ingress

teach me how OAuth 2.0 authorization code flow works, as HTML

help me learn Java virtual threads, save it as a PDF under docs/learning/
```

## Files

- **SKILL.md** — Directives and process
- **README.md** — This file
- **assets/lesson-template.md** — Markdown lesson skeleton
- **assets/lesson-template.html** — HTML lesson skeleton (styles, icons, theme toggle, copy buttons)
- **scripts/validate_lesson.py** — Structural validator for Markdown and HTML lessons
- **scripts/html_to_pdf.py** — HTML-to-PDF converter wrapper (tests for both scripts in `tests/test_validate_teach_me.py`)

## See Also

- [Tutorial Author](../tutorial-author/README.md) — hands-on, build-one-thing walkthroughs
- [Architecture Diagram Generator](../arch-diagram-generator/README.md) — produces the optional diagram
- [Agent Skills Catalog](../../README.md) — complete skill listing and installation guide

## License

Apache-2.0 © [Srikanth Kakumanu](https://github.com/srikanthkakumanu)
