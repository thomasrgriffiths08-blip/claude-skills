---
name: crm-build
description: Generate a client-ready, single-file CRM (crm.html) for any trade or local business — pipeline kanban with drag-and-drop, contacts, follow-ups, tasks, reports with live count-up, quote/invoice PDFs, CSV import/export, plus demo Inbox/Calendar/Payments/Automations/Reviews screens — in a deliberately minimal flat style, seeded with believable data relative to today. Use this EVERY time the user asks for a CRM in any phrasing — "build a CRM for [business/trade]", "one of those CRMs like the roofing one", "customer tracker for my plumber client", "pipeline tool", "CRM demo for a reel" — even when they don't say "skill" or name a file. Also use when they want an existing crm.html rebranded for a different business.
---

# CRM Build

One proven CRM, re-skinned per business. The template in `assets/crm-template.html` is the
finished Ridgeline Roofing build (2026-08-13): every feature already works, the design is
already the one that survived client review ("simple — I like it"), and the seed-data patterns already
survive a sceptic zooming in. **Never rebuild it from scratch and never restyle it** — a
fresh generation loses hundreds of small verified decisions. Copy it, then change only
content: business identity, pipeline vocabulary, seed data, demo-screen data.

## Why copy-don't-rebuild

The template encodes three hard-won layers you'd otherwise re-litigate every time:
1. **Working features** — kanban drag-and-drop with undo, localStorage persistence +
   migration, follow-ups/tasks/agenda, reports (count-up, funnel, revenue chart, source
   donut), branded quote/invoice PDFs with VAT maths, CSV import/export, JSON backup,
   global search, bulk contact actions, in-app settings.
2. **App-UI taste** (standing rule): flat, monochrome
   + one accent, hairline borders, radius ≤6px, dense 15px base, grey initials avatars, no
   gradients/glows/pills, no entrance animations (count-up stays). He rejects colourful
   app UIs as "vibecoded" — do not add colour back, whatever the client's brand is.
3. **Camera realism** — dates relative to today so the overdue list is always live,
   non-round money, one messy note, a 4-star review with an owner reply.

## Workflow

1. **Gather the business facts** (from the prompt; invent plausible UK details for gaps):
   business name, trade, town/area, 4–8 job types with a realistic £ price range, lead
   sources, pipeline stages if non-standard. Don't ask questions for the rest — pick
   believable defaults, they're one Settings-screen edit away.

2. **Create the output folder and copy the template.** Default location
   `~/Desktop/builds/<KEYWORD>/` (e.g. `builds/CRM-FLOWFIX/`) unless the prompt says
   otherwise. Copy `assets/crm-template.html` → `crm.html`.

3. **Customize content only** — follow `references/customization-map.md` for the exact
   anchors. In order: `DEFAULTS` config block → `seedContacts()` → the five demo datasets
   (inbox threads, calendar events, invoices, automation flows, reviews) → notification
   bell items → title/favicon. Change the `storageKey` (e.g. `flowfix-crm-v1`) so two
   client CRMs in the same browser never share data.

4. **Keep the numbers honest.** The reports cross-check against the seed: donut centre =
   sum of all won values; "collected last 30 days" tile = invoices with paidAt in that
   window; the overdue invoice in Payments should be a real Job-Done contact. The
   customization map lists every figure that must stay consistent. A sceptic pausing the
   reel WILL check.

5. **Verify in the browser** (localhost, not file:// — the preview pane renders file:// as
   a static snapshot with no localStorage). Walk it like the reality contract demands: every
   tab renders, drag a card, refresh (data survives), open a drawer, generate a quote,
   zero console errors. Then clear localStorage so the first real open reseeds fresh.

6. **Write BUILD-NOTES.md** next to it: what's real vs prop (see below), the reset-before-
   filming tip, and the 6-beat Instagram cut adapted to this trade (hook on the board →
   Today pain → Inbox auto text-back wow → speed round → count-up payoff → keyword CTA).

## Real vs prop — say it plainly

Pipeline, Today, Contacts, Reports, Settings, quotes/invoices, CSV, search and bulk
actions are fully functional. Inbox, Calendar, Payments, Automations and Reviews are
**camera props** — polished demo screens with believable content, clickable enough to film
(threads switch, replies append, toggles flip) but not wired to the contact database.
BUILD-NOTES must say so, and any DM asset built from this must not claim the prop screens
work — the honest line is "the working inbox and automations are the next build up."

## Relationship to other skills

- **film-build** owns the recording workflow (stages/, teleprompter beats) when the user is
  filming the build itself. When both apply, film-build runs the show and this skill is
  how the app gets made.
- **better-websites** does NOT apply here — its pipeline is for marketing pages. The
  template already embodies the product-UI rules; adding its colour/motion/backgrounds to
  a CRM is the exact failure that reads as "super vibecoded".
