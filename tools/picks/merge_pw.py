"""Merge new widget batches (pw_*.json in this folder) INTO content/pick_widgets.json.

Each batch maps gig id -> {"w": widget id, "ck": "len:hash"} as returned by __gv in the browser
(see browser_helpers.md). The checksum catches copy mistakes; bad entries are skipped and listed.
Existing entries are kept, so a batch only needs the new or fixed widgets. Batches are applied in
numeric order (pw_2 before pw_10), so a later batch overrides an earlier one.
"""
import glob, json, os, pathlib

HERE = pathlib.Path(__file__).resolve().parent
TARGET = HERE.parents[1] / "content" / "pick_widgets.json"


def ck(s):
    x = 0
    for c in s:
        x = (x * 31 + ord(c)) & 0xffffffff
    return f"{len(s)}:{x}"


out = json.loads(TARGET.read_text(encoding="utf-8")) if TARGET.exists() else {}
before, bad, added = len(out), [], 0
for f in sorted(glob.glob(str(HERE / "pw_*.json")), key=lambda p: int(os.path.basename(p)[3:-5])):
    for k, v in json.load(open(f, encoding="utf-8")).items():
        if ck(v["w"]) == v["ck"]:
            out[k] = v["w"]
            added += 1
        else:
            bad.append(k)
TARGET.write_text(json.dumps(out, indent=1), encoding="utf-8")
print("before", before, "applied", added, "now", len(out), "bad", bad)
