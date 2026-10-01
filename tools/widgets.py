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
    "ai-applications": "ai app development",
    "ai-integration": "ai integration",
    "ai-model-fine-tuning": "llm fine tuning",
    "midjourney-artists": "midjourney",
    "ai-music-videos": "ai music video",
    "ai-video-art": "ai video",
    "ai-spokesperson-videos": "ai avatar video",
    "custom-prompt-writing": "prompt engineering",
    "text-to-speech": "text to speech",
    "custom-ai-voices": "ai voice clone",
    "machine-learning": "machine learning model",
    "computer-vision": "computer vision",
    "nlp": "nlp",
    "data-engineering": "data engineering",
    "data-processing": "data processing",
    "data-tagging-and-annotation": "data annotation",
    "data-enrichment": "data enrichment",
    "speech-recognition": "speech to text",
    "ai-strategy": "ai consulting",
    "ai-lessons": "ai tutor",
    "project-management": "project manager",
    "e-commerce-management": "ecommerce store manager",
    "event-management": "event planner",
    "product-management": "product manager",
    "sales": "sales representative",
    "customer-experience-management-cxm": "customer experience",
    "presentations": "pitch deck",
    "supply-chain-management": "supply chain",
    "game-concept-design": "game design document",
    "business-consulting": "business consultant",
    "generative-engine-optimization-geo": "ai search optimization",
    "online-communities": "discord community manager",
    "email-automations": "klaviyo email flows",
    "affiliate-marketing": "affiliate program management",
    "display-advertising": "display ads",
    "digital-marketing-strategy": "digital marketing strategy",
    "ugc-strategy": "ugc strategy",
    "social-commerce": "tiktok shop",
    "marketing-concepts-and-ideation": "marketing campaign ideas",
    "pr-strategy": "pr strategy",
    "online-tutoring": "online tutor",
    "language-lessons": "language teacher",
    "online-music-lessons": "guitar lessons",
    "online-coding-lessons": "coding tutor",
    "arts-and-crafts": "handmade crafts",
    "recipe-creation": "recipe development",
    "puzzle-and-game-creation": "custom crossword puzzle",
    "game-testing-and-feedback": "game testing",
    "embroidery-digitizing": "embroidery digitizing",
    "greeting-cards-and-videos": "greeting card design",
    "videographers": "videographer",
    "animation-for-streamers": "stream alerts animation",
    "virtual-and-streaming-avatars": "vtuber model",
    "article-to-video": "article to video",
    "rigging": "character rigging",
    "portrait-photographers": "portrait retouching",
    "event-photographers": "event photography",
    "drone-photographers": "drone video",
    "fashion-design": "fashion tech pack",
    "jewelry-design": "jewelry cad design",
    "art-direction": "art director",
    "landscape-design": "landscape design",
    "lighting-design": "lighting design",
    "3d-architecture": "3d architectural rendering",
    "3d-industrial-design": "3d product rendering",
    "3d-fashion-and-garment": "clo3d",
    "ai-generated-character-design": "ai character design",
    "design-consultation": "design feedback",
    "building-information-modeling": "revit bim",
    "music-transcription": "sheet music transcription",
    "dj-mixing": "dj mix",
    "custom-patches-and-samples": "sample pack",
    "audio-plugin-development": "vst plugin development",
    "music-and-audio-consultation": "music feedback",
    "video-art": "video art",
    "video-templates-editing": "video template editing",
    "filmed-video-production": "video production",
    "meditation-videos": "meditation video",
    "video-consultation": "youtube channel review",
    "content-strategy": "content strategy",
    "ai-content-editing": "humanize ai content",
    "writing-advice": "writing coach",
    "interpretation": "interpreter",
    "handwriting": "handwritten letters",
    "godaddy": "godaddy website",
    "consultation-and-training": "tech consultation",
    "development-for-streamers": "twitch bot",
    "electronics-engineering": "pcb design",
    "blockchain-development-and-solutions": "smart contract development",
    "data-typing": "typing job",
    "data-formatting": "excel formatting",
    "data-governance-and-protection": "data protection",
    "deep-learning": "deep learning",
    "generative-models": "generative ai model",
    "tabletop-games": "board game design",
    "game-coaching": "game coaching",
    "esports-management-and-strategy": "esports team manager",
    "ingame-creation": "minecraft build",
    "game-recordings-and-guides": "gameplay recording",
    "cosplay-creation": "cosplay costume",
    "traveling": "travel itinerary",
    "collectibles": "collectibles",
    "modeling-and-acting": "model for product photos",
    "styling-and-beauty": "personal stylist",
    "trend-forecasting": "trend report",
    "family-and-genealogy": "genealogy research",
    "lifestyle-and-fashion-photographers": "lifestyle photography",
    "scenic-photographers": "landscape photography",
    "photography-advice": "photography mentor",
    "social-media-strategy": "social media strategy",
    "influencers-strategy": "influencer marketing strategy",
    "video-marketing-strategy": "video marketing strategy",
    "sem-strategy": "google ads audit",
    "sales-strategy": "sales strategy",
    "software-development-consulting": "software consultant",
    "mobile-apps-consulting": "app development consultation",
    "cybersecurity-consulting": "cybersecurity consultant",
    "game-development-consulting": "game development consultation",
    "data-visualization-consulting": "dashboard review",
    "databases-consulting": "database consultant",
    "data-processing-consulting": "data workflow automation",
    "market-research-consulting": "market research consultant",
    "customer-care-consulting": "customer support consultant",
    "travel-advice": "travel advice",
    "software-management": "crm setup",
    "sustainability-consulting": "sustainability consultant",
    "conscious-branding-and-marketing": "purpose driven branding",
    "deployments-and-devops": "deploy website",
    "blockchain-security-and-auditing": "smart contract audit",
    "stable-diffusion-artists": "stable diffusion",
    "career-counseling": "career coach",
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
