#!/usr/bin/env python3
"""Verify an explainer HTML deliverable.

Checks: HTML tag balance, zero external references (must open offline),
no duplicate ids (SVG marker/id collisions), every inline SVG well-formed
and geometrically clean (via check-svg.py).

Usage: verify-explainer.py FILE
Exit 0 when every check passes, 1 otherwise.
"""
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

VOID_TAGS = {"meta", "link", "br", "img", "input", "hr"}


class BalanceChecker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"tag mismatch </{tag}> near line {self.getpos()[0]}")


def main():
    path = sys.argv[1]
    html = open(path, encoding="utf-8").read()
    findings = []

    checker = BalanceChecker()
    checker.feed(html)
    if checker.errors or checker.stack:
        findings.append(f"HTML unbalanced: {checker.errors} leftover {checker.stack}")

    external = [m for m in re.findall(r'(?:src|href)="(?!#)([^"]+)"', html)
                if m.startswith(("http", "//"))]
    if external:
        findings.append(f"external references (must open offline): {external}")

    ids = re.findall(r'\sid="([^"]+)"', html)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        findings.append(f"duplicate ids (SVG defs collide page-wide): {dupes}")

    svgs = re.findall(r"<svg.*?</svg>", html, re.S)
    if not svgs:
        findings.append("no inline SVG diagrams found")
    with tempfile.TemporaryDirectory() as tmp:
        extracted = []
        for i, svg in enumerate(svgs):
            p = f"{tmp}/diagram-{i}.svg"
            open(p, "w", encoding="utf-8").write(svg)
            extracted.append(p)
            try:
                ET.fromstring(svg)
            except ET.ParseError as e:
                findings.append(f"inline SVG {i} is not well-formed XML: {e}")
        if extracted:
            result = subprocess.run(
                [sys.executable, f"{__file__.rsplit('/', 1)[0]}/check-svg.py", *extracted],
                capture_output=True, text=True)
            if result.returncode != 0:
                findings.append("label geometry findings:\n" + result.stdout.strip())

    for f in findings:
        print(f"{path}: {f}")
    print(f"{path}: {'CLEAN' if not findings else f'{len(findings)} finding(s)'}")
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
