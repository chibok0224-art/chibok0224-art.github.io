import add_picks

add_picks.CHECKED = "2026-10-09"


def r(user, name, best_for, title, rating, reviews, price, path, why, watch_out=""):
    return dict(user=user, name=name, best_for=best_for, title=title, rating=rating, reviews=reviews,
                level="Vetted Pro", price=price, url=path, why=why, watch_out=watch_out)


add_picks.put("video-animation/ugc-ads", [
    r("mandi_mada", "Mandi Mada", "Best overall for selfie-style video ads",
      "I will create ugc videos for instagram reels, facebook or tiktok", "5.0", "551", "100",
      "/mandi_mada/create-captivating-ugc-content-to-boost-presence-and-sales",
      "A Vetted Pro with a perfect rating across 551 reviews who films selfie-style videos speaking to camera. Every package includes the script, and the 30- and 60-second versions come with unlimited usage rights.",
      "The 15-second package includes only three months of usage rights."),
    r("starwarsnaimad", "Damian J", "Best for ads with captions and B-roll included",
      "I will create user generated content ugc video ads for tiktok or reels", "4.9", "493", "200",
      "/starwarsnaimad/create-ugc-video-ads-for-tik-tok-instagram-and-facebook",
      "A Vetted Pro with 493 reviews who makes UGC ads for short-video platforms. Every package includes a script, B-roll, captions and unlimited revisions, and the longer versions add unlimited usage rights."),
    r("oleleo6", "Ole", "Best for UK creator ads",
      "I will create ugc video ads for tiktok, instagram and facebook", "5.0", "335", "295",
      "/oleleo6/create-ugc-video-ads-for-tiktok-and-instagram-user-generated-content",
      "A Vetted Pro and Top Rated creator from the UK with a perfect rating across 335 reviews. Packages include a script and captions, from a 15-second attention grabber to a 60-second brand video.",
      "Usage rights are three months on every package, and each includes one revision."),
    r("abigail_loves", "Abigail G", "Best for several short videos in one order",
      "I will be your social media expert, female ugc creator and content planner", "4.9", "313", "130",
      "/abigail_loves/your-ugc-content-creator-for-tiktok-youtube-and-instagram",
      "A Vetted Pro and Top Rated creator with 313 reviews. Packages include a script, B-roll, graphics and captions, and the higher tiers deliver three or six videos.",
      "Delivery takes about two weeks, slower than most others here."),
    r("xandermotion", "Xander", "Best for French-language ads with hook variations",
      "I will create french ugc ads with multi hook for tiktok and meta", "5.0", "156", "100",
      "/xandermotion/create-authentic-ugc-content-and-social-media-ads-in-french-and-english",
      "A Vetted Pro with a perfect rating across 156 reviews who makes French UGC ads with several opening hooks to test. Packages include script, B-roll, graphics and captions, with two-day delivery on the basic package.",
      "The seller asks you to make contact before ordering."),
    r("jpoppvoice", "Jonathan", "Best for unboxing and product demo videos",
      "I will create a ugc unboxing and demo video for your amazon product", "5.0", "73", "160",
      "/jpoppvoice/create-a-ugc-unboxing-and-demo-video-for-your-amazon-product",
      "A Vetted Pro with a perfect rating across 73 reviews who films conversational unboxing and demo videos for products, with delivery in three to four days.",
      "Usage rights are three months, and you post the video yourself."),
], status="live")
