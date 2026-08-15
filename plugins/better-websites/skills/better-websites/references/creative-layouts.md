# Creative layouts — where builds stop being templates

Color, motion, and backgrounds decorate a layout; they cannot rescue one. This file is the layout playbook. Pick deliberately — one hero archetype, one grid strategy, one signature moment — and name them in the art-direction summary.

## Banned defaults

These are what every AI builds when nobody's watching. Any of them appearing without a deliberate reason is a failure:

- Centered hero: eyebrow → H1 → subhead → two buttons → trust row
- Three equal cards in a row (or any N equal cards with icon/title/text)
- Stats row of 3–4 centered numbers
- Centered section headers on every section
- Every section the same container width, same ~120px padding, stacked like pancakes
- Testimonial cards with quote-name-role, all identical
- Content that never touches, overlaps, or crosses anything

You may still *use* cards, stats, testimonials — but composed, not defaulted (see Section treatments).

## The concept

One sentence, derived from the brand's physical world, that the layout dramatizes. Not a tagline — a *design organizing principle*.

- Forge/gym → "The page is a temperature scale: white-hot at the top, cooling to black steel at the bottom" → palette shifts per section, molten dividers, heat-glow hovers
- Barber → "The page is a price list taped to a mirror" → full-bleed photo background, content as taped paper scraps, handwritten annotations
- Accountant → "The page is a ledger" → ruled lines, tabular everything, numbers oversized, red/black ink
- Kids brand → "The page is a sticker book" → elements rotated and layered like stickers, die-cut white borders

Every major layout decision should be explainable by the concept. That's what makes a site feel *designed by a person with an idea*.

## Hero archetypes (never the centered stack)

1. **Giant word** — brand name or one power word at 18–28vw filling the viewport, everything else tiny around it. Photo or texture can sit *inside* the letters (`background-clip: text`) — the proven photo-in-type formula.
2. **Split screen** — hard vertical split; one side type, other side full-bleed media/color/generated scene. Asymmetric splits (60/40, 70/30) beat 50/50.
3. **Editorial cover** — magazine front page: masthead, huge multi-line headline flush-left, dateline/issue-number microtype, one dominant image, credits in the corners.
4. **Offset composition** — headline pinned to a corner or crossing the fold-line; big whitespace on one side; supporting elements scattered on a visible or implied grid.
5. **Scene** — the hero is a picture built from layers (SVG scene, gradient sky, silhouettes, particles) with the type *inside* the scene, not on top of a rectangle.
6. **Ticker frame** — content framed by marquees running along edges (top/bottom or sides), center stage minimal.

## Grid strategies

- **Editorial 12-col**: place items on odd spans (2–7, 8–12, 3–11). Neighbors get different widths and vertical offsets (`margin-top` staggers). Nothing centers unless it earns it.
- **Overlap**: negative margins / grid areas that share tracks; type crossing image edges; a card breaking into the next section's background. Depth via z-index + shadow discipline.
- **Bleed contrast**: alternate full-bleed color-blocked sections with narrow-measure text sections (55–65ch). The rhythm wide-narrow-wide reads as pacing, not stacking.
- **Rotation & scatter**: small elements (stamps, labels, badges) rotated 2–8°, positioned absolutely near content they annotate. Keep body text straight.
- **Vertical text**: `writing-mode: vertical-rl` for section labels along the edge — instant editorial feel, costs one line of CSS.

## Signature moments (pick ONE, make it the page's centerpiece)

- **Sticky scene**: a `position: sticky` panel that stays while 2–4 story beats scroll past it (steps, before/after states, numbers changing)
- **Horizontal scroll strip**: one section scrolls sideways inside vertical scroll (scroll-snap; graceful fallback to overflow-x)
- **Scroll-driven transformation**: something builds as you scroll — a word fills with color, a scene assembles, a number climbs with scroll position (`animation-timeline: scroll()` with rAF fallback)
- **Type-as-hero interaction**: giant word reacts to cursor (spotlight through letters, characters scatter/magnetize)
- **The reveal**: a full-viewport color/image flip mid-page — the page "turns over" into an inverted palette for its second half (great for concept contrast: day/night, before/after)

## Section treatments (instead of the defaults)

- Cards → **index list**: full-width rows, huge outline numerals, title at display size, hover expands or reveals an image. Or one BIG card + two small, sized by importance.
- Stats → **one enormous number** (20vw) with the story around it, others as marginalia. Or numbers inline inside sentences at 3× body size.
- Testimonials → **one editorial pull-quote** at display size with oversized punctuation, others as a compact strip. Or a marquee of short quotes.
- Process → sticky scene (above) or a numbered spine down the page edge that fills as you scroll.
- Form → make it conversational ("I'm __name__ and I want to __goal__") or place it inside the signature moment, not in a grey card at the end.
- Footer → **poster footer**: the brand name at giant scale, links as microtype around it. The last thing seen should look intentional.

## The details layer (2–3 per page, minimum)

Marginalia and microtype are what make a page feel art-directed: index numbers ("01 / Method"), rotated edge labels, coordinates/postcode as decoration ("53.4808°N"), file-folder tabs, stamps ("EST. 2019", "NO CROWDS"), oversized asterisks/arrows as graphic elements, a footnote that's actually funny, `¶` section marks, grain overlay (SVG feTurbulence at 4–6% opacity), custom selection color (`::selection` in accent).

## Guardrails (creative ≠ chaotic)

- The concept picks ONE of everything: one hero archetype, one signature moment, 2–3 details. A page trying five ideas reads as slop from the other direction.
- Break the grid *from* a grid: set the 12-col system first, then violate it deliberately. Random placement without an underlying grid reads as broken, not bold.
- Type scale needs contrast to feel designed: if H1 is 8rem, body stays ~1.06rem, and *nothing* lives between 3–6rem except one thing. Mid-sized-everything is the template look.
- Readability of body copy is never the creative sacrifice: measure 55–75ch, contrast AA, no body text over busy backgrounds without a scrim.
- Mobile: overlaps and offsets flatten gracefully (grid falls to fewer columns, offsets reduce, horizontal strips become swipe). Check the narrow viewport before ship.
