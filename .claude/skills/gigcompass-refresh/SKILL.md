---
name: gigcompass-refresh
description: Routine check-up for the GigCompass site. Finds seller picks whose rating, reviews or price were checked long ago, re-reads the Fiverr listings, updates the numbers, replaces sellers who dropped below the bar or disappeared, rebuilds and publishes, and reports what changed. Triggers: "사이트 점검해줘", "판매자 정보 갱신", "오래된 카드 확인", "refresh picks", "gigcompass-refresh".
---

# GigCompass: refresh seller picks

Run from the site root (`D:\Claude_Projects\Fiverr_Affiliate\fiverr-affiliate-site`). Set `PYTHONIOENCODING=utf-8` before Python.
Report to the user in Korean. This needs the Claude desktop app open (Browser pane) and ideally the
user at the PC, because Fiverr may show a bot check.

## 1. What needs checking

```
python tools/picks.py stale --days 90
python build.py --release
```

`stale` lists pages whose live picks were last checked more than 90 days ago, oldest first (use a smaller
`--days` if the user asks for a full check). The build prints any other warnings (for example picks older
than 120 days). If nothing is stale, say so and stop.

Do **1–2 pages per session**; more Fiverr page loads means more bot checks.

## 2. Re-read the listing for each page

Open the service's `fiverr_path` (from `content/taxonomy/<top>.json`) and run the listing snippet from
`gigcompass-picks` step 1 (it also collects cover images). If fewer than half the page's picks appear,
load `?page=2` (5+ s later) and append. Save as `<scratchpad>/candidates.json`, then:

```
python tools/picks.py refresh <scratchpad>/candidates.json --page <top>/<service>
```

It updates rating, reviews, starting price and level for picks it finds, stamps them checked today,
and prints three lists: updated picks (with what changed), picks that **no longer meet the bar**, and
picks **not in this listing**.

**Bot check:** if the title is "It needs a human touch", stop, never solve it, bring the tab to the front,
send a PushNotification, and ask the user to hold the button (they may do it from their phone through
Chrome Remote Desktop). Continue when they say it passed.

## 3. Handle the problem picks

- **Not in this listing:** open that gig's `gig_url` directly (5+ s apart). If it loads and still shows a
  rating that meets the bar, keep it and set its `checked` to today by hand in `content/gigs.csv`
  (write the file with Python's csv module or the Write tool, keeping UTF-8 with BOM). If the gig is
  gone, paused or below the bar, it must be replaced.
- **Below the bar / gone:** re-run the **gigcompass-picks** procedure for that page (steps 1b–4) with the
  candidates you already have. `picks.py add` replaces the whole page, so the final `picks.json` must
  contain the kept picks too (reuse their existing `best_for`, `why`, `watch_out`) plus the new ones,
  ranked again with Vetted Pro and designed covers first.
- If a kept pick's numbers changed a lot (rating down, price up sharply), reread its `why` and
  `watch_out` and fix any sentence that is no longer true ("the lowest price in our top five").

## 4. Build, preview, publish

```
python build.py --release
```

Preview the changed pages in the Browser pane, then:

```
git add -A && git commit -m "Refresh picks: <pages>" && git push
```

## 5. Report

Tell the user, per page: how many picks were checked, what changed (rating, reviews, price), which
sellers were replaced and why, and the live URLs. Mention the next pages that will become stale.

## Rules

- Same selection bar and house style as gigcompass-picks (Vetted Pro first, designed covers only,
  no copied seller text, no "Fiverr" in card text).
- Never change a pick's text to sound better than the facts; only correct it.
- This skill is run on request. If the user wants a reminder, suggest a weekly scheduled task that
  only reminds them; do not publish unattended.
