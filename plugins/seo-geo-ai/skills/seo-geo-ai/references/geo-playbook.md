# GEO / AI-Search Playbook

How to make a site get cited by ChatGPT, Perplexity, Claude, Google AI Overviews, and Bing Copilot — not just ranked by Google. Classic SEO gets you crawled; GEO gets you *quoted*.

## Why this differs from SEO

AI engines don't send a user to a results page — they synthesize an answer and cite 2-5 sources. To be a source, a page must contain **extractable, self-contained answer passages**: a paragraph that fully answers one question without needing the rest of the page. Rankings signals still matter (AI engines lean on search indexes for retrieval), but the passage-level answer quality decides who gets quoted.

## The checklist

### 1. llms.txt (site root)
A curated markdown summary for AI crawlers. Format:

```markdown
# Site Name

> One-sentence description of who this is and what they do.

Key facts: location, services, what makes them different — 3-6 bullet lines.

## Pages
- [Page name](https://full-url/): one-line description of what's on it
```

Keep it under ~80 lines. Every fact must be true and on the site already.

### 2. robots.txt must not block AI crawlers
Unless the client explicitly wants otherwise, allow: `GPTBot`, `OAI-SearchBot`, `ClaudeBot`, `Claude-SearchBot`, `PerplexityBot`, `Google-Extended`, `Bingbot`, `CCBot`. Blocking these = invisible to AI search. Simplest correct file:

```
User-agent: *
Allow: /
Sitemap: https://full-url/sitemap.xml
```

### 3. Answer-shaped content
- **Answer first, elaborate second.** Open each section with the direct answer in 1-2 sentences, then detail. AI extraction favors the first sentences after a heading.
- **Question headings.** H2/H3s phrased the way people actually ask: "How much does BMW brake service cost?" beats "Our Services".
- **Self-contained paragraphs.** Each key paragraph should make sense quoted alone — restate the subject noun instead of leaning on "it"/"we" ("Æsir Automotive services all BMW models" not "We service all models").
- **Named entities everywhere.** Business name, city, service names, product names spelled out consistently. Entity clarity is how AI models connect the page to the query.
- **Concrete numbers and specifics.** Prices, years in business, counts, timeframes. Studies on GEO show adding statistics and citations measurably lifts inclusion in AI answers.

### 4. Structured data that matches the page
JSON-LD (in `<script type="application/ld+json">`), types by site kind:
- Local business → `LocalBusiness` (or subtype like `AutoRepair`) with name, address, phone, geo, openingHours, url — **must match the real Google Business Profile details**
- Any site → `Organization` or `Person`, `WebSite`, `BreadcrumbList` on inner pages
- Q&A section → `FAQPage` with the on-page questions/answers, verbatim
- Articles/blog → `Article` with datePublished/dateModified
- NEVER add `AggregateRating`/`Review` markup for reviews that don't visibly exist on the page — that's a penalty risk and a lie.

### 5. FAQ section
An on-page FAQ (5-8 real questions customers ask) + matching FAQPage schema is the single highest-leverage GEO addition to a small site: it creates ready-made Q→A extraction pairs.

### 6. Semantic HTML
`<main>`, `<article>`, `<section>`, `<nav>`, `<header>`, `<footer>`, one `<h1>`, logical heading hierarchy. Extraction models use document structure to find answer boundaries. A div-soup site quotes badly.

### 7. Freshness signals
Visible "Updated <month year>" on key pages + `dateModified` in schema. AI engines weight recency for anything answer-like.

### 8. Discovery beyond Google
- `sitemap.xml` listed in robots.txt
- Bing matters more than people think: Bing's index feeds ChatGPT search and Copilot. If the user controls DNS/hosting, note "submit to Bing Webmaster Tools + consider IndexNow" in the final report as an owner action.

## What NOT to do
- No keyword stuffing, no hidden text, no doorway pages — AI engines inherit spam detection from the underlying indexes.
- Don't fabricate facts, stats, reviews, or credentials to look authoritative. Every claim added must come from the site, the client's real business info, or the user.
- Don't bloat pages with generic filler "SEO text" — it *lowers* extraction quality. Dense, specific, short beats long and vague.
