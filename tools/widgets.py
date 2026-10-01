"""Make Fiverr Gig Ads Widget embeds for guides and save them to content/widgets.json.

The widget is Fiverr's own ad unit from the affiliate dashboard (Marketing Tools > Gig Ads Widget).
Its builder turns settings into an encrypted id by POSTing to /nga_builder/encode_settings;
we call the same endpoint with a search keyword per guide. Fiverr picks and serves the gigs.

Fiverr answers 403 to calls from outside a signed-in browser, so main() only works from such a
session. In practice the ids are made in the signed-in builder tab (same request, a few seconds
apart) and pasted into content/widgets.json; KEYWORDS below is the keyword list used for that.

    python tools/widgets.py            # add widgets for guides that have none
    python tools/widgets.py --redo     # rebuild every widget (e.g. after changing keywords)
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
AFFILIATE_ID = json.loads((CONTENT / "site.json").read_text(encoding="utf-8-sig"))["affiliate"]["bta"]
ENDPOINT = "https://www.fiverr.com/nga_builder/encode_settings"

# Search keyword per guide slug when the service name alone is a poor Fiverr search.
KEYWORDS = {
    "search-engine-optimization-seo": "seo", "search-engine-marketing-sem": "google ads",
    "paid-social-media": "facebook ads", "ugc-videos": "ugc video", "thumbnails-design": "youtube thumbnail",
    "mixing-and-mastering": "mixing mastering", "video-editing": "youtube video editing",
    "business-plans": "business plan", "e-commerce-seo": "ecommerce seo",
    "troubleshooting-and-improvements": "website bug fix", "development-and-mvp": "mvp development",
    "support-and-it": "it support", "qa-and-review": "software testing", "apis-and-integrations": "api integration",
    "music-producers": "music producer", "singers-and-vocalists": "singer vocals", "jingles-and-intros": "jingle",
    "custom-songs": "custom song", "composers": "music composer", "book-and-ebook-writing": "ghostwriter book",
    "book-and-ebook-marketing": "book marketing", "architecture-and-interior-design": "interior design",
    "industrial-and-product-design": "product design", "t-shirts-and-merchandise": "tshirt design",
    "childrens-book-illustration": "childrens book illustration",  # ' and - make the builder return no id
    "business-cards-and-stationery": "business card design", "packaging-and-label-design": "packaging design",
    "crowdfunding": "crowdfunding campaign", "graphics-for-streamers": "twitch overlay",
    "intro-and-outro-videos": "youtube intro", "app-and-website-previews": "app preview video",
    "e-commerce-product-videos": "product video", "elearning-video-production": "elearning video",
    "real-estate-promos": "real estate video", "real-estate-photographers": "real estate photo editing",
    "food-photographers": "food photography", "product-photographers": "product photography",
    "conversion-rate-optimization-cro": "conversion rate optimization", "linkedin-profiles": "linkedin profile",
    "articles-and-blog-posts": "blog post writing", "press-releases": "press release",
    "case-studies": "case study writing", "email-copy": "email copywriting",
    "social-media-videos": "short form video editing", "video-repurposing": "repurpose video clips",
    "spokesperson-videos": "spokesperson video", "screencasting-videos": "screen recording tutorial",
    "website-content": "website content writing", "proofreading-and-editing": "proofreading",
    "lead-generation": "b2b lead generation", "data-visualization": "dashboard data visualization",
    "image-editing": "photo editing", "website-maintenance": "wordpress maintenance",
    "plugins-development": "wordpress plugin development", "scripting": "python automation script",
    "full-stack-web-apps": "full stack web app", "desktop-applications": "desktop application",
    "mobile-app-maintenance": "mobile app bug fix", "user-testing": "user testing",
    "logo-animation": "logo animation", "subtitles-and-captions": "subtitles",
    "audio-editing": "audio editing", "sound-design": "sound effects", "beat-making": "beat maker",
    "session-musicians": "session musician", "audiobook-production": "audiobook narrator",
    "podcast-production": "podcast editing", "podcast-cover-art": "podcast cover art",
    "cross-platform-apps": "flutter app development", "custom-websites": "custom website",
    "data-scraping": "web scraping", "dashboards": "power bi dashboard", "ugc-ads": "ugc ads",
    "slideshow-videos": "slideshow video", "databases": "database design", "video-seo": "youtube seo",
    "text-message-marketing": "sms marketing", "visual-effects": "vfx", "animated-gifs": "animated gif",
    "lottie-and-web-animation": "lottie animation", "business-names-and-slogans": "business name",
    "cover-letters": "cover letter", "storyboards": "storyboard",
    "portraits-and-caricatures": "caricature", "pattern-design": "seamless pattern",
    "speechwriting": "speech writing", "beta-reading": "beta reader", "crowdfunding-videos": "kickstarter video",
    "remixing": "remix",
    "fonts-and-typography": "custom font", "trade-booth-design": "trade show booth design",
    "car-wraps": "car wrap design", "character-modeling": "3d character modeling",
    "live-action-explainers": "live action explainer video", "text-animation": "kinetic typography",
    "animation-for-kids": "kids animation", "audio-ads-production": "radio ad",
    "audio-logo-and-sonic-branding": "audio logo", "creative-writing": "short story writing",
    "podcast-writing": "podcast script", "research-and-summaries": "research summary",
    "brand-voice-and-tone": "brand voice", "elearning-content-development": "elearning course content",
    "photo-preset-creation": "lightroom presets", "convert-files": "convert pdf to word", "dj-drops-and-tags": "dj drops",
}


def keyword_for(slug, name):
    if slug in KEYWORDS:
        return KEYWORDS[slug]
    name = re.sub(r"\s*\(.*?\)", "", name).replace("&", "and")
    return name.lower().strip()


def encode(query):
    body = {"widgetData": {
        "affiliateId": AFFILIATE_ID, "brand": "fiverrmarketplace", "utmCampaign": "gig_ads",
        "widgetLocalization": "en", "widgetMoreButton": "Explore more services",
        "widgetTitle": "Recommended services", "mode": "random_gigs", "version": "2", "domain": "",
        "gigFilters": {"minPrice": None, "maxPrice": None, "category": None, "subCategory": None,
                       "searchQuery": query}}}
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())["widgetData"]
    return (f"https://www.fiverr.com/gig_widgets?id={data}&affiliate_id={AFFILIATE_ID}"
            "&strip_google_tagmanager=true")


def main():
    redo = "--redo" in sys.argv
    path = CONTENT / "widgets.json"
    widgets = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    names = {}
    for f in (CONTENT / "taxonomy").glob("*.json"):
        top = json.loads(f.read_text(encoding="utf-8-sig"))
        for g in top["groups"]:
            for s in g["subs"]:
                names[f'{top["slug"]}/{s["slug"]}'] = (s["slug"], s["name"])
    guides = sorted(f'{p.parent.parent.name}/{p.parent.name}' for p in (CONTENT / "pages").glob("*/*/page.json"))
    made = 0
    for key in guides:
        if key in widgets and not redo:
            continue
        slug, name = names[key]
        kw = keyword_for(slug, name)
        try:
            widgets[key] = {"keyword": kw, "src": encode(kw)}
            made += 1
            print(f"ok   {key}  [{kw}]")
        except Exception as e:  # keep going; report at the end
            print(f"FAIL {key}  [{kw}]  {e}")
        time.sleep(1.5)
    path.write_text(json.dumps(widgets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"made {made}, total {len([k for k in widgets if not k.startswith('_')])}")


if __name__ == "__main__":
    main()
