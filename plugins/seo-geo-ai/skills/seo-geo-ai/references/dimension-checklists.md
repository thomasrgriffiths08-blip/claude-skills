# Audit Dimension Checklists

Each audit agent gets ONE dimension. Report only real, fixable findings with exact file + exact fix. No style rewrites, no redesigns — the site's look is off-limits.

Your prompt includes the SITE PROFILE. It is your training: judge pages against their assigned target queries from the profile's table, use only its Facts bank for claims, respect its Voice and "Do not touch" sections. Where the profile and this checklist disagree, the profile wins.

## D1 — technical
Per page: `<title>` (30-60 chars, unique per page, brand + primary term), meta description (70-160, written to earn the click), canonical link, `lang` on `<html>`, viewport meta, favicon, charset. Open Graph: og:title, og:description, og:image (must point at a file that exists), og:url, og:type + twitter:card (summary_large_image if there's a hero image). Site root: robots.txt (crawlable, sitemap line, AI bots not blocked), sitemap.xml (every real page, valid XML). Broken internal links/assets (check href/src targets exist). No `noindex` left in by accident.

## D2 — structured-data
Every JSON-LD block parses, has @context/@type, and describes what's actually on the page. Right type for the site (LocalBusiness subtype / Organization / Person + WebSite; FAQPage where an FAQ exists; Article for posts; BreadcrumbList on inner pages). NAP (name/address/phone) consistent across all pages and matching the client's real details. Flag any Review/AggregateRating markup that lacks visible on-page reviews — that markup must be removed or the reviews shown. Missing schema entirely = one finding per page type, not per page.

## D3 — content
Exactly one H1 per page, containing what the page IS (service + place for local businesses). Heading hierarchy logical, headings descriptive not decorative ("BMW Servicing in Manchester" not "What We Do"). **Query targeting**: each page's primary query from the profile's Target queries table must be naturally represented in its title, H1, and first paragraph — same spelling, no stuffing; secondary queries covered somewhere sensible on the page. A page whose title/H1 targets nothing from its assigned queries is a finding. Internal links between pages with descriptive anchor text (not "click here"). Every `<img>` has specific alt text (what's IN the image; empty alt="" only for pure decoration). Thin pages (<~120 words of real content) flagged with what's missing. No keyword stuffing introduced — if existing copy already reads natural, do not pad it.

## D4 — geo-ai
Read `references/geo-playbook.md` first — it is the spec for this dimension. **Every AI-search question in the profile's Target queries table must have an answer-shaped section or FAQ entry somewhere on the site** — a missing one is a finding (answer content comes from the Facts bank only). Also check: llms.txt exists, accurate, well-formed. robots.txt allows AI crawlers. FAQ section exists with real questions + matching FAQPage schema. Answer-first paragraphs under question-shaped headings. Self-contained quotable passages (no orphan "it/we" openers on key paragraphs). Entities spelled out. Concrete numbers where the business has them. Freshness signal on key pages. Semantic HTML5 landmarks.

## D5 — performance
Only what's checkable statically and fixable safely: images missing width/height (layout shift), oversized images (>500KB) that should be compressed/resized — flag, don't recompress binaries without noting it; missing `loading="lazy"` on below-fold images (never on the LCP/hero image); render-blocking external scripts that could take `defer`; fonts without `font-display: swap`; missing `rel="preconnect"` for third-party origins actually used; enormous inline base64 blobs. Do NOT suggest build tooling, bundlers, or framework migrations.
