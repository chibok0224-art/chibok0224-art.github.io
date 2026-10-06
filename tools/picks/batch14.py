import add_picks

add_picks.CHECKED = "2026-10-06"


def r(user, name, best_for, title, rating, reviews, price, path, why, watch_out=""):
    return dict(user=user, name=name, best_for=best_for, title=title, rating=rating, reviews=reviews,
                level="Vetted Pro", price=price, url=path, why=why, watch_out=watch_out)


add_picks.put("graphics-design/character-modeling", [
    r("saswatakar135", "Saswat K", "Best overall for game-ready 3D characters", "I will create high quality 3D character models for games", "5.0", "635", "100",
      "/saswatakar135/do-3d-model-for-game-asset-product-model-backgraund-model",
      "A Vetted Pro with a perfect rating across 635 reviews who creates 3D character models for games, at a low starting price."),
    r("evandromiguel", "Evandro Miguel", "Best for collectible and animation-ready characters", "I will do a 3D character model for you", "5.0", "65", "1200",
      "/evandromiguel/do-a-3d-character-model-for-game-collectible-and-animation",
      "A Vetted Pro with a perfect rating who makes 3D character models for games, collectibles and animation.",
      "Premium pricing, starting near 1,200 dollars."),
    r("peanutsbee_lab", "Bre", "Best for 3D-printable figures and statues", "I will sculpt a 3D model, toy, action figure or statue", "4.9", "272", "100",
      "/peanutsbee_lab/do-3d-model-for-3d-printing-stl-file",
      "A Vetted Pro with 272 reviews who sculpts 3D characters, figures and statues for printing."),
    r("leombv", "Leomar B", "Best for sculpted characters for games or prints", "I will make a 3D character for you", "4.9", "139", "200",
      "/leombv/sculpt-your-piece-3d-for-game-or-prints-3d",
      "A Vetted Pro with 139 reviews who sculpts 3D characters for games or 3D printing."),
    r("devkumar3d", "Dev Kumar", "Best for turning 2D artwork into a 3D character", "I will create a 3D character model from 2D artwork", "4.9", "51", "150",
      "/devkumar3d/create-3d-character-model-from-2d-artwork",
      "A Vetted Pro who builds 3D character models from your 2D artwork."),
], status="live")

add_picks.put("business/e-commerce-management", [
    r("joelturcotte", "Joel", "Best for Amazon coaching and account guidance", "I will provide expert Amazon FBA coaching and 1-on-1 consultation", "5.0", "234", "100",
      "/joelturcotte/dropshipping-coach-and-help-you-grow-a-6-figure-brand",
      "A Vetted Pro with a perfect rating across 234 reviews who coaches sellers on Amazon FBA, at a low starting price."),
    r("razashah158", "FBA Venture", "Best for an Amazon virtual assistant team", "We will be your Amazon FBA virtual assistant", "5.0", "125", "100",
      "/razashah158/amazon-virtual-assistant-amazon-fba-amazon-fba-virtual-assistant-amazon-store-va",
      "A Vetted Pro agency with a perfect rating across 125 reviews that provides Amazon store virtual assistants."),
    r("mrcolossus", "Donovan", "Best for live one-to-one account help", "I will provide FBA Amazon 1-to-1 mentoring with live screen sharing", "5.0", "76", "135",
      "/mrcolossus/manage-your-amazon-fba-account",
      "A Vetted Pro with a perfect rating who mentors sellers on managing an Amazon FBA account."),
    r("ikhtiyorabdupat", "Tiyor", "Best for an account and PPC audit", "I will audit your Amazon FBA account, PPC campaigns and product listings", "5.0", "53", "145",
      "/ikhtiyorabdupat/audit-your-amazon-account-ppc-campaigns-product-listing-create-action-plan",
      "A Vetted Pro with a perfect rating who audits Amazon accounts, ads and listings and writes an action plan."),
    r("rameeztemuri", "Cosign Theta", "Best budget pick for an Amazon account manager", "We will be your Amazon account manager and virtual assistant", "4.9", "79", "100",
      "/rameeztemuri/be-your-amazon-fba-wholesale-expert-va",
      "A Vetted Pro agency with 79 reviews that manages Amazon wholesale accounts, at a low starting price."),
    r("ballymalik", "Malik Bilal", "Best for Amazon PPC and ads management", "I will be your Amazon PPC manager and run your ads campaigns", "4.8", "373", "350",
      "/ballymalik/amazon-va-amazon-fba-va-amazon-fba-virtual-assistant",
      "A Vetted Pro with 373 reviews who manages Amazon PPC and ads campaigns."),
], status="live")

add_picks.put("graphics-design/email-design", [
    r("marin_y", "Marin", "Best for a custom Mailchimp newsletter design", "I will create a custom Mailchimp email template design", "5.0", "301", "140",
      "/marin_y/create-a-custom-made-mailchimp-design-for-your-newsletter",
      "A Vetted Pro with a perfect rating across 301 reviews who designs custom Mailchimp newsletter templates."),
    r("nevlin18", "Nevlin", "Best for designed and coded HTML emails", "I will design and code an HTML email template", "4.9", "296", "150",
      "/nevlin18/design-and-code-your-html-marketing-email",
      "A Vetted Pro with 296 reviews who designs and codes HTML marketing emails."),
    r("massivework", "Sumit S.", "Best for responsive HTML email templates", "I will design responsive HTML email templates", "4.8", "63", "195",
      "/massivework/design-professional-responsive-html-email-templates",
      "A Vetted Pro with 63 reviews who designs responsive HTML email templates."),
], status="live")

add_picks.put("graphics-design/storyboards", [
    r("natmatt500", "Nat Matthew", "Best overall for animation, film and game storyboards", "I will storyboard your animation, film, game or commercial", "5.0", "119", "100",
      "/natmatt500/storyboard-your-animation-film-game-etc",
      "A Vetted Pro with a perfect rating across 119 reviews who storyboards animation, film, games and commercials."),
    r("storygeekdom84", "Steph Skiles", "Best for ad, film and video storyboards", "I will create storyboards for ads, films and video", "4.9", "554", "110",
      "/storygeekdom84/do-3-pages-of-storyboards",
      "A Vetted Pro with 554 reviews who creates storyboards for ads, films and videos."),
    r("artofgiuseppe", "Giuseppe Russo", "Best for digital storyboards and illustrations", "I will create professional digital storyboards for your project", "4.9", "91", "100",
      "/artofgiuseppe/create-stunning-images-from-your-ideas-storyboard-and-illustrations",
      "A Vetted Pro with 91 reviews who creates digital storyboards and illustrations."),
    r("claratejeda", "Clara Barbeito", "Best for commercials and animation storyboards", "I will draw storyboards for advertisements, film, animation and comics", "4.9", "60", "100",
      "/claratejeda/draw-storyboards-for-your-advertisement-film-production-animation",
      "A Vetted Pro with 60 reviews who draws storyboards for advertisements, film and animation."),
], status="live")

add_picks.put("video-animation/lottie-and-web-animation", [
    r("gadzstudio", "Agung Adhi", "Best for looping website animations", "I will create cartoon looping animation for a website background and more", "5.0", "99", "150",
      "/gadzstudio/create-animated-twitch-offline-brb-coming-soon",
      "A Vetted Pro with a perfect rating who creates looping animations for websites."),
    r("alan_art", "Alan", "Best for interactive Rive UI motion", "I will create interactive Rive UI animation and motion for your SaaS", "4.9", "97", "650",
      "/alan_art/make-a-custom-lottie-animation-for-you",
      "A Vetted Pro with 97 reviews who creates Lottie and Rive UI animations for products.",
      "Starts at 650 dollars."),
    r("motiongrapherr", "Gayane G.", "Best for Lottie and Rive animations", "I will create Lottie and Rive animations", "4.9", "53", "150",
      "/motiongrapherr/create-custom-animated-gifs",
      "A Vetted Pro who creates custom Lottie and Rive animations."),
    r("graphicslc", "Arigato Studio", "Best budget pick for a Lottie or GIF animation", "I will create a custom Lottie animation for your website or app", "4.8", "197", "100",
      "/graphicslc/create-a-lottie-or-gif-animation-for-your-website-or-app",
      "A Vetted Pro with 197 reviews who creates Lottie and GIF animations for websites and apps, at a low starting price."),
], status="live")
