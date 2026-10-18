---
name: explain-it-with-pictures
description: Explain how a codebase works using hand-drawn annotated diagrams — inline SVG built on a locked type, spacing and color system — plus plain-language captions, for people who don't code. Use when the user asks how their project works, wants a visual or illustrated explanation, architecture or flow diagram, says they built it with AI and don't understand it, wants docs or onboarding for non-developers, or needs to explain their system to a stakeholder, a friend, or themselves.
license: MIT
metadata:
  version: "1.2.0"
---

# Explain It With Pictures

Turn a codebase into pictures a non-technical person can follow — and tell the story in an order they can actually receive: hook, reveal, mechanism, payoff, takeaway. The reader is usually the builder — someone who prompted an AI until the app worked, and now owns something they can't explain. They are smart and motivated; they lack the vocabulary. Your job is to hand them that vocabulary, one picture at a time.

Draw everything yourself. Hand-authored SVG, Mermaid, and ASCII beat AI image generation here: text stays crisp, edits are one-line changes, files stay tiny, and it costs nothing. Every deliverable is self-contained — one file, no dependencies, no CDNs, no build step, opens offline, prints cleanly.

## The reader

Write for a smart adult who has never written code. They know apps from using them — taps, forms, uploads, "the internet". Their curiosity is about *their* project, so anchor every diagram where they stand: "you" is the person using the app, and the first numbered step is always something the user does.

Explain like a museum placard: name the thing, say what it does, add one vivid detail. Define every technical word at first use, in the same sentence — "the server (the program that listens for requests and answers them)".

## The story: hook → reveal → mechanism → payoff → takeaway

1. **Survey the project.** Read just enough to tell the story: the entry point, the 2–4 user-visible actions, where data lives, which outside services get called. Read the running code, not guesses about it. Scope to what was asked — a single feature gets its own flows, while the Big Picture appears only when they asked for the project.
   *Done when:* you can narrate each user action end-to-end — click → what happens → what comes back → where it is stored — from memory.

2. **Write the story list.** Each picture answers one question the reader would actually ask, phrased in their words ("What happens when I save a recipe?"). The full set, in order: one Big Picture (reveal), then 2–4 day-in-the-life flows (mechanism), then one anatomy picture (one thing opened up) and one hierarchy picture (the files) (payoff), then the cast of characters, the glossary, and a one-paragraph takeaway (takeaway). Precede it all with a one-paragraph plain-words hook.
   *Done when:* the story list exists in writing before any drawing starts.

3. **Pick the format** by where the answer lands:

   | Situation | Deliverable |
   |---|---|
   | Quick answer in chat | ASCII or Mermaid diagram, inline, with the numbered story in prose around it |
   | Issue, PR, or markdown doc | Mermaid — GitHub renders it natively |
   | A file the user opens and keeps | Single-file HTML with inline SVGs — the flagship deliverable |
   | They want a PDF | Build the HTML, then tell them: open it → Print → Save as PDF |

   *Done when:* one format is chosen; default to the HTML explainer whenever a file makes sense.

4. **Draw and write.** Start from the templates: [diagram-kit.svg](templates/diagram-kit.svg) is the reference kit showing every diagram type and all conventions; [explainer-page.html](templates/explainer-page.html) is the document skeleton carrying the type, spacing, color and motion system; [chat-flow.mmd](templates/chat-flow.mmd) shows the chat-format pattern. Copy the template, adapt the story, keep the conventions. Typography: serif display for titles, humanist sans for body, monospace for real names — paste [fonts.css](templates/fonts.css) (embedded OFL fonts) into the marked slot so the deliverable keeps its typography while staying one offline file. When several SVGs live in one HTML file, prefix each diagram's internal ids (`arrow`, `cursor`, markers) with a letter per diagram — ids are shared across the whole page.
   *Done when:* every entry in the story list has the right diagram type, drawn to the craft rules, and a plain-words caption.

5. **Self-check, then deliver.** Run the self-check at the bottom of this file; fix everything it catches. Save the HTML to `docs/how-it-works.html` in their project unless they asked for another path. Tell them how to open it in one line ("double-click `docs/how-it-works.html`"). Offer the print-to-PDF path when they want something shareable as a document.
   *Done when:* the self-check is green and the file opens offline with no missing pieces.

## Craft rules for annotated diagrams

1. **One question per diagram.** A second question earns a second diagram.
2. **Dual-label every box.** Plain-language name on top ("The kitchen — your server"), real name small underneath (`server.js`). The reader learns the map and the territory together.
3. **Number the story.** Numbered bubbles ①②③ in reading order, sitting on the flow path like numbered stops on a map. The caption walks the numbers in prose. Arrows alone tell no story — numbers do. Bubbles belong to flows; an anatomy picture (one thing opened up and labeled) uses named callouts instead.
4. **Label every arrow** with what travels it: "your recipe, as a message", "the finished recipe", "error: needs a title".
5. **Mark user touchpoints.** A cursor glyph beside anything the user clicks or types. This is where the reader says "that's me".
6. **Five semantic colors, one meaning each, one legend per flow diagram.** Blue = what you see (the front end), green = server code, amber = where data lives, red = errors, gray = the outside world. Same meanings in every diagram in the document; anatomy pictures label their own parts instead of carrying a legend.
7. **Group boxes into labeled zones** when a diagram has more than three parts — soft-tinted background bands with small caps titles, as in the kit.
8. **Zoom-in callouts for mysterious parts.** Dashed ring around the box, dashed line to an enlarged detail — the map's "you are here" insert.
9. **"In plain words:" caption under every diagram** — the caption walks the numbered story, then closes with one sentence carrying an everyday analogy (restaurant kitchen, filing cabinet, postal service). Pick one analogy per concept and sustain it across the whole document.
10. **Simplify honestly.** Where you collapsed steps, write "(simplified)" on the diagram. Leave one red error arrow as a hint even when you skip the details.
11. **Scale large codebases by zooming, never by crowding.** The Big Picture boxes whole subsystems; each subsystem then gets its own day-in-the-life diagram.
12. **Geometry safety — boxes, labels, arrows never touch.** Every box gets inner padding of at least 16px horizontally and 12px vertically; its width is the widest line inside it plus 2 × padding, never eyeballed. Boxes stay at least 24px apart. Labels sit in gutters between boxes, at least 8px from any box edge. Arrows start and end at box edges; arrowheads never sit inside a box. No text may touch or overlap another text. The checker (scripts/check-svg.py) enforces all of this — run it before delivering.
13. **Type scale — five sizes, far apart.** Display (titles, clamp 3–9rem), head (sections, clamp 2–4rem), lead (plain-words statement, clamp 1.25–1.625rem), body (17–19px), small (captions/labels, 13–14px). No sizes between them. Tracking tightens as size grows (display −0.02 to −0.05em); body leading 1.45–1.6; text left-aligned, max 75 characters per line; five sizes maximum on a page.
14. **Spacing scale — one base, every gap a step.** Base 4px: 4, 8, 12, 16, 24, 32, 48, 64. Section gaps are clearly larger than gaps inside one section (desktop 120–220px); related things close, unrelated things far; a heading gets at least twice as much space above as below. Never arbitrary pixel values.
15. **Color — ground, ink, muted, accent.** One ground (most of the surface), one ink (text and strongest marks), one muted (secondary text; still passes contrast on the ground), one accent (marks the action, under 5% of any screen — never on headings, borders, icons or underlines). Diagram semantic colors live inside figures only and never double as the document accent. Every text/background pair passes 4.5:1; graphics pass 3:1 (scripts/check-contrast.py encodes the palette contract).
16. **Move with restraint.** Reveal each diagram once, on scroll, in story order: zones settle, boxes fade, arrows draw, bubbles pop, labels follow, insets last — everything inside 1.2 seconds. Motion lives under a `prefers-reduced-motion: no-preference` media query, hidden states only apply under a JS-set class (a frozen page still shows everything), and print forces final states. The skeleton in [explainer-page.html](templates/explainer-page.html) carries the whole system — copy it, set `--seq` per story beat.

## Plain-language rules

- Box labels max 14 words; full sentences live in captions, never in boxes.
- Define every technical term at first use, then gather all of them into a glossary section titled "Words you'll hear".
- Active voice. The user is "you". Systems get named things, not acronyms.
- Numbers over adjectives: "about 3 files change" beats "a few files".
- Screenshot-sized honesty: where reality has more moving parts than your picture, say so in the caption.

## Diagram type library — pick the type by the question

| Diagram type | Answers… |
|---|---|
| **Flow** — numbered bubbles on labeled arrows | "What happens when I do X?" one user action, start to finish |
| **Hierarchy** — nested boxes, parent contains children | "What is this made of?" files in folders, subsystems in system |
| **Comparison** — two columns, shared parts aligned | "What changed?" before / after, option A / option B |
| **Timeline** — horizontal marks on actor rows | "When does what happen?" over time, who acts when |
| **Anatomy** — one thing opened up, fields with callout labels | "What does this look like inside?" one file, one record, one message |
| **Decision tree** — yes/no branches to outcomes | "What happens if…?" validation, errors, routing |
| **Small multiples** — same diagram, N states side by side | "What does it look like over time?" empty → one → many → error |
| **Zoom callout** — dashed ring + enlarged detail | "What is inside that one part?" a mysterious box explained |

Never force a second question into a diagram that already answers one — the type list is a reason to split, not to pack.

## Document outline (HTML deliverable)

1. **Title + "In plain words"** (hook) — one paragraph anyone can follow, zero jargon, set large.
2. **The big picture** (reveal) — one flow diagram showing every part and how they connect.
3. **What happens when you…** (mechanism) — one day-in-the-life flow diagram per user action.
4. **Where your data lives** — one anatomy diagram, one record opened up.
5. **The book over time** — one small-multiples diagram: empty → one → many → error.
6. **The cast of characters** (payoff) — hierarchy diagram of the real file tree: what each file is, what happens if it goes missing.
7. **Words you'll hear** — the glossary, in the order they appeared.
8. **How to explain it to a friend** (takeaway) — a three-sentence summary the reader can memorize and repeat.

## Self-check before delivering

- [ ] Every box dual-labeled; every arrow labeled; every technical term defined at first use and in the glossary.
- [ ] Every flow diagram has numbered bubbles; every diagram has a plain-words caption and answers exactly one question; diagram type matches the question it answers.
- [ ] Geometry clean: text inside its box with padding, boxes ≥ 24px apart, labels ≥ 8px from boxes, no overlapping text — `scripts/check-svg.py` is green.
- [ ] A legend is present on every flow diagram, five colors or fewer, same meanings throughout the document.
- [ ] Every user touchpoint is marked; the first numbered step is something the user does.
- [ ] Type scale holds: five sizes or fewer, sizes clearly different, text left-aligned, measure ≤ 75 chars.
- [ ] Color: ground / ink / muted / accent roles; accent under 5% and never on headings; every pair passes 4.5:1 — `scripts/check-contrast.py` is green.
- [ ] Motion: story-ordered reveals under 1.2s, disabled for reduced-motion and print, content fully visible without JS.
- [ ] The file opens offline (every font and image is inline or system) and prints cleanly (light background, text ≥14px).
- [ ] The cast list matches the real file tree; the story list covers every user-visible action.
- [ ] A person who has never coded could read it top to bottom without asking a single question.
