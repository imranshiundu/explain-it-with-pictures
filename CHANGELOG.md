# Changelog

## 1.2.0 — 2026-10-18

The "agents can't draw" release: geometry enforcement, diagram variety, storytelling.

- **Geometry safety, enforced**: rewritten `check-svg.py` — text-in-box padding (14px sides / 8px vertical), 24px box-to-box clearance with nesting awareness, floating-label placement, glyph coverage against the embedded-font subset. Caught and fixed real overlaps in the previous templates on first run.
- **Diagram-type library** (8 types with use-cases): flow, hierarchy, comparison, timeline, anatomy, decision tree, small multiples, zoom callout — shipped as `templates/diagram-kit.svg`, the new reference kit with a live conventions strip (type scale, spacing ruler, color roles).
- **Story structure**: hook → reveal → mechanism → payoff → takeaway; document outline now includes small multiples ("the book over time") and a file **hierarchy** diagram replacing the ASCII tree.
- **Design system rebuilt** on the house rules: ground/surface/ink/muted/accent roles (warm off-white ground, flat surfaces, no gradients, no shadows, no thin rules, square corners), 5-size type scale with clamps, spacing scale (4–64px + 140px section rhythm), tight margins, no eyebrows, no index numbering.
- **Example explainer rebuilt**: 6 diagrams (big picture, save flow + message inset, search flow, anatomy, small multiples, hierarchy), story-ordered, all geometry CLEAN under the new checker.
- **Contrast suite grown to 44 pairs** (rose-tint error cards, hierarchy grays).
- **Harness hardened**: server readiness wait (kills a start-up race that flaked the smoke test), kit screenshot + 3 new example screenshots, 9-page PDF.

## 1.1.0 — 2026-10-12

Design-language release: Apple-grade polish, motion, and a hardened test loop.

- **New design system** in `explainer-page.html`: Fraunces/Inter/JetBrains Mono embedded as subset base64 woff2 (`templates/fonts.css`, SIL OFL), sticky blurred header with reading-progress hairline, numbered chapters, card figures, print stylesheet.
- **Scroll motion**: story-ordered reveals (zones → boxes → arrows drawing via `pathLength` → bubbles popping → insets), spring easing, all under 1.2s; gated behind `prefers-reduced-motion: no-preference` and a JS class so no-JS/reduced-motion/print all show the fully-rendered page.
- **Diagram upgrade**: gradient boxes with soft shadows, contrast-fixed palette (`#1D4ED8/#047857/#B45309` labels, `#BE123C` error text), monospace filenames, explicit `.head` arrowheads, a violet zoom-in inset in the save-flow diagram demonstrating craft rule 8.
- **Demo app redesign**: same architecture, new surface — kicker/Fraunces heading, focus rings, green-gradient button, toast, empty/no-results states, staggered list, disabled-while-pending submit, network-error message.
- **New craft rules** 12 (move with restraint) + typography guidance; self-check now covers motion and contrast.
- **Hardened harness**: `check-contrast.py` (41 WCAG pairs), extended `verify-explainer.py` (fonts decode, motion gating, `<title>` per diagram), `verify.sh` now runs live headless-Chrome render assertions, a 7-page print-to-PDF test, and a pixel sanity pass on shipped screenshots.

## 1.0.0 — 2026-10-12

Initial release.

- Skill: full workflow (survey → story list → format → draw → self-check), 11 craft rules for annotated diagrams, plain-language rules, document outline, delivery self-check.
- Templates: `annotated-diagram.svg` (worked example of every convention), `explainer-page.html` (single-file skeleton), `chat-flow.mmd` (chat/PR pattern).
- Example: `recipe-saver` demo app + `recipe-saver-explainer.html` — a complete generated explainer with four hand-drawn diagrams.
- Tooling: `scripts/verify.sh` — SVG geometry checks, explainer validation, live app smoke test, fixture integrity check.
