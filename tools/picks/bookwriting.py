import add_picks

add_picks.CHECKED = "2026-10-09"


def r(user, name, best_for, title, rating, reviews, price, path, why, watch_out=""):
    return dict(user=user, name=name, best_for=best_for, title=title, rating=rating, reviews=reviews,
                level="Vetted Pro", price=price, url=path, why=why, watch_out=watch_out)


add_picks.put("writing-translation/book-and-ebook-writing", [
    r("tme2012", "Nick G", "Best overall for fiction or nonfiction books",
      "I will ghostwrite a book or ebook of any length for you", "4.9", "305", "925",
      "/tme2012/write-a-book-or-ebook-for-you-up-to-10k-words-long",
      "A Vetted Pro with 305 reviews who ghostwrites fiction and nonfiction on any subject. Packages are priced by length, from up to 5,000 words in seven days to up to 20,000 words in 21 days, with topic research and references included.",
      "Each package includes only one round of revisions."),
    r("rickflix", "Rich S", "Best for writing a novel chapter by chapter",
      "I will ghostwrite your novel chapter by chapter", "5.0", "91", "300",
      "/rickflix/ghostwrite-your-book-chapter-by-chapter",
      "A Vetted Pro with a perfect rating across 91 reviews who writes novels one segment at a time, so you can review each part before paying for the next. Packages run from a single chapter of up to 1,500 words to a 5,000-word section, each with two revisions.",
      "A full novel adds up over many orders, and each chapter takes about two weeks."),
    r("carlo_be", "ElitePublishing", "Best for short nonfiction ebooks ready to publish",
      "Our agency will be your nonfiction kindle book ghostwriter", "4.9", "59", "320",
      "/carlo_be/be-your-nonfiction-ebook-ghostwriter",
      "A Vetted Pro agency with 59 reviews that writes nonfiction ebooks delivered already formatted. Every package includes an outline, topic research, a book blurb, ebook formatting and five revisions.",
      "Best suited to shorter practical books; the top package goes up to 25,000 words."),
    r("sethapmiller", "Seth Miller", "Best for children's picture books",
      "I will write an engaging and humorous book for children", "5.0", "175", "120",
      "/sethapmiller/write-an-engaging-and-funny-book-for-children",
      "A Vetted Pro with a perfect rating across 175 reviews who writes funny children's stories. Packages cover picture book text, early readers and chapter books for ages up to nine, each with two revisions.",
      "Text only: illustrations need a separate illustrator."),
    r("briannashrum", "Bri", "Best for memoirs and life stories",
      "I will write your memoir, autobiography, or nonfiction book", "4.8", "54", "275",
      "/briannashrum/write-your-memoir-or-autobiography",
      "A Vetted Pro with 54 reviews who writes memoirs and nonfiction. The entry package is a consultation with an outline and a sample introduction, so you can test the fit before the full memoir, which includes in-depth interviews.",
      "The full memoir package costs far more than the entry price and takes about 90 days."),
    r("victor_serrano", "Victor Serrano", "Best for fantasy and science fiction novels",
      "I will ghostwrite a fantasy or science fiction ebook", "5.0", "106", "2500",
      "/victor_serrano/write-an-exciting-story-for-you",
      "A Vetted Pro with a perfect rating across 106 reviews who ghostwrites fantasy and science fiction. Packages range from turning a screenplay into a book to writing a full-length original novel that you own.",
      "Premium pricing: full novels are priced in the five figures and take about 90 days."),
], status="live")
