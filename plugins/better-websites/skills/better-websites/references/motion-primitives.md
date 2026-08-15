# Motion-Primitives — catalog + vanilla recipes

Site: https://motion-primitives.com/ · GitHub: ibelick/motion-primitives · MIT
Built on **Motion** (the `motion` package, Framer Motion's successor) + Tailwind CSS. shadcn-style: components are copied into your project, fully editable.

## Install (React/Next.js projects)

```bash
npx motion-primitives@latest add <component-name>
# or via the shadcn registry:
npx shadcn@latest add "https://motion-primitives.com/c/<component-name>.json"
```

Component docs live at `https://motion-primitives.com/docs/<component-name>` — fetch the page for props/usage when installing one you haven't used.

## Component catalog

**Text effects**
| Component | What it does |
|---|---|
| `text-effect` | Per-character/word entrance animations (fade, blur, slide) |
| `text-shimmer` | Gradient shimmer sweeping across text |
| `text-shimmer-wave` | Per-character wave shimmer |
| `text-loop` | Cycles through a list of words ("built for **founders** / **agencies** / **creators**") |
| `text-morph` | Morphs one string into another |
| `text-roll` | Slot-machine style character roll |
| `text-scramble` | Decodes text from random characters |
| `spinning-text` | Text on a circular path, rotating |
| `animated-number` | Animated counting number |
| `sliding-number` | Odometer-style digit slide |

**Layout & interaction**
| Component | What it does |
|---|---|
| `animated-group` | Staggers entrance of children |
| `in-view` | Triggers animation when scrolled into view |
| `infinite-slider` | Seamless marquee (logos, testimonials) |
| `carousel` | Swipeable carousel |
| `transition-panel` | Animated switching between panels/tabs |
| `accordion` / `disclosure` | Animated expand/collapse |
| `dialog` / `morphing-dialog` | Modal that morphs from its trigger card |
| `morphing-popover` | Popover morphing from trigger |
| `dock` | macOS-style magnifying dock |
| `toolbar-dynamic` / `toolbar-expandable` | Animated expanding toolbars |

**Hover & decoration**
| Component | What it does |
|---|---|
| `spotlight` | Radial light that follows the cursor over a card/section |
| `border-trail` | Light dot traveling around an element's border |
| `glow-effect` | Animated glow behind an element |
| `tilt` | 3D tilt following the cursor |
| `magnetic` | Element magnetically pulls toward the cursor |
| `cursor` | Custom animated cursor |
| `animated-background` | Shared highlight that slides between hovered items (tabs, nav) |
| `progressive-blur` | Gradient blur mask (edge fades on sliders) |
| `image-comparison` | Before/after slider |
| `scroll-progress` | Page scroll progress bar |

## Choosing effects (2–4 signature effects per page)

- SaaS/startup hero → `text-effect` entrance + `text-loop` in the headline, `infinite-slider` logo marquee
- Stats/proof section → `animated-number` or `sliding-number`
- Card grids → `spotlight` or `tilt` (pick one, not both)
- Premium/dark aesthetic → `border-trail`, `glow-effect`, `text-shimmer` on the eyebrow
- Nav/tabs → `animated-background`
- Long-scroll content page → `scroll-progress`

## Vanilla recipes (single-file HTML builds)

Recreations of the highest-value components, no dependencies. All respect the palette variables (`--primary`, `--accent`, etc.).

Wrap all scroll/hover motion in:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
```

### 1. Blur-in reveal (= `in-view` + `animated-group`)
```css
.reveal { opacity: 0; transform: translateY(24px); filter: blur(8px);
  transition: opacity .7s ease-out, transform .7s ease-out, filter .7s ease-out; }
.reveal.is-visible { opacity: 1; transform: none; filter: none; }
/* stagger children: */
.reveal.is-visible > * { transition-delay: calc(var(--i, 0) * 90ms); }
```
```js
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
}), { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
```

### 2. Text shimmer (= `text-shimmer`)
```css
.shimmer { background: linear-gradient(110deg, var(--text) 35%, var(--accent) 50%, var(--text) 65%);
  background-size: 250% 100%; -webkit-background-clip: text; background-clip: text;
  color: transparent; animation: shimmer 2.8s linear infinite; }
@keyframes shimmer { to { background-position: -250% 0; } }
```

### 3. Infinite slider / marquee (= `infinite-slider`)
Duplicate the track content once, then:
```css
.marquee { overflow: hidden; mask: linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent); }
.marquee-track { display: flex; gap: 3rem; width: max-content; animation: marquee 28s linear infinite; }
@keyframes marquee { to { transform: translateX(-50%); } }
.marquee:hover .marquee-track { animation-play-state: paused; }
```
(The mask is the vanilla version of `progressive-blur` edges.)

### 4. Spotlight card (= `spotlight`)
```css
.card { position: relative; overflow: hidden; }
.card::before { content: ''; position: absolute; inset: 0; opacity: 0; transition: opacity .4s;
  background: radial-gradient(320px circle at var(--mx) var(--my), color-mix(in srgb, var(--accent) 14%, transparent), transparent 65%); }
.card:hover::before { opacity: 1; }
```
```js
document.querySelectorAll('.card').forEach(c => c.addEventListener('pointermove', e => {
  const r = c.getBoundingClientRect();
  c.style.setProperty('--mx', e.clientX - r.left + 'px');
  c.style.setProperty('--my', e.clientY - r.top + 'px');
}));
```

### 5. Border trail (= `border-trail`)
```css
.trail { position: relative; border-radius: 16px; }
.trail::after { content: ''; position: absolute; inset: -1px; border-radius: inherit; padding: 1px;
  background: conic-gradient(from var(--a, 0deg), transparent 0 340deg, var(--accent) 355deg, transparent 360deg);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude;
  animation: trail 4s linear infinite; }
@property --a { syntax: '<angle>'; initial-value: 0deg; inherits: false; }
@keyframes trail { to { --a: 360deg; } }
```

### 6. Animated counter (= `animated-number`)
```js
function countUp(el) {
  const end = parseFloat(el.dataset.count), dur = 1400, t0 = performance.now();
  (function tick(t) {
    const p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3); // ease-out cubic
    el.textContent = Math.round(end * e).toLocaleString();
    if (p < 1) requestAnimationFrame(tick);
  })(t0);
}
// trigger from the IntersectionObserver in recipe 1
```

### 7. Tilt (= `tilt`)
```js
document.querySelectorAll('.tilt').forEach(el => {
  el.style.transition = 'transform .2s'; el.style.transformStyle = 'preserve-3d';
  el.addEventListener('pointermove', e => {
    const r = el.getBoundingClientRect();
    const rx = ((e.clientY - r.top) / r.height - .5) * -10;
    const ry = ((e.clientX - r.left) / r.width - .5) * 10;
    el.style.transform = `perspective(800px) rotateX(${rx}deg) rotateY(${ry}deg)`;
  });
  el.addEventListener('pointerleave', () => el.style.transform = '');
});
```

### 8. Scroll progress (= `scroll-progress`)
```css
.progress { position: fixed; top: 0; left: 0; height: 3px; background: var(--accent);
  width: 100%; transform-origin: 0 50%; transform: scaleX(0); z-index: 99; }
```
```js
addEventListener('scroll', () => {
  const h = document.documentElement;
  document.querySelector('.progress').style.transform =
    `scaleX(${h.scrollTop / (h.scrollHeight - h.clientHeight)})`;
}, { passive: true });
```

### 9. Magnetic button (= `magnetic`)
```js
document.querySelectorAll('.magnetic').forEach(el => {
  el.style.transition = 'transform .25s cubic-bezier(.2,.8,.2,1)';
  el.addEventListener('pointermove', e => {
    const r = el.getBoundingClientRect();
    el.style.transform = `translate(${(e.clientX - r.left - r.width/2) * .25}px, ${(e.clientY - r.top - r.height/2) * .25}px)`;
  });
  el.addEventListener('pointerleave', () => el.style.transform = '');
});
```

### 10. Text loop (= `text-loop`)
```html
<span class="loop-wrap"><span class="loop-words"><span>founders</span><span>agencies</span><span>creators</span></span></span>
```
```css
.loop-wrap { display: inline-block; height: 1.2em; overflow: hidden; vertical-align: bottom; }
.loop-words { display: flex; flex-direction: column; animation: loop 6s cubic-bezier(.7,0,.3,1) infinite; }
.loop-words span { height: 1.2em; color: var(--accent); }
@keyframes loop { 0%,28% { transform: none; } 33%,61% { transform: translateY(-1.2em); }
  66%,94% { transform: translateY(-2.4em); } 100% { transform: translateY(-3.6em); } }
```
(Repeat the first word as a 4th child so the loop wraps seamlessly.)
