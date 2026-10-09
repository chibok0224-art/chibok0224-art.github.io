import add_picks

add_picks.CHECKED = "2026-10-09"


def r(user, name, best_for, title, rating, reviews, price, path, why, watch_out=""):
    return dict(user=user, name=name, best_for=best_for, title=title, rating=rating, reviews=reviews,
                level="Vetted Pro", price=price, url=path, why=why, watch_out=watch_out)


add_picks.put("programming-tech/software-development", [
    r("kunalkhurana401", "Kunal Khurana", "Best overall for custom full-stack software",
      "I will be software developer full stack developer ai software developer mern stack dev", "5.0", "369", "110",
      "/kunalkhurana401/web-developer-or-software-developer-for-full-stack-web-development-php-laravel",
      "A Vetted Pro with a perfect rating across 369 reviews who builds full-stack software with frontend, backend and database. Every package includes source code with code comments, and the larger ones add API integrations.",
      "The entry package is a small three-page solution; full custom software is priced much higher and takes about six weeks."),
    r("aignatov", "Ruby Monkey", "Best for Ruby on Rails apps and fixes",
      "I will help with ruby on rails application", "5.0", "308", "100",
      "/aignatov/make-ruby-on-rails-application",
      "A Vetted Pro with a perfect rating across 308 reviews who builds and maintains Ruby on Rails applications. Packages range from a bug fix or small task to a new feature or a complete new application, all with unlimited revisions.",
      "Only for projects built, or to be built, in Ruby on Rails."),
    r("thechoyon", "Choyon", "Best for Python bots and task automation",
      "I will write python bots and crawlers", "5.0", "766", "100",
      "/thechoyon/write-python-script-for-you",
      "A Vetted Pro with a perfect rating across 766 reviews who writes Python scripts that automate repetitive work, including bots and data collection. Every package includes the source code, installation and testing.",
      "The seller asks you to discuss the job before ordering."),
    r("zainmustafad", "Geeksofkolachi", "Best for planning a web app before you build",
      "Our agency will do ai saas web application custom software development as software app developer", "5.0", "76", "190",
      "/zainmustafad/do-saas-web-application-custom-software-development-as-software-developer",
      "A Vetted Pro agency with a perfect rating across 76 reviews. The entry package is a consultation with project analysis and planning, and the larger packages build custom web apps with design, security features and a week of support after launch.",
      "Full builds start in the thousands, well above the consultation price."),
    r("zeeshansikander", "Zenkoders", "Best for AI-powered SaaS products",
      "Our agency will develop ai web application custom software development saas developer ai agents", "5.0", "144", "200",
      "/zeeshansikander/be-your-react-next-node-next-developer",
      "A Vetted Pro agency with a perfect rating across 144 reviews that builds web applications, SaaS products and AI tools. Packages include source code and code comments, from a single frontend page up to apps with user roles and an admin dashboard.",
      "Larger apps are priced in the thousands and take one to three months."),
    r("umermalik_", "Esquall LLC", "Best for testing an idea with a clickable prototype",
      "Our agency will develop complete software and web applications", "4.8", "204", "500",
      "/umermalik_/make-you-java-and-python-components",
      "A Vetted Pro agency with 204 reviews. The entry package is a clickable prototype to test your idea, and higher packages build core features with APIs or full web, mobile and desktop apps, with source code included.",
      "The prototype package lists no revisions, and full builds take two to three months."),
], status="live")
