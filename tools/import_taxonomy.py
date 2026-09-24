"""Turn a scraped Fiverr bucket list into content/taxonomy/<top>.json.

usage: python save_taxonomy.py <top-slug> "<Top Name>" <order> <raw.json> "<blurb>" "<intro>"
"""
import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("&", "and").replace("'", "")).strip("-")


top_slug, top_name, order, raw_path, blurb, intro = sys.argv[1:7]
raw = json.loads(Path(raw_path).read_text(encoding="utf-8"))
groups, seen = [], set()
for g in raw:
    subs = []
    for name, path in g["s"]:
        s = slug(name)
        if s in seen:
            continue
        seen.add(s)
        subs.append({"slug": s, "name": name, "fiverr_path": f"/categories/{top_slug}/{path}"})
    groups.append({"name": g["g"], "subs": subs})

out = SITE / "content" / "taxonomy" / f"{top_slug}.json"
old = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
top = {
    "slug": top_slug,
    "name": top_name,
    "order": int(order),
    "fiverr_path": f"/categories/{top_slug}",
    "source_checked": __import__("datetime").date.today().isoformat(),
    "blurb": old.get("blurb") or blurb,
    "intro": old.get("intro") or intro,
    "groups": groups,
}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(top, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(top_slug, len(groups), "groups,", sum(len(g["subs"]) for g in groups), "subs")

