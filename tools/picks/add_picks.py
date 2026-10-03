"""Append or replace pick rows in content/gigs.csv. Usage: import and call put(page, rows)."""
import csv, io, os
import pathlib
CSV = pathlib.Path(__file__).resolve().parents[2] / "content" / "gigs.csv"
FIELDS = ["id", "page", "status", "rank", "name", "best_for", "gig_title", "rating", "reviews", "level",
          "starting_price", "checked", "why", "watch_out", "gig_url", "affiliate_url", "photo", "gig_image"]
CHECKED = "2026-10-02"

def put(page, rows, status="draft"):
    with open(CSV, encoding="utf-8-sig", newline="") as f:
        old = [r for r in csv.DictReader(f) if r["page"] != page]
    slug = page.split("/")[1]
    new = []
    for i, r in enumerate(rows, 1):
        d = {k: "" for k in FIELDS}
        d.update(id=f"{slug}-{r['user']}", page=page, status=status, rank=str(i), name=r["name"],
                 best_for=r["best_for"], gig_title=r["title"], rating=r["rating"], reviews=r["reviews"],
                 level=r["level"], starting_price=r["price"], checked=CHECKED, why=r["why"],
                 watch_out=r.get("watch_out", ""), gig_url="https://www.fiverr.com" + r["url"])
        new.append(d)
    with open(CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(old + new)
    print(page, len(new), "rows")
