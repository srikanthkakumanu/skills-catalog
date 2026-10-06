#!/usr/bin/env python3
"""
Convert a teach-me HTML lesson to PDF with whichever converter is installed.

Tries, in order: a Chromium-based browser in headless mode, Playwright, WeasyPrint.

Usage:
    python3 html_to_pdf.py <lesson.html> [output.pdf]

Exit codes: 0 PDF written, 1 conversion failed, 2 input not found, 3 no converter available.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

BROWSER_COMMANDS = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "chrome",
    "microsoft-edge",
    "msedge",
    "brave-browser",
)
MAC_BROWSERS = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
)
WINDOWS_BROWSERS = (
    r"Google\Chrome\Application\chrome.exe",
    r"Microsoft\Edge\Application\msedge.exe",
)
TIMEOUT_SECONDS = 120

NO_CONVERTER_HELP = """\
No HTML-to-PDF converter was found (looked for Chrome/Chromium/Edge/Brave, Playwright, WeasyPrint).
To make the PDF by hand: open the HTML file in any browser, choose Print, then "Save as PDF".
The lesson's print styles are already set up for this."""


def find_browser() -> str | None:
    for command in BROWSER_COMMANDS:
        found = shutil.which(command)
        if found:
            return found
    candidates = list(MAC_BROWSERS)
    for variable in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
        base = os.environ.get(variable)
        if base:
            candidates += [str(Path(base) / relative) for relative in WINDOWS_BROWSERS]
    return next((c for c in candidates if Path(c).is_file()), None)


def with_browser(browser: str, source: Path, output: Path) -> None:
    subprocess.run(
        [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--virtual-time-budget=5000",  # give web fonts and the highlighter time to load
            f"--print-to-pdf={output}",
            source.as_uri(),
        ],
        check=True,
        capture_output=True,
        timeout=TIMEOUT_SECONDS,
    )


def with_playwright(source: Path, output: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(source.as_uri(), wait_until="networkidle")
        page.pdf(path=str(output), print_background=True)
        browser.close()


def with_weasyprint(source: Path, output: Path) -> None:
    subprocess.run(
        ["weasyprint", str(source), str(output)],
        check=True,
        capture_output=True,
        timeout=TIMEOUT_SECONDS,
    )


def available_converters() -> list[tuple[str, object]]:
    converters: list[tuple[str, object]] = []
    browser = find_browser()
    if browser:
        converters.append((Path(browser).name, lambda s, o: with_browser(browser, s, o)))
    try:
        import playwright.sync_api  # noqa: F401

        converters.append(("playwright", with_playwright))
    except ImportError:
        pass
    if shutil.which("weasyprint"):
        converters.append(("weasyprint", with_weasyprint))
    return converters


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert a teach-me HTML lesson to PDF.")
    parser.add_argument("source", type=Path, help="path to the lesson HTML file")
    parser.add_argument("output", type=Path, nargs="?", help="PDF path (default: beside the HTML)")
    args = parser.parse_args(argv)

    if not args.source.is_file():
        print(f"error: file not found: {args.source}", file=sys.stderr)
        return 2
    source = args.source.resolve()
    output = (args.output or source.with_suffix(".pdf")).resolve()

    converters = available_converters()
    if not converters:
        print(NO_CONVERTER_HELP, file=sys.stderr)
        return 3

    for name, convert in converters:
        try:
            convert(source, output)
        except Exception as error:  # try the next converter; report each failure
            detail = getattr(error, "stderr", None) or error
            if isinstance(detail, bytes):
                detail = detail.decode(errors="replace")
            print(f"warning: {name} failed: {str(detail).strip()[:500]}", file=sys.stderr)
            continue
        if output.is_file() and output.stat().st_size > 0:
            print(f"{output}: written with {name}")
            return 0
        print(f"warning: {name} produced no output", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
