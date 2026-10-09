import add_picks

add_picks.CHECKED = "2026-10-09"


def r(user, name, best_for, title, rating, reviews, price, path, why, watch_out=""):
    return dict(user=user, name=name, best_for=best_for, title=title, rating=rating, reviews=reviews,
                level="Vetted Pro", price=price, url=path, why=why, watch_out=watch_out)


# Only the first gig page was opened (bot checks); the others use listing data from 2026-10-09.
add_picks.put("writing-translation/technical-writing", [
    r("filipdevaere", "Filip De Vaere", "Best overall for product user manuals",
      "I will design ce compliant user manual for amazon or bol com with safety chapter", "5.0", "107", "160",
      "/filipdevaere/design-or-redesign-your-user-manual-for-bol-com-in-dutch",
      "A Vetted Pro with a perfect rating across 107 reviews who writes and designs user manuals for products sold in Europe, including a safety chapter. Packages cover manuals of up to 6,000 to 10,000 words with proofreading.",
      "Extra languages cost more, and each package includes one revision."),
    r("sohaibqaiser", "Sohaib Qaiser", "Best for a product knowledge base",
      "I will create a knowledge base that works for humans and ai", "5.0", "61", "625",
      "/sohaibqaiser/create-a-knowledge-base-for-your-product",
      "A Vetted Pro with a perfect rating across 61 reviews who builds product knowledge bases, the help articles customers read before contacting support.",
      "Higher starting price than single documents."),
    r("documentspider", "Penelope H", "Best budget pick for software user guides",
      "I will create professional user guides for your software", "5.0", "12", "75",
      "/documentspider/develop-documentation-and-how-to-guides-for-your-software",
      "A Vetted Pro with a perfect rating who writes user guides and how-to documentation for software, with the lowest starting price here.",
      "Only 12 reviews so far."),
    r("narsildev", "Damaso Sanoja", "Best for technical articles on AI, DevOps and security",
      "I will write expert ai, devops, mlops, k8s, platform engineering, and security content", "5.0", "14", "200",
      "/narsildev/write-your-technical-content-on-devops-cyber-security-ai-and-more",
      "A Vetted Pro with a perfect rating who writes in-depth technical content for engineering audiences, covering AI, DevOps, cloud platforms and security.",
      "Only 14 reviews; best suited to technical readers rather than end users."),
    r("bonemakes", "Andrew B", "Best for software tutorials and help docs",
      "I will write software documentation, user guides, and tutorials", "5.0", "6", "450",
      "/bonemakes/write-software-documentation-user-guides-or-tutorials",
      "A Vetted Pro with a perfect rating who writes software documentation, user guides and step-by-step tutorials.",
      "Only 6 reviews so far."),
], status="live")
