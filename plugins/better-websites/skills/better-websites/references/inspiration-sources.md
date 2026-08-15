# Inspiration sources — how to actually use them

Three sources, three altitudes: Refero = whole design systems, MotionSites = motion direction, Pinterest = low-level details. Phase 0 output is 3–5 written art-direction decisions, stated to the user before building.

## Refero Styles — structure & typography

`https://styles.refero.design/` — 2,000+ design systems extracted from real shipped product sites, browsable by Trending/Popular/Newest. Each style has an **AI-readable DESIGN.md** built specifically for tools like Claude Code, covering colors, typography, spacing, and components.

Workflow:
1. WebFetch the index (or a search/category page) and ask for styles matching the project's vibe ("premium automotive", "playful kids brand", "clean SaaS").
2. Pick ONE. Fetch its page / DESIGN.md.
3. Extract and adopt: type scale + weights, spacing rhythm, corner radii, shadow/border language, layout density.
4. **Do not adopt its palette** — colors come from Phase 1 (Realtime Colors roles). You're borrowing skeleton, not skin.

If WebFetch returns thin content (JS-rendered), open it in the Browser pane (`preview_start {url}`) and read the page there.

## MotionSites — motion direction

`https://motionsites.ai/` — gallery of animated example sites by category: SaaS, agencies, portfolios, 3D, e-commerce, travel, wellness, fintech, fashion. Also has ready-made builder prompts and animated background ideas.

Workflow:
1. Fetch/browse the category matching the project.
2. Look at 1–2 examples; identify what moves and how (hero entrance, scroll behavior, hover language, tempo).
3. Write a one-line motion direction, e.g. "slow luxury: blur-in hero, parallax product shots, nothing bounces" or "energetic SaaS: text-loop headline, marquee logos, spotlight cards".
4. Every effect chosen in Phase 3 must serve this line. If an effect doesn't fit the direction, it doesn't ship.

## Pinterest — low-level ideas

`https://uk.pinterest.com/search/pins/?q=<url-encoded query>` — the best place for detail-level ideas: textures, grain, card treatments, typography layouts, photo treatments, color moods in the wild.

When: client brand work, hero concepts, or any build where the user asks for a specific *feel*. Skip for utility pages and quick demos.

Workflow:
1. Pinterest is JS-heavy — **use the Browser pane** (`preview_start {url: "https://uk.pinterest.com/search/pins/?q=..."}`), not WebFetch.
2. Search concrete queries: "editorial landing page typography", "grain texture website", "automotive website dark ui", "kids brand pattern".
3. Screenshot the results grid; pick 1–2 detail ideas (a texture, a card style, a type treatment) and name them in the art-direction summary.
4. Ideas only — never copy an image from Pinterest into a build (unlicensed). Recreate the *technique* in code (CSS grain, gradients, layout).

## The art-direction summary (Phase 0 deliverable)

Template — post this to the user before coding:

```
Art direction:
- Concept: "<one sentence — the design organizing principle from creative-layouts.md>"
- Signature moment: <the one centerpiece — sticky scene / reveal / giant-word interaction / …>
- Hero: <archetype from creative-layouts.md>
- Style reference: <Refero style name> — taking its <type scale / spacing / radii>
- Motion direction: "<one line>"
- Details: <2–3 marginalia/texture ideas>
- Palette: <realtimecolors preview URL>
```
