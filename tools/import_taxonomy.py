"""Turn a Fiverr category list into content/taxonomy/<top>.json.

usage: python tools/import_taxonomy.py <top-slug> "<Top Name>" <order> <raw.json> "<blurb>" "<intro>"

raw.json is what the browser snippet collects from a Fiverr category page:
    [{"g": "<group name>", "s": [["<service name>", "<fiverr slug or full /categories/... path>"], ...]}, ...]
A bare slug is taken to live under /categories/<top-slug>/. Showcase categories such as
AI Services link into other categories, so their entries carry full paths.
An existing file keeps its blurb and intro; pass new ones by deleting the file first.
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("&", "and").replace("'", "")).strip("-")


def main():
    top_slug, top_name, order, raw_path, blurb, intro = sys.argv[1:7]
    raw = json.loads(Path(raw_path).read_text(encoding="utf-8-sig"))
    groups, seen = [], set()
    for g in raw:
        subs = []
        for name, path in g["s"]:
            s = slug(name)
            if s in seen:
                continue
            seen.add(s)
            full = path if path.startswith("/") else f"/categories/{top_slug}/{path}"
            subs.append({"slug": s, "name": name, "fiverr_path": full})
        groups.append({"name": g["g"], "subs": subs})

    out = SITE / "content" / "taxonomy" / f"{top_slug}.json"
    old = json.loads(out.read_text(encoding="utf-8-sig")) if out.exists() else {}
    top = {
        "slug": top_slug,
        "name": top_name,
        "order": int(order),
        "fiverr_path": f"/categories/{top_slug}",
        "source_checked": dt.date.today().isoformat(),
        "blurb": old.get("blurb") or blurb,
        "intro": old.get("intro") or intro,
        "groups": groups,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(top, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{top_slug}: {len(groups)} groups, {sum(len(g['subs']) for g in groups)} services")


if __name__ == "__main__":
    main()
