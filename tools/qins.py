"""Insert a 'Questions to ask before you order' section before a guide's checklist.

Usage: python tools/qins.py batchN.py
The batch file defines Q = {"category/service": ([five questions], "one tip paragraph")}.
Guides that already have id="questions" are skipped. Files are saved with LF endings.
"""
import html
import os
import runpy
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "pages")
Q = runpy.run_path(sys.argv[1])["Q"]
for path, (qs, tip) in Q.items():
    assert len(qs) == 5, path
    assert "fiverr" not in (" ".join(qs) + tip).lower(), path
    fn = os.path.join(ROOT, *path.split("/"), "guide.html")
    s = open(fn, encoding="utf-8").read().replace("\r\n", "\n")
    if 'id="questions"' in s:
        print("skip", path)
        continue
    mark = '<h2 id="checklist">'
    assert s.count(mark) == 1, path
    items = "\n".join(f"  <li>{html.escape(q, quote=False)}</li>" for q in qs)
    block = (f'<h2 id="questions">Questions to ask before you order</h2>\n<ul>\n{items}\n</ul>\n'
             f'<p>{html.escape(tip, quote=False)}</p>\n\n')
    open(fn, "w", encoding="utf-8", newline="\n").write(s.replace(mark, block + mark))
    print("ok", path)
