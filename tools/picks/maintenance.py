import add_picks

add_picks.CHECKED = "2026-10-09"


def r(user, name, best_for, title, rating, reviews, price, path, why, watch_out=""):
    return dict(user=user, name=name, best_for=best_for, title=title, rating=rating, reviews=reviews,
                level="Vetted Pro", price=price, url=path, why=why, watch_out=watch_out)


add_picks.put("programming-tech/website-maintenance", [
    r("w0rdpressdesign", "WPDesigns", "Best overall for a monthly WordPress care plan",
      "Our agency will host, carry out work, renew licenses and or maintain your wordpress website", "5.0", "199", "125",
      "/w0rdpressdesign/update-and-maintain-your-wordpress-website",
      "A Vetted Pro agency with a perfect rating across 199 reviews. The basic package covers updates to plugins, themes and WordPress core plus onsite, offsite and cloud backups; the next tier adds up to 15 small content edits a month.",
      "Unlimited changes are only in the top package, which costs far more than the basic plan."),
    r("kaushik_15", "Kaushik V", "Best budget pick for a faster WordPress site",
      "I will increase wordpress speed optimization for gtmetrix, google page speed insights", "5.0", "1163", "100",
      "/kaushik_15/speed-up-wordpress-site-optimize-gtmetrix-page-speed-score",
      "A Vetted Pro with a perfect rating across more than 1,100 reviews. Every package includes caching, minification, image resizing and database optimization, with three-day delivery.",
      "This is a one-time speed job, not ongoing maintenance; ask what happens to the scores after future updates."),
    r("hbasoglu", "Hasan B.", "Best for fast one-off WordPress fixes",
      "I will fix your wordpress website issue", "5.0", "487", "100",
      "/hbasoglu/fix-your-wordpress-website-issue",
      "A Vetted Pro with a perfect rating across 487 reviews who fixes broken WordPress sites, such as server errors, image upload problems or a site stuck after an update. The package lists one-day delivery and three revisions for a small issue.",
      "The single package covers one small issue or change; larger problems need a custom quote."),
    r("tijn22", "Martijn", "Best for cleaning a hacked WordPress site",
      "I will do wordpress malware removal and fix your hacked website within 24 hours", "5.0", "268", "125",
      "/tijn22/clean-your-hacked-website-of-malware-and-malicious-code",
      "A Vetted Pro with a perfect rating across 268 reviews who removes malware, spam redirects and backdoors by hand. Packages include vulnerability testing, security patches and blacklist removal, and the top tier adds three months of support.",
      "Security hardening after the cleanup starts from the middle package."),
    r("bestsurprise", "Supriyadi W", "Best for a fix plus a full site update",
      "I will fix an issue with your wordpress", "5.0", "368", "120",
      "/bestsurprise/fix-an-issue-with-your-wordpress",
      "A Vetted Pro with a perfect rating across 368 reviews. The basic package fixes one small WordPress issue; higher tiers also update WordPress core, plugins and theme, and the top tier sets up backups and speed optimization.",
      "The seller asks you to send a message describing the problem before ordering, and each order covers one issue."),
    r("sebastian__de", "Sebastian K", "Best for Shopify store bugs",
      "I will fix shopify bugs as a professional shopify developer", "5.0", "141", "145",
      "/sebastian__de/fix-shopify-bugs-in-html-css-liquid-as-professional-shopify-developer",
      "A Vetted Pro with a perfect rating across 141 reviews who fixes Shopify theme and code bugs. Each fix is tested and comes with a short screen-recorded walkthrough of what was changed, with two-day delivery on the basic package.",
      "Priced per bug, so several problems add up quickly."),
], status="live")
