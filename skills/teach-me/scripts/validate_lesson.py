#!/usr/bin/env python3
"""
Structural linter for lessons produced by the teach-me skill (Markdown or HTML).

Usage:
    python3 validate_lesson.py <path/to/lesson.md|lesson.html> [--strict]

Exit code 0 when there are no errors (warnings are printed but do not fail unless --strict).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

TOC_ANCHOR = "toc"
TOC_TITLE = "table of contents"
BACK_TO_TOP_TARGETS = {TOC_ANCHOR, "top", "table-of-contents"}
# Topic (H2), sub-topic (H3), sub-sub-topic (H4).
SECTION_LEVELS = (2, 3, 4)
SOURCES_TITLES = ("sources", "references", "further reading")
MD_CALLOUTS = {"NOTE", "TIP", "WARNING", "IMPORTANT", "CAUTION"}
HTML_CALLOUTS = {"callout-note", "callout-tip", "callout-warning", "callout-best"}
HTML_SUFFIXES = {".html", ".htm"}
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source",
    "track", "wbr",
}  # fmt: skip

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
LINK_RE = re.compile(r"\]\(#([^)\s]+)\)")
ANCHOR_RE = re.compile(r"<a\s+(?:id|name)=[\"']([^\"']+)[\"']")
TOC_ITEM_RE = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s+")
CALLOUT_RE = re.compile(r"^\s*>\s*\[!([^\]]*)\]")
HTML_HEADING_RE = re.compile(r"^h([1-6])$")
EMOJI_RE = re.compile("[\U0001f000-\U0001faff☀-➿⬀-⯿️]")


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
    anchor: str
    order: int  # position in document order; lets sections be compared across formats


@dataclass
class Link:
    line: int
    target: str
    order: int
    depth: int = 0  # list nesting depth, used for TOC entries only


@dataclass
class Lesson:
    """Format-neutral view of a lesson; both parsers fill this in."""

    headings: list[Heading] = field(default_factory=list)
    toc: list[Link] | None = None  # None means no table of contents was found
    links: list[Link] = field(default_factory=list)  # in-page links outside the TOC
    anchors: set[str] = field(default_factory=set)
    findings: list[Finding] = field(default_factory=list)


def slugify(text: str) -> str:
    """GitHub-style heading slug: lowercase, drop punctuation, spaces to hyphens."""
    text = re.sub(r"[`*_]", "", text.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def parse_markdown(text: str) -> Lesson:
    lines = text.splitlines()
    lesson = Lesson()
    in_code = [False] * len(lines)
    slug_counts: dict[str, int] = {}
    toc_heading: Heading | None = None

    fence_marker = None
    fence_start = 0
    for idx, line in enumerate(lines):
        match = FENCE_RE.match(line)
        if fence_marker is None:
            if match:
                fence_marker = match.group(1)
                fence_start = idx + 1
                in_code[idx] = True
                if not match.group(2).strip():
                    lesson.findings.append(
                        Finding(fence_start, "code-language", "code fence has no language tag")
                    )
                continue
            heading = HEADING_RE.match(line)
            if heading:
                slug = slugify(heading.group(2))
                seen = slug_counts.get(slug, 0)
                slug_counts[slug] = seen + 1
                found = Heading(
                    idx + 1,
                    len(heading.group(1)),
                    heading.group(2),
                    f"{slug}-{seen}" if seen else slug,
                    idx + 1,
                )
                if found.level == 2 and found.text.lower() == TOC_TITLE and toc_heading is None:
                    toc_heading = found
                else:
                    lesson.headings.append(found)
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
        lesson.findings.append(Finding(fence_start, "fence-unclosed", "code fence is never closed"))

    prose = [(i + 1, line) for i, line in enumerate(lines) if not in_code[i]]
    explicit_anchors = {a for _, line in prose for a in ANCHOR_RE.findall(line)}
    lesson.anchors = {h.anchor for h in lesson.headings} | explicit_anchors

    toc_start = toc_end = 0
    if toc_heading is not None:
        lesson.toc = []
        lesson.anchors.add(toc_heading.anchor)
        toc_start = toc_heading.line
        toc_end = next((h.line - 1 for h in lesson.headings if h.line > toc_start), len(lines))
        if TOC_ANCHOR not in explicit_anchors:
            lesson.findings.append(
                Finding(toc_start, "toc-anchor", f'missing <a id="{TOC_ANCHOR}"></a> anchor')
            )

    indents: list[int] = []
    for number, line in prose:
        callout = CALLOUT_RE.match(line)
        if callout and callout.group(1).upper() not in MD_CALLOUTS:
            lesson.findings.append(
                Finding(number, "callout-type", f"unknown callout type '[!{callout.group(1)}]'")
            )
        if toc_start < number <= toc_end:
            item = TOC_ITEM_RE.match(line)
            if not item:
                continue
            indent = len(item.group(1).expandtabs(4))
            while indents and indent < indents[-1]:
                indents.pop()
            if not indents or indent > indents[-1]:
                indents.append(indent)
            for target in LINK_RE.findall(line):
                lesson.toc.append(Link(number, target, number, len(indents) - 1))
        else:
            for target in LINK_RE.findall(line):
                lesson.links.append(Link(number, target, number))
    return lesson


@dataclass
class _Frame:
    tag: str
    line: int
    is_toc: bool = False
    is_list: bool = False
    is_callout: bool = False
    has_icon: bool = False


class _LessonHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lesson = Lesson()
        self._stack: list[_Frame] = []
        self._order = 0
        self._heading: Heading | None = None
        self._pre: list | None = None  # [line, has_language]

    def _toc_depth(self) -> int | None:
        """List nesting depth inside the TOC element, or None when outside it."""
        for index, frame in enumerate(self._stack):
            if frame.is_toc:
                return sum(f.is_list for f in self._stack[index:]) - 1
        return None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        line = self.getpos()[0]
        self._order += 1
        frame = _Frame(tag, line, is_list=tag in ("ul", "ol"))

        element_id = attributes.get("id")
        if element_id:
            if element_id in self.lesson.anchors:
                self.lesson.findings.append(
                    Finding(line, "duplicate-id", f"id '{element_id}' is used more than once")
                )
            self.lesson.anchors.add(element_id)
            if element_id == TOC_ANCHOR:
                frame.is_toc = True
                self.lesson.toc = []

        toc_depth = self._toc_depth()
        heading = HTML_HEADING_RE.match(tag)
        if heading and toc_depth is None:
            self._heading = Heading(line, int(heading.group(1)), "", element_id or "", self._order)

        href = attributes.get("href") or ""
        if tag == "a" and href.startswith("#") and len(href) > 1:
            if toc_depth is None:
                self.lesson.links.append(Link(line, href[1:], self._order))
            else:
                self.lesson.toc.append(Link(line, href[1:], self._order, max(toc_depth, 0)))

        has_language = any(c.startswith(("language-", "lang-")) for c in classes)
        if tag == "pre":
            self._pre = [line, has_language]
        elif tag == "code" and self._pre and has_language:
            self._pre[1] = True

        if tag == "svg":
            for open_frame in self._stack:
                open_frame.has_icon = True
        if "callout" in classes:
            frame.is_callout = True
            if not HTML_CALLOUTS.intersection(classes):
                self.lesson.findings.append(
                    Finding(
                        line,
                        "callout-type",
                        "callout needs one of: " + ", ".join(sorted(HTML_CALLOUTS)),
                    )
                )

        if tag not in VOID_TAGS:
            self._stack.append(frame)

    def handle_endtag(self, tag):
        if self._heading is not None and tag == f"h{self._heading.level}":
            found = self._heading
            found.text = " ".join(found.text.split())
            self._heading = None
            self.lesson.headings.append(found)
            if found.level in SECTION_LEVELS and not found.anchor:
                self.lesson.findings.append(
                    Finding(found.line, "heading-id", f"heading '{found.text}' has no id attribute")
                )
        if tag == "pre" and self._pre is not None:
            if not self._pre[1]:
                self.lesson.findings.append(
                    Finding(
                        self._pre[0],
                        "code-language",
                        'code block has no language class (use <code class="language-...">)',
                    )
                )
            self._pre = None
        if not any(frame.tag == tag for frame in self._stack):
            return
        while self._stack:
            frame = self._stack.pop()
            if frame.is_callout and not frame.has_icon:
                self.lesson.findings.append(
                    Finding(frame.line, "callout-icon", "callout has no inline <svg> icon")
                )
            if frame.tag == tag:
                break

    def handle_data(self, data):
        if self._heading is not None:
            self._heading.text += data


def parse_html(text: str) -> Lesson:
    parser = _LessonHTMLParser()
    parser.feed(text)
    parser.close()
    return parser.lesson


def check(lesson: Lesson) -> list[Finding]:
    findings = list(lesson.findings)
    headings = lesson.headings

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
    for h in headings:
        if EMOJI_RE.search(h.text):
            findings.append(
                Finding(h.line, "heading-emoji", f"heading contains an emoji or icon: '{h.text}'")
            )

    sections = [(i, h) for i, h in enumerate(headings) if h.level in SECTION_LEVELS]
    by_anchor = {h.anchor: h for _, h in sections if h.anchor}

    # Table of contents: complete, resolvable, nested like the headings, in reading order.
    if lesson.toc is None:
        findings.append(Finding(1, "toc-missing", "no table of contents found"))
    else:
        toc_targets = {entry.target for entry in lesson.toc}
        for _, h in sections:
            if h.anchor and h.anchor not in toc_targets:
                findings.append(
                    Finding(h.line, "toc-entry", f"'{h.text}' (#{h.anchor}) is not in the TOC")
                )
        last_order = 0
        for entry in lesson.toc:
            target = by_anchor.get(entry.target)
            if target is None:
                if entry.target not in lesson.anchors:
                    findings.append(
                        Finding(
                            entry.line, "toc-link", f"TOC link '#{entry.target}' matches no heading"
                        )
                    )
                continue
            if entry.depth != target.level - 2:
                findings.append(
                    Finding(
                        entry.line,
                        "toc-nesting",
                        f"TOC entry '#{entry.target}' is nested at depth {entry.depth}, "
                        f"but its heading is H{target.level} (expected depth {target.level - 2})",
                    )
                )
            if target.order < last_order:
                findings.append(
                    Finding(
                        entry.line,
                        "toc-order",
                        f"TOC entry '#{entry.target}' is out of order with the headings",
                    )
                )
            last_order = max(last_order, target.order)

    # Back-to-top: somewhere between a heading and the next heading of the same or a higher level.
    back_links = [link.order for link in lesson.links if link.target in BACK_TO_TOP_TARGETS]
    for i, h in sections:
        end = next((later.order for later in headings[i + 1 :] if later.level <= h.level), None)
        if not any(h.order < order and (end is None or order < end) for order in back_links):
            findings.append(
                Finding(h.line, "back-to-top", f"section '{h.text}' has no back-to-top link")
            )

    for link in lesson.links:
        if link.target not in lesson.anchors:
            findings.append(
                Finding(link.line, "link-target", f"link '#{link.target}' matches no anchor")
            )

    if not any(h.level == 2 and h.text.lower().startswith(SOURCES_TITLES) for h in headings):
        findings.append(
            Finding(1, "sources", "no 'Sources' section found", severity="warning")
        )

    return sorted(findings, key=lambda f: f.line)


def validate(text: str, fmt: str = "md") -> list[Finding]:
    return check(parse_html(text) if fmt == "html" else parse_markdown(text))


def detect_format(path: Path) -> str:
    return "html" if path.suffix.lower() in HTML_SUFFIXES else "md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the structure of a teach-me lesson.")
    parser.add_argument("path", type=Path, help="path to the lesson (.md or .html)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args(argv)

    if not args.path.is_file():
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 2

    findings = validate(args.path.read_text(encoding="utf-8"), detect_format(args.path))
    for finding in findings:
        print(f"{args.path}:{finding}")
    failing = [f for f in findings if args.strict or f.severity == "error"]
    if not findings:
        print(f"{args.path}: OK")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
