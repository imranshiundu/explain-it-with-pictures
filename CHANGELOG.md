# Changelog

## 1.3.0 — 2026-10-25

The "use the frontend skills properly" release: the design was rebuilt through a measured process (dealt direction → build → lint → real-browser inspection), not by eye.

- **Direction dealt and adopted: the quiet instrument** — radical understatement. Headline barely larger than body text, diagrams run full width, restraint as the claim.
- **Typography: Clash Grotesk** (Fontshare, one family, two weights), subset and embedded as base64 — 26KB. No monospace anywhere; real names in diagrams set in the body face, smaller and softer.
- **Fixed the actual "text over each other" bug**: a `max-width` on the section container was squashing every diagram to 544px, scaling viewBox-960 labels to ~9px. The measure now lives on paragraphs only; figures run full width — diagram text renders ~23px at desktop.
- **Hero rebuilt per the dealt blueprint**: split into two tone halves, a real fragment of the product built in HTML (`data-ui`, real labels) on the right — the focal point the first screen was missing.
- **Story text fixed**: captions and glossary are running text — moved to body size in the full ink (the inspector caught them at 14px grey).
- **Real pictures**: the four book states became real interface fragments (one `data-ui` fragment per state, ≥300×200px); two photographs of the subject's world (a kitchen and a spice bazaar, CC0 and CC BY-SA, credited) carry the analogy. SVG drawings no longer count alone.
- **Closing field**: the takeaway pitch sits on the palette's deep leaf-green band, its own ink.
- **Motion per the dealt signature**: masked headline (two authored lines rising from behind their baselines) plus quiet section entrances — a measured floor of 8+ moving elements; the example renders 29.
- **Gates added to the harness**: zero banned patterns in lint (no gradients, shadows at rest, thin rules, tracked caps, monospace labels, index numbers); real-browser inspection at 1440/768/390 — 0 FAIL (headline line counts, body size 19px, contrast 9.3:1, every screen ≥26% filled, no covered text, no empty screens).
- **Contract audits updated**: 42 WCAG pairs for the new palette; verify-explainer now checks fragments, photographs (width/height/alt/lazy), fonts decode, and `data-io` arming; verify.sh prints a 10-page PDF.
- **Templates synced**: fonts.css → Clash Grotesk; annotated-diagram.svg and diagram-kit.svg restyled flat (no gradients, no drop-shadow filters, no monospace, sentence-case zone labels); explainer-page.html rewritten as the quiet-instrument skeleton with slots.

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
