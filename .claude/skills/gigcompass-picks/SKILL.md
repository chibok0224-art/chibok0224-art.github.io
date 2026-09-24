---
name: gigcompass-picks
description: Fill a GigCompass service guide with recommended Fiverr sellers, automatically. Reads the Fiverr listing for that service in the built-in browser, takes Vetted Pro sellers first and fills any remaining slots with other sellers who pass the bar (4.8+ rating with 100+ reviews), writes a short card for each in our own words, saves them to content/gigs.csv, builds and publishes. Triggers: "추천 판매자 채워줘", "셀러 골라줘", "fill picks for <service>", "gigcompass-picks".
---

# GigCompass: fill seller picks for a service

Run from the site root (`D:\my_playlist\fiverr-affiliate-site`). Set `PYTHONIOENCODING=utf-8` before running Python.

## 0. Which page

The page key is `<top>/<service>`, e.g. `graphics-design/logo-design`. It must already have a guide in
`content/pages/<top>/<service>/`. If it does not, stop and offer to write the guide first:
picks without a guide are not published. The Fiverr address is the service's `fiverr_path` in
`content/taxonomy/<top>.json`.

## 1. Read the Fiverr listing (built-in browser)

Open `https://www.fiverr.com<fiverr_path>` in the Browser pane, wait ~3 s, then run this in the page:

```js
const out=[]; for (const c of document.querySelectorAll('.gig-wrapper[data-gig-id]')) {
  const a=c.querySelector('a[aria-label="Go to gig"]'); if(!a) continue;
  const href=a.getAttribute('href').split('?')[0]; const t=c.innerText;
  const revRaw=(t.match(/\(([\d.,]+k?\+?)\)/i)||[])[1]||'';
  out.push({seller:c.querySelector('figure')?.getAttribute('title')||'', user:href.split('/')[1],
    title:c.querySelector('h3')?.textContent.trim(), rating:parseFloat(c.querySelector('strong')?.textContent)||null,
    reviews:revRaw.toLowerCase().includes('k')?Math.round(parseFloat(revRaw)*1000):parseInt(revRaw.replace(/,/g,''))||null,
    reviews_plus:revRaw.includes('+'), price:parseFloat(((t.match(/From\s+US\$\s?([\d,.]+)/)||[])[1]||'').replace(/,/g,''))||null,
    badges:['Vetted Pro','Top Rated','Level 2','Level 1',"Fiverr's Choice"].filter(b=>t.includes(b)),
    image:(()=>{const i=a.querySelector('img'); const s=i&&(i.currentSrc||i.src||i.dataset.src)||'';
      return s.includes('fiverr-res.cloudinary.com')?s:'';})(),
    url:'https://www.fiverr.com'+href}); }
JSON.stringify(out)
```

Save the result to the scratchpad as `candidates.json`.

**Vetted Pro first.** The user wants Vetted Pro sellers before anyone else. Count how many cards on
page 1 carry the "Vetted Pro" badge with a rating of 4.7+ and 20+ reviews. If fewer than 8, load
page 2 (`?page=2` on the same listing URL, 5+ s later), run the snippet again, and append the new
cards to `candidates.json`. Stop after page 2; other sellers then fill the remaining slots.

**Bot check.** If the page title is "It needs a human touch", stop. Never press or solve it. Bring that
tab to the front and ask the user to hold the button, then continue after they say it passed.
The user may be away from the PC: also send a PushNotification such as
"GigCompass: Fiverr bot check needs you (hold the button in the browser pane)". They can pass it from
their phone through Chrome Remote Desktop. Do not email them about it: sending mail needs their
approval each time, which they cannot give while away.
Keep at least 5 seconds between Fiverr page loads, and read only the pages this procedure needs.

## 2. Rank

```
python tools/picks.py select <scratchpad>/candidates.json --out <scratchpad>/shortlist.json --n 8
```

This applies the site's bar, removes duplicate sellers, puts every qualifying Vetted Pro seller
first (ranked by rating, then review volume), and only then fills leftover slots with other
qualifying sellers. Entries priced at $50 or less are flagged `budget` so one of them can be
labelled "Best budget pick". Show the printed table to the user in Korean.

## 3. Look at the top picks' gig pages

For the top 5 in the shortlist, open each gig page (5+ s apart) and read `document.body.innerText`
for: package names and prices, what each package includes, delivery time, revisions, and whether
commercial or ad usage rights are mentioned. If a bot check appears, handle it as above. If the user
is not around to pass it, use only the listing data for the remaining picks.

## 4. Write the cards

Add to each shortlist entry, in English:
- `best_for`: one short label, all different, e.g. "Best overall for minimalist brands",
  "Best budget pick", "Best for full brand kits".
- `why`: 2–3 sentences in our own words, **only facts you saw**: track record, badge, what the
  packages include, delivery time. Never copy the seller's description, never invent experience
  ("we ordered", "we loved their portfolio"), never claim results.
- `watch_out`: one honest limitation you actually saw (e.g. source files only in the top package,
  longer delivery, rights sold as an extra). Leave empty if none.
- `page`: the page key.

Save as `<scratchpad>/picks.json`, then:

```
python tools/picks.py add <scratchpad>/picks.json
python build.py --release
```

`add` replaces that page's old rows (drafts included) and stamps today's date as `checked`.
The build turns each `gig_url` into an affiliate deep link, using the `pro` brand for Vetted Pro sellers.

## 5. Check and publish

Preview the page (serve `dist/` on port 8080 if it is not running) and check the cards render.
Then commit and push:

```
git add -A && git commit -m "Picks: <service>" && git push
```

Report to the user in Korean: how many candidates, how many passed the bar, the final list (name,
rating, reviews, level, price, best_for), and the live URL.

## Gig cover images

Cards can show the gig's own cover image (the seller's advertising image) as a banner. The listing
snippet above already returns each card's cover address as `image` (a `fiverr-res.cloudinary.com`
URL), so no extra page loads are needed; `tools/picks.py add` stores it as `gig_image`. It is
hotlinked, never downloaded.

The build shows these banners only when `content/site.json` has `"show_gig_images": true`. Leave it
false until the user has confirmed the Fiverr affiliate terms allow showing gig images; turning it on
later makes every stored image appear at once.

If the auto-mode safety check refuses to read image addresses (covers often show the seller's face),
do not work around it: save the picks without images and tell the user they can copy the cover
addresses by right-click and send them to you.

## Rules

- No copied seller text or portfolio galleries on our site. Stats, our summary, the gig cover image
  (when allowed, see above) and a link only.
- Ratings and prices change: every row carries `checked`, and the build warns after 120 days.
  Re-running this skill for a page refreshes it.
- One or two services per session. Fiverr may block heavier browsing.
