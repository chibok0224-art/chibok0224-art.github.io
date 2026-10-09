import add_picks

add_picks.CHECKED = "2026-10-09"


def r(user, name, best_for, title, rating, reviews, price, path, why, watch_out=""):
    return dict(user=user, name=name, best_for=best_for, title=title, rating=rating, reviews=reviews,
                level="Level 2", price=price, url=path, why=why, watch_out=watch_out)


# No Pro-vetted sellers in this category (2026-10-09); these are the best-rated Level 2 sellers.
add_picks.put("video-animation/video-repurposing", [
    r("davinchi_beatz", "David", "Best overall for quick clips with captions",
      "I will repurpose video or podcast to ig reels, tiktok and shorts in 24 hrs", "5.0", "134", "30",
      "/davinchi_beatz/repurpose-video-or-podcast-to-ig-reels-tiktok-and-shorts-in-24-hrs",
      "A Level 2 seller with a perfect rating across 134 reviews who cuts long videos and podcasts into short vertical clips with music and captions. The basic package delivers a 30-second clip in one day, with three revisions on every package.",
      "One clip per package below the top tier, which delivers four."),
    r("tawhid2x", "Tawhid A.", "Best for a month of short videos",
      "I will repurpose your youtube or podcast videos into viral shorts, reels and tiktoks", "4.9", "62", "35",
      "/tawhid2x/repurpose-your-youtube-or-podcast-videos-into-viral-shorts-reels-and-tiktoks",
      "A Level 2 seller with 62 reviews who turns long videos into short clips with captions, sound effects and motion graphics. Packages go from one sample clip to a bundle of five or a monthly plan of 30 short videos.",
      "Fewer reviews than the others here."),
    r("fahad_zaffar", "Fahad Zaffar", "Best budget pick for podcast clips",
      "I will repurpose your podcast into viral shorts, reels, tiktok", "4.8", "80", "20",
      "/fahad_zaffar/repurpose-your-podcast-into-viral-shorts-reels-tiktok",
      "A Level 2 seller with 80 reviews who clips podcasts and interviews into short videos with English captions and sound effects. The entry package is a single 30-second demo clip; larger packages deliver five or ten clips.",
      "The entry package includes only one revision."),
    r("savanpipariya", "Savan P.", "Best for simply resizing videos for each platform",
      "I will resize or crop your videos for any platform", "4.9", "289", "5",
      "/savanpipariya/crop-or-resize-your-videos-within-24-hours",
      "A Level 2 seller with 289 reviews who resizes and crops existing videos into any format or dimension, for example from widescreen to vertical. Packages are priced by total video length, with three revisions.",
      "Resizing only: no picking of highlights or creative editing."),
], status="live")
