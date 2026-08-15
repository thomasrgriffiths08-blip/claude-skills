---
name: better-websites
description: The mandatory website-build stack. Use EVERY time the user asks to make, build, redesign, or improve a website, landing page, client site, hero section, or web page of any kind — even when they don't mention any tools by name. It routes every build through six resources — Refero Styles + MotionSites + Pinterest for inspiration, Realtime Colors for the palette system, Haikei-style SVGs for backgrounds, and Motion-Primitives for animation. Trigger on "make me a site", "build a landing page", "website for [client]", "redesign this page", "make this look better", or any request that produces a web page. Also use when an existing build looks flat and the user asks to level it up.
---

# Better Websites — The Site-Build Stack

Every website that leaves this machine goes through the same six-resource pipeline. The point is not to name-drop tools — it's that each one kills a specific failure mode of AI-built sites:

| Failure mode | Fixed by |
|---|---|
| Generic "AI slop" layout invented from nothing | **Refero Styles** — steal structure from real shipped products |
| Static, lifeless page | **MotionSites** — pick a motion direction before coding |
| Vague vibes, no art direction in the details | **Pinterest** — low-level texture/detail ideas |
| Random hex colors sprinkled ad hoc | **Realtime Colors** — 5-role palette + 60-30-10 rule |
| Flat solid-color section backgrounds | **Haikei** — generative SVG waves/blobs/gradients |
| No animation, or janky hand-rolled animation | **Motion-Primitives** — proven motion components |

Work the phases in order. Phase 0 is cheap (a few minutes of fetching) and is what separates a designed site from a generated one — don't skip it to "save time."

## ⚠️ FIRST: is this a marketing page or a product UI?

This pipeline is calibrated for **marketing surfaces** — landing pages, client sites, hero sections. It is the WRONG treatment for **product UIs** (CRMs, dashboards, admin tools, app demos, anything with a sidebar and data). Applying hero-page moves to an app is how a build ends up "super vibecoded" — learned the hard way, on a CRM build that got the full hero treatment and looked it.

**For product UIs, skip Haikei/MotionSites/Pinterest entirely and follow the app-UI rules instead:**
- **Monochrome + one accent.** White/near-white surfaces, 1px hairline borders, ink text, ONE restrained accent used sparingly. Semantic red/green as *text colour*, not filled pills.
- **Flat.** No gradients, no glows, no coloured shadows, no glassmorphism, no tinted icon chips, no per-category colour rainbows. Radius ≤6px — nothing pill-shaped.
- **Dense.** Information first: smaller base font (14–15px), tight padding, more data per screen. Decoration ≈ 0 — no watermarks, motifs, or ornamental SVGs.
- **Still.** No entrance animations, staggers, blur reveals, or pulses. Animated *data* (a counting number, a growing bar) is fine; animated *chrome* is not.
- **Neutral identity.** Grey initials avatars, flat ink logo marks. Reference: Linear light mode / a serious internal tool — not a launch page.

Marketing pages keep the full pipeline below. When in doubt ("improve the look" of something with a sidebar): it's a product UI.

**The creative mandate — read this first.** Executing the phases cleanly is not enough. A page can pass every rule below and still be a template: centered hero with eyebrow + two buttons, three equal cards, a stats row, testimonials, a form. That layout is *banned as a default*. Every build must be organized around **one concept** — a single big idea derived from the brand, stated in one sentence — and must contain **one signature moment** the visitor will remember. Layout is where creativity lives; color and motion only decorate it. Before Phase 1, read `references/creative-layouts.md` and pick a hero archetype, a grid strategy, and a signature moment from it (or invent better ones). The test: *if you swapped the logo and copy, could this be any other business's site?* If yes, the layout failed regardless of polish.

## Phase 0 — Concept & inspiration (before writing any code)

Read `references/inspiration-sources.md` for the exact URLs and fetch patterns. Summary:

1. **Refero Styles** (`https://styles.refero.design/`) — 2,000+ design systems extracted from real product sites, each with an AI-readable DESIGN.md built for Claude Code. Find one style that matches the project's vibe, fetch its DESIGN.md, and use it as design context: typography scale, spacing rhythm, corner radii, shadow language. Keep the house color roles (Phase 1) — you're borrowing *structure and typography*, not the palette.
2. **MotionSites** (`https://motionsites.ai/`) — gallery of animated sites by category (SaaS, agency, portfolio, 3D, e-commerce, wellness…). Match the project's category, look at 1–2 examples, and write down a one-line *motion direction* (e.g. "slow blur-in hero, marquee logos, cards tilt on hover"). Every animation you add later must serve this one direction — that's what makes motion feel designed instead of sprinkled.
3. **Pinterest** (`https://uk.pinterest.com/search/pins/?q=<query>`) — for lower-level ideas: textures, grain, card treatments, type layouts, photo treatment. Use when the build needs art direction in the details (client brand work, hero concepts) — skip for quick utility pages. Pinterest is JS-heavy; use the Browser pane, not WebFetch.

Deliverable of Phase 0: the art-direction summary — **concept sentence, signature moment, hero archetype**, style reference, motion direction, 1–2 detail ideas. State it to the user before building — it reads as taste and lets them redirect early. If you can't write the concept sentence, you're not ready to code; go back to the brand and dig for its physical world (a forge has heat, sparks, metal, temperature — a bakery has flour dust, ovens, 4am — every business has one).

## Phase 1 — Color system (Realtime Colors)

Read `references/color-system.md` for full detail. The rules:

- Every site uses exactly **5 color roles**: `text`, `background`, `primary`, `secondary`, `accent`. Define them once as CSS variables; never introduce an unrelated hex mid-build.
- Distribute by the **60-30-10 rule**: ~60% background/neutral, ~30% secondary/primary surfaces, ~10% accent. Accent is precious — CTAs, links, one highlight per viewport.
- If the client has brand colors, map them into the 5 roles. If not, start from **the house default palette**: text `#050315`, background `#fbfbfe`, primary `#2f27ce`, secondary `#dedcff`, accent `#433bff`, font Inter.
- **Always give the user a live preview link** for the chosen palette so they can eyeball it before you build:
  `https://www.realtimecolors.com/?colors=<text>-<bg>-<primary>-<secondary>-<accent>&fonts=<Heading>-<Body>` (hex values without `#`).

## Phase 2 — Backgrounds (Haikei-style SVG)

Flat solid sections are the #1 tell of a generated site. Haikei (`https://haikei.app/`) makes layered waves, blobs, blob scenes, blurry gradients, low-poly grids, and circle scatters — but it's GUI-only, so generate equivalent SVGs in code with the bundled script:

```bash
python3 scripts/haikei.py layered-waves --colors 2f27ce,433bff,dedcff --width 1440 --height 420 --seed 7
```

Generators: `wave`, `layered-waves`, `blob`, `blob-scene`, `blurry-gradient`, `circle-scatter`. Paste the SVG inline (single-file HTML) or save as an asset. Read `references/haikei-backgrounds.md` for placement rules — which generator suits hero vs. section divider vs. footer, opacity/layering guidance, and when to send the user to the Haikei app itself for manual export.

Use palette colors only (shades of primary/secondary/accent) so backgrounds feel like the same design system.

## Phase 3 — Motion (Motion-Primitives)

Motion-Primitives (`https://motion-primitives.com/`) is a shadcn-style library of animation components built on Motion (Framer Motion's successor) + Tailwind. Two paths — pick by project type:

- **React/Next.js project** → install the real components:
  `npx motion-primitives@latest add <component>` (or via shadcn registry: `npx shadcn@latest add "https://motion-primitives.com/c/<component>.json"`).
- **Single-file HTML / static site** (most client builds) → recreate the named effects in vanilla CSS/JS. `references/motion-primitives.md` has the full component catalog plus tested vanilla recipes for the ten most useful ones (blur-in reveal, text shimmer, infinite slider, spotlight card, border trail, animated counter, tilt, scroll progress, magnetic button, text loop).

Motion rules regardless of path:
- Every animation must serve the Phase-0 motion direction. If you can't say which direction an effect serves, cut it.
- Reveal-on-scroll for content entering the viewport (IntersectionObserver, once, ~0.6s, ease-out, slight blur+y-offset) is the baseline — every section gets it.
- Then add **2–4 signature effects maximum**. A page where everything moves reads as AI slop just as hard as a page where nothing does.
- Respect `prefers-reduced-motion`.

## Phase 4 — Ship check

Before showing the user the result, verify:

- [ ] **The template test**: swap the logo and copy in your head — if the layout could belong to any other business, rebuild the layout before showing anything
- [ ] The concept sentence is *visible in the layout* (not just in the copy), and the signature moment exists and is the strongest thing on the page
- [ ] At least two sections break the standard stack (per `references/creative-layouts.md`: overlap, asymmetry, sticky scene, horizontal scroll, editorial grid, type-as-architecture…)
- [ ] All colors trace to the 5 CSS variables; realtimecolors preview link included in your summary
- [ ] At least one Haikei-style background in the hero or a major section (not tiled everywhere — 1–3 per page)
- [ ] Scroll reveals on all sections + your 2–4 signature motion effects, reduced-motion respected
- [ ] The Phase-0 art-direction decisions are visible in the result (name them in your summary)
- [ ] Open it in the Browser pane and screenshot it for the user — never ask them to check it themselves

## Plays with other skills

- **hallmark / avoid-ai-design / frontend-design** govern taste and slop-removal — they still apply; this skill adds the mandatory resource pipeline on top.
- **vibecode-site-stack** adds Spline 3D heroes and publish/analytics — when a build wants a 3D hero or one-click publish, use both skills together; this one owns inspiration, color, backgrounds, and motion.
