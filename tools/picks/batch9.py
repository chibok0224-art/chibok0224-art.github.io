import add_picks

add_picks.CHECKED = "2026-10-04"


def r(user, name, best_for, title, rating, reviews, price, url, why, watch_out=""):
    return dict(user=user, name=name, best_for=best_for, title=title, rating=rating, reviews=reviews,
                level="Vetted Pro", price=price, url=url, why=why, watch_out=watch_out)


add_picks.put("graphics-design/album-cover-design", [
    r("o2brisson", "Aude", "Best overall for unique album artwork", "I will design a unique album artwork cover", "5.0", "270", "195",
      "/o2brisson/design-a-unique-album-artwork-cover",
      "A Vetted Pro with a perfect rating across 270 reviews who designs unique album artwork covers."),
    r("nibera", "Nibera Visuals", "Best for premium custom cover artwork", "I will create custom cover artwork for your music album", "5.0", "188", "1200",
      "/nibera/create-a-custom-cover-art-for-your-music-project",
      "A Vetted Pro with a perfect rating across 188 reviews who creates custom cover artwork for music projects.",
      "Premium pricing, starting around 1,200 dollars."),
    r("trippiesteff", "Steff H", "Best for psychedelic illustrated covers", "I will illustrate an epic psychedelic album cover artwork for you", "5.0", "134", "600",
      "/trippiesteff/do-you-an-album-artwork",
      "A Vetted Pro with a perfect rating who illustrates psychedelic album cover artwork.",
      "Starts at 600 dollars."),
    r("bjornbauerart", "Bjorn B", "Best for abstract painted covers", "I will design sophisticated album cover artwork with an abstract painting", "5.0", "123", "250",
      "/bjornbauerart/create-a-sophisticated-album-cover-with-an-abstract-painting",
      "A Vetted Pro with a perfect rating who designs album covers built around abstract paintings."),
    r("spncrrbns", "Spencer R", "Best budget pick for vintage cover art", "I will design your vintage album cover and single cover art, no AI", "4.9", "1000", "105",
      "/spncrrbns/craft-your-individual-music-artwork",
      "A Vetted Pro with more than a thousand reviews who designs vintage-style album and single cover art without AI, at a low starting price."),
    r("athena_eft", "Athina", "Best for eye-catching singles and albums", "I will design eye-catching album or single cover art", "4.9", "259", "185",
      "/athena_eft/design-unique-cover-art",
      "A Vetted Pro with 259 reviews who designs album and single cover art."),
], status="live")

add_picks.put("graphics-design/web-banners", [
    r("edharutyunyan", "Ed H.", "Best for ad banners on social and search", "I will design Meta ads, Instagram, Facebook and Google banners using Figma", "5.0", "140", "100",
      "/edharutyunyan/design-ad-banners-for-facebook-google-and-ig-that-sell",
      "A Vetted Pro with a perfect rating across 140 reviews who designs ad banners for Meta and Google in Figma, at a low starting price."),
    r("vladymyr_kytsia", "Vlad", "Best for brand covers and social banners", "I will design premium brand covers, banners and ads for LinkedIn, Facebook and more", "5.0", "66", "165",
      "/vladymyr_kytsia/create-unique-social-media-banners-posts-and-ads",
      "A Vetted Pro with a perfect rating who designs brand covers, banners and ads for social platforms."),
    r("appsposure", "Adshop", "Best for static or animated banner ads", "Our agency will design a static or animated banner ad", "4.9", "69", "100",
      "/appsposure/design-banner-ads-for-web-social-media-or-ppc-5e59",
      "A Vetted Pro agency with 69 reviews that designs static or animated banner ads for web, social media and PPC."),
    r("olegchuprina", "Oleg", "Best for HTML5 and premium static banners", "I will create social media ads and premium static ad designs", "4.8", "89", "150",
      "/olegchuprina/create-html5-banner-for-google-adwords",
      "A Vetted Pro with 89 reviews who creates HTML5 banners for Google ads and premium static ad designs."),
], status="live")

add_picks.put("graphics-design/icon-design", [
    r("denkravets", "Denys K", "Best for flat vector icon sets", "I will create unique flat vector icons for web, app or SaaS", "5.0", "96", "100",
      "/denkravets/design-custom-flat-vector-icon-set-for-website-and-app",
      "A Vetted Pro with a perfect rating who creates flat vector icon sets for websites, apps and SaaS, at a low starting price."),
    r("dreejc7", "Dee7 Studio", "Best agency for flat icons", "Our agency will design beautiful and unique flat icons", "5.0", "67", "450",
      "/dreejc7/design-a-flat-icon",
      "A Vetted Pro agency with a perfect rating that designs unique flat icons.",
      "Starts at 450 dollars."),
    r("spiner144", "Elijah Y.", "Best for illustrated icons and iconography", "I will create custom illustrated icons and iconography for brands", "4.9", "95", "120",
      "/spiner144/make-an-icon-illustration-for-web-and-mobile",
      "A Vetted Pro with 95 reviews who creates custom illustrated icons for web and mobile."),
    r("aldocersal", "Aldo", "Best for app icons", "I will design a custom app icon that stands out for iOS and Android", "4.9", "144", "120",
      "/aldocersal/design-you-a-creative-app-icon-that-stands-out",
      "A Vetted Pro with 144 reviews who designs custom app icons for iOS and Android."),
    r("syahrirallil", "Andi S", "Most reviewed for simple icon sets", "I will design a simple modern custom icon set", "4.8", "855", "100",
      "/syahrirallil/design-simple-icon-set-for-web-and-app-in-12-hours",
      "A Vetted Pro with 855 reviews who designs simple modern icon sets for web and apps, at a low starting price."),
    r("summarydesign", "Chang", "Best for hand-drawn icons", "I will create unique hand-drawn illustrated icons for digital and brand use", "4.8", "73", "100",
      "/summarydesign/draw-a-beautiful-icon",
      "A Vetted Pro with 73 reviews who creates hand-drawn illustrated icons."),
], status="live")

add_picks.put("graphics-design/business-cards-and-stationery", [
    r("perocha", "Pedro Rocha", "Best overall for an outstanding business card", "I will design an outstanding business card", "5.0", "236", "120",
      "/perocha/design-an-outstanding-business-card",
      "A Vetted Pro with a perfect rating across 236 reviews who designs business cards."),
    r("alena_chili", "Alena Ch.", "Best for minimalist stationery", "I will design minimalist stationery and business cards", "5.0", "70", "100",
      "/alena_chili/design-minimalistic-business-card",
      "A Vetted Pro with a perfect rating who designs minimalist stationery and business cards, at a low starting price."),
    r("architect_g", "Gizem", "Best for minimal, elegant cards in a day", "I will design minimal and elegant business cards", "4.9", "189", "100",
      "/architect_g/design-minimal-and-elegant-business-cards-in-a-day",
      "A Vetted Pro with 189 reviews who designs minimal and elegant business cards, with a quick turnaround."),
], status="live")

add_picks.put("graphics-design/poster-design", [
    r("athena_eft", "Athina", "Best for artistic event and party posters", "I will design artistic movie, event or party posters", "5.0", "61", "190",
      "/athena_eft/design-modern-artistic-poster",
      "A Vetted Pro with a perfect rating who designs artistic movie, event and party posters.",
      "Fewer reviews than others on this list, at 61."),
    r("armstranger", "Armstranger", "Best for illustrated concert and movie posters", "I will illustrate movie posters, concerts and event posters", "5.0", "77", "150",
      "/armstranger/design-professionally-event-poster-movie-poster-band-show",
      "A Vetted Pro with a perfect rating who illustrates movie, concert and event posters."),
    r("davidcolonfilm", "David", "Most reviewed for movie posters", "I will help you design your movie poster", "4.9", "226", "240",
      "/davidcolonfilm/help-you-design-your-movie-poster",
      "A Vetted Pro with 226 reviews who designs movie posters."),
    r("eveeelin", "Evelin", "Best for minimalist event posters", "I will create minimalistic event poster or flyer designs", "4.8", "147", "150",
      "/eveeelin/create-minimalistic-event-poster-or-flyer-designs",
      "A Vetted Pro with 147 reviews who creates minimalist event posters and flyers."),
    r("flppvdd", "Daria Filippova", "Best for illustrated event posters", "I will illustrate poster design for events, covers and movies", "4.8", "71", "250",
      "/flppvdd/do-illustrated-poster-design-for-event",
      "A Vetted Pro with 71 reviews who illustrates poster designs for events, covers and films.",
      "Starts at 250 dollars."),
], status="live")

add_picks.put("graphics-design/brochure-design", [
    r("frannnz", "Fran", "Best for catalogs and lookbooks", "I will design a product catalog, brochure or lookbook", "5.0", "358", "380",
      "/frannnz/design-your-catalog-or-magazine",
      "A Vetted Pro with a perfect rating across 358 reviews who designs product catalogs, brochures and lookbooks.",
      "Starts at 380 dollars."),
    r("vladymyr_kytsia", "Vlad", "Best for corporate bifold and trifold brochures", "I will design a premium corporate trifold or bifold brochure, flyer or booklet", "5.0", "96", "210",
      "/vladymyr_kytsia/design-business-brochure-proposal-booklet-flyer",
      "A Vetted Pro with a perfect rating who designs corporate trifold and bifold brochures, flyers and booklets."),
    r("victorysamonova", "Victoria", "Best for company profiles and booklets", "I will design a premium brochure, company profile or booklet", "5.0", "93", "350",
      "/victorysamonova/design-clean-and-appealing-flyer",
      "A Vetted Pro with a perfect rating who designs premium brochures, company profiles and booklets."),
    r("designer119", "Priyantha D", "Most reviewed for corporate brochures", "I will design a premium corporate brochure", "4.9", "1000", "225",
      "/designer119/amazing-corporate-brochure-design",
      "A Vetted Pro with more than a thousand reviews who designs premium corporate brochures."),
    r("sanjamicro", "Sanya D.", "Best for brochures and catalogs", "I will design a professional brochure or catalog", "4.9", "764", "250",
      "/sanjamicro/design-a-brochure-catalog-flyer-poster-or-anything-you-need",
      "A Vetted Pro with 764 reviews who designs professional brochures and catalogs."),
    r("tasouph", "Pavel H", "Best for print or digital brochures", "I will design superb print or digital brochures", "4.9", "151", "300",
      "/tasouph/design-perfect-print-or-digital-brochure",
      "A Vetted Pro with 151 reviews who designs print and digital brochures."),
], status="live")

add_picks.put("online-marketing/local-seo", [
    r("sovosowravdatta", "Sowrav Datta", "Best for Google Business and map ranking", "I will dominate local SEO, Google Business and local 3-pack ranking", "5.0", "75", "220",
      "/sovosowravdatta/do-the-local-seo-service-for-google-and-map-ranking",
      "A Vetted Pro with a perfect rating who does local SEO work aimed at Google Business and map rankings."),
    r("onlinedoctors", "Eyal", "Best for local traffic and leads", "I will rock your local SEO traffic and leads", "5.0", "66", "295",
      "/onlinedoctors/rock-your-local-seo-traffic-and-leads",
      "A Vetted Pro with a perfect rating who offers local SEO aimed at traffic and leads.",
      "Starts at 295 dollars."),
    r("miranda_davis", "Miranda", "Most reviewed for local SEO and GMB", "I will skyrocket your local SEO, Google Business and GMB ranking", "4.9", "493", "245",
      "/miranda_davis/do-local-seo-google-business-gmb-ranking",
      "A Vetted Pro with 493 reviews who does local SEO and Google Business Profile optimization."),
    r("atharrasool696", "Athar R", "Best budget pick for a Google Business profile", "I will optimize your Google Maps business profile for local SEO", "4.9", "132", "100",
      "/atharrasool696/setup-and-optimize-google-my-business-profile",
      "A Vetted Pro with 132 reviews who sets up and optimizes Google Business profiles for local SEO, at a low starting price."),
    r("gettclicks", "Alastair D.", "Best for local SEO management", "I will do local SEO management for your local business", "4.8", "144", "100",
      "/gettclicks/transform-local-seo-for-your-business",
      "A Vetted Pro with 144 reviews who manages local SEO for local businesses, at a low starting price."),
], status="live")

add_picks.put("music-audio/singers-and-vocalists", [
    r("seankilleen_", "Sean Killeen", "Most reviewed male pop and EDM singer", "I will be your professional EDM and pop male singer and songwriter", "5.0", "1000", "100",
      "/seankilleen_/be-your-male-singer-and-songwriter",
      "A Vetted Pro with a perfect rating and more than a thousand reviews who sings and writes for pop and EDM tracks, at a low starting price."),
    r("madishu", "Madishu", "Best for a female vocalist and songwriter", "I will be your female vocalist and singer-songwriter", "5.0", "729", "150",
      "/madishu/be-your-female-vocalist-singer-songwriter",
      "A Vetted Pro with a perfect rating across 729 reviews who works as a female vocalist and singer-songwriter."),
    r("kelophone", "Ykati", "Best for female pop and EDM vocals", "I will be your female human vocalist for pop and EDM music", "5.0", "520", "250",
      "/kelophone/be-your-professional-singer",
      "A Vetted Pro with a perfect rating across 520 reviews who records female human vocals for pop and EDM.",
      "Starts at 250 dollars."),
    r("iammissgeist", "Rebecca S", "Best for pop, rock, EDM and country vocals", "I will be your pro singer and songwriter for pop, rock, EDM and country", "5.0", "336", "150",
      "/iammissgeist/be-your-new-favorite-session-vocalist",
      "A Vetted Pro with a perfect rating across 336 reviews who works as a session vocalist and songwriter across several genres."),
    r("hirejoebills", "Joe Bills", "Best for male vocals without AI", "I will be your male vocalist and songwriter, without AI", "5.0", "332", "195",
      "/hirejoebills/record-professional-male-vocals-for-you",
      "A Vetted Pro with a perfect rating across 332 reviews who records male vocals and songwriting without AI."),
    r("natalianekare", "Natalia Nekare", "Best for powerful rock vocals", "I will be the best rock professional female singer for you", "5.0", "298", "100",
      "/natalianekare/sing-the-most-powerful-vocals-you-can-imagine",
      "A Vetted Pro with a perfect rating across 298 reviews who sings rock vocals as a female singer, at a low starting price."),
], status="live")
