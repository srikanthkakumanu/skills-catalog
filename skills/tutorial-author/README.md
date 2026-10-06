# Tutorial Author Skill

**Version:** 1.0.0 | **Status:** Supported | **License:** Apache-2.0

**Writes a hands-on, structurally checked `TUTORIAL.md` that takes a reader from zero to a working result.**

## Overview

This skill turns a concept, tool, feature, or existing codebase into a tutorial a reader can follow start to finish. It explains the idea briefly in plain language, then walks through the implementation one step at a time — and for every code or configuration change it says **where** the change goes, **what** it is, **how** to make it, **why** it is needed, and how to **verify** it worked.

It follows the Diátaxis definition of a tutorial: learning-oriented, one guided path, one working outcome. It is not a reference manual or a menu of options.

## What It Does

1. **Asks where to write the file** — default `docs/TUTORIAL.md`; asks before overwriting an existing file.
2. **Scopes the tutorial** — audience level, the end result, and the versions it is tested with.
3. **Explains the concept** — 1–3 short paragraphs, terms defined on first use.
4. **Adds an architecture diagram when it helps** — via [`arch-diagram-generator`](../arch-diagram-generator/README.md), saved under `images/` beside the tutorial. Falls back to an inline Mermaid block when that skill is unavailable or the picture is a sequence/flow.
5. **Builds a table of contents** — every section (H2) and sub-section (H3), nested and linked.
6. **Adds a back-to-top link** to every section and sub-section.
7. **Writes numbered steps** — each with an example and an expected result, ordered so the project works after every step.
8. **Self-checks** — runs the bundled validator and fixes findings before delivering.

## How Each Implementation Step Is Written

| Part | What the reader is told |
| :-- | :-- |
| **Where** | File path from the project root, whether the file is new or existing, and the spot inside it (class, function, section, config key, or "after the `X` block") |
| **What** | The change itself — full contents for a new file; a `diff` or before/after for an existing one |
| **How** | The action (create, add, replace, delete, rename) and any command that performs it |
| **Why** | What the change does and why it is needed at this point |
| **Verify** | The command or observation that proves it worked, with the expected output |

Supporting rules:

- A **Project Structure** tree and a **Files You Will Change** table summarise every edit up front.
- **Configuration** changes name the file, key path, value, and the environment or profile they apply to; environment variables say where to set them.
- **Dependencies** give the exact manifest entry with version, plus the install command.
- Examples are **copy-paste runnable** — language-tagged, labelled with their file path, no elisions; placeholders look like `<LIKE_THIS>`.
- Commands are **run, not invented** — when no shell is available the step is marked "not verified".
- For an existing repository, paths, symbols, and snippets are **read from the repo**.
- A **Complete Code** section gives the final version of each changed file.

## Input

Any of:

- A topic or concept ("JWT authentication in Spring Boot")
- A feature or module in the current repository ("how to add a new skill to this catalog")
- Existing notes, a design document, or a PRD excerpt to turn into a walkthrough

Optional: audience level, target versions, output location.

## Output: `TUTORIAL.md`

```text
# Title
> One-line promise · Audience · Time · Tested with

## Table of Contents
## Overview
   ### Concept
   ### What You Will Build
   ### What You Will Learn
## Architecture                (only when it helps)
## Prerequisites
## Project Structure
   ### Files You Will Change
## Step 1: <outcome>           (Where / How / What / Why / Verify + checkpoint)
## Step N: <outcome>
## Complete Code
## Troubleshooting             (symptom | cause | fix)
## Recap
## Cleanup                     (only when resources were created)
## Next Steps
## Glossary                    (optional)
```

The full skeleton is in [`assets/tutorial-template.md`](assets/tutorial-template.md).

## Validator

[`scripts/validate_tutorial.py`](scripts/validate_tutorial.py) is a standalone linter (Python ≥ 3.9, no dependencies):

```bash
python3 skills/tutorial-author/scripts/validate_tutorial.py docs/TUTORIAL.md

# Treat warnings as errors
python3 skills/tutorial-author/scripts/validate_tutorial.py docs/TUTORIAL.md --strict
```

| Rule | Severity | Checks |
| :-- | :-- | :-- |
| `toc-missing`, `toc-anchor` | error | A `## Table of Contents` section and the `<a id="toc"></a>` anchor exist |
| `toc-entry` | error | Every H2/H3 heading is listed in the TOC |
| `toc-link` | error | Every TOC link resolves to a heading |
| `back-to-top` | error | Every H2/H3 section links back to the TOC |
| `single-h1`, `heading-skip` | error | Exactly one title; no skipped heading levels |
| `fence-language`, `fence-unclosed` | error | Code fences are tagged and closed |
| `prerequisites`, `steps` | error | A Prerequisites section and at least one `## Step N` section exist |
| `file-label` | warning | A code block inside a step names the file it belongs to |

Exit codes: `0` no errors, `1` findings, `2` file not found. It is suitable for CI.

## When to Use

- Onboarding material for a codebase, feature, or internal tool
- Teaching a concept or technology through a worked example
- Turning a completed implementation into a repeatable walkthrough

**Do NOT use this skill for:**

- Explaining a topic so the reader understands it, without building one specific thing — use [`teach-me`](../teach-me/README.md)
- API or configuration reference documentation
- READMEs, changelogs, or release notes
- Short how-to recipes for readers who already know the topic
- Deciding architecture or technology — it documents what exists or what you specify

## Installation & Activation

### Install

```bash
# Install to all runtimes (symlinks)
./install.sh --skill tutorial-author

# Install via file copy (if symlinks don't work)
./install.sh --skill tutorial-author --mode copy

# Install to a specific runtime
./install.sh --skill tutorial-author --target claude
```

For general installation details, see the [**Installation & Deployment**](../../README.md#-installation--deployment) section in the root README. Install `arch-diagram-generator` as well if you want generated architecture diagrams.

### Invocation

```text
/tutorial-author Explain how to add JWT authentication to this service

write a tutorial for setting up Flyway migrations

create tutorial: adding a new skill to this catalog, save under docs/guides/
```

## Files

- **SKILL.md** — Directives and process
- **README.md** — This file
- **assets/tutorial-template.md** — `TUTORIAL.md` skeleton
- **scripts/validate_tutorial.py** — Structural validator (tests in `tests/test_validate_tutorial.py`)

## See Also

- [Teach Me](../teach-me/README.md) — explains a topic so the reader understands it, in HTML, PDF, or Markdown
- [Architecture Diagram Generator](../arch-diagram-generator/README.md) — produces the optional architecture diagram
- [Agent Skills Catalog](../../README.md) — complete skill listing and installation guide

## License

Apache-2.0 © [Srikanth Kakumanu](https://github.com/srikanthkakumanu)
