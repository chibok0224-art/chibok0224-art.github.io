#!/usr/bin/env python3
"""Build the static site from content/ into dist/.

    python build.py            preview build: draft gigs are shown (dashed, with a DRAFT banner)
    python build.py --release  public build: only live gigs; stops if a live gig has errors

All gigs live in content/gigs.csv (one row per gig, UTF-8). Editorial text per
category lives in content/categories/<slug>/category.json + guide.html.
"""
import csv
import datetime as dt
import html
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
DIST = ROOT / "dist"
STALE_DAYS = 120  # warn when a gig's rating/price was last checked longer ago than this

esc = html.escape


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_categories():
    cats = []
    for meta in sorted((CONTENT / "categories").glob("*/category.json")):
        cat = load(meta)
        cat["guide_html"] = (meta.parent / "guide.html").read_text(encoding="utf-8")
        cats.append(cat)
    return sorted(cats, key=lambda c: c.get("order", 99))


def _num(value, kind):
    value = (value or "").strip().replace(",", "").lstrip("$")
    return kind(value) if value else None


def load_gigs():
    """Read gigs.csv. utf-8-sig so the file also opens cleanly when saved by Excel as 'CSV UTF-8'."""
    gigs, errors = [], []
    with open(CONTENT / "gigs.csv", encoding="utf-8-sig", newline="") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            row = {k: (v or "").strip() for k, v in row.items() if k}
            if not any(row.values()):
                continue
            try:
                row["rank"] = _num(row.get("rank"), int) or 999
                row["rating"] = _num(row.get("rating"), float)
                row["reviews"] = _num(row.get("reviews"), int)
                row["starting_price"] = _num(row.get("starting_price"), float)
            except ValueError as e:
                errors.append(f"gigs.csv line {line_no}: bad number ({e})")
                continue
            row["status"] = row.get("status", "").lower() or "draft"
            row["line"] = line_no
            gigs.append(row)
    return gigs, errors


def check_gigs(gigs, cats):
    """Errors block a release build; warnings are only printed."""
    errors, warnings = [], []
    slugs = {c["slug"] for c in cats}
    for gid, n in Counter(g["id"] for g in gigs).items():
        if n > 1:
            errors.append(f"duplicate id '{gid}' ({n} rows)")
    today = dt.date.today()
    for g in gigs:
        where = f"line {g['line']} ({g['id'] or 'no id'})"
        if g["status"] not in ("live", "draft"):
            errors.append(f"{where}: status must be 'live' or 'draft'")
        if g["category"] not in slugs:
            errors.append(f"{where}: unknown category '{g['category']}'")
        if g["status"] != "live":
            continue
        for field in ("id", "name", "best_for", "why", "affiliate_url", "checked"):
            if not g.get(field):
                errors.append(f"{where}: missing '{field}'")
        if g["affiliate_url"] and "fiverr" not in g["affiliate_url"].lower():
            errors.append(f"{where}: affiliate_url does not look like a Fiverr link")
        if g["rating"] is not None and not 0 <= g["rating"] <= 5:
            errors.append(f"{where}: rating must be 0-5")
        if g["checked"]:
            try:
                age = (today - dt.date.fromisoformat(g["checked"])).days
                if age > STALE_DAYS:
                    warnings.append(f"{where}: last checked {age} days ago, re-check rating and price")
            except ValueError:
                errors.append(f"{where}: checked must be YYYY-MM-DD")
    return errors, warnings


# ---------- layout ----------

def page(site, cats, *, title, description, path, body, schema=None, draft=False):
    url = site["base_url"].rstrip("/") + path
    nav = "".join(f'<a href="/{c["slug"]}/">{esc(c["nav_title"])}</a>' for c in cats[:4])
    banner = ('<div class="draft">PREVIEW: draft gigs are shown. The public build hides them.</div>'
              if draft else "")
    ld = (f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'
          if schema else "")
    contact = (f' · <a href="mailto:{esc(site["contact_email"])}">Contact</a>'
               if site.get("contact_email") else "")
    return f"""<!doctype html>
<html lang="{site['language']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{esc(site['name'])}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
{ld}
</head>
<body>
{banner}
<header class="site-header">
  <div class="wrap bar">
    <a class="logo" href="/"><img src="/favicon.svg" alt="" width="24" height="24">{esc(site['name'])}</a>
    <nav>{nav}<a href="/how-we-pick/">How we pick</a></nav>
  </div>
</header>
<main class="wrap">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>{esc(site['name'])} is reader-supported. When you hire through links on this site we may earn a commission from Fiverr, at no extra cost to you. Sellers cannot pay to be listed.</p>
    <p>{esc(site['name'])} is independent and not affiliated with or endorsed by Fiverr.</p>
    <p><a href="/disclosure/">Affiliate disclosure</a> · <a href="/privacy/">Privacy</a> · <a href="/how-we-pick/">How we pick</a>{contact}</p>
  </div>
</footer>
</body>
</html>
"""


def disclosure_note():
    return ('<p class="disclosure-note">We may earn a commission if you hire through links on this page, '
            'at no extra cost to you. <a href="/how-we-pick/">How we choose picks</a>.</p>')


# ---------- gig rendering ----------

def stats_line(g):
    parts = []
    if g["rating"] is not None and g["reviews"] is not None:
        parts.append(f'<span class="stars">★ {g["rating"]:.1f}</span> ({g["reviews"]:,} reviews)')
    if g.get("level"):
        parts.append(esc(g["level"]))
    if g["starting_price"] is not None:
        parts.append(f'From ${g["starting_price"]:,.0f}')
    return " · ".join(parts)


def cta(g, label):
    if not g.get("affiliate_url"):
        return '<span class="btn btn-off">Affiliate link missing</span>'
    return (f'<a class="btn" href="{esc(g["affiliate_url"])}" rel="sponsored nofollow noopener" '
            f'target="_blank">{label}</a>')


def gig_card(g, i):
    stats = stats_line(g) or "Rating, level and price go here"
    gig = f'<p class="gig-title">“{esc(g["gig_title"])}”</p>' if g.get("gig_title") else ""
    watch = f'<p class="watch"><strong>Keep in mind:</strong> {esc(g["watch_out"])}</p>' if g.get("watch_out") else ""
    checked = (f'<p class="checked">Checked on Fiverr on {esc(g["checked"])}. Ratings and prices change, '
               'so confirm on the gig page.</p>' if g.get("checked") else "")
    cls = "pick" + (" placeholder" if g["status"] != "live" else "")
    return f"""<article class="{cls}" id="{esc(g['id'])}">
  <div class="pick-head">
    <span class="rank">#{i}</span>
    <div>
      <p class="best-for">{esc(g.get("best_for", ""))}</p>
      <h3>{esc(g["name"])}</h3>
      {gig}
      <p class="stats">{stats}</p>
    </div>
  </div>
  <p>{esc(g.get("why", ""))}</p>
  {watch}
  {checked}
  {cta(g, f'See {esc(g["name"])} on Fiverr →')}
</article>"""


def gig_row(g):
    """Compact entry for the long list below the featured cards. data-* attrs drive filter/sort."""
    cls = "row" + (" placeholder" if g["status"] != "live" else "")
    search = " ".join(g.get(k, "") for k in ("name", "best_for", "gig_title", "level")).lower()
    return f"""<li class="{cls}" id="{esc(g['id'])}" data-search="{esc(search)}" data-rank="{g['rank']}"
    data-rating="{g['rating'] or 0}" data-reviews="{g['reviews'] or 0}" data-price="{g['starting_price'] or 0}">
  <div class="row-main">
    <h3>{esc(g["name"])}</h3>
    <p class="best-for">{esc(g.get("best_for", ""))}</p>
    <p class="stats">{stats_line(g)}</p>
    <p class="row-why">{esc(g.get("why", ""))}</p>
  </div>
  {cta(g, "View gig →")}
</li>"""


LIST_SCRIPT = """<script>
(() => {
  const list = document.getElementById('more-list');
  const q = document.getElementById('more-q');
  const sort = document.getElementById('more-sort');
  const count = document.getElementById('more-count');
  const rows = [...list.children];
  function apply() {
    const term = q.value.trim().toLowerCase();
    const key = sort.value;
    const dir = key === 'price' || key === 'rank' ? 1 : -1;
    rows.sort((a, b) => dir * (a.dataset[key] - b.dataset[key]));
    let shown = 0;
    for (const r of rows) {
      const hit = !term || r.dataset.search.includes(term);
      r.hidden = !hit;
      if (hit) shown++;
      list.appendChild(r);
    }
    count.textContent = shown + ' of ' + rows.length;
  }
  q.addEventListener('input', apply);
  sort.addEventListener('change', apply);
  apply();
})();
</script>"""


def category_page(site, cats, cat, gigs, draft):
    n = cat.get("featured_count", 5)
    featured, more = gigs[:n], gigs[n:]
    url = f'{site["base_url"].rstrip("/")}/{cat["slug"]}/'

    if featured:
        toc = "".join(f'<li><a href="#{esc(g["id"])}">{esc(g.get("best_for") or g["name"])}</a></li>'
                      for g in featured)
        more_link = f'<li><a href="#more">{len(more)} more options</a></li>' if more else ""
        picks_html = (f'<nav class="toc"><p>Our top picks</p><ol>{toc}{more_link}</ol></nav>'
                      f'<section class="picks">{"".join(gig_card(g, i) for i, g in enumerate(featured, 1))}</section>')
    else:
        picks_html = ('<p class="empty">We are finalizing our shortlist for this category. '
                      'Until then, the guide below walks you through how we evaluate sellers.</p>')

    more_html = ""
    if more:
        tools = ""
        script = ""
        if len(more) > 6:
            tools = """<div class="list-tools">
  <input id="more-q" type="search" placeholder="Filter by name or specialty" aria-label="Filter">
  <select id="more-sort" aria-label="Sort">
    <option value="rank">Our ranking</option>
    <option value="rating">Highest rated</option>
    <option value="reviews">Most reviews</option>
    <option value="price">Lowest starting price</option>
  </select>
  <span id="more-count" class="muted"></span>
</div>"""
            script = LIST_SCRIPT
        more_html = (f'<section class="more"><h2 id="more">More {esc(cat["card_title"])} worth a look</h2>'
                     f'{tools}<ul id="more-list" class="rows">{"".join(gig_row(g) for g in more)}</ul>{script}</section>')

    faq_html = "".join(f'<details><summary>{esc(f["q"])}</summary><p>{esc(f["a"])}</p></details>'
                       for f in cat["faq"])
    graph = [
        {"@type": "Article", "headline": cat["title"], "description": cat["description"],
         "dateModified": cat["updated"], "mainEntityOfPage": url,
         "author": {"@type": "Organization", "name": site["name"]},
         "publisher": {"@type": "Organization", "name": site["name"]}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in cat["faq"]]},
    ]
    live = [g for g in gigs if g["status"] == "live"]
    if live:
        graph.append({"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": g["name"], "url": f'{url}#{g["id"]}'}
            for i, g in enumerate(live, 1)]})

    body = f"""<article class="article">
<p class="crumbs"><a href="/">Home</a> › {esc(cat.get("group", ""))} › {esc(cat["nav_title"])}</p>
<h1>{esc(cat["h1"])}</h1>
<p class="updated">Updated {esc(cat["updated"])}</p>
{disclosure_note()}
<p class="lead">{esc(cat["intro"])}</p>
{picks_html}
{more_html}
<section class="guide">
{cat["guide_html"]}
</section>
<section class="faq">
<h2 id="faq">FAQ</h2>
{faq_html}
</section>
</article>"""
    return page(site, cats, title=cat["title"], description=cat["description"],
                path=f'/{cat["slug"]}/', body=body,
                schema={"@context": "https://schema.org", "@graph": graph}, draft=draft)


def home_page(site, cats, gigs_by_cat, draft):
    groups = {}
    for c in cats:
        groups.setdefault(c.get("group", "Other"), []).append(c)
    sections = ""
    for group, members in groups.items():
        cards = ""
        for c in members:
            n = len(gigs_by_cat.get(c["slug"], []))
            label = f"See {n} picks →" if n else "Read the hiring guide →"
            cards += (f'<a class="card" href="/{c["slug"]}/"><h3>{esc(c["card_title"])}</h3>'
                      f'<p>{esc(c["card_blurb"])}</p><span>{label}</span></a>')
        sections += f'<h2>{esc(group)}</h2><div class="cards">{cards}</div>'
    schema = {"@context": "https://schema.org", "@type": "WebSite", "name": site["name"],
              "url": site["base_url"].rstrip("/") + "/", "description": site["description"]}
    body = f"""<section class="hero">
<h1>{esc(site["tagline"])}</h1>
<p>Fiverr has thousands of marketing freelancers. We shortlist the ones with a long, public track record, and explain what to check before you hire, so you can order with confidence.</p>
</section>
<section>
{sections}
<p class="muted">More categories are on the way.</p>
</section>
<section class="method">
<h2>How we pick</h2>
<ul>
  <li><strong>Track record first.</strong> Typically 100+ reviews with a 4.8+ average, or Fiverr Pro verification.</li>
  <li><strong>Portfolio reviewed by hand.</strong> We look at the actual work, not just the star rating.</li>
  <li><strong>Clear packages.</strong> Deliverables, revisions and usage rights must be spelled out.</li>
  <li><strong>Dated and re-checked.</strong> Every pick shows when we last checked it.</li>
</ul>
<p><a href="/how-we-pick/">Read our full method →</a></p>
</section>"""
    return page(site, cats, title=f'{site["name"]}: {site["tagline"]}',
                description=site["description"], path="/", body=body, schema=schema, draft=draft)


def text_page(site, cats, *, slug, title, description, body_html, draft):
    body = f'<article class="article prose"><h1>{esc(title)}</h1>{body_html}</article>'
    return page(site, cats, title=f'{title} | {site["name"]}', description=description,
                path=f"/{slug}/", body=body, draft=draft)


HOW_WE_PICK = """
<p>Every freelancer on this site is chosen by us. Sellers cannot pay to be listed or to move up a list.</p>
<h2>Our criteria</h2>
<ul>
  <li><strong>Public track record.</strong> As a rule, at least 100 reviews with an average of 4.8 or higher, or Fiverr Pro verification. We read recent reviews, not only the average.</li>
  <li><strong>Portfolio quality.</strong> We review the seller's sample work ourselves and judge whether it fits the use case we list them for.</li>
  <li><strong>Clear scope.</strong> The gig must state what is delivered, how many revisions are included, and, where relevant, what usage rights you get.</li>
  <li><strong>Recent activity.</strong> Sellers should be actively delivering orders.</li>
</ul>
<h2>What we do not claim</h2>
<p>Unless a pick says otherwise, we have not personally ordered from that seller. Our picks are based on their public track record and our review of their portfolio. Ratings, prices and availability change, so each pick shows the date we last checked it. Always confirm the details on the gig page before ordering.</p>
<h2>How we make money</h2>
<p>We are members of the Fiverr affiliate program. If you hire through our links, Fiverr may pay us a commission. You pay the same price. This never decides who we list.</p>
"""

DISCLOSURE = """
<p>This site contains affiliate links. If you click a link to Fiverr and then make a purchase, we may receive a commission from Fiverr. This costs you nothing extra.</p>
<p>Affiliate links are the buttons that take you to a gig on Fiverr. Commissions help us keep the site running, but they do not affect which freelancers we recommend. Sellers cannot pay for placement.</p>
<p>This site is independent and is not affiliated with, sponsored by, or endorsed by Fiverr. “Fiverr” is a trademark of its owner and is used here only to describe the services we link to.</p>
"""

PRIVACY = """
<p>This site does not use cookies, does not run analytics, and does not ask you for personal information.</p>
<p>When you click a link to Fiverr, you leave this site. Fiverr may then set its own cookies, including cookies that record that you came from our link so that a commission can be credited. That is governed by Fiverr's own privacy policy.</p>
<p>Our hosting provider may keep standard server logs (such as IP address and pages requested) for security and reliability.</p>
<p>If we add analytics or any form in the future, we will update this page first.</p>
"""

NOT_FOUND = """<section class="hero"><h1>Page not found</h1>
<p>That page does not exist. <a href="/">Go to the home page</a>.</p></section>"""


def sitemap(site, cats):
    base = site["base_url"].rstrip("/")
    entries = [("/", site["updated"])] + [(f'/{c["slug"]}/', c["updated"]) for c in cats]
    entries += [(f"/{s}/", site["updated"]) for s in ("how-we-pick", "disclosure", "privacy")]
    urls = "".join(f"<url><loc>{base}{p}</loc><lastmod>{d}</lastmod></url>" for p, d in entries)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')


def clean_dist():
    """Empty dist/ file by file. Removing the folders themselves can fail on Windows while
    Google Drive sync or the preview server holds a handle, so leftover empty folders are fine."""
    if not DIST.exists():
        return
    for p in sorted(DIST.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        try:
            p.unlink() if p.is_file() else p.rmdir()
        except OSError:
            if p.is_file():
                raise


def write(rel, text):
    out = DIST / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


def main():
    release = "--release" in sys.argv
    site = load(CONTENT / "site.json")
    cats = load_categories()
    gigs, errors = load_gigs()
    check_errors, warnings = check_gigs(gigs, cats)
    errors += check_errors

    for w in warnings:
        print("  warning:", w)
    if errors:
        print("Fix these in content/gigs.csv:")
        for e in errors:
            print("  -", e)
        if release:
            sys.exit(1)

    shown = [g for g in gigs if g["status"] == "live" or not release]
    draft = any(g["status"] != "live" for g in shown)
    gigs_by_cat = {}
    for g in sorted(shown, key=lambda g: (g["rank"], g["name"].lower())):
        gigs_by_cat.setdefault(g["category"], []).append(g)

    clean_dist()
    shutil.copytree(STATIC, DIST, dirs_exist_ok=True)

    write("index.html", home_page(site, cats, gigs_by_cat, draft))
    for cat in cats:
        write(f'{cat["slug"]}/index.html',
              category_page(site, cats, cat, gigs_by_cat.get(cat["slug"], []), draft))
    write("how-we-pick/index.html", text_page(
        site, cats, slug="how-we-pick", title="How we pick freelancers",
        description="The criteria we use to choose the Fiverr freelancers we recommend.",
        body_html=HOW_WE_PICK, draft=draft))
    write("disclosure/index.html", text_page(
        site, cats, slug="disclosure", title="Affiliate disclosure",
        description="How this site earns money through Fiverr affiliate links.",
        body_html=DISCLOSURE, draft=draft))
    write("privacy/index.html", text_page(
        site, cats, slug="privacy", title="Privacy policy",
        description="What data this site collects (none) and how affiliate links work.",
        body_html=PRIVACY, draft=draft))
    write("404.html", page(site, cats, title=f'Page not found | {site["name"]}',
                           description="Page not found.", path="/404", body=NOT_FOUND, draft=draft))
    write("sitemap.xml", sitemap(site, cats))
    write("robots.txt", f'User-agent: *\nAllow: /\n\nSitemap: {site["base_url"].rstrip("/")}/sitemap.xml\n')
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    live = sum(g["status"] == "live" for g in gigs)
    mode = "release" if release else "preview"
    print(f"Built ({mode}): {len(cats)} categories, {live} live gigs, "
          f"{len(gigs) - live} draft gigs {'hidden' if release else 'shown'} -> {DIST}")


if __name__ == "__main__":
    main()
