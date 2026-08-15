# Realtime Colors — palette system

Site: https://www.realtimecolors.com/ — previews a palette + font pairing on a realistic website mockup instead of abstract swatches. Free; exports CSS, Tailwind, SCSS, shadcn/DaisyUI presets, shades, gradients.

## The 5 roles

Every palette is exactly five colors. Order matters — it's how the URL encodes them:

| # | Role | Used for | Share of page |
|---|---|---|---|
| 1 | `text` | Body copy, headings | — |
| 2 | `background` | Page background | ~60% |
| 3 | `primary` | Main CTAs, key sections, brand surfaces | ~30% (with secondary) |
| 4 | `secondary` | Muted surfaces, info cards, less-important buttons | ~30% (with primary) |
| 5 | `accent` | Links, highlights, hover states, decorative pops | ~10% |

**60-30-10 rule**: ~60% of any viewport is background/neutral, ~30% primary/secondary surfaces, ~10% accent. When a page looks "off", it's almost always accent overuse — accent belongs on the CTA, links, and at most one decorative element per viewport.

## URL format (always share this with the user)

```
https://www.realtimecolors.com/?colors=<text>-<bg>-<primary>-<secondary>-<accent>&fonts=<HeadingFont>-<BodyFont>
```

Hex values **without** `#`, in the role order above. Font names capitalized, Google Fonts names with spaces URL-encoded (`Space+Grotesk`).

House default (use when the client has no brand colors):
```
https://www.realtimecolors.com/?colors=050315-fbfbfe-2f27ce-dedcff-433bff&fonts=Inter-Inter
```
→ text `#050315` · background `#fbfbfe` · primary `#2f27ce` · secondary `#dedcff` · accent `#433bff` · Inter/Inter.

## Deriving a palette for a client

1. Start from the brand: logo color → `primary`. If no brand, pick primary by industry mood (trust/tech → blue-violet; automotive/premium → near-black + metallic accent; wellness → deep green; kids → warm saturated).
2. `accent` = a brighter/shifted sibling of primary (same hue family, +10–20 lightness or a 20–40° hue shift). Not a random second color.
3. `secondary` = primary desaturated and lifted to near-pastel (works as card/surface tint).
4. `text` = near-black tinted toward primary's hue (never pure `#000`); `background` = near-white tinted the same way (never pure `#fff`).
5. Dark sites: invert — `text` near-white, `background` near-black (tinted), keep primary/accent saturated, `secondary` becomes a dark elevated-surface tone.
6. Build the realtimecolors URL and include it in your summary so the user can preview and veto before/while you build.

## In code

Define once, use everywhere — no loose hexes:

```css
:root {
  --text: #050315;
  --background: #fbfbfe;
  --primary: #2f27ce;
  --secondary: #dedcff;
  --accent: #433bff;
}
```

Derived values via `color-mix()` instead of new hexes:
```css
--surface: color-mix(in srgb, var(--secondary) 35%, var(--background));
--border:  color-mix(in srgb, var(--text) 10%, transparent);
--accent-soft: color-mix(in srgb, var(--accent) 12%, transparent); /* glows, spotlights */
```

Contrast floor: text-on-background and text-on-primary must clear WCAG AA (4.5:1 body, 3:1 large text). If a role fails, adjust lightness of that role, not with a sixth color.
