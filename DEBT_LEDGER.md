# Debt Ledger

Known issues in this repo, ordered by severity. Burn items down; never walk past a defect silently.

- [Medium] `templates/chat-flow.mmd` (the Mermaid chat-format pattern) is UNTESTED — no mermaid CLI was available in the build environment and the npm install timed out. Render it at mermaid.live or with `npx @mermaid-js/mermaid-cli` before relying on it, then remove this entry.
- [Low] Visual pass pending human eyes: the agent session that built this repo cannot view images. The 1.1.0 redesign passed all structural, geometry, contrast, render, and pixel-variance checks — but a human should still scroll `examples/recipe-saver-explainer.html` and glance at `assets/*.png` to confirm it *feels* right.
- [Low] Cold-agent test pending: the plan was to have a fresh subagent (no author context) run the skill against the demo app, but the subagent channel was rate-limited during the build; the end-to-end runs were performed by the author instead. Re-running with a fresh session would give a cleaner signal on skill clarity.
- [Low] `scripts/check-svg.py` estimates text width (0.62 em per character) rather than measuring rendered glyph boxes. It is deliberately conservative; treat findings as warnings to confirm.
- [Low] `scripts/check-contrast.py` encodes the palette contract by hand — if a color changes in CSS/SVG, the pair list must be updated in step. A future version could extract pairs from the artifacts directly.
