#!/usr/bin/env python3
"""Deterministic SEO/GEO checker. Stdlib only.

Usage:
  python3 seo_check.py /path/to/site-dir [--json]
  python3 seo_check.py --url https://example.com [--json]

Directory mode scans every .html file (skipping node_modules/.git/backups)
and also checks for robots.txt, sitemap.xml, and llms.txt at the root.
URL mode fetches one page and runs the per-page checks on it.

Exit code 0 = no errors (warnings allowed), 1 = errors found.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "backup", "backups", "__pycache__"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.metas = []          # list of attr dicts
        self.links = []          # list of attr dicts
        self.headings = []       # [(level, text-so-far)] — text not tracked, level only
        self.h1_count = 0
        self.imgs_missing_alt = 0
        self.img_count = 0
        self.jsonld_blocks = []
        self._in_jsonld = False
        self._jsonld_buf = []
        self.html_lang = None
        self.saw_html_tag = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.saw_html_tag = True
            self.html_lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
            if self.title is None:
                self.title = ""
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            self.headings.append(level)
            if level == 1:
                self.h1_count += 1
        elif tag == "img":
            self.img_count += 1
            alt = a.get("alt")
            if alt is None or not alt.strip():
                self.imgs_missing_alt += 1
        elif tag == "script" and a.get("type", "").strip().lower() == "application/ld+json":
            self._in_jsonld = True
            self._jsonld_buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            self.jsonld_blocks.append("".join(self._jsonld_buf))

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data
        if self._in_jsonld:
            self._jsonld_buf.append(data)

    def meta_content(self, **match):
        """First meta content= where all match attrs equal (name/property, case-insensitive)."""
        for m in self.metas:
            ok = True
            for k, v in match.items():
                if (m.get(k) or "").strip().lower() != v:
                    ok = False
                    break
            if ok:
                return m.get("content")
        return None


def check_page(html, label, findings):
    """Run per-page checks; append (severity, label, message) tuples to findings.

    Returns a dict of this page's identity tags so the caller can run cross-page
    checks (duplicate titles/descriptions across pages tank rankings, and no
    single-page check can ever catch that).
    """
    p = PageParser()
    try:
        p.feed(html)
    except Exception as e:  # malformed enough to break the parser is itself a finding
        findings.append(("error", label, f"HTML failed to parse: {e}"))
        return None

    err = lambda msg: findings.append(("error", label, msg))
    warn = lambda msg: findings.append(("warning", label, msg))

    # Fragments (partials/templates) without an <html> tag: only run universal checks
    full_page = p.saw_html_tag

    title = (p.title or "").strip()
    if full_page:
        if not title:
            err("missing <title>")
        elif len(title) > 60:
            warn(f"<title> is {len(title)} chars (aim 30-60): {title[:70]!r}")
        elif len(title) < 15:
            warn(f"<title> is only {len(title)} chars (aim 30-60): {title!r}")

        desc = p.meta_content(name="description")
        if not desc or not desc.strip():
            err("missing meta description")
        else:
            d = desc.strip()
            if len(d) > 165:
                warn(f"meta description is {len(d)} chars (aim 70-160)")
            elif len(d) < 50:
                warn(f"meta description is only {len(d)} chars (aim 70-160)")

        if not p.html_lang:
            err("missing lang attribute on <html>")

        if not p.meta_content(name="viewport"):
            err("missing viewport meta")

        canonical = [l for l in p.links if (l.get("rel") or "").strip().lower() == "canonical"]
        if not canonical:
            warn("missing canonical link")

        icons = [l for l in p.links if "icon" in (l.get("rel") or "").lower()]
        if not icons:
            warn("no favicon link")

        for prop, sev in [("og:title", "error"), ("og:description", "error"),
                          ("og:image", "error"), ("og:url", "warning")]:
            if not p.meta_content(property=prop):
                findings.append((sev, label, f"missing {prop}"))
        if not p.meta_content(name="twitter:card") and not p.meta_content(property="twitter:card"):
            warn("missing twitter:card")

        if p.h1_count == 0:
            err("no <h1> on page")
        elif p.h1_count > 1:
            warn(f"{p.h1_count} <h1> tags (should be exactly 1)")

        prev = 0
        for level in p.headings:
            if prev and level > prev + 1:
                warn(f"heading level skips from h{prev} to h{level}")
                break
            prev = level

        if not p.jsonld_blocks:
            warn("no JSON-LD structured data on page")

    if p.imgs_missing_alt:
        err(f"{p.imgs_missing_alt}/{p.img_count} <img> tags missing alt text")

    for i, block in enumerate(p.jsonld_blocks):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            err(f"JSON-LD block {i + 1} is invalid JSON: {e}")
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict):
                continue
            if "@context" not in item:
                warn(f"JSON-LD block {i + 1} missing @context")
            if "@type" not in item and "@graph" not in item:
                warn(f"JSON-LD block {i + 1} missing @type")
            blob = json.dumps(item)
            if "AggregateRating" in blob or '"Review"' in blob:
                warn(f"JSON-LD block {i + 1} contains ratings/reviews — "
                     "verify these are REAL and shown on-page (fake ones risk penalties)")

    if not full_page:
        return None
    canon = next((l.get("href") for l in p.links
                  if (l.get("rel") or "").strip().lower() == "canonical"), None)
    desc = p.meta_content(name="description")
    return {
        "label": label,
        "title": title,
        "description": (desc or "").strip(),
        "canonical": (canon or "").strip(),
    }


def check_cross_page(summaries, findings):
    """Duplicate titles/descriptions/canonicals across pages — invisible to per-page checks."""
    def group(field):
        buckets = {}
        for s in summaries:
            v = s.get(field)
            if v:
                buckets.setdefault(v, []).append(s["label"])
        return {v: labels for v, labels in buckets.items() if len(labels) > 1}

    for value, labels in group("title").items():
        findings.append(("error", ", ".join(sorted(labels)),
                         f"duplicate <title> across {len(labels)} pages: {value[:60]!r} — "
                         "each page needs a unique title"))
    for value, labels in group("description").items():
        findings.append(("error", ", ".join(sorted(labels)),
                         f"duplicate meta description across {len(labels)} pages — "
                         "each page needs its own"))
    for value, labels in group("canonical").items():
        findings.append(("error", ", ".join(sorted(labels)),
                         f"{len(labels)} pages share canonical {value!r} — "
                         "all but one will be dropped from the index"))


def run_dir(root: Path, findings):
    pages = 0
    summaries = []
    for f in sorted(root.rglob("*.html")):
        if any(part in SKIP_DIRS for part in f.parts):
            continue
        pages += 1
        label = str(f.relative_to(root))
        s = check_page(f.read_text(encoding="utf-8", errors="replace"), label, findings)
        if s:
            summaries.append(s)
    check_cross_page(summaries, findings)

    if pages == 0:
        findings.append(("error", ".", "no .html files found — wrong directory, "
                         "or a framework site (point me at the build output or use --url)"))

    for name, sev, why in [
        ("robots.txt", "warning", "search + AI crawlers have no crawl guidance"),
        ("sitemap.xml", "warning", "crawlers have no page inventory"),
        ("llms.txt", "warning", "AI search engines get no curated site summary"),
    ]:
        if not (root / name).exists():
            findings.append((sev, ".", f"missing {name} — {why}"))
    return pages


def run_url(url: str, findings):
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (seo-check)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="replace")
    check_page(html, url, findings)
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="site directory to scan")
    ap.add_argument("--url", help="check a single live URL instead of a directory")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    findings = []
    if args.url:
        pages = run_url(args.url, findings)
    elif args.target:
        root = Path(args.target).resolve()
        if not root.is_dir():
            print(f"not a directory: {root}", file=sys.stderr)
            sys.exit(2)
        pages = run_dir(root, findings)
    else:
        ap.error("provide a directory or --url")

    errors = [f for f in findings if f[0] == "error"]
    warnings = [f for f in findings if f[0] == "warning"]

    if args.json:
        print(json.dumps({
            "pages_checked": pages,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "errors": [{"where": w, "message": m} for _, w, m in errors],
            "warnings": [{"where": w, "message": m} for _, w, m in warnings],
        }, indent=2))
    else:
        print(f"checked {pages} page(s): {len(errors)} errors, {len(warnings)} warnings\n")
        for sev, where, msg in errors + warnings:
            print(f"  [{sev.upper():7}] {where}: {msg}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
