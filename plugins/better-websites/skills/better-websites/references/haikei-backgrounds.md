# Haikei-style backgrounds

Site: https://haikei.app/ — free web app generating SVG/PNG backgrounds: waves, layered waves, blobs, blob scenes, blurry gradients, low-poly grids, circle/blob scatters (15 generators). **GUI-only, no API** — so for automated builds, generate equivalent SVGs with the bundled script; send the user to the app only when they want to hand-pick a shape themselves.

## Generating

```bash
python3 scripts/haikei.py <generator> --colors <hex,hex,...> [--width 1440] [--height 420] [--seed 7] [-o out.svg]
```

Generators: `wave` · `layered-waves` · `blob` · `blob-scene` · `blurry-gradient` · `circle-scatter`

- `--colors` — palette hexes without `#`, first = backmost layer. Use shades of primary/secondary/accent only (see color-system.md; generate shades with `color-mix` values baked into the hexes you pass).
- `--seed` — deterministic output; bump it until the shape looks right.
- No `-o` prints SVG to stdout for pasting inline.

Regenerate with a few different seeds and pick the best — that mirrors Haikei's dice button and costs nothing.

## Placement rules (what goes where)

| Spot | Generator | Notes |
|---|---|---|
| Hero background | `blurry-gradient` or `blob-scene` | Soft, behind content; keep text contrast (overlay `color-mix(in srgb, var(--background) 60%, transparent)` if needed) |
| Section divider | `wave` or `layered-waves` | Between color-block sections; wave fill = the *next* section's background so they interlock |
| Stats / CTA band | `layered-waves` | 3–4 layers of primary shades, darkest at bottom |
| Footer top edge | `wave` | Flipped vertically (`transform="scale(1,-1)"`) |
| Empty corners / whitespace | `blob` or `circle-scatter` | Low opacity (0.08–0.2), absolutely positioned, `pointer-events: none`, overflow hidden |

## Rules

- **1–3 per page.** One hero treatment + one or two dividers. Backgrounds on every section = wallpaper, not design.
- **Palette colors only.** A teal wave on a violet site instantly reads as clip-art.
- Inline the SVG in single-file builds; set `aria-hidden="true"` and `preserveAspectRatio="none"` on dividers so they stretch responsively.
- Dividers: width 100%, explicit height in `vh` or `px` (80–160px typical); the SVG's flat edge must sit flush against its section (no 1px gaps — overlap by 1px if needed).
- Subtle beats loud: blurry-gradient at full opacity behind a hero is fine; blobs/scatters over content areas stay under 0.2 opacity.

## Manual export path (when the user wants to drive)

Point him at https://app.haikei.app — pick generator, hit the dice for variations, set the palette hexes, export SVG, drop the file in the project. Then inline it and recolor fills to the CSS variables.
