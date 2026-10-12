# Changelog

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
