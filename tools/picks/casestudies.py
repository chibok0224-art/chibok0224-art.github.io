import add_picks

add_picks.CHECKED = "2026-10-09"


def r(user, name, best_for, title, rating, reviews, price, path, why, watch_out=""):
    return dict(user=user, name=name, best_for=best_for, title=title, rating=rating, reviews=reviews,
                level="Vetted Pro", price=price, url=path, why=why, watch_out=watch_out)


add_picks.put("writing-translation/case-studies", [
    r("mongiardo", "Victoria M", "Best overall for fast, structured case studies",
      "I will write impactful content for a case study", "4.8", "19", "100",
      "/mongiardo/write-content-for-a-case-study",
      "A Vetted Pro who writes case studies in a challenge, solution and result structure. Packages run from 500 to 1,500 words, all with three-day delivery, three revisions and extra research.",
      "Only 19 reviews on this gig so far."),
    r("ggerbus", "Gabrielle", "Best for a case study with branded design",
      "I will write a compelling case study for your business", "5.0", "12", "175",
      "/ggerbus/write-a-compelling-case-study-for-your-business",
      "A Vetted Pro with a perfect rating who writes customer case studies. The entry package gives a title, opening and problem-solution-result points; the top package is a 1,500-word case study with visual design in a branded document.",
      "Only 12 reviews, and the entry package includes one revision."),
    r("mattmacintosh", "Matthew M.", "Best for case studies built on a customer interview",
      "I will write a customer case study to showcase your strengths", "5.0", "10", "350",
      "/mattmacintosh/write-a-customer-case-study-to-showcase-your-strengths",
      "A Vetted Pro with a perfect rating whose every package includes an interview with your customer, research, writing and two revisions, with seven-day delivery.",
      "Higher starting price, and only 10 reviews."),
    r("crawford_copy", "John Crawford", "Best for print-ready case study brochures",
      "I will create a case study, report, or analysis for business, financial or marketing", "4.9", "10", "125",
      "/crawford_copy/case-study-copywriter-i-write-professional-business-case-studies",
      "A Vetted Pro who writes and designs case studies and project reports. Packages run from a one-page designed case study to a four-page brochure or an eight-page booklet, with three to five revisions.",
      "Only 10 reviews; delivery takes seven to ten days."),
    r("gerimileva", "Geri Mileva", "Best budget pick with the most revisions",
      "I will write effective case studies that drive conversions", "4.8", "9", "100",
      "/gerimileva/write-effective-case-studies-that-drive-conversions",
      "A Vetted Pro who writes one- to three-page case studies with references and extra research. Every package includes five revisions and delivery in three to five days.",
      "Only 9 reviews so far."),
], status="live")
