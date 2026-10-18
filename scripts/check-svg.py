#!/usr/bin/env python3
"""Geometry checker for annotated SVG diagrams.

Enforces the craft rules mechanically:
  1. Text never overlaps text (estimated bounding boxes, 0.62 em/char).
  2. Text stays inside the viewBox.
  3. Every text that belongs to a group containing rects must sit inside its
     smallest containing rect with >= 14px side and >= 8px vertical clearance
     (descenders counted), and must never cross into a sibling rect.
  4. Rects stay >= 24px apart in both axes — unless one contains the other
     (hierarchy nesting is legitimate).
  5. Floating labels (texts outside any box group, excluding bubbles, legends
     and insets) never intersect a box rect.
  6. Glyph coverage: every character is inside the embedded-font subset, so
     text never falls back to a mismatched system face.

Exemptions: the canvas ground rect (>= viewBox size), zone background bands
(class "zone"), and small marker rects (legend chips, spacing rulers —
w < 40 or h < 24). Texts inside bubble/legend/inset groups are exempt from
containment rules (they belong to circles and panels).

Usage: check-svg.py FILE [FILE ...]
Exit 0 when all files are clean, 1 when any finding is reported.
"""
import re
import sys
import xml.etree.ElementTree as ET

WIDTH_FACTOR = 0.62
HEIGHT_FACTOR = 1.35
SIDE_PAD = 14
VERT_PAD = 8
BOX_GAP = 24
SVG_NS = "{http://www.w3.org/2000/svg}"
GLYPH_RANGES = [
    (0x0020, 0x007E), (0x00A0, 0x00FF), (0x2013, 0x2026),
    (0x2190, 0x2193), (0x2212, 0x2212), (0x2460, 0x2469),
]


def build_parent_map(root):
    return {c: p for p in root.iter() for c in p}


def classes_of(elem):
    return (elem.get("class") or "").split()


def group_has_rect(elem):
    return any(c.tag == SVG_NS + "rect" for c in elem)


def is_exempt_rect(rect, vb=None):
    try:
        x = float(rect.get("x", "0"))
        y = float(rect.get("y", "0"))
        w = float(rect.get("width", "0"))
        h = float(rect.get("height", "0"))
    except ValueError:
        return True
    if vb and w >= vb[2] - 2 and h >= vb[3] - 2:
        return True  # canvas ground
    if "zone" in classes_of(rect):
        return True  # background band
    return w < 40 or h < 24


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
        "fs": fs,
    }


def rect_box(rect):
    return (
        float(rect.get("x", "0")),
        float(rect.get("y", "0")),
        float(rect.get("x", "0")) + float(rect.get("width", "0")),
        float(rect.get("y", "0")) + float(rect.get("height", "0")),
    )


def contains(outer, inner, slack=1.0):
    return (outer[0] - slack <= inner[0] and outer[1] - slack <= inner[1]
            and outer[2] + slack >= inner[2] and outer[3] + slack >= inner[3])


def intersects(a, b, slack=2.0):
    return (a[0] < b[2] - slack and a[2] > b[0] + slack
            and a[1] < b[3] - slack and a[3] > b[1] + slack)


def gap(a, b):
    dx = max(b[0] - a[2], a[0] - b[2], 0)
    dy = max(b[1] - a[3], a[1] - b[3], 0)
    return dx, dy


def overlap_area(a, b):
    dx = min(a["right"], b["right"]) - max(a["left"], b["left"])
    dy = min(a["bottom"], b["bottom"]) - max(a["top"], b["top"])
    return max(0, dx) * max(0, dy)


def glyphs_covered(text):
    for ch in text:
        if ch in "\n\t":
            continue
        code = ord(ch)
        if not any(lo <= code <= hi for lo, hi in GLYPH_RANGES):
            return False, ch
    return True, None


def check_file(path):
    findings = []
    root = ET.parse(path).getroot()
    parents = build_parent_map(root)
    vb = [float(v) for v in root.get("viewBox", "0 0 960 560").split()]

    texts, boxes = [], []
    for elem in root.iter(SVG_NS + "text"):
        content = "".join(elem.itertext()).strip()
        if not content:
            continue
        bbox = text_bbox(elem, parents)
        bbox["status"] = "floating"
        node = parents.get(elem)
        while node is not None:
            cls = classes_of(node) if isinstance(node.tag, str) else []
            if "bubble" in cls or "legend" in cls or "inset-item" in cls:
                bbox["status"] = "exempt"
                break
            if node.tag == SVG_NS + "g" and group_has_rect(node):
                bbox["status"] = "boxed"
                bbox["group"] = node
                break
            node = parents.get(node)
        texts.append(bbox)

    for rect in root.iter(SVG_NS + "rect"):
        if not is_exempt_rect(rect, vb):
            boxes.append(rect_box(rect))

    # 2. viewBox containment
    for t in texts:
        if t["left"] < vb[0] or t["right"] > vb[0] + vb[2] or t["top"] < vb[1] or t["bottom"] > vb[1] + vb[3]:
            findings.append(
                f"out of viewBox: {t['text']!r} bbox=({t['left']:.0f},{t['top']:.0f})-({t['right']:.0f},{t['bottom']:.0f})")

    # 1. text-text overlap
    for i, a in enumerate(texts):
        for b in texts[i + 1:]:
            area = overlap_area(a, b)
            if area > 4:
                findings.append(f"overlap {area:.0f}px2: {a['text']!r} and {b['text']!r}")

    # 3. text-in-box: smallest containing rect, padding, no crossing into siblings
    for t in texts:
        if t["status"] != "boxed":
            continue
        rects = [rect_box(r) for r in t["group"] if r.tag == SVG_NS + "rect" and not is_exempt_rect(r, vb)]
        if not rects:
            continue
        tb = (t["left"], t["top"], t["right"], t["bottom"])
        containing = [r for r in rects if contains(r, tb, slack=0.0)]
        if not containing:
            findings.append(f"text outside every box of its group: {t['text']!r}")
            continue
        chosen = min(containing, key=lambda r: (r[2] - r[0]) * (r[3] - r[1]))
        side_ok = t["left"] >= chosen[0] + SIDE_PAD and t["right"] <= chosen[2] - SIDE_PAD
        vert_ok = t["top"] >= chosen[1] + VERT_PAD and t["bottom"] <= chosen[3] - VERT_PAD
        if not (side_ok and vert_ok):
            findings.append(
                f"text not inside its box with padding (need {SIDE_PAD}px sides / {VERT_PAD}px vertical): "
                f"{t['text']!r} bbox=({t['left']:.0f},{t['top']:.0f})-({t['right']:.0f},{t['bottom']:.0f})")
        for other in rects:
            if other is chosen or contains(other, chosen):
                continue
            if intersects(tb, other):
                findings.append(
                    f"text crosses into another box: {t['text']!r} vs rect({other[0]:.0f},{other[1]:.0f},{other[2]:.0f},{other[3]:.0f})")

    # 4. rect-rect clearance (containment allowed)
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            if contains(a, b) or contains(b, a):
                continue
            dx, dy = gap(a, b)
            if dx < BOX_GAP and dy < BOX_GAP:
                findings.append(
                    f"boxes {BOX_GAP - max(dx, dy):.0f}px too close: need {BOX_GAP}px — "
                    f"rect({a[0]:.0f},{a[1]:.0f},{a[2]:.0f},{a[3]:.0f}) vs rect({b[0]:.0f},{b[1]:.0f},{b[2]:.0f},{b[3]:.0f})")

    # 5. floating labels never intersect a box rect
    for t in texts:
        if t["status"] != "floating":
            continue
        tb = (t["left"], t["top"], t["right"], t["bottom"])
        for r in boxes:
            if intersects(tb, r, slack=0.0):
                findings.append(
                    f"label sits on a box: {t['text']!r} bbox=({t['left']:.0f},{t['top']:.0f})-({t['right']:.0f},{t['bottom']:.0f})")
                break

    # 6. glyph coverage
    for t in texts:
        ok, ch = glyphs_covered(t["text"])
        if not ok:
            findings.append(f"character {ch!r} (U+{ord(ch):04X}) is outside the embedded-font subset: {t['text']!r}")

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
