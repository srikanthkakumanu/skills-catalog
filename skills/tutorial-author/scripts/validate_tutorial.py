#!/usr/bin/env python3
"""
Structural linter for TUTORIAL.md files produced by the tutorial-author skill.

Usage:
    python3 validate_tutorial.py <path/to/TUTORIAL.md> [--strict]

Exit code 0 when there are no errors (warnings are printed but do not fail unless --strict).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

TOC_ANCHOR = "toc"
TOC_TITLE = "table of contents"
BACK_TO_TOP_TARGETS = {TOC_ANCHOR, "table-of-contents"}
# Blocks that show commands, output, or pictures rather than a change to a file.
UNLABELLED_LANGS = {"bash", "sh", "shell", "zsh", "console", "powershell", "text", "output", "mermaid"}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
LINK_RE = re.compile(r"\]\(#([^)\s]+)\)")
ANCHOR_RE = re.compile(r"<a\s+(?:id|name)=[\"']([^\"']+)[\"']")
STEP_RE = re.compile(r"^step\s+\d+", re.IGNORECASE)
PATH_LABEL_RE = re.compile(r"`[^`\s]*[./][^`\s]*`")


@dataclass
class Finding:
    line: int
    rule: str
    message: str
    severity: str = "error"

    def __str__(self) -> str:
        return f"{self.line}: {self.severity}: {self.rule}: {self.message}"


@dataclass
class Heading:
    line: int
    level: int
    text: str
    slug: str


def slugify(text: str) -> str:
    """GitHub-style heading slug: lowercase, drop punctuation, spaces to hyphens."""
    text = re.sub(r"[`*_]", "", text.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def validate(text: str) -> list[Finding]:
    lines = text.splitlines()
    findings: list[Finding] = []
    headings: list[Heading] = []
    fences: list[tuple[int, str]] = []  # (opening line, language)
    in_code = [False] * len(lines)
    slug_counts: dict[str, int] = {}

    fence_marker = None
    fence_start = 0
    for idx, line in enumerate(lines):
        match = FENCE_RE.match(line)
        if fence_marker is None:
            if match:
                fence_marker = match.group(1)
                fence_start = idx + 1
                info = match.group(2).strip()
                fences.append((fence_start, info.split()[0].lower() if info else ""))
                in_code[idx] = True
                if not info:
                    findings.append(
                        Finding(fence_start, "fence-language", "code fence has no language tag")
                    )
                continue
            heading = HEADING_RE.match(line)
            if heading:
                slug = slugify(heading.group(2))
                seen = slug_counts.get(slug, 0)
                slug_counts[slug] = seen + 1
                headings.append(
                    Heading(
                        idx + 1,
                        len(heading.group(1)),
                        heading.group(2),
                        f"{slug}-{seen}" if seen else slug,
                    )
                )
        else:
            in_code[idx] = True
            closes = (
                match
                and match.group(1)[0] == fence_marker[0]
                and len(match.group(1)) >= len(fence_marker)
                and not match.group(2).strip()
            )
            if closes:
                fence_marker = None
    if fence_marker is not None:
        findings.append(Finding(fence_start, "fence-unclosed", "code fence is never closed"))

    prose = [(i + 1, line) for i, line in enumerate(lines) if not in_code[i]]

    # Heading hierarchy
    h1s = [h for h in headings if h.level == 1]
    if len(h1s) != 1:
        findings.append(
            Finding(
                h1s[1].line if len(h1s) > 1 else 1,
                "single-h1",
                f"expected exactly one H1 title, found {len(h1s)}",
            )
        )
    for prev, cur in zip(headings, headings[1:]):
        if cur.level > prev.level + 1:
            findings.append(
                Finding(
                    cur.line,
                    "heading-skip",
                    f"heading jumps from H{prev.level} to H{cur.level}: '{cur.text}'",
                )
            )

    def section_end(index: int, stop_level: int) -> int:
        """Last line (1-based, inclusive) of the section opened by headings[index]."""
        for later in headings[index + 1 :]:
            if later.level <= stop_level:
                return later.line - 1
        return len(lines)

    def links_between(start: int, end: int) -> list[tuple[int, str]]:
        return [
            (number, target)
            for number, line in prose
            if start <= number <= end
            for target in LINK_RE.findall(line)
        ]

    # Table of contents
    anchors = {a for _, line in prose for a in ANCHOR_RE.findall(line)}
    toc_index = next(
        (i for i, h in enumerate(headings) if h.level == 2 and h.text.lower() == TOC_TITLE), None
    )
    sections = [
        (i, h) for i, h in enumerate(headings) if h.level in (2, 3) and i != toc_index
    ]
    if toc_index is None:
        findings.append(Finding(1, "toc-missing", "no '## Table of Contents' section found"))
    else:
        toc = headings[toc_index]
        if TOC_ANCHOR not in anchors:
            findings.append(
                Finding(toc.line, "toc-anchor", f'missing <a id="{TOC_ANCHOR}"></a> anchor')
            )
        toc_links = links_between(toc.line, section_end(toc_index, 2))
        toc_targets = {target for _, target in toc_links}
        for _, h in sections:
            if h.slug not in toc_targets:
                findings.append(
                    Finding(h.line, "toc-entry", f"'{h.text}' (#{h.slug}) is not in the TOC")
                )
        valid_targets = {h.slug for h in headings} | anchors
        for number, target in toc_links:
            if target not in valid_targets:
                findings.append(
                    Finding(number, "toc-link", f"TOC link '#{target}' matches no heading")
                )

    # Back-to-top: an H3 needs the link in its own body; an H2 anywhere up to the next H2.
    for i, h in sections:
        end = section_end(i, 2 if h.level == 2 else 3)
        if not any(t in BACK_TO_TOP_TARGETS for _, t in links_between(h.line, end)):
            findings.append(
                Finding(h.line, "back-to-top", f"section '{h.text}' has no back-to-top link")
            )

    # Required sections
    h2_titles = [h.text for h in headings if h.level == 2]
    if not any(t.lower().startswith("prerequisites") for t in h2_titles):
        findings.append(Finding(1, "prerequisites", "no '## Prerequisites' section found"))
    step_ranges = [
        (h.line, section_end(i, 2))
        for i, h in enumerate(headings)
        if h.level == 2 and STEP_RE.match(h.text)
    ]
    if not step_ranges:
        findings.append(Finding(1, "steps", "no '## Step N: ...' section found"))

    # Code changes inside steps must say which file they belong to.
    for start, lang in fences:
        if lang in UNLABELLED_LANGS or not lang:
            continue
        if not any(first <= start <= last for first, last in step_ranges):
            continue
        preceding = [line for n, line in prose if n < start and line.strip()][-3:]
        if not any(PATH_LABEL_RE.search(line) for line in preceding):
            findings.append(
                Finding(
                    start,
                    "file-label",
                    f"'{lang}' block does not say which file it belongs to "
                    "(add a `path/to/file` label just above it)",
                    severity="warning",
                )
            )

    return sorted(findings, key=lambda f: f.line)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the structure of a TUTORIAL.md file.")
    parser.add_argument("path", type=Path, help="path to the tutorial Markdown file")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args(argv)

    if not args.path.is_file():
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 2

    findings = validate(args.path.read_text(encoding="utf-8"))
    for finding in findings:
        print(f"{args.path}:{finding}")
    failing = [f for f in findings if args.strict or f.severity == "error"]
    if not findings:
        print(f"{args.path}: OK")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
