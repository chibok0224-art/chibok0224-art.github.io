"""Choose and save recommended sellers for one service page.

    python tools/picks.py select <candidates.json> [--out shortlist.json] [--n 10]
        Filter and rank sellers scraped from a Fiverr listing page. Prints the shortlist.
    python tools/picks.py add <picks.json>
        Write the final picks into content/gigs.csv as live rows, replacing that page's old rows.

candidates.json is the list the gigcompass-picks skill's browser snippet returns:
    [{"seller", "user", "title", "rating", "reviews", "reviews_plus", "price", "badges", "url"}, ...]
picks.json is the shortlist after Claude has filled in best_for, why and watch_out for each pick,
plus "page": "<top>/<service>".
"""
import csv
import datetime as dt
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GIGS = ROOT / "content" / "gigs.csv"
FIELDS = ["id", "page", "status", "rank", "name", "best_for", "gig_title", "rating", "reviews", "level",
          "starting_price", "checked", "why", "watch_out", "gig_url", "affiliate_url"]

# Same bar as the site's "How we pick" page.
MIN_RATING = 4.8
MIN_REVIEWS = 100
PRO_MIN_RATING = 4.7   # Vetted Pro sellers are pre-vetted by Fiverr, so fewer reviews are enough
PRO_MIN_REVIEWS = 20
BUDGET_PRICE = 50      # a pick at or under this price is labelled as the budget option
LEVEL_ORDER = ["Vetted Pro", "Top Rated", "Level 2", "Level 1"]


def level_of(c):
    return next((b for b in LEVEL_ORDER if b in c.get("badges", [])), "")


def eligible(c):
    r, n = c.get("rating") or 0, c.get("reviews") or 0
    if r >= MIN_RATING and n >= MIN_REVIEWS:
        return True
    return level_of(c) == "Vetted Pro" and r >= PRO_MIN_RATING and n >= PRO_MIN_REVIEWS


def score(c):
    """Rating matters most, then review volume (log scale), then Fiverr's own vetting."""
    bonus = {"Vetted Pro": 3, "Top Rated": 1.5, "Level 2": 0.5}.get(level_of(c), 0)
    return round((c["rating"] - 4.5) * 10 + math.log10(c["reviews"] + 1) * 2 + bonus, 2)


def select(cands, n):
    """Vetted Pro sellers first; other sellers who pass the bar only fill the slots left over."""
    seen, pool = set(), []
    for c in cands:
        if c.get("user") in seen or not c.get("url") or not eligible(c):
            continue
        seen.add(c["user"])
        pool.append(dict(c, level=level_of(c), score=score(c)))
    pool.sort(key=lambda c: (c["level"] == "Vetted Pro", c["score"]), reverse=True)
    chosen = pool[:n]
    for i, c in enumerate(chosen, 1):
        c["rank"] = i
        c["budget"] = (c.get("price") or 1e9) <= BUDGET_PRICE
    return chosen, len(pool)


def cmd_select(args):
    src = Path(args[0])
    out = Path(args[args.index("--out") + 1]) if "--out" in args else src.with_name("shortlist.json")
    n = int(args[args.index("--n") + 1]) if "--n" in args else 10
    cands = json.loads(src.read_text(encoding="utf-8-sig"))
    chosen, eligible_count = select(cands, n)
    out.write_text(json.dumps(chosen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pros = sum(c["level"] == "Vetted Pro" for c in chosen)
    print(f"{len(cands)} candidates, {eligible_count} eligible, {len(chosen)} shortlisted "
          f"({pros} Vetted Pro, {len(chosen) - pros} other) -> {out}")
    if pros < n:
        print(f"  only {pros} Vetted Pro sellers qualified; load the next listing page for more before "
              "accepting other sellers")
    for c in chosen:
        reviews = f'{c["reviews"]:,}{"+" if c.get("reviews_plus") else ""}'
        print(f'  #{c["rank"]:<2} {c["score"]:>5}  {c["rating"]}★ {reviews:>7}  {c["level"] or "-":<10} '
              f'${c.get("price") or "?":<5} {"budget " if c["budget"] else ""}{c["seller"]}')


def cmd_add(args):
    picks = json.loads(Path(args[0]).read_text(encoding="utf-8-sig"))
    pages = {p["page"] for p in picks}
    today = dt.date.today().isoformat()
    missing = [f'{p.get("seller") or p.get("name")}: {f}' for p in picks
               for f in ("page", "best_for", "why", "url") if not p.get(f)]
    if missing:
        sys.exit("picks.json is missing fields:\n  " + "\n  ".join(missing))

    with open(GIGS, encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r.get("page") not in pages]
    for p in picks:
        service = p["page"].split("/")[-1]
        rows.append({
            "id": f'{service}-{p["user"]}',
            "page": p["page"],
            "status": "live",
            "rank": p["rank"],
            "name": p["seller"].strip(),
            "best_for": p["best_for"],
            "gig_title": p.get("title", ""),
            "rating": p["rating"],
            "reviews": p["reviews"],
            "level": p.get("level", ""),
            "starting_price": p.get("price") or "",
            "checked": today,
            "why": p["why"],
            "watch_out": p.get("watch_out", ""),
            "gig_url": p["url"],
            "affiliate_url": "",
        })
    # utf-8-sig so the file opens correctly in Excel.
    with open(GIGS, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(picks)} picks for {', '.join(sorted(pages))} -> {GIGS}")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("select", "add"):
        sys.exit(__doc__)
    {"select": cmd_select, "add": cmd_add}[sys.argv[1]](sys.argv[2:])
