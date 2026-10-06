---
name: teach-me
description: Teaches any topic in simple English as one ordered lesson document. Researches the topic first, proposes an outline of topics, sub-topics, and sub-sub-topics, asks which related topics to include and whether to write HTML, PDF, or Markdown, then explains step by step with easy code and configuration examples, the files to create or modify, best practices in context, Note/Warning/Help callouts, a nested table of contents, and back-to-top links. Use when asked to "teach me", explain, or help learn a topic. To be walked through building one specific thing, use tutorial-author instead.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
metadata:
  tier_policy: "reasoning tier for research, outline, and lesson drafting; lightweight tier for TOC/anchor generation, format conversion, and final formatting"
---
# Teach Me Skill

## Directives
1. **Research first** — before outlining, search the web and read official documentation if a search or fetch tool is available; read the current repository when the topic is about it. Take version numbers, API names, and config keys from a source, never from memory. If no research was possible, say so in the lesson's "Researched" line. Keep the list of sources used.
2. **Learning order** — arrange topics (H2), sub-topics (H3), and sub-sub-topics (H4, only when needed) so each part relies only on what came before. Number them (`1.`, `1.1`, `1.1.1`). This order is the backbone; everything else hangs on it.
3. **One checkpoint, then write** — after research, show the outline and ask in a single round:
   - related topics the research found that were not requested (one line each on why it matters) — which to include;
   - output format: **HTML**, **PDF**, or **Markdown**;
   - save location, default `docs/<topic-slug>.<ext>` — ask before overwriting an existing file.

   Do not ask anything else unless the topic itself is ambiguous.
4. **Simple English** — short sentences, everyday words, one idea per paragraph. Explain every technical term the first time it appears. Write for a smart reader who is new to the topic. No filler, no hype.
5. **Right size** — a sub-topic is usually a few short paragraphs plus an example. Cover every outline entry properly; cut anything that is padding. If the topic is too big for one comfortable read (roughly 25 minutes), propose splitting it into parts at the checkpoint.
6. **Examples where they are taught** — code is small, complete enough to run or paste, fenced with a language tag, and labelled with its file path. No `...` gaps in blocks meant to be copied. Placeholders look like `<LIKE_THIS>`. Never real secrets.
7. **Configuration is exact** — name the file, the key, and the value; show before/after (a `diff` block) when changing something that exists.
8. **Files to create or modify** — wherever a topic touches files, list them (path, new or modified, purpose). Give one combined "Files at a Glance" table near the start.
9. **Best practices in the flow** — place each best practice inside the topic it belongs to, at the point the reader can use it, with its own code or config example. Never a separate best-practices section at the end.
10. **Callouts only where they help** — Note (a detail that is easy to miss), Warning (something that can break things or lose data), Help (a friendly shortcut, or where to look when stuck). Each has an icon and a short description. Markdown: `> [!NOTE]`, `> [!WARNING]`, `> [!TIP]`. HTML: the template's `callout` blocks with inline SVG icons.
11. **Only what the topic has** — for a non-technical topic leave out code, configuration, and file lists. Do not invent them to fill the structure.
12. **Table of contents** — at the top, nested exactly like the headings (topic → sub-topic → sub-sub-topic), every entry a working link.
13. **Back to top** — every topic, sub-topic, and sub-sub-topic ends with a back-to-top link.
14. **No emoji or icons in headings** — keeps anchor links predictable. Icons belong in callouts and page furniture.
15. **Diagram only when it helps** — use the `arch-diagram-generator` skill if it is available; otherwise an inline Mermaid block (Markdown) or a simple inline SVG (HTML).
16. **Context** — load only the template for the chosen format, and only when drafting.

## Process
1. **Research** *(reasoning)* — per directive 1. Note related topics worth offering.
2. **Outline** *(reasoning)* — per directive 2; list every file the lesson will create or change.
3. **Checkpoint** — per directive 3. Wait for the answer.
4. **Draft** *(reasoning)* — fill the template for the chosen format, in outline order:
   - Markdown → `assets/lesson-template.md`
   - HTML or PDF → `assets/lesson-template.html` (keep its styles, icon sprite, and script unchanged; escape `&`, `<`, `>` inside code blocks)
5. **TOC and anchors** *(lightweight)* — rebuild the table of contents from the final headings; add back-to-top links.
6. **Self-check** *(mandatory, before output)* — run `python3 scripts/validate_lesson.py <path>` and fix every finding. Without a shell, check the same rules by hand: TOC complete and nested like the headings, links resolve, back-to-top present at every level, code blocks tagged and closed, no emoji in headings.
7. **PDF** *(only if chosen)* — run `python3 scripts/html_to_pdf.py <lesson.html>`; it uses whichever converter is installed and keeps the HTML beside the PDF. If it exits with code 3 (no converter), tell the user plainly, deliver the HTML, and explain: open it in a browser → Print → Save as PDF. A PDF skill or tool in the runtime may be used instead.
8. **Deliver** — give the file path, the reading time, and anything that could not be researched or verified.

## Output: `<topic-slug>.md` / `.html` / `.pdf`
- Title, one-line promise, level / reading time / researched line
- `Table of Contents` — nested
- `Before You Start` — What You Will Learn, What You Need, Files at a Glance (technical topics only)
- `N. <Topic>` → `N.N <Sub-topic>` → `N.N.N <Sub-sub-topic>` — explanation, examples, files, best practices, callouts, in learning order
- `Summary` — key ideas and where to go next
- `Sources` — what was read, with links

## Out of Scope
- A hands-on walkthrough that builds one specific thing end to end — use `tutorial-author`.
- API reference docs, READMEs, and changelogs.
- Making architecture or stack decisions — the lesson explains; it does not decide.
