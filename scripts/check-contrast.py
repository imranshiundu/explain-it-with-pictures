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
    ("explainer body on page", "#1E293B", "#F6F7F9", 4.5),
    ("explainer body on sheet", "#1E293B", "#FFFFFF", 4.5),
    ("explainer headings on paper", "#0F172A", "#FFFFFF", 4.5),
    ("captions on figure card", "#475569", "#FFFFFF", 4.5),
    ("footer on page", "#475569", "#F6F7F9", 4.5),
    ("diagram subtitle on white", "#64748B", "#FFFFFF", 4.5),
    ("box title on front tint", "#0F172A", "#DBEAFE", 4.5),
    ("box title on server tint", "#0F172A", "#D1FAE5", 4.5),
    ("box title on data tint", "#0F172A", "#FEF3C7", 4.5),
    ("box note on front tint", "#334155", "#DBEAFE", 4.5),
    ("box note on server tint", "#334155", "#D1FAE5", 4.5),
    ("box note on data tint", "#334155", "#FEF3C7", 4.5),
    ("box filename on front tint", "#475569", "#DBEAFE", 4.5),
    ("box filename on server tint", "#475569", "#D1FAE5", 4.5),
    ("box filename on data tint", "#475569", "#FEF3C7", 4.5),
    ("legend text on legend card", "#475569", "#F8FAFC", 4.5),
    ("zone label front", "#1D4ED8", "#EEF4FF", 4.5),
    ("zone label server", "#047857", "#ECFDF5", 4.5),
    ("zone label data", "#B45309", "#FFFBEB", 4.5),
    ("bubble number on bubble", "#FFFFFF", "#334155", 4.5),
    ("reply label on white", "#1D4ED8", "#FFFFFF", 4.5),
    ("error label on white", "#BE123C", "#FFFFFF", 4.5),
    ("edge labels on white", "#374151", "#FFFFFF", 4.5),
    ("edge labels over front zone", "#374151", "#EEF4FF", 4.5),
    ("inset title on white", "#7C3AED", "#FFFFFF", 4.5),
    ("print button on tint", "#7C3AED", "#F5F3FF", 4.5),
    ("anatomy footer note", "#92400E", "#FFFBEB", 4.5),
    ("json text on white card", "#1F2937", "#FFFFFF", 4.5),
    ("step chip", "#FFFFFF", "#0F172A", 4.5),
    ("app body on page", "#1E293B", "#FAFAF9", 4.5),
    ("app heading on card", "#0F172A", "#FFFFFF", 4.5),
    ("app input text", "#0F172A", "#FEFEFD", 4.5),
    ("app button label top", "#FFFFFF", "#15803D", 4.5),
    ("app button label bottom", "#FFFFFF", "#166534", 4.5),
    ("app error message", "#BE123C", "#FFFFFF", 4.5),
    ("app success message", "#15803D", "#FFFFFF", 4.5),
    ("app toast", "#FFFFFF", "#0F172A", 4.5),
    ("error text on rose tint", "#BE123C", "#FEE2E2", 4.5),
    ("note on rose tint card", "#374151", "#FEE2E2", 4.5),
    ("hierarchy text on gray card", "#111827", "#F8FAFC", 4.5),
    ("edge graphic on white", "#475569", "#FFFFFF", 3.0),
    ("return arrow graphic", "#2563EB", "#FFFFFF", 3.0),
    ("error arrow graphic", "#E11D48", "#FFFFFF", 3.0),
    ("cursor glyph graphic", "#0F172A", "#DBEAFE", 3.0),
]


def main():
    failures = 0
    for name, fg, bg, minimum in PAIRS:
        r = ratio(fg, bg)
        status = "ok" if r >= minimum else "FAIL"
        if r < minimum:
            failures += 1
        print(f"{status}  {name:.<38} {fg} on {bg}  {r:.2f}:1 (need {minimum})")
    print(f"\n{len(PAIRS) - failures}/{len(PAIRS)} pairs pass")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
