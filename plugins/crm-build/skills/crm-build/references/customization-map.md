# Customization map — exact anchors in crm-template.html

Everything you change lives in the `<script>` block (plus `<title>` and the favicon
`<link>` in `<head>`). Never touch the CSS — the look is signed off. Search for each
anchor below; they are unique strings.

## 1. `const DEFAULTS = {` — business identity

| Field | Change to |
|---|---|
| `businessName` / `shortName` | Full legal-ish name / header name |
| `stages` | Keep `["Lead","Contacted","Quoted","Booked","Job Done","Paid"]` unless the trade genuinely differs (e.g. design-led trades: add "Survey" or "Design"). 6 stages max — 7 columns don't fit a reel. |
| `wonFromStage` / `paidStage` | Update if stages changed |
| `jobTypes` | 5–6 for the trade, priced services not vague ("Boiler install", not "Heating") |
| `sources` | Keep Word of Mouth / Facebook / Google / Checkatrade (or trade equivalent: MyBuilder, Rated People) / Van Signage / Repeat Customer |
| `storageKey` | `<client>-crm-v1` — REQUIRED change, prevents data collisions between client CRMs |
| `address`, `phone`, `email`, `vatNo` | Plausible for the town. Blank `vatNo` = VAT lines vanish from docs (fine for small trades) |
| `bankDetails`, `quoteValidDays`, `paymentTermsDays` | Plausible |
| `textTemplate`, `emailSubject`, `emailTemplate` | Rewrite in the trade's voice, keep the `{{merge}}` tokens |

Also update `<title>` and the favicon (keep the ink rounded-square; the ridge-peak path
suits most trades — swap the path only if it jars, e.g. a droplet-ish stroke for a
plumber; keep it a simple white 2-stroke line mark).

## 2. `function seedContacts() {` — the board

Keep the exact structure: **14 active** (3 Lead / 3 Contacted / 3 Quoted / 2 Booked /
2 Job Done / 1 Paid) + **8 archived Paid** (settled history) + **3 lost**. Helpers:
`A(dayOffset, type, text)` = activity entry, `T(dayOffset, text, done)` = task,
`dateFromNow(n)` / `tsFromNow(n)` = relative dates — always relative, never hardcoded.

Reality rules (the contract — a sceptic zooms in):
- Values non-round and trade-appropriate (plumber: £95 callout–£3,800 boiler+bathroom
  £6k; landscaper: £400–£25k). Vary magnitudes; exactly one "big one" in the pipeline.
- Follow-ups: 3–4 overdue (−1…−7), one due today (0), rest +1…+9. One note like
  "chase Thursday — no answer x2". Some blank emails (older customers). One landline.
- UK names, no alphabetical runs, one non-Anglo name minimum, addresses clustered in one
  real area (the client's town + neighbouring villages, real road-name style + postcode
  prefix).
- 2–4 seeded tasks on active jobs, ONE of them overdue (feeds the Today screen).
- Archived paid jobs: `paidAt` spread over the past ~5 months, roughly one or two per
  month, uneven totals — this IS the revenue chart. `createdAt` < `wonAt` < `paidAt`,
  gaps 7–20 days (feeds "days to win").
- Lost: realistic reasons ("went with cheaper quote", "gone quiet", "doing it himself").

## 3. Demo-suite datasets (the prop screens)

| Anchor | What to write |
|---|---|
| `const DEMO_THREADS = [` | 5 threads using seed-contact names. Thread 2 MUST be the missed-call + AUTO text-back pair (the reel's wow moment). Mix WhatsApp/SMS/Email/Call. Texts sound like real customers: gate codes, insurance, "still OK for Thursday?" |
| `const EVENTS = [` (in `renderCalendar`) | ~13 offset events: site visits (`ev-visit`), job days incl. a 2-day run (`ev-job`), one invoice-due (`ev-money`), 2 past done (`ev-done`). Trade-specific labels ("Powerflush — Ogden", "Turf delivery") |
| `renderPayments` rows + tiles | 6 rows: the seed's Paid contact + 2 Job Done (one **overdue** — same contact whose note says chase) + 2 archived + 1 draft deposit. Tiles must equal the rows: collected-30-days sum, outstanding = Job Done sum, overdue = the red one |
| `const flows = [` (renderAutomations) | 6 workflow cards, 4 on / 2 off-or-scheduled. Keep missed-call text-back, quote follow-up, review request; make the seasonal one trade-specific (gutter clear = autumn, aircon = spring, lawn treatments = Feb) |
| `renderReviews` list + header | 5 reviews from PAID/archived seed names only. Exactly one 4-star with a specific niggle AND an owner reply. Rating 4.8–4.9, review count 25–60 |
| Bell dropdown (HTML, `id="bellDrop"`) | 3 items referencing the same customers (missed call / new review / overdue invoice) |

## 4. Cross-check table — numbers that must agree

- Donut centre "won all-time" = sum of value over every contact with `wonAt` (active won
  + archived).
- Payments "Collected — last 30 days" = seed contacts with `paidAt` within 30 days.
- Payments "Outstanding" = sum of the two Job Done actives; "Overdue" = the one whose
  note says chase — and she/he appears in the bell dropdown and (ideally) an inbox thread.
- Automation stats plausible vs seed scale (a 25-contact book didn't send 5,000 texts —
  keep low hundreds max).
- Quote/invoice numbering (`db.docs` seed `{quote:146, invoice:118}`) — vary the starting
  numbers per client so screenshots differ.

## 5. What NOT to touch

CSS (any layer), the render functions' logic, drag-and-drop, storage/migration, the
minimal-pass overrides, print styles. If a change request is about look and feel, the
answer lives in the app-UI taste rules in SKILL.md — not in new colours.
