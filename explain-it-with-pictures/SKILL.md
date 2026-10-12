---
name: explain-it-with-pictures
description: Explain how a codebase, app, or feature works using hand-drawn annotated diagrams — inline SVG, Mermaid, or ASCII — with plain-language captions for people who don't code. Use when the user asks how their project works, wants a visual or illustrated explanation, architecture or flow diagram, says they built it with AI and don't understand it, wants docs or onboarding for non-developers, or needs to explain their system to a stakeholder, a friend, or themselves.
license: MIT
metadata:
  version: "1.0.0"
---

# Explain It With Pictures

Turn a codebase into pictures a non-technical person can follow. The reader is usually the builder — someone who prompted an AI until the app worked, and now wants to understand what they own. They are smart and motivated; they lack the vocabulary. Your job is to hand them that vocabulary, one picture at a time.

Draw everything yourself. Hand-authored SVG, Mermaid, and ASCII beat AI image generation here: text stays crisp, edits stay cheap, files stay tiny, and it costs nothing. Every deliverable is self-contained — one file, no dependencies, no CDNs, no build step, opens offline, prints cleanly.

## The reader

Write for a smart adult who has never written code. They know apps from using them — taps, forms, uploads, "the internet". Their curiosity is about *their* project, so anchor every diagram where they stand: "you" is the person using the app, and the first numbered step is always something the user does.

Explain like a museum placard: name the thing, say what it does, add one vivid detail. Define every technical word at first use, in the same sentence — "the server (the program that listens for requests and answers them)".

## Workflow

1. **Survey the project.** Read just enough to tell the story: the entry point, the 2–4 user-visible actions, where data lives, which outside services get called. Read the running code, not guesses about it. Scope to what was asked — a single feature gets its own flows, while the Big Picture appears only when they asked for the project.
   *Done when:* you can narrate each user action end-to-end — click → what happens → what comes back → where it is stored — from memory.

2. **Write the story list.** Each picture answers one question the reader would actually ask, phrased in their words ("What happens when I save a recipe?"). The full set: one Big Picture, then 2–4 day-in-the-life flows (one per user-visible action), then the cast of characters (the file tree, annotated), then the glossary.
   *Done when:* the story list exists in writing before any drawing starts.

3. **Pick the format** by where the answer lands:

   | Situation | Deliverable |
   |---|---|
   | Quick answer in chat | ASCII or Mermaid diagram, inline, with the numbered story in prose around it |
   | Issue, PR, or markdown doc | Mermaid — GitHub renders it natively |
   | A file the user opens and keeps | Single-file HTML with inline SVGs — the flagship deliverable |
   | They want a PDF | Build the HTML, then tell them: open it → Print → Save as PDF |

   *Done when:* one format is chosen; default to the HTML explainer whenever a file makes sense.

4. **Draw and write.** Start from the templates: [annotated-diagram.svg](templates/annotated-diagram.svg) demonstrates every diagram convention on a worked example; [explainer-page.html](templates/explainer-page.html) is the document skeleton; [chat-flow.mmd](templates/chat-flow.mmd) shows the chat-format pattern. Copy the template, adapt the story, keep the conventions. When several SVGs live in one HTML file, prefix each diagram's internal ids (`arrow`, `cursor`, markers) with a letter per diagram — ids are shared across the whole page.
   *Done when:* every entry in the story list has a diagram — numbered bubbles for flows, named callouts for anatomy — and a plain-words caption.

5. **Self-check, then deliver.** Run the self-check at the bottom of this file; fix everything it catches. Save the HTML to `docs/how-it-works.html` in their project unless they asked for another path. Tell them how to open it in one line ("double-click `docs/how-it-works.html`"). Offer the print-to-PDF path when they want something shareable as a document.
   *Done when:* the self-check is green and the file opens offline with no missing pieces.

## Craft rules for annotated diagrams

1. **One question per diagram.** A second question earns a second diagram.
2. **Dual-label every box.** Plain-language name on top ("The kitchen — your server"), real name small underneath (`server.js`). The reader learns the map and the territory together.
3. **Number the story.** Numbered bubbles ①②③ in reading order, sitting on the flow path like numbered stops on a map. The caption walks the numbers in prose. Arrows alone tell no story — numbers do. Bubbles belong to flows; an anatomy picture (one thing opened up and labeled) uses named callouts instead.
4. **Label every arrow** with what travels it: "your recipe, as a message", "the finished recipe", "error: needs a title".
5. **Mark user touchpoints.** A cursor glyph beside anything the user clicks or types. This is where the reader says "that's me".
6. **Five colors, one meaning each, one legend per flow diagram.** Blue = what you see (the front end), green = server code, amber = where data lives, red = errors, gray = the outside world. Same meanings in every diagram in the document; anatomy pictures label their own parts instead of carrying a legend.
7. **Group boxes into labeled zones** when a diagram has more than three parts — soft-tinted background bands with small caps titles, as in the template.
8. **Zoom-in callouts for mysterious parts.** Dashed ring around the box, dashed line to an enlarged detail — the map's "you are here" insert.
9. **"In plain words:" caption under every diagram** — the caption walks the numbered story, then closes with one sentence carrying an everyday analogy (restaurant kitchen, filing cabinet, postal service). Pick one analogy per concept and sustain it across the whole document.
10. **Simplify honestly.** Where you collapsed steps, write "(simplified)" on the diagram. Leave one red error arrow as a hint even when you skip the details.
11. **Scale large codebases by zooming, never by crowding.** The Big Picture boxes whole subsystems; each subsystem then gets its own day-in-the-life diagram.

## Plain-language rules

- Box labels max 14 words; full sentences live in captions, never in boxes.
- Define every technical term at first use, then gather all of them into a glossary section titled "Words you'll hear".
- Active voice. The user is "you". Systems get named things, not acronyms.
- Numbers over adjectives: "about 3 files change" beats "a few files".
- Screenshot-sized honesty: where reality has more moving parts than your picture, say so in the caption.

## Document outline (HTML deliverable)

1. **Title + "In plain words"** — one paragraph anyone can follow, zero jargon.
2. **The big picture** — one diagram showing every part and how they connect.
3. **What happens when you…** — one day-in-the-life diagram per user action.
4. **The cast of characters** — the real file tree, one human sentence per file: what it is and what happens if you delete it.
5. **Words you'll hear** — the glossary, in the order they appeared.
6. **How to explain it to a friend** — a three-sentence summary the reader can memorize and repeat.

## Self-check before delivering

- [ ] Every box dual-labeled; every arrow labeled; every technical term defined at first use and in the glossary.
- [ ] Every flow diagram has numbered bubbles; every diagram has a plain-words caption and answers exactly one question.
- [ ] A legend is present, five colors or fewer, same meanings throughout the document.
- [ ] Every user touchpoint is marked; the first numbered step is something the user does.
- [ ] The cast list matches the real file tree; the story list covers every user-visible action.
- [ ] The file opens offline (every font and image is inline or system) and prints cleanly (light background, text ≥14px).
- [ ] A person who has never coded could read it top to bottom without asking a single question.
