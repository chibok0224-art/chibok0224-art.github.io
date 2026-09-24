---
name: gigcompass-guide
description: Write new GigCompass hiring guides (one page per freelance service) in the site's house format, then build, preview and publish. Picks the next services from CONTENT_PLAN.md unless the user names them, and hands over to gigcompass-picks to add sellers once the affiliate id is set. Triggers: "가이드 써줘", "가이드 추가", "다음 가이드", "1순위 1~3번 가이드", "write a guide for <service>", "gigcompass-guide".
---

# GigCompass: write hiring guides

Run from the site root (`D:\my_playlist\fiverr-affiliate-site`). Set `PYTHONIOENCODING=utf-8` before Python.
Talk to the user in Korean; the site itself is in English.

## 0. Choose the services

- If the user names services, use those. Otherwise open `CONTENT_PLAN.md` and take the next 2–3 rows
  that are not under "완료". Tell the user which ones before writing.
- Find each service's path `<top>/<service>` in `content/taxonomy/<top>.json` (the `slug` fields).
  A service that appears in both a showcase category (`ai-services`, `consulting-services`) and its
  original category is written under the **original** one, e.g. `programming-tech/ai-development`.
- Skip services that already have `content/pages/<top>/<service>/`.

## 1. (Optional) Look at the market

To make the guide concrete, you may open the service's Fiverr listing (`fiverr_path` in the taxonomy)
once and read the gig titles and starting prices with the snippet in `gigcompass-picks` step 1. Use it
only to learn what buyers are offered (common package types, typical deliverables). Never copy seller
text, never quote seller names in the guide, and never print specific prices. If a bot check appears,
stop and ask the user to hold the button (see gigcompass-picks); if they are away, skip this step.

## 2. Write two files per service

`content/pages/<top>/<service>/page.json` (copy the shape of an existing one, e.g.
`content/pages/graphics-design/logo-design/page.json`):

| field | rule |
|---|---|
| `title` | `Best <Plural Role> (<year>): <promise>` — under ~65 characters where possible |
| `h1` | `Best <Plural Role>` |
| `description` | one sentence, under ~155 characters, starts "How to hire a/an …" |
| `intro` | 2–3 sentences: why this service matters and what goes wrong most often |
| `updated` | today's date `YYYY-MM-DD` |
| `featured_count` | 5 |
| `faq` | exactly 5 questions buyers really ask (rights, revisions, timing, what to send, pricing model) |

`content/pages/<top>/<service>/guide.html`, same section ids as the other guides:

1. `<h2 id="what-you-get">` what the package must state (deliverables, formats, revisions, rights, delivery)
2. `<h2 id="brief">` an ordered list of what to send the freelancer
3. `<h2 id="price">` what drives the price (factors only, **no numbers**)
4. `<h2 id="red-flags">` 4–5 concrete warning signs
5. `<h2 id="checklist">` `<ul class="checklist">` with 5 "I have…" items

Optional: a relevant Fiverr product button with `{{fiverr:/path|Label on Fiverr →}}` (e.g. Logo Maker).

**House rules**
- Do not name Fiverr anywhere in `page.json` or the guide text. Say "the marketplace", "Pro-vetted",
  "reviews". The only exception is the label inside a `{{fiverr:...}}` button. The build warns if this slips.
- Facts and practical advice only. No invented statistics, prices, success stories or testimonials, no
  "we tested", no guarantees. Advice that depends on law or tax (finance, legal) says to check local rules.
- Plain English, short sentences, 450–750 words of guide body. Write for a first-time buyer.
- Link to a related guide on the site when one exists (`<a href="/<top>/<service>/">`).

## 3. Build, check, preview

```
python build.py --release
```

It must finish without errors or "mentions Fiverr" warnings. Serve `dist/` on port 8080 if nothing is
running there (`python -m http.server 8080 --directory dist`, in the background), open each new page in
the Browser pane, and check the heading, FAQ and layout. On Windows, write JSON and HTML with the
Write tool, not PowerShell `Set-Content` (it adds a BOM and mangles quotes).

## 4. Record and publish

- In `CONTENT_PLAN.md`, add the service to the "완료" line and strike or remove its row from the tier table.
- Update the memory file `gigcompass-guide-priority.md` (the 완료 list) so the next session knows.
- Commit and push:

```
git add -A && git commit -m "Guides: <service>, <service>" && git push
```

GitHub Actions publishes in about a minute. Report the new live URLs to the user in Korean.

## 5. Sellers

If `content/site.json` has a non-empty `affiliate.bta`, offer to run **gigcompass-picks** for each new
guide right away (Vetted Pro first, designed covers first). Until then the page shows "We are
finalizing our shortlist", which is expected.
