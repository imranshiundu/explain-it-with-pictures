#!/usr/bin/env python3
"""Verify an explainer HTML deliverable.

Checks:
  1. HTML tag balance; zero external references (must open offline).
  2. No duplicate ids (SVG marker/id collisions across diagrams).
  3. Every inline SVG well-formed and geometrically clean (check-svg.py).
  4. Design system: embedded fonts decode, reduced-motion + print media
     present, JS gated by class so no-JS stays visible, IntersectionObserver
     present, motion-ready edges (pathLength), every diagram titled (a11y).

Usage: verify-explainer.py FILE
Exit 0 when every check passes, 1 otherwise.
"""
import base64
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


def check_design(html, findings):
    faces = re.findall(r"@font-face\s*\{[^}]*src:\s*url\(data:font/woff2;base64,([A-Za-z0-9+/=]+)\)", html)
    if not faces:
        findings.append("no embedded fonts found (deliverable must carry its own)")
    for i, b64 in enumerate(faces):
        try:
            base64.b64decode(b64, validate=True)
        except Exception as e:
            findings.append(f"font {i} base64 is corrupt: {e}")

    for marker, description in [
        ("prefers-reduced-motion: no-preference", "motion only applies under a no-preference media query (the reduced-motion fallback)"),
        ("@media print", "print stylesheet exists"),
        ("classList.add('js')", "motion is JS-gated (no-JS keeps content visible)"),
        ("IntersectionObserver", "scroll-reveal observer present"),
        ('pathLength="1"', "edges are motion-ready (pathLength)"),
    ]:
        if marker not in html:
            findings.append(f"design system incomplete: missing {description}")

    svgs = re.findall(r"<svg.*?</svg>", html, re.S)
    untitled = sum(1 for s in svgs if "<title>" not in s)
    if untitled:
        findings.append(f"{untitled} inline SVG diagram(s) missing a <title> (accessibility)")


def main():
    path = sys.argv[1]
    html = open(path, encoding="utf-8").read()
    findings = []

    checker = BalanceChecker()
    checker.feed(html)
    if checker.errors or checker.stack:
        findings.append(f"HTML unbalanced: {checker.errors} leftover {checker.stack}")

    external = [m for m in re.findall(r'(?:<link[^>]+href|<script[^>]+src|\b[^a-]src)="(https?://[^"]+|//[^"]+)"', html)
                if not m.startswith("#")] + re.findall(r"url\((https?://[^)]+)\)", html)
    if external:
        findings.append(f"external resources loaded (must open offline): {external}")

    ids = re.findall(r'\sid="([^"]+)"', html)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        findings.append(f"duplicate ids (SVG defs collide page-wide): {dupes}")

    check_design(html, findings)

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
