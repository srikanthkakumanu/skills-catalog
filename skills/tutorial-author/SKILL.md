---
name: tutorial-author
description: Authors a hands-on TUTORIAL.md for a concept, tool, or codebase — plain-language concept intro, optional architecture diagram, full table of contents, back-to-top anchors, and verified step-by-step implementation instructions that say exactly where and how to make each code/config change, plus troubleshooting and next steps. Asks where to write the file (default docs/). Use when asked to write a tutorial, walkthrough, or step-by-step guide.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
metadata:
  tier_policy: "reasoning tier for scoping, outline, and step drafting; lightweight tier for TOC/anchor generation and final formatting"
---
# Tutorial Author Skill

## Directives
1. **Location first** — ask the user where to write the file; default `docs/TUTORIAL.md`. If a file already exists there, ask before overwriting.
2. **One guided path** — a tutorial is learning-oriented: one route to one working result. No option surveys, no reference dumps; link out for those.
3. **Concept brief** — 1–3 short paragraphs in plain language. Define each term on first use; one analogy at most.
4. **Diagram only when it helps** — multiple components or a data flow. Use the `arch-diagram-generator` skill, save the result under `images/` beside the tutorial, embed with alt text and a one-line caption. If that skill is unavailable, or the picture is a sequence/flow, use an inline Mermaid block instead.
5. **Table of contents** — every section (H2) and sub-section (H3), nested and linked, under `<a id="toc"></a>`.
6. **Back to top** — every H2 and H3 section ends with `[⬆ Back to top](#toc)`.
7. **Numbered steps, one outcome each** — ordered so the project builds or runs after every step; a step that leaves it broken says so and names the step that fixes it.
8. **Implementation detail in every step that changes code or config** — state all five:
   - **Where** — file path from the project root, new or existing, and the spot inside it (class, function, section, or key; "after the `X` block"). Line numbers are a hint, never the only locator.
   - **What** — the change. New file: full contents. Existing file: a `diff` block or before/after with enough context to find it.
   - **How** — the action (create, add, replace, delete, rename) and any command that performs it.
   - **Why** — one or two sentences on what it does and why now.
   - **Verify** — the command or observation that proves it worked, with the expected result.
9. **Examples are runnable** — fenced with a language tag, labelled with their file path, no `...` elisions in blocks meant to be copied. Placeholders look like `<LIKE_THIS>` and are listed once. Never real secrets.
10. **Config and dependencies are exact** — file, key path, value, and the environment/profile it applies to; manifest entry with version plus the install command; environment variables with where to set them.
11. **Verify, don't invent** — run commands when a shell is available; otherwise mark the step "not verified". For an existing repo, read paths, symbols, versions, and snippets from the repo — never guess them.
12. **No emoji in headings** — keeps anchor slugs predictable across renderers. Use `> [!NOTE]`, `> [!TIP]`, `> [!WARNING]` callouts sparingly for pitfalls.
13. **Context** — load `assets/tutorial-template.md` only when drafting; keep only the latest draft.

## Process
1. **Scope** *(reasoning)* — confirm location; ask or infer audience level, the end result the reader will have, and tested versions.
2. **Outline** *(reasoning)* — sections and steps; list every file the reader will create or modify; decide whether a diagram is warranted. If the outline exceeds ~10 steps or ~600 lines, propose splitting into parts and confirm.
3. **Draft** *(reasoning)* — fill `assets/tutorial-template.md`; apply directive 8 to each step; add a checkpoint after each step.
4. **Diagram** *(reasoning)* — generate per directive 4, if warranted.
5. **TOC and anchors** *(lightweight)* — build the TOC from the final headings; add back-to-top links.
6. **Self-check** *(mandatory, before output)* — run `python3 scripts/validate_tutorial.py <path>` and fix every finding. Without a shell, check the same rules by hand: TOC complete, links resolve, back-to-top present, fences tagged and closed, every code change says where.

## Output: `TUTORIAL.md`
- Title, one-line promise, audience / time / tested-with line
- `## Table of Contents`
- `## Overview` — Concept, What You Will Build, What You Will Learn (3–5 outcomes)
- `## Architecture` — only if directive 4 applies
- `## Prerequisites` — tools with versions, prior knowledge, accounts/access
- `## Project Structure` — layout tree + **Files You Will Change** table (path | new/modified | step | purpose)
- `## Step N: <outcome>` — per directive 8, each with a checkpoint
- `## Complete Code` — final version of each changed file, or a link to it
- `## Troubleshooting` — table: symptom | cause | fix
- `## Recap`, `## Cleanup` (if resources were created), `## Next Steps`, `## Glossary` (optional)

## Out of Scope
- Explaining a topic for understanding rather than building one specific thing — use `teach-me`.
- API reference docs, READMEs, changelogs, and how-to recipes for readers who already know the topic.
- Making architecture or stack decisions — document what exists or what the user specifies.
