import add_picks

add_picks.CHECKED = "2026-10-04"


def r(user, name, best_for, title, rating, reviews, price, url, why, watch_out=""):
    return dict(user=user, name=name, best_for=best_for, title=title, rating=rating, reviews=reviews,
                level="Vetted Pro", price=price, url=url, why=why, watch_out=watch_out)


add_picks.put("writing-translation/proofreading-and-editing", [
    r("arianelaurent", "Ariane L. Smith", "Best for business documents and white papers", "I will professionally proofread and edit your business document", "5.0", "99", "100",
      "/arianelaurent/professionally-edit-your-white-paper",
      "A Vetted Pro with a perfect rating who proofreads and edits business documents, including white papers."),
    r("emma_moylan", "Emma Moylan", "Best for self-published books", "I will copy edit and proofread your book, ebook or novel", "5.0", "415", "100",
      "/emma_moylan/proofread-self-published-book-manuscript-proof-read-errors-fix-grammar-spelling",
      "A Vetted Pro with a perfect rating across 415 reviews who copy edits and proofreads books, ebooks and novels for grammar and spelling errors."),
    r("ccutting", "Chrissy Cutting", "Most reviewed for documents, reports and articles", "I will professionally proofread and edit your document, report or article", "4.9", "1000", "100",
      "/ccutting/professionally-proofread-and-edit-1000-words",
      "A Vetted Pro with more than a thousand reviews who proofreads and edits documents, reports and articles, with pricing built around word count."),
    r("kevin100percent", "Kevin O", "Best for fast document editing", "I will proofread and edit your document right now", "4.9", "806", "100",
      "/kevin100percent/proofread-and-edit-your-work-to-100-percent-satisfaction",
      "A Vetted Pro with more than 800 reviews who offers quick proofreading and editing of documents."),
    r("jillianrene", "Jill S.", "Best for proofreading and copy editing together", "I will professionally proofread and copy edit your documents", "4.9", "484", "100",
      "/jillianrene/professionally-proofread-and-copy-edit-your-documents",
      "A Vetted Pro with 484 reviews who combines proofreading and copy editing for documents."),
    r("mongiardo", "Victoria M", "Best for rewriting weak text as well", "I will proofread, edit and rewrite any text as your copy editor", "4.9", "269", "100",
      "/mongiardo/edit-and-proofread-your-writing",
      "A Vetted Pro with 269 reviews who proofreads, edits and rewrites text as a copy editor."),
], status="live")

add_picks.put("writing-translation/sales-copy", [
    r("naimal_masood6", "Naimal", "Best budget pick with a top rating", "I will write sales copy for your sales page, landing page and website", "5.0", "438", "75",
      "/naimal_masood6/craft-high-converting-copywriting-and-sales-copy",
      "A Vetted Pro with a perfect rating across 438 reviews who writes sales copy for sales pages, landing pages and websites, at the lowest starting price in this list."),
    r("francescatrdd", "Francesca T.", "Best for sales funnels and landing pages", "I will do sales funnel and landing page copywriting that converts", "5.0", "169", "445",
      "/francescatrdd/do-marketing-funnels-copywriting-with-email-ads-sales-page",
      "A Vetted Pro with a perfect rating who writes whole marketing funnels, covering email, ads and sales pages.",
      "Starts at 445 dollars."),
    r("morena2003", "Emily", "Best for a single persuasive sales page", "I will deliver sales copywriting that converts", "5.0", "68", "100",
      "/morena2003/write-powerful-sales-copy-for-you",
      "A Vetted Pro with a perfect rating who writes sales copy aimed at conversion."),
    r("sarahvause", "Sarah V", "Best for bespoke sales copy", "I will write professional sales copy", "5.0", "59", "100",
      "/sarahvause/deliver-high-converting-bespoke-sales-copy",
      "A Vetted Pro with a perfect rating who writes bespoke sales copy for businesses.",
      "Fewer reviews than others on this list, at 59."),
    r("mayasayvanova", "Maya S", "Best for copy across a full funnel", "I will do copywriting for sales funnels, landing pages, ads, emails and video scripts", "4.9", "130", "165",
      "/mayasayvanova/write-start-to-end-sales-funnel",
      "A Vetted Pro with 130 reviews who covers the funnel from landing page and ads to emails and video scripts."),
    r("jakeeck", "Jacob", "Most reviewed for sales pages and funnels", "I will write sales copy for a sales page, funnel or landing page", "4.8", "658", "85",
      "/jakeeck/provide-professional-sales-copy-landing-pages-sales-funnels-and-ads",
      "A Vetted Pro with 658 reviews who writes sales pages, funnels, landing pages and ads, with a low starting price."),
], status="live")

add_picks.put("photography/product-photographers", [
    r("seanviens", "Sean Audet", "Best overall for brand product photography", "I will produce beautiful product photography for your brand", "5.0", "156", "250",
      "/seanviens/produce-beautiful-product-photography-for-your-brand-6cb6",
      "A Vetted Pro with a perfect rating across 156 reviews who produces product photography for brands.",
      "Starts at 250 dollars, above most sellers in this list."),
    r("lindaze", "Linda E", "Best for creative product shots", "I will shoot all kinds of product photography", "5.0", "48", "150",
      "/lindaze/shoot-creative-product-photography",
      "A Vetted Pro with a perfect rating who shoots a wide range of creative product photography.",
      "Fewer reviews than others on this list, at 48."),
    r("loui8961", "Jose Luis", "Best budget pick for Amazon listings", "I will shoot product photography for Amazon", "5.0", "44", "100",
      "/loui8961/shoot-high-quality-amazon-product-photography",
      "A Vetted Pro with a perfect rating who shoots product photography for Amazon listings, at a low starting price.",
      "Fewer reviews than others on this list, at 44."),
    r("aslito", "Avec Studio", "Best for lifestyle and e-commerce shoots", "I will shoot premium lifestyle and ecommerce product photography", "4.9", "109", "140",
      "/aslito/lifestyle-and-product-photography",
      "A Vetted Pro with 109 reviews who shoots lifestyle and e-commerce product photography."),
    r("jeffbrianphoto", "Jeffrey Brian", "Best for white-background product photos", "I will create professional white-background product photography", "4.9", "337", "100",
      "/jeffbrianphoto/produce-professional-white-background-product-photography",
      "A Vetted Pro with 337 reviews who produces product photography on white backgrounds for listings."),
    r("jesse468099", "Jesse J", "Best for product shots with models", "I will shoot Amazon product photography with models", "4.9", "163", "100",
      "/jesse468099/create-professional-product-photography-in-my-studio",
      "A Vetted Pro with 163 reviews whose listing includes product photography with models, shot in the seller's studio.",
      "The seller shoots in their own studio, so ask how your products should reach the studio."),
], status="live")

add_picks.put("music-audio/music-producers", [
    r("orishlez", "Ori Shlez", "Most reviewed, high-end production", "I will be your high end music producer", "5.0", "1000", "175",
      "/orishlez/record-a-professional-keyboard-track-piano-or-rhodes-or-hammond-for-any-3-minutes-song-in-any-key",
      "A Vetted Pro with a perfect rating and more than a thousand reviews who records professional keyboard tracks for songs in any key.",
      "The listing shown is for a keyboard track, so check that the package matches your project."),
    r("jass1410", "James S", "Best for taking a demo to a finished track", "I will produce, record and mix your song", "5.0", "828", "350",
      "/jass1410/take-your-song-from-a-worktape-to-a-fully-produced-track",
      "A Vetted Pro with a perfect rating across 828 reviews who turns a rough work tape into a fully produced and mixed track.",
      "Starts at 350 dollars."),
    r("dariomarcello", "Dario Marcello", "Best budget pick for pop, rock and blues", "I will be your pop, rock, country and blues music producer", "5.0", "596", "100",
      "/dariomarcello/produce-blues-funk-rnb-tracks-for-you",
      "A Vetted Pro with a perfect rating across 596 reviews who produces pop, rock, country and blues tracks, with a low starting price."),
    r("dyhard", "Ian Hardwick", "Best for an original one-off song", "I will be your pro songwriter and music producer", "5.0", "376", "100",
      "/dyhard/write-and-record-a-personalised-original-one-off-song-for-you",
      "A Vetted Pro with a perfect rating across 376 reviews who writes and records personalised original songs."),
    r("elguapomusica", "Juan And Joni", "Best for live-instrument productions", "I will ghost produce original music using live instruments", "5.0", "303", "250",
      "/elguapomusica/produce-your-original-music",
      "A Vetted Pro duo with a perfect rating who produce original music using live instruments."),
    r("davidg_music", "David G", "Best for full song arranging", "I will be your music producer and song arranger", "5.0", "190", "300",
      "/davidg_music/fully-arrange-and-produce-your-song",
      "A Vetted Pro with a perfect rating who fully arranges and produces songs."),
], status="live")
