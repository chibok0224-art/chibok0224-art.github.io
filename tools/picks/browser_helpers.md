# Browser helpers for seller picks

Picks are researched and widgets are made in the built-in browser, logged in to Fiverr.
Two tabs: one on `https://www.fiverr.com/nga_builder?affid=1176697` (widget builder) and one for research.
If a page title is "It needs a human touch" (bot check), stop and ask the user to solve it. Never solve it yourself.
Open gig pages one at a time with a pause in between; fast runs trigger bot checks.

## Research (saved in Fiverr's localStorage, survives reloads)

- `await eval(localStorage.__cx)` on a search page: cards that pass the rules
  (Vetted Pro, or rating >= 4.8 with >= 100 reviews) as `[name, level, rating, reviews, url]`.
  Pro-only results: add `&ref=pro%3Aany` to the search URL.
- `await eval(localStorage.__tx)` on a gig page: title, exact level/rating/reviews, the three packages
  (price, what is included) and the start of "About this gig".

If localStorage was cleared, the sources are below.

```js
// __cx
(async()=>{if(/human touch/i.test(document.title))return 'BOTCHECK';await new Promise(r=>setTimeout(r,2000));for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,200))}const s=new Set();return JSON.stringify([...document.querySelectorAll('div.gig-card-layout')].map(c=>{const t=c.innerText;const a=[...c.querySelectorAll('a[href]')].map(x=>x.getAttribute('href')).find(h=>/^\/[^\/]+\/[^\/?]+/.test(h)&&!h.startsWith('/categories')&&!h.startsWith('/pro'));const m=t.match(/\n(\d\.\d)\n\(([\d,.k+]+)\)/i);const lines=t.split('\n').filter(Boolean);return [lines[1],(t.match(/Vetted Pro|Top Rated|Level 2|Level 1/)||[''])[0],m&&m[1],m&&m[2],a&&a.split('?')[0]]}).filter(x=>x[4]&&!s.has(x[4])&&s.add(x[4])&&(x[1]==='Vetted Pro'||(x[3]&&(/k/.test(x[3])||parseInt(x[3].replace(/,/g,''))>=100)&&parseFloat(x[2])>=4.8))))})()

// __tx
(async()=>{if(/human touch/i.test(document.title))return 'BOTCHECK';await new Promise(r=>setTimeout(r,2000));const out=[];const tabs=[...document.querySelectorAll('label')].filter(e=>/^(Basic|Standard|Premium)$/.test(e.innerText.trim()));const grab=()=>{const t=document.body.innerText;const i=t.indexOf('US$');return t.slice(i,i+420).replace(/\n+/g,' | ')};if(tabs.length){for(const tb of tabs){tb.click();await new Promise(r=>setTimeout(r,600));out.push(tb.innerText.trim()[0]+': '+grab())}}else out.push(grab());const t=document.body.innerText;return JSON.stringify({title:document.title.split(' | ')[0],head:(t.match(/(Vetted Pro|Top Rated|Level 2|Level 1)[\s\S]{0,40}?(\d\.\d)\s*\n?\(?([\d,]+)/)||[]).slice(1),pk:out,about:(t.split('About this gig')[1]||'').replace(/\s+/g,' ').slice(0,350)})})()
```

## Widgets (window functions, lost on reload: redefine them in the builder tab)

1. Hook `XMLHttpRequest.prototype.open` / `setRequestHeader` to record the headers the builder sends,
   then click the builder's Apply button once so a real request goes out. Keep those headers
   (the CSRF-style ones) in `window.__hdr`.
2. `__enc2(username, slug, keyword)`: POST `/nga_builder/encode_settings` with the recorded headers and
   `{widgetData:{affiliateId:"1176697",brand:"fiverrmarketplace",utmCampaign:"gig_ads",widgetLocalization:"en",
   widgetMoreButton:"Explore more services",widgetTitle:"",mode:"specific_gig",version:"2",domain:"",
   gigFilters:{minPrice:null,maxPrice:null,category:null,subCategory:null,searchQuery:keyword},
   gig:{username,slug}}}`; return `{d: <encoded widget id>, status}`. A 403 means the headers are stale
   (or a bot check happened): reload, re-hook, click Apply again.
3. `__ck2(s)`: checksum `len:hash` with `x=(x*31+charCode)>>>0` (same as merge_pw.py `ck`).
4. `__gv(list, keyword)` with `list = [[gigId, username, slug], ...]`:

```js
async(L,kw)=>{const out={};for(const [id,u,s] of L){const r=await window.__enc2(u,s,kw);if(!r.d){out[id]={err:r.status};continue}const h=await (await fetch('/gig_widgets?id='+encodeURIComponent(r.d)+'&affiliate_id=1176697&strip_google_tagmanager=true')).text();const users=[...new Set([...h.matchAll(/landingPage=https%3A%2F%2Ffiverr.com%2F([^%]+)%2F/g)].map(m=>m[1]))].filter(x=>x!=='categories'&&x!=='search');out[id]={w:r.d,ck:window.__ck2(r.d),ok:users.length===1&&users[0]===u?'OK':'BAD:'+users.join(',')};await new Promise(z=>setTimeout(z,3500))}return JSON.stringify(out)}
```

Only keep entries with `ok:"OK"` (the rendered widget shows exactly that seller). Use the full gig slug from
the gig URL; a truncated slug makes Fiverr fall back to other sellers. Save the result as the next
`pw_N.json` here, run `python merge_pw.py`, then build.
Gig ids are `<guide slug>-<username>`, matching `add_picks.py`. Keyword: `tools/widgets.py keyword_for`.
