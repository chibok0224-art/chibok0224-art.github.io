#!/usr/bin/env python3
"""Build the static site from content/ into dist/.

    python build.py            preview build: draft gigs are shown (dashed, with a PREVIEW banner)
    python build.py --release  public build: only live gigs; stops on any content error

Content model (mirrors Fiverr):
    content/taxonomy/<top>.json          top category -> groups -> services (every Fiverr subcategory)
    content/pages/<top>/<service>/       our hiring guide for one service: page.json + guide.html
    content/gigs.csv                     recommended sellers, one row each, keyed by page "<top>/<service>"

Every service is listed on its category hub. Services with a guide get their own page;
the rest link straight to Fiverr (through the affiliate link template, once it is set).
"""
import csv
import datetime as dt
import hashlib
import html
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
DIST = ROOT / "dist"
STALE_DAYS = 120  # warn when a gig's rating/price was last checked longer ago than this
FIVERR = "https://www.fiverr.com"

esc = html.escape


def asset_version():
    """Short hash of the CSS and JS, appended to their URLs so browsers fetch new versions after a change."""
    h = hashlib.sha1()
    for name in ("style.css", "site.js"):
        h.update((STATIC / name).read_bytes())
    return h.hexdigest()[:8]


ASSET_V = asset_version()


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


# ---------- content loading ----------

def load_taxonomy():
    """Return (tops, services). Each service dict gets 'top', 'group' and 'path' added."""
    tops, services = [], {}
    for f in sorted((CONTENT / "taxonomy").glob("*.json")):
        top = load(f)
        for group in top["groups"]:
            for s in group["subs"]:
                s["top"], s["group"] = top, group["name"]
                s["path"] = f'{top["slug"]}/{s["slug"]}'
                s["page"] = None
                services[s["path"]] = s
        tops.append(top)
    return sorted(tops, key=lambda t: t.get("order", 99)), services


def load_pages(services, errors, warnings):
    pages = []
    for meta in sorted((CONTENT / "pages").glob("*/*/page.json")):
        key = f"{meta.parent.parent.name}/{meta.parent.name}"
        if key not in services:
            errors.append(f"content/pages/{key}: no such service in content/taxonomy")
            continue
        page = load(meta)
        page["guide_html"] = (meta.parent / "guide.html").read_text(encoding="utf-8")
        # House style: guides don't name Fiverr; only {{fiverr:...}} buttons, the footer and disclosures do.
        text = json.dumps({k: page.get(k) for k in ("title", "h1", "description", "intro", "faq")})
        text += FIVERR_TAG.sub("", page["guide_html"])
        if "fiverr" in text.lower():
            warnings.append(f"content/pages/{key}: mentions Fiverr in the guide text (house style: don't)")
        page["service"] = services[key]
        services[key]["page"] = page
        pages.append(page)
    return pages


# Categories that regroup services from other categories (AI Services, Consulting).
SHOWCASE_TOPS = {"ai-services", "consulting-services"}


def link_showcase_copies(services, warnings):
    """A showcase service with no guide of its own points to the guide of the same service in its
    original category (same Fiverr listing, or same slug). Guides live under the original path."""
    originals = {}
    for s in services.values():
        if s["top"]["slug"] not in SHOWCASE_TOPS and s["page"]:
            originals.setdefault(s["fiverr_path"].rstrip("/"), s)
            if s["slug"] != "other":
                originals.setdefault(s["slug"], s)
    for s in services.values():
        if s["top"]["slug"] not in SHOWCASE_TOPS:
            continue
        orig = originals.get(s["fiverr_path"].rstrip("/")) or originals.get(s["slug"])
        if not orig:
            continue
        if s["page"]:
            warnings.append(f'content/pages/{s["path"]}: write this guide under {orig["path"]} instead')
            continue
        s["page"], s["guide_path"] = orig["page"], orig["path"]


def _num(value, kind):
    value = (value or "").strip().replace(",", "").lstrip("$")
    return kind(value) if value else None


def load_gigs(errors):
    """Read gigs.csv. utf-8-sig so the file also opens cleanly when saved by Excel as 'CSV UTF-8'."""
    gigs = []
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
    return gigs


def check_gigs(gigs, services):
    """Errors block a release build; warnings are only printed."""
    errors, warnings = [], []
    for gid, n in Counter(g["id"] for g in gigs).items():
        if n > 1:
            errors.append(f"gigs.csv: duplicate id '{gid}' ({n} rows)")
    today = dt.date.today()
    for g in gigs:
        where = f"gigs.csv line {g['line']} ({g['id'] or 'no id'})"
        if g["status"] not in ("live", "draft"):
            errors.append(f"{where}: status must be 'live' or 'draft'")
        svc = services.get(g["page"])
        if not svc or not svc["page"]:
            errors.append(f"{where}: page '{g['page']}' has no guide in content/pages")
        elif "guide_path" in svc:
            errors.append(f"{where}: use page '{svc['guide_path']}' (the guide lives there)")
        if g["status"] != "live":
            continue
        for field in ("id", "name", "best_for", "why", "checked"):
            if not g.get(field):
                errors.append(f"{where}: missing '{field}'")
        if not (g.get("gig_url") or g.get("affiliate_url")):
            errors.append(f"{where}: needs gig_url (plain Fiverr gig address)")
        if g.get("gig_url") and not g["gig_url"].startswith("https://www.fiverr.com/"):
            errors.append(f"{where}: gig_url must start with https://www.fiverr.com/")
        if g.get("affiliate_url") and "fiverr" not in g["affiliate_url"].lower():
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


# ---------- links ----------

class Links:
    """Builds outbound Fiverr links as affiliate deep links once site.json has our affiliate id (bta).

    A deep link is https://go.fiverr.com/visit/?bta=<id>&brand=<product>&landingPage=<encoded url>.
    brand picks the commission plan: Fiverr Pro gigs use "pro", Logo Maker pages use "logomaker",
    everything else "marketplace". Without a bta, links are plain Fiverr URLs.
    """

    def __init__(self, site):
        aff = site.get("affiliate", {})
        self.bta = str(aff.get("bta", "")).strip()
        self.pattern = aff.get("link", "")
        self.encode_times = int(aff.get("landing_page_encode_times", 1))
        self.brands = aff.get("brands", {})

    @property
    def active(self):
        return bool(self.bta and self.pattern)

    def brand_for(self, url, pro=False):
        if "/logo-maker" in url:
            return "logomaker"
        return "pro" if pro else "marketplace"

    def deep(self, url, pro=False):
        """url: a full https://www.fiverr.com/... address, or a path starting with '/'."""
        if url.startswith("/"):
            url = FIVERR + url
        if not self.active:
            return url
        landing = url
        for _ in range(self.encode_times):
            landing = quote(landing, safe="")
        brand = self.brands.get(self.brand_for(url, pro), self.brands.get("marketplace", ""))
        return (self.pattern.replace("{bta}", quote(self.bta, safe=""))
                .replace("{brand}", brand).replace("{url}", landing))

    @property
    def rel(self):
        return "sponsored nofollow noopener" if self.active else "nofollow noopener"

    def a(self, path, label, cls=""):
        c = f' class="{cls}"' if cls else ""
        return f'<a{c} href="{esc(self.deep(path))}" rel="{self.rel}" target="_blank">{label}</a>'


FIVERR_TAG = re.compile(r"\{\{fiverr:(/[^|}]*)\|([^}]+)\}\}")


def expand_fiverr_links(text, links):
    """Guides write {{fiverr:/path|Label}}; it becomes an outbound link through the affiliate template."""
    return FIVERR_TAG.sub(lambda m: links.a(m.group(1), esc(m.group(2)), "btn btn-ghost"), text)


def service_link(s, links, *, badge=True):
    """Our guide if we have one, otherwise straight to Fiverr."""
    if s["page"]:
        tag = ' <span class="badge">Guide</span>' if badge else ""
        return f'<a href="/{s.get("guide_path", s["path"])}/">{esc(s["name"])}</a>{tag}'
    return links.a(s["fiverr_path"], f'{esc(s["name"])} <span class="ext">↗</span>', "out")


# ---------- layout ----------

def page(site, *, title, description, path, body, schema=None, draft=False):
    url = site["base_url"].rstrip("/") + path
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
<link rel="stylesheet" href="/style.css?v={ASSET_V}">
<script src="/site.js?v={ASSET_V}" defer></script>
{ld}
</head>
<body>
{banner}
<header class="site-header">
  <div class="wrap bar">
    <a class="logo" href="/"><img src="/favicon.svg" alt="" width="24" height="24">{esc(site['name'])}</a>
    <nav><a href="/#categories">Categories</a><a href="/services/">All services A–Z</a><a href="/how-we-pick/">How we pick</a></nav>
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


def crumbs(*parts):
    """parts: (label, href or None) pairs."""
    out = ['<a href="/">Home</a>']
    for label, href in parts:
        out.append(f'<a href="{href}">{esc(label)}</a>' if href else esc(label))
    return f'<p class="crumbs">{" › ".join(out)}</p>'


def breadcrumb_schema(site, items):
    base = site["base_url"].rstrip("/")
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": name, "item": base + href}
        for i, (name, href) in enumerate([("Home", "/")] + items, 1)]}


DISCLOSURE_NOTE = ('<p class="disclosure-note">We may earn a commission if you hire through links on this page, '
                   'at no extra cost to you. <a href="/how-we-pick/">How we choose picks</a>.</p>')


# ---------- gig rendering ----------

def stats_line(g):
    parts = []
    if g["rating"] is not None and g["reviews"] is not None:
        parts.append(f'<span class="stars">★ {g["rating"]:.1f}</span> ({g["reviews"]:,} reviews)')
    if g["starting_price"] is not None:
        parts.append(f'From ${g["starting_price"]:,.0f}')
    return " · ".join(parts)


def is_pro(g):
    return "pro" in g.get("level", "").lower()


def gig_cta(g, links, label):
    """A hand-made affiliate_url wins; otherwise the gig's plain Fiverr URL becomes a deep link."""
    if g.get("affiliate_url"):
        href, rel = g["affiliate_url"], "sponsored nofollow noopener"
    elif g.get("gig_url"):
        href, rel = links.deep(g["gig_url"], pro=is_pro(g)), links.rel
    else:
        return '<span class="btn btn-off">Gig link missing</span>'
    return f'<a class="btn" href="{esc(href)}" rel="{rel}" target="_blank">{label}</a>'


def avatar(name, size=""):
    """A colored initial, like Fiverr shows for sellers without a photo. We never copy seller photos."""
    name = (name or "?").strip()
    hue = sum(ord(ch) for ch in name) * 37 % 360
    cls = f"avatar {size}".strip()
    return f'<span class="{cls}" style="--h:{hue}" aria-hidden="true">{esc(name[:1].upper())}</span>'


def stars(rating):
    """Five stars, filled to the rating. The number itself is always printed next to it."""
    pct = max(0, min(100, (rating or 0) / 5 * 100))
    return f'<span class="star-bar" style="--pct:{pct:.0f}%" role="img" aria-label="{rating:.1f} out of 5"></span>'


def badges(g):
    level = g.get("level", "")
    if not level:
        return ""
    cls = "pill pro" if is_pro(g) else "pill"
    return f'<span class="{cls}">{esc(level)}</span>'


def hi_res(url):
    """Listing cards use Fiverr's small 330x220 transform; ask its CDN for the 680px version instead."""
    return url.replace("t_gig_cards_web", "t_main1,q_auto,f_auto")


def gig_card(g, i, links):
    gig = f'<p class="gig-title">“{esc(g["gig_title"])}”</p>' if g.get("gig_title") else ""
    watch = f'<p class="watch"><strong>Keep in mind:</strong> {esc(g["watch_out"])}</p>' if g.get("watch_out") else ""
    checked = (f'<p class="checked">Checked on {esc(g["checked"])}. Ratings and prices change, '
               'so confirm on the gig page.</p>' if g.get("checked") else "")
    if g["rating"] is not None:
        reviews = f'{g["reviews"]:,} reviews' if g["reviews"] is not None else ""
        score = (f'<div class="score"><strong>{g["rating"]:.1f}</strong>{stars(g["rating"])}'
                 f'<span>{reviews}</span></div>')
    else:
        score = '<div class="score empty"><span>Rating goes here</span></div>'
    price = f'<p class="price">From <strong>${g["starting_price"]:,.0f}</strong></p>' if g["starting_price"] is not None else ""
    # photo: only an image the seller has allowed us to use, stored under static/img/sellers/.
    photo = g.get("photo", "")
    side_photo = (f'<img class="pick-photo" src="{esc(photo)}" alt="{esc(g["name"])}" '
                  'loading="lazy" decoding="async">' if photo else "")
    # gig_image: the gig's own cover image (landscape), shown as a banner across the card.
    # Covers come in any shape, vertical video frames included. Show the whole image (never crop a face)
    # and fill the rest of the 16:9 frame with a blurred copy of it.
    banner = ""
    if g.get("gig_image"):
        src = esc(hi_res(g["gig_image"]))
        banner = (f'<div class="pick-banner" style="--img:url(\'{src}\')">'
                  f'<img src="{src}" alt="{esc(g.get("gig_title") or g["name"])}" '
                  'loading="lazy" decoding="async" referrerpolicy="no-referrer"></div>')
    cls = "pick" + (" placeholder" if g["status"] != "live" else "") + (" has-banner" if banner else "")
    return f"""<article class="{cls}" id="{esc(g['id'])}">
  {banner}
  <div class="pick-main">
    <p class="best-for"><span class="rank">#{i}</span>{esc(g.get("best_for", ""))}</p>
    <div class="who">
      {"" if photo else avatar(g["name"])}
      <div>
        <h3>{esc(g["name"])}</h3>
        {badges(g)}
      </div>
    </div>
    {gig}
    <p class="why">{esc(g.get("why", ""))}</p>
    {watch}
    <div class="pick-actions">{gig_cta(g, links, f'View {esc(g["name"])} on Fiverr ↗')}</div>
    {checked}
  </div>
  <aside class="pick-side{" has-photo" if photo else ""}">
    {side_photo}
    {score}
    {price}
  </aside>
</article>"""


def gig_row(g, links):
    cls = "row" + (" placeholder" if g["status"] != "live" else "")
    search = " ".join(g.get(k, "") for k in ("name", "best_for", "gig_title", "level")).lower()
    return f"""<li class="{cls}" id="{esc(g['id'])}" data-search="{esc(search)}" data-rank="{g['rank']}"
    data-rating="{g['rating'] or 0}" data-reviews="{g['reviews'] or 0}" data-price="{g['starting_price'] or 0}">
  {f'<img class="avatar sm" src="{esc(g["photo"])}" alt="" loading="lazy">' if g.get("photo") else avatar(g["name"], "sm")}
  <div class="row-main">
    <h3>{esc(g["name"])} {badges(g)}</h3>
    <p class="best-for">{esc(g.get("best_for", ""))}</p>
    <p class="stats">{stats_line(g)}</p>
    <p class="row-why">{esc(g.get("why", ""))}</p>
  </div>
  {gig_cta(g, links, "View gig →")}
</li>"""


def filter_box(target, placeholder, count_id):
    return (f'<div class="list-tools"><input type="search" data-filter="{target}" data-count="#{count_id}" '
            f'placeholder="{esc(placeholder)}" aria-label="Filter"><span id="{count_id}" class="muted"></span></div>')


# ---------- pages ----------

def service_page(site, links, svc, gigs, draft):
    pg, top = svc["page"], svc["top"]
    n = pg.get("featured_count", 5)
    featured, more = gigs[:n], gigs[n:]
    url = f'{site["base_url"].rstrip("/")}/{svc["path"]}/'
    browse = links.a(svc["fiverr_path"], f'Browse all {esc(svc["name"])} gigs on Fiverr →', "btn btn-ghost")

    if featured:
        toc = "".join(f'<li><a href="#{esc(g["id"])}">{esc(g.get("best_for") or g["name"])}</a></li>'
                      for g in featured)
        more_link = f'<li><a href="#more">{len(more)} more options</a></li>' if more else ""
        picks_html = (f'<nav class="toc"><p>Our top picks</p><ol>{toc}{more_link}</ol></nav>'
                      f'<section class="picks">{"".join(gig_card(g, i, links) for i, g in enumerate(featured, 1))}</section>')
    else:
        picks_html = ('<p class="empty">We are finalizing our shortlist for this service. '
                      'Until then, the guide below walks you through how to evaluate sellers yourself.</p>')

    more_html = ""
    if more:
        tools = ""
        if len(more) > 6:
            tools = f"""<div class="list-tools">
  <input type="search" data-filter="#more-list" data-count="#more-count" placeholder="Filter by name or specialty" aria-label="Filter">
  <select data-sort="#more-list" aria-label="Sort">
    <option value="rank">Our ranking</option>
    <option value="rating">Highest rated</option>
    <option value="reviews">Most reviews</option>
    <option value="price">Lowest starting price</option>
  </select>
  <span id="more-count" class="muted"></span>
</div>"""
        more_html = (f'<section class="more"><h2 id="more">More {esc(svc["name"])} sellers worth a look</h2>'
                     f'{tools}<ul id="more-list" class="rows">{"".join(gig_row(g, links) for g in more)}</ul></section>')

    related = [s for g in top["groups"] if g["name"] == svc["group"] for s in g["subs"] if s is not svc]
    related_html = ""
    if related:
        items = "".join(f"<li>{service_link(s, links)}</li>" for s in related)
        related_html = (f'<section class="related"><h2>Related in {esc(svc["group"])}</h2>'
                        f'<ul class="sub-list">{items}</ul></section>')

    faq_html = "".join(f'<details><summary>{esc(f["q"])}</summary><p>{esc(f["a"])}</p></details>'
                       for f in pg.get("faq", []))
    faq_section = f'<section class="faq"><h2 id="faq">FAQ</h2>{faq_html}</section>' if faq_html else ""

    graph = [
        {"@type": "Article", "headline": pg["title"], "description": pg["description"],
         "dateModified": pg["updated"], "mainEntityOfPage": url,
         "author": {"@type": "Organization", "name": site["name"]},
         "publisher": {"@type": "Organization", "name": site["name"]}},
        breadcrumb_schema(site, [(top["name"], f'/{top["slug"]}/'), (svc["name"], f'/{svc["path"]}/')]),
    ]
    if pg.get("faq"):
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in pg["faq"]]})
    live = [g for g in gigs if g["status"] == "live"]
    if live:
        graph.append({"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": g["name"], "url": f'{url}#{g["id"]}'}
            for i, g in enumerate(live, 1)]})

    body = f"""<article class="article">
{crumbs((top["name"], f'/{top["slug"]}/'), (svc["group"], None))}
<h1>{esc(pg["h1"])}</h1>
<p class="updated">Updated {esc(pg["updated"])}</p>
{DISCLOSURE_NOTE}
<p class="lead">{esc(pg["intro"])}</p>
{picks_html}
{more_html}
<p class="browse">{browse}</p>
<section class="guide">
{expand_fiverr_links(pg["guide_html"], links)}
</section>
{faq_section}
{related_html}
</article>"""
    return page(site, title=pg["title"], description=pg["description"], path=f'/{svc["path"]}/',
                body=body, schema={"@context": "https://schema.org", "@graph": graph}, draft=draft)


def top_page(site, links, top, draft):
    groups_html = ""
    for i, g in enumerate(top["groups"]):
        items = "".join(
            f'<li data-search="{esc((s["name"] + " " + g["name"]).lower())}">{service_link(s, links)}</li>'
            for s in g["subs"])
        groups_html += (f'<section class="group" data-group id="g{i}"><h2>{esc(g["name"])}</h2>'
                        f'<ul class="sub-list">{items}</ul></section>')
    count = sum(len(g["subs"]) for g in top["groups"])
    guides = sum(1 for g in top["groups"] for s in g["subs"] if s["page"])
    partial = ('<p class="muted">We are still adding services to this category.</p>'
               if top.get("partial") else "")
    browse = links.a(top["fiverr_path"], f'Browse all {esc(top["name"])} on Fiverr →', "btn btn-ghost")
    body = f"""<article class="article wide">
{crumbs((top["name"], None))}
<div class="top-head">
  <div>
    <h1>{esc(top["name"])} services</h1>
    {DISCLOSURE_NOTE}
    <p class="lead">{esc(top["intro"])}</p>
  </div>
  {art(top, "top-art")}
</div>
<p class="muted">{count} services · {guides} with our hiring guide · <span class="badge">Guide</span> = our picks and checklist, <span class="ext">↗</span> = opens Fiverr</p>
{filter_box("#groups", f"Find a {top['name']} service", "groups-count")}
<div id="groups" class="groups">{groups_html}</div>
{partial}
<p class="browse">{browse}</p>
</article>"""
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": f'{top["name"]} services', "description": top["blurb"]},
        breadcrumb_schema(site, [(top["name"], f'/{top["slug"]}/')])]}
    return page(site, title=f'{top["name"]} Services: Every Specialty, Explained | {site["name"]}',
                description=f'{top["blurb"]} Browse {count} {top["name"]} services and read our hiring guides.',
                path=f'/{top["slug"]}/', body=body, schema=schema, draft=draft)


def services_page(site, links, services, draft):
    rows = "".join(
        f'<li data-search="{esc((s["name"] + " " + s["group"] + " " + s["top"]["name"]).lower())}">'
        f'{service_link(s, links)} <span class="muted">· {esc(s["top"]["name"])}</span></li>'
        for s in sorted(services.values(), key=lambda s: s["name"].lower()))
    body = f"""<article class="article">
{crumbs(("All services", None))}
<h1>All services A–Z</h1>
<p class="lead">Every freelance service we track, in one list. Start typing to filter.</p>
{filter_box("#az", "Logo, UGC, voice over, SEO…", "az-count")}
<ul id="az" class="az">{rows}</ul>
</article>"""
    return page(site, title=f'All Freelance Services A–Z | {site["name"]}',
                description="Every freelance service category in one searchable list, with our hiring guides where available.",
                path="/services/", body=body, draft=draft)


def art(top, cls="card-art"):
    return (f'<img class="{cls}" src="/img/cat/{top["slug"]}.svg" alt="" width="320" height="180" '
            'loading="lazy" decoding="async">')


def home_page(site, tops, pages, draft):
    cards = ""
    for t in tops:
        count = sum(len(g["subs"]) for g in t["groups"])
        guides = sum(1 for g in t["groups"] for s in g["subs"] if s["page"])
        meta = f"{count} services" + (f" · {guides} guide{'s' if guides != 1 else ''}" if guides else "")
        cards += (f'<a class="card" href="/{t["slug"]}/">{art(t)}<div class="card-body">'
                  f'<h3>{esc(t["name"])}</h3><p>{esc(t["blurb"])}</p><span>{meta} →</span></div></a>')
    latest = sorted(pages, key=lambda p: p["updated"], reverse=True)[:12]
    latest_html = "".join(
        f'<a class="card guide-card" href="/{p["service"]["path"]}/">{art(p["service"]["top"])}'
        f'<div class="card-body"><p class="eyebrow">{esc(p["service"]["top"]["name"])}</p>'
        f'<h3>{esc(p["h1"])}</h3><span>Read the guide →</span></div></a>' for p in latest)
    schema = {"@context": "https://schema.org", "@type": "WebSite", "name": site["name"],
              "url": site["base_url"].rstrip("/") + "/", "description": site["description"]}
    body = f"""<section class="hero">
<h1>{esc(site["tagline"])}</h1>
<p>Freelance marketplaces list hundreds of service categories and thousands of sellers in each. We map every category, explain what to check before you hire, and shortlist sellers with a long, public track record.</p>
<p><a class="btn" href="/services/">Search all services</a></p>
</section>
<section>
<h2 id="categories">Browse by category</h2>
<div class="cards">{cards}</div>
</section>
<section>
<h2>Latest hiring guides</h2>
<div class="cards">{latest_html}</div>
</section>
<section class="method">
<h2>How we pick</h2>
<ul>
  <li><strong>Vetted Pro first.</strong> Pro-vetted sellers come first; others need 100+ reviews with a 4.8+ average.</li>
  <li><strong>Gig pages checked.</strong> We look at what each package includes, delivery times and revisions.</li>
  <li><strong>Honest notes.</strong> Every pick lists a limitation when we find one.</li>
  <li><strong>Dated and re-checked.</strong> Every pick shows when we last checked it.</li>
</ul>
<p><a href="/how-we-pick/">Read our full method →</a></p>
</section>"""
    return page(site, title=f'{site["name"]}: {site["tagline"]}',
                description=site["description"], path="/", body=body, schema=schema, draft=draft)


def text_page(site, *, slug, title, description, body_html, draft):
    body = f'<article class="article prose"><h1>{esc(title)}</h1>{body_html}</article>'
    return page(site, title=f'{title} | {site["name"]}', description=description,
                path=f"/{slug}/", body=body, draft=draft)


HOW_WE_PICK = """
<p>Sellers cannot pay to be listed or to move up a list. Our picks follow fixed, public rules, applied the same way in every category.</p>
<h2>Our criteria</h2>
<ul>
  <li><strong>Public track record.</strong> An average rating of 4.8 or higher from at least 100 reviews, or Vetted Pro verification with a rating of 4.7 or higher.</li>
  <li><strong>Vetted Pro first.</strong> We start with sellers vetted for the marketplace's Pro program, ranked by rating and then by the number of reviews. Other top-rated sellers fill the list only when there are not enough qualifying Pro sellers.</li>
  <li><strong>Gig check.</strong> For our top picks we read the gig page: what each package includes, delivery times, revisions and, where relevant, usage rights. Each pick's summary is written from that, in our own words.</li>
  <li><strong>Limitations.</strong> When a gig has a catch, such as source files only in the top package, we say so on the pick.</li>
</ul>
<h2>What we do not claim</h2>
<p>We have not personally ordered from the sellers we list, and we do not judge creative taste for you. Our picks are a shortlist based on public track record and what each gig offers. Ratings, prices and availability change, so each pick shows the date we last checked it. Always look at the seller's portfolio and confirm the details on the gig page before ordering.</p>
<h2>How we make money</h2>
<p>We are members of the Fiverr affiliate program. If you hire through our links, Fiverr may pay us a commission. You pay the same price. This never decides who we list.</p>
"""

DISCLOSURE = """
<p>This site contains affiliate links. If you click a link to Fiverr and then make a purchase, we may receive a commission from Fiverr. This costs you nothing extra.</p>
<p>Links that take you to Fiverr, including category links and seller buttons, may be affiliate links. Commissions help us keep the site running, but they do not affect which freelancers we recommend. Sellers cannot pay for placement.</p>
<p>This site is independent and is not affiliated with, sponsored by, or endorsed by Fiverr. “Fiverr” is a trademark of its owner and is used here only to describe the services we link to.</p>
"""

PRIVACY = """
<p>This site does not use cookies, does not run analytics, and does not ask you for personal information.</p>
<p>When you click a link to Fiverr, you leave this site. Fiverr may then set its own cookies, including cookies that record that you came from our link so that a commission can be credited. That is governed by Fiverr's own privacy policy.</p>
<p>Our hosting provider may keep standard server logs (such as IP address and pages requested) for security and reliability.</p>
<p>If we add analytics or any form in the future, we will update this page first.</p>
"""

NOT_FOUND = """<section class="hero"><h1>Page not found</h1>
<p>That page does not exist. <a href="/">Go to the home page</a> or <a href="/services/">search all services</a>.</p></section>"""


def sitemap(site, tops, pages):
    base = site["base_url"].rstrip("/")
    entries = [("/", site["updated"]), ("/services/", site["updated"])]
    entries += [(f'/{t["slug"]}/', t.get("source_checked", site["updated"])) for t in tops]
    entries += [(f'/{p["service"]["path"]}/', p["updated"]) for p in pages]
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
    links = Links(site)
    errors, warnings = [], []
    tops, services = load_taxonomy()
    pages = load_pages(services, errors, warnings)
    link_showcase_copies(services, warnings)
    gigs = load_gigs(errors)
    e, w = check_gigs(gigs, services)
    errors += e
    warnings += w
    if not links.active:
        warnings.append("affiliate.bta is empty in site.json: Fiverr links are plain (no commission)")
    for t in tops:
        if not (STATIC / "img" / "cat" / f'{t["slug"]}.svg').exists():
            warnings.append(f'no card image for {t["slug"]}: add it to tools/category_art.py and run it')
    unverified = [s["path"] for s in services.values() if s.get("unverified")]
    if unverified:
        warnings.append(f"fiverr_path not verified for: {', '.join(unverified)}")

    for msg in warnings:
        print("  warning:", msg)
    if errors:
        print("Fix these first:")
        for msg in errors:
            print("  -", msg)
        if release:
            sys.exit(1)

    # Gig cover images are collected with the picks but only shown once the affiliate terms allow it.
    if not site.get("show_gig_images"):
        for g in gigs:
            g["gig_image"] = ""

    shown = [g for g in gigs if g["status"] == "live" or not release]
    draft = any(g["status"] != "live" for g in shown)
    by_page = {}
    for g in sorted(shown, key=lambda g: (g["rank"], g["name"].lower())):
        by_page.setdefault(g["page"], []).append(g)

    clean_dist()
    shutil.copytree(STATIC, DIST, dirs_exist_ok=True)

    write("index.html", home_page(site, tops, pages, draft))
    write("services/index.html", services_page(site, links, services, draft))
    for top in tops:
        write(f'{top["slug"]}/index.html', top_page(site, links, top, draft))
    for pg in pages:
        svc = pg["service"]
        write(f'{svc["path"]}/index.html', service_page(site, links, svc, by_page.get(svc["path"], []), draft))
    write("how-we-pick/index.html", text_page(
        site, slug="how-we-pick", title="How we pick freelancers",
        description="The criteria we use to choose the freelancers we recommend.",
        body_html=HOW_WE_PICK, draft=draft))
    write("disclosure/index.html", text_page(
        site, slug="disclosure", title="Affiliate disclosure",
        description="How this site earns money through Fiverr affiliate links.",
        body_html=DISCLOSURE, draft=draft))
    write("privacy/index.html", text_page(
        site, slug="privacy", title="Privacy policy",
        description="What data this site collects (none) and how affiliate links work.",
        body_html=PRIVACY, draft=draft))
    write("404.html", page(site, title=f'Page not found | {site["name"]}',
                           description="Page not found.", path="/404", body=NOT_FOUND, draft=draft))
    write("sitemap.xml", sitemap(site, tops, pages))
    write("robots.txt", f'User-agent: *\nAllow: /\n\nSitemap: {site["base_url"].rstrip("/")}/sitemap.xml\n')
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    live = sum(g["status"] == "live" for g in gigs)
    print(f"Built ({'release' if release else 'preview'}): {len(tops)} categories, {len(services)} services, "
          f"{len(pages)} guides, {live} live gigs -> {DIST}")


if __name__ == "__main__":
    main()
