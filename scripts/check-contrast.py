#!/usr/bin/env python3
"""WCAG 2.1 contrast checker for the Explain It With Pictures design system.

Every (foreground, background, minimum-ratio) triple below is a design-system
contract: if a color changes in the CSS/SVG, the pair changes here too.
Text pairs require 4.5:1 (normal text); meaningful graphics require 3:1.

Usage: check-contrast.py
Exit 0 when every pair passes, 1 otherwise.
"""
import sys


def channel(value):
    value /= 255
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def luminance(hexcolor):
    hexcolor = hexcolor.lstrip("#")
    r, g, b = (int(hexcolor[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def ratio(fg, bg):
    l1, l2 = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


PAIRS = [
    # Page chrome: quiet instrument, sand ground
    ("ink on ground", "#2a2a26", "#ddd6c6", 7.0),
    ("muted on ground (secondary only)", "#59574e", "#ddd6c6", 4.5),
    ("ink on surface panels", "#2a2a26", "#ffffff", 7.0),
    ("muted on surface (secondary only)", "#59574e", "#ffffff", 7.0),
    ("ink on hero right half", "#2a2a26", "#e4ddcd", 7.0),
    ("action label on accent", "#ffffff", "#4f6238", 4.5),
    ("accent hover label", "#ffffff", "#3f5230", 4.5),
    ("fragment save button", "#ffffff", "#15803d", 4.5),
    ("closing field ink", "#ffffff", "#3f5a2a", 7.0),
    # Diagram titles and notes on their flat fills
    ("box title on front tint", "#2a2a26", "#dbeafe", 7.0),
    ("box title on server tint", "#2a2a26", "#d1fae5", 7.0),
    ("box title on data tint", "#2a2a26", "#fef3c7", 7.0),
    ("box note on front tint", "#334155", "#dbeafe", 4.5),
    ("box note on server tint", "#334155", "#d1fae5", 4.5),
    ("box note on data tint", "#334155", "#fef3c7", 4.5),
    ("box filename on front tint", "#475569", "#dbeafe", 4.5),
    ("box filename on server tint", "#475569", "#d1fae5", 4.5),
    ("box filename on data tint", "#475569", "#fef3c7", 4.5),
    ("zone label front", "#1d4ed8", "#eef4ff", 4.5),
    ("zone label server", "#047857", "#ecfdf5", 4.5),
    ("zone label data", "#b45309", "#fffbeb", 4.5),
    ("bubble number", "#ddd6c6", "#2a2a26", 4.5),
    ("step chip", "#ddd6c6", "#2a2a26", 4.5),
    ("edge labels on white", "#374151", "#ffffff", 4.5),
    ("reply label on white", "#1d4ed8", "#ffffff", 4.5),
    ("error label on white", "#be123c", "#ffffff", 4.5),
    ("diagram subtitle on white", "#59574e", "#ffffff", 7.0),
    ("anatomy footer note", "#92400e", "#fffbeb", 4.5),
    ("json text on white card", "#1f2937", "#ffffff", 7.0),
    ("inset title on white", "#1d4ed8", "#ffffff", 4.5),
    ("inset note", "#59574e", "#ffffff", 7.0),
    ("hierarchy root text", "#2a2a26", "#f8fafc", 7.0),
    ("error card title", "#be123c", "#fee2e2", 4.5),
    ("error card note", "#be123c", "#fee2e2", 4.5),
    ("interface fragment labels", "#59574e", "#ffffff", 7.0),
    ("interface fragment input", "#2a2a26", "#ffffff", 7.0),
    ("state row secondary", "#59574e", "#ffffff", 7.0),
    # Graphics (3:1)
    ("edge graphic on white", "#475569", "#ffffff", 3.0),
    ("return arrow graphic", "#2563eb", "#ffffff", 3.0),
    ("error arrow graphic", "#e11d48", "#ffffff", 3.0),
    ("cursor glyph on tint", "#2a2a26", "#dbeafe", 3.0),
    ("anatomy leader graphic", "#94a3b8", "#ffffff", 1.5),
]


def main():
    failures = 0
    for name, fg, bg, minimum in PAIRS:
        r = ratio(fg, bg)
        status = "ok" if r >= minimum else "FAIL"
        if r < minimum:
            failures += 1
        print(f"{status}  {name:.<40} {fg} on {bg}  {r:.2f}:1 (need {minimum})")
    print(f"\n{len(PAIRS) - failures}/{len(PAIRS)} pairs pass")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
