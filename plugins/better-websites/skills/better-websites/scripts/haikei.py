#!/usr/bin/env python3
"""Haikei-style SVG background generator.

Usage:
  python3 haikei.py <generator> --colors 2f27ce,433bff,dedcff [--width 1440] [--height 420] [--seed 7] [-o out.svg]

Generators: wave, layered-waves, blob, blob-scene, blurry-gradient, circle-scatter
No -o prints the SVG to stdout (for pasting inline). Same seed -> same output.
"""
import argparse
import random
import sys


def smooth_path(pts, closed=False):
    """Catmull-Rom -> cubic bezier path through pts [(x,y), ...]."""
    n = len(pts)
    if n < 3:
        return ""
    def p(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    d = [f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"]
    last = n if closed else n - 1
    for i in range(last):
        p0, p1, p2, p3 = p(i - 1), p(i), p(i + 1), p(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C {c1[0]:.1f} {c1[1]:.1f}, {c2[0]:.1f} {c2[1]:.1f}, {p2[0]:.1f} {p2[1]:.1f}")
    if closed:
        d.append("Z")
    return " ".join(d)


def wave_path(rng, w, h, base_y, amp, segments=5, close_to="bottom"):
    """One horizontal wave line, closed to the top or bottom edge."""
    step = w / segments
    pts = [(-step * 0.2, base_y + rng.uniform(-amp, amp))]
    for i in range(1, segments + 1):
        pts.append((i * step + rng.uniform(-step * 0.2, step * 0.2),
                    base_y + rng.uniform(-amp, amp)))
    pts[-1] = (w + step * 0.2, pts[-1][1])
    d = smooth_path(pts)
    edge = h if close_to == "bottom" else 0
    return f"{d} L {w:.1f} {edge} L 0 {edge} Z"


def blob_path(rng, cx, cy, r, wobble=0.35, points=8):
    import math
    pts = []
    for i in range(points):
        a = (i / points) * 2 * math.pi
        rr = r * (1 - wobble / 2 + rng.random() * wobble)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return smooth_path(pts, closed=True)


def svg_open(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" preserveAspectRatio="none" aria-hidden="true">')


def gen_wave(rng, w, h, colors):
    return [f'<path d="{wave_path(rng, w, h, h * 0.45, h * 0.25)}" fill="#{colors[0]}"/>']


def gen_layered_waves(rng, w, h, colors):
    out = []
    n = len(colors)
    for i, c in enumerate(colors):
        base = h * (0.30 + 0.55 * i / max(1, n - 1))
        amp = h * 0.16 * (1 - i * 0.12)
        out.append(f'<path d="{wave_path(rng, w, h, base, amp)}" fill="#{c}"/>')
    return out


def gen_blob(rng, w, h, colors):
    out = []
    for i, c in enumerate(colors):
        r = min(w, h) * (0.42 - i * 0.09)
        out.append(f'<path d="{blob_path(rng, w / 2, h / 2, r)}" fill="#{c}"/>')
    return out


def gen_blob_scene(rng, w, h, colors):
    out = [f'<rect width="{w}" height="{h}" fill="#{colors[0]}"/>'] if len(colors) > 2 else []
    fills = colors[1:] if len(colors) > 2 else colors
    corners = [(w * 0.9, h * 0.85), (w * 0.1, h * 0.15), (w * 0.85, h * 0.1), (w * 0.15, h * 0.9)]
    for i, c in enumerate(fills):
        cx, cy = corners[i % 4]
        r = min(w, h) * (0.55 - i * 0.1)
        out.append(f'<path d="{blob_path(rng, cx, cy, r, wobble=0.45)}" fill="#{c}" opacity="{0.95 - i * 0.15:.2f}"/>')
    return out


def gen_blurry_gradient(rng, w, h, colors):
    out = [f'<defs><filter id="blur" x="-40%" y="-40%" width="180%" height="180%">'
           f'<feGaussianBlur stdDeviation="{min(w, h) * 0.18:.0f}"/></filter></defs>',
           f'<rect width="{w}" height="{h}" fill="#{colors[0]}"/>']
    for c in colors[1:]:
        cx, cy = rng.uniform(w * 0.15, w * 0.85), rng.uniform(h * 0.15, h * 0.85)
        r = min(w, h) * rng.uniform(0.28, 0.5)
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="#{c}" filter="url(#blur)"/>')
    return out


def gen_circle_scatter(rng, w, h, colors):
    out = []
    for _ in range(26):
        c = rng.choice(colors)
        out.append(f'<circle cx="{rng.uniform(0, w):.0f}" cy="{rng.uniform(0, h):.0f}" '
                   f'r="{rng.uniform(4, min(w, h) * 0.06):.0f}" fill="#{c}" '
                   f'opacity="{rng.uniform(0.25, 0.9):.2f}"/>')
    return out


GENERATORS = {
    "wave": gen_wave,
    "layered-waves": gen_layered_waves,
    "blob": gen_blob,
    "blob-scene": gen_blob_scene,
    "blurry-gradient": gen_blurry_gradient,
    "circle-scatter": gen_circle_scatter,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("generator", choices=sorted(GENERATORS))
    ap.add_argument("--colors", required=True, help="comma-separated hexes without #, backmost first")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=420)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("-o", "--out", help="output file (default: stdout)")
    a = ap.parse_args()

    colors = [c.strip().lstrip("#") for c in a.colors.split(",") if c.strip()]
    rng = random.Random(a.seed)
    body = GENERATORS[a.generator](rng, a.width, a.height, colors)
    svg = "\n".join([svg_open(a.width, a.height), *body, "</svg>"])

    if a.out:
        with open(a.out, "w") as f:
            f.write(svg)
        print(f"wrote {a.out}", file=sys.stderr)
    else:
        print(svg)


if __name__ == "__main__":
    main()
