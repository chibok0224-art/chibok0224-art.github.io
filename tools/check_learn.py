import json, re, os, glob
os.chdir(r"D:\Claude_Projects\Fiverr_Affiliate\fiverr-affiliate-site")
bad=False
for d in sorted(glob.glob("content/learn/*/")):
    j=json.load(open(d+"page.json",encoding="utf-8")); g=open(d+"article.html",encoding="utf-8").read()
    w=len(re.sub(r"<[^>]+>"," ",g).split())
    broken=[h for h in re.findall(r'href="(/[^"#]*)',g) if not os.path.exists("dist"+h+"index.html")]
    money=bool(re.search(r'[$€£]',g+json.dumps(j))); fv="fiverr" in (g+json.dumps(j)).lower()
    ok=600<=w<=1400 and len(j["faq"])==5 and not broken and not money and not fv and len(j["title"])<=70 and len(j["description"])<=160
    bad|=not ok
    print("OK " if ok else "BAD", d, w, len(j["title"]), len(j["description"]), broken, money, fv)
print("ALL OK" if not bad else "SOME BAD")
