# Debt Ledger

Known issues in this repo, ordered by severity. Burn items down; never walk past a defect silently.

- [Medium] `templates/chat-flow.mmd` (the Mermaid chat-format pattern) is UNTESTED — no mermaid CLI was available in the build environment and the npm install timed out. Render it at mermaid.live or with `npx @mermaid-js/mermaid-cli` before relying on it, then remove this entry.
- [Medium] Cold-agent test pending: a fresh subagent (no author context) running the skill against the demo app would give a cleaner signal on skill clarity than the author's own runs. Re-run with a fresh session.
- [Low] Visual pass: the agent cannot view images, so the final *feel* is verified by measurement instead — lint (0 banned patterns), geometry (0 collisions), contrast (45/45), and a real-browser inspection (0 FAIL at 1440/768/390: line counts, body size, screen fill, motion count 29, no covered text). A human should still glance at `assets/explainer-hero.png` and scroll the example; the two honest WARNs are: no video (an honest clip of a local app does not exist, and one would break the single-file promise) and diagrams are small on phones (SVG scales down at 390px; the HTML captions and fragments carry the story there).
- [Low] `scripts/check-svg.py` estimates text width (0.62 em per character) rather than measuring rendered glyph boxes. Deliberately conservative; treat findings as warnings to confirm.
- [Low] `scripts/check-contrast.py` encodes the palette contract by hand — if a color changes in CSS/SVG, the pair list must be updated in step. A future version could extract pairs from the artifacts directly.
- [Low] The full design-taste-frontend inspection (inspect.mjs) lives in that skill, not in this repo — contributors without it get the self-contained subset via `./scripts/verify.sh`. Document both paths.
