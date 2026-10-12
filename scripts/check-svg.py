#!/usr/bin/env python3
"""Geometry checker for annotated SVG diagrams.

Verifies that text elements inside an SVG do not collide with each other and
stay inside the viewBox. Widths are estimated (sans-serif, ~0.6 em average
glyph), so treat findings as warnings to confirm, then fix by moving labels.

Usage: check-svg.py FILE [FILE ...]
Exit 0 when all files are clean, 1 when any finding is reported.
"""
import re
import sys
import xml.etree.ElementTree as ET

WIDTH_FACTOR = 0.62
HEIGHT_FACTOR = 1.35


def build_parent_map(root):
    return {c: p for p in root.iter() for c in p}


def text_bbox(elem, parents):
    x = float(elem.get("x", "0"))
    y = float(elem.get("y", "0"))
    anchor = elem.get("text-anchor", "start")
    fs = 16.0
    node = elem
    while node is not None:
        fs_attr = node.get("font-size")
        if fs_attr:
            fs = float(re.match(r"[\d.]+", fs_attr).group())
            break
        node = parents.get(node)
    content = "".join(elem.itertext())
    width = fs * WIDTH_FACTOR * len(content)
    if anchor == "middle":
        left = x - width / 2
    elif anchor == "end":
        left = x - width
    else:
        left = x
    return {
        "text": content.strip(),
        "left": left,
        "right": left + width,
        "top": y - fs * (HEIGHT_FACTOR - 1),
        "bottom": y + fs * 0.3,
    }


def overlap_area(a, b):
    dx = min(a["right"], b["right"]) - max(a["left"], b["left"])
    dy = min(a["bottom"], b["bottom"]) - max(a["top"], b["top"])
    return max(0, dx) * max(0, dy)


def check_file(path):
    findings = []
    root = ET.parse(path).getroot()
    parents = build_parent_map(root)
    vb = [float(v) for v in root.get("viewBox", "0 0 960 560").split()]
    vb_x, vb_y, vb_w, vb_h = vb
    boxes = []
    for elem in root.iter("{http://www.w3.org/2000/svg}text"):
        if not "".join(elem.itertext()).strip():
            continue
        boxes.append(text_bbox(elem, parents))
    for i, a in enumerate(boxes):
        if a["left"] < vb_x or a["right"] > vb_x + vb_w or a["top"] < vb_y or a["bottom"] > vb_y + vb_h:
            findings.append(f"out of viewBox: {a['text']!r} bbox=({a['left']:.0f},{a['top']:.0f})-({a['right']:.0f},{a['bottom']:.0f})")
        for b in boxes[i + 1:]:
            area = overlap_area(a, b)
            if area > 4:
                findings.append(f"overlap {area:.0f}px2: {a['text']!r} and {b['text']!r}")
    return findings


def main():
    any_finding = False
    for path in sys.argv[1:]:
        findings = check_file(path)
        for f in findings:
            print(f"{path}: {f}")
        print(f"{path}: {'CLEAN' if not findings else f'{len(findings)} finding(s)'}")
        any_finding = any_finding or bool(findings)
    sys.exit(1 if any_finding else 0)


if __name__ == "__main__":
    main()
