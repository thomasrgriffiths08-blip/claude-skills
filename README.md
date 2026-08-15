# Claude Code skills for building client work

Three skills I use daily to build websites, CRMs, and search visibility for real clients. Not demos — this is the working stack, with the opinions left in.

## Install

```bash
/plugin marketplace add thomasrgriffiths08-blip/claude-skills
```

Then install whichever you want:

```bash
/plugin install better-websites@tom-claude-skills
```

```bash
/plugin install crm-build@tom-claude-skills
```

```bash
/plugin install seo-geo-ai@tom-claude-skills
```

They trigger on their own once installed — you don't have to name them. Ask for a landing page and `better-websites` engages; ask for a pipeline tool and `crm-build` does.

---

## `better-websites`

The problem it solves: ask any AI for a website and you get the same page. Centered hero, eyebrow text, two buttons, three equal cards, a stats row, testimonials, a form. Polished and completely forgettable.

This routes every build through six resources, each killing one specific failure mode:

| Failure mode | Fixed by |
|---|---|
| Generic layout invented from nothing | Real design systems, borrowed for structure and typography |
| Static, lifeless page | A motion *direction* chosen before any code |
| Vague vibes, no art direction | Reference hunting for texture and detail |
| Random hex colors sprinkled ad hoc | A 5-role palette on the 60-30-10 rule |
| Flat solid-color sections | Generated SVG waves, blobs, and gradients |
| No animation, or janky animation | Proven motion recipes, 2–4 per page maximum |

The rule that does the heavy lifting is the **template test**: swap the logo and copy in your head. If the layout could belong to any other business, it gets rebuilt before you ever see it.

It also knows when *not* to apply itself. Hero-page treatment on a dashboard is exactly how a build ends up looking, in the skill's own words, "super vibecoded" — so product UIs get a separate, deliberately boring set of rules: flat, monochrome, dense, still.

Ships with a Python generator for the SVG backgrounds, so there's no GUI step:

```bash
python3 scripts/haikei.py layered-waves --colors 2f27ce,433bff,dedcff --seed 7
```

## `crm-build`

One prompt produces a single-file `crm.html` for any trade or local business — roofer, plumber, electrician, landscaper.

Drag-and-drop pipeline kanban, contacts, follow-ups, tasks, reports with live count-up, quote and invoice PDFs, CSV import/export, plus demo Inbox, Calendar, Payments, Automations, and Reviews screens.

The part that matters is the seed data. Every date is relative to the day you generate it, so the pipeline always looks *alive* — jobs quoted last Tuesday, an invoice paid three weeks ago, two deals gone cold. It ships with lost deals in it, because every real pipeline has them and a demo without them reads as fake to anyone who's run a business.

Demo contacts use Ofcom drama-reserved phone ranges. Nothing in here dials a real person.

## `seo-geo-ai`

Covers three things that are usually sold separately:

- **SEO** — the classic layer: titles, meta, headings, internal links, sitemaps, Core Web Vitals
- **GEO** — generative engine optimization, so AI systems can parse and cite the site
- **AI search** — showing up in ChatGPT, Perplexity, and Google AI Overviews

It trains itself on the specific site first, writing a profile it keeps and reuses. Then it audits across five dimensions in parallel, fixes what it finds, verifies with a deterministic checker, and loops until a full sweep comes back with nothing new.

Two design decisions worth knowing about. A round only counts as clean when the auditors find nothing *and* the checker passes — auditors agreeing with each other isn't the same as a good site. And any fix that needs a fact nobody has (a real opening time, a genuine review) is never quietly marked done; it lands in a `blocked` list and comes back as an owner action. A fix silently dropped is how a site ships broken while reporting clean.

---

## Requirements

Claude Code. `seo-geo-ai` uses multi-agent workflows, which need `"enableWorkflows": true` in your `settings.json`.

## License

MIT — use them, fork them, rip bits out.
