# Explain It With Pictures

An open-source skill for AI coding agents (Claude Code, opencode, Cursor, Codex…) that turns any codebase into **illustrated, annotated explanations a non-technical person can follow** — with the polish of a designed product, not a generated doc.

Built for **vibe coders** — people who build working software by prompting AI and end up owning something they can't fully explain. Ask your agent *"explain how my project works"* and instead of a wall of jargon you get a single illustrated HTML document: hand-drawn diagrams that animate their story step by step, labeled arrows, plain-words captions, an annotated file tree, and a glossary.

![The big-picture diagram from the example explainer](assets/example-big-picture.png)
*A diagram the skill produced for a small real app: labeled zones, dual-labeled boxes (plain words + real filename), numbered story bubbles, labeled arrows, a legend.*

## Free and simple, on purpose

- **Hand-drawn, not AI-generated.** The agent draws SVG diagrams itself. Text stays crisp, edits are one-line changes, files stay tiny — and it never calls an image-generation API.
- **One self-contained file.** No dependencies, no CDNs, no build step. Fonts are embedded as base64 (SIL OFL), so it opens offline with its typography intact and prints to a clean PDF. Try it: [recipe-saver-explainer.pdf](assets/recipe-saver-explainer.pdf) (7 pages, straight from Print).
- **Zero paid services.** No accounts, no network calls, no API keys.
- **Readable by someone who has never coded.** Every technical word defined at first use and gathered into a glossary; every diagram ends with an "In plain words:" analogy caption.

## Design language

The templates ship a complete, opinionated design system — the example below is generated from it, not hand-tuned:

| Layer | What it does |
|---|---|
| **Typography** | Fraunces (display serif) for titles, Inter for body, JetBrains Mono for real names and code — embedded, subset, offline |
| **Motion** | One reveal per diagram, on scroll, in story order: zones settle → boxes fade → arrows draw themselves → numbered bubbles pop → zoom-in insets last. All under 1.2s, spring-eased |
| **Accessibility** | Reduced-motion gets the fully-rendered static page; JS dies → content stays visible; every diagram has a `<title>`; print forces final states |
| **Color** | Five semantic colors (front end / server / data / errors / replies), violet as the signature accent — every pair WCAG-checked |
| **Structure** | Sticky blurred header with reading progress, numbered chapters, generous spacing, print-safe layout |

## What you get

Ask your agent:

> "Explain how my project works — illustrate it. I built this with AI and don't really understand it."

You'll get `docs/how-it-works.html` in your project, containing:

1. A one-paragraph, zero-jargon summary
2. **The big picture** — every part and how they connect
3. **What happens when you…** — an animated day-in-the-life per user action, including a zoom-in on the actual messages that travel
4. Your data opened up and labeled, field by field
5. **The cast of characters** — every file in one human sentence, including what happens if you delete it
6. **Words you'll hear** — the glossary
7. **How to explain it to a friend** — a three-sentence summary to memorize

See it for real — the skill was run end-to-end against a small working app:

- **The app:** [`examples/recipe-saver/`](examples/recipe-saver/) — a real recipe saver with a server, a page, and a data file
- **The result:** [`examples/recipe-saver-explainer.html`](examples/recipe-saver-explainer.html) — open it in a browser and scroll
- **What the app looks like:** `assets/app-ui.png` · **Full page:** [`assets/explainer-full.png`](assets/explainer-full.png) · **Print:** [`assets/recipe-saver-explainer.pdf`](assets/recipe-saver-explainer.pdf)

![The save-recipe story diagram, with the message zoom-in inset](assets/example-save-flow.png)
*The save flow — including a violet zoom-in inset showing the actual JSON message that travels from page to server.*

## Install

**Skills CLI:**

```bash
npx skills add imranshiundu/explain-it-with-pictures@explain-it-with-pictures -g -y
```

**Manual:** clone and copy (or symlink) the `explain-it-with-pictures/` folder into your agent's skills directory:

| Agent | Global | Project |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| opencode | `~/.config/opencode/skills/` | `.opencode/skills/` |
| Cursor / Codex / others | your agent's skills folder | |

```bash
git clone https://github.com/imranshiundu/explain-it-with-pictures
ln -s "$(pwd)/explain-it-with-pictures/explain-it-with-pictures" ~/.claude/skills/explain-it-with-pictures
```

The skill fires on questions like *"how does my app work?"*, *"make me a diagram"*, *"explain this to a non-programmer"* — no special invocation needed.

## What the skill teaches your agent

- **One question per diagram** — a second question earns a second diagram.
- **Dual-label every box** — "The kitchen — your server" over `server.js`: the reader learns the map and the territory together.
- **Number the story** — ①②③ bubbles on the flow path, with a caption that walks the numbers.
- **Label every arrow** — "your recipe, as a message", "if something is missing: a friendly error".
- **Five colors, one meaning each** — same meanings in every diagram; legends on every flow.
- **Mark user touchpoints** — a cursor glyph wherever a human clicks or types.
- **Zoom-in callouts** — dashed ring, dashed line, enlarged detail: "here's what the message actually looks like".
- **Sustain one analogy** — if the server is a kitchen, it stays a kitchen for the whole document.
- **Simplify honestly** — "(simplified)" markers where steps were collapsed.
- **Move with restraint** — story-ordered reveals, reduced-motion-safe, print-safe.
- **Scale by zooming, never crowding** — big codebases get subsystem boxes in the big picture and a diagram each.

## Verify / stress test

```bash
./scripts/verify.sh
```

Runs the whole loop on any machine with `node` + `python3` + `curl` (render/PDF checks need Chrome, skipped-and-declared otherwise):

- SVG geometry check — no colliding or clipped labels, on template *and* example
- Explainer validation — balanced HTML, zero loaded external resources, valid diagrams, embedded fonts decode, motion/print/JS-gating present, every diagram titled
- **WCAG 2.1 contrast audit** — 41 design-system color pairs, all ≥ 4.5:1 (text) / 3:1 (graphics)
- Live smoke test of the example app — endpoints, validation errors, path-traversal blocked
- **Live render test** — headless Chrome confirms the reveal script actually runs, and the page prints to a real 7-page PDF
- Fixture integrity — tests never dirty the demo data

## License

[MIT](LICENSE) — use it, fork it, ship it. Diagrams for everyone.
