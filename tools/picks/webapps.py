import add_picks

add_picks.CHECKED = "2026-10-09"


def r(user, name, best_for, title, rating, reviews, price, path, why, watch_out=""):
    return dict(user=user, name=name, best_for=best_for, title=title, rating=rating, reviews=reviews,
                level="Vetted Pro", price=price, url=path, why=why, watch_out=watch_out)


add_picks.put("programming-tech/full-stack-web-apps", [
    r("asadawan88", "Eazisols", "Best overall for a complete web app",
      "Our agency will create a custom ai web application, ai website and software development", "4.9", "81", "495",
      "/asadawan88/develop-n-fix-websites-in-php-dotnet-html-css-asp-etc",
      "A Vetted Pro agency with 81 reviews. Even the basic package is a complete web application with essential features in ten days; higher tiers add APIs, user accounts, integrations and long-term support. All packages include source code and unlimited revisions."),
    r("sarahahmad", "Desol Int.", "Best budget pick for scoping your app first",
      "Our agency will develop ai web application custom software development saas full stack developer", "4.9", "112", "100",
      "/sarahahmad/make-you-trendy-super-hero-from-your-photo",
      "A Vetted Pro agency with 112 reviews. The entry package scopes your project and recommends a tech stack and architecture; larger packages build a prototype or a full web app with AI features, APIs and deployment.",
      "Building the app itself starts in the thousands, well above the scoping price."),
    r("mercury_sols", "Mob", "Best for .NET and database-driven apps",
      "I will create database driven website with asp net core mvc, dot net", "5.0", "99", "100",
      "/mercury_sols/develop-database-driven-websites",
      "A Vetted Pro with a perfect rating across 99 reviews who builds web applications in ASP.NET Core. Packages are sized by hours of work, from about four hours of fixes or components to a full application of roughly 60 to 70 hours, with source code included.",
      "Best if your project uses or can use Microsoft .NET technology."),
    r("amaar_developer", "Ammar Afzal", "Best for apps with admin and user portals",
      "I will be your full stack web developer and website programmer", "4.9", "133", "525",
      "/amaar_developer/full-stack-web-developer-html-css-js-angular-react-custom-website-development",
      "A Vetted Pro with 133 reviews who builds custom web apps and business sites. Packages scale from four pages to large builds with several portals and API integrations, each with source code and five or more revisions.",
      "The seller asks you to make contact before ordering, and larger builds take two to three months."),
    r("jd4877", "Joshua D", "Best for reviewing and fixing an existing app",
      "I will build a custom saas web application for your business", "5.0", "34", "350",
      "/jd4877/develop-a-complex-web-application-for-your-business",
      "A Vetted Pro with a perfect rating who builds SaaS and full-stack web apps. The entry package reviews your existing app, fixes critical bugs and adds basic features; higher packages build production-ready or large SaaS apps.",
      "The entry package includes one revision."),
    r("reliableapps", "Priority Soft", "Best for a clickable demo before full build",
      "Our agency will be your full stack web developer in react node js next js", "5.0", "46", "500",
      "/reliableapps/be-your-full-stack-web-developer-in-react-node-js-next-js",
      "A Vetted Pro product studio with a perfect rating across 46 reviews. The entry package is a clickable demo of your idea; higher packages cover strategy, design and a production web app, with source code and code comments.",
      "Production builds are priced in the five figures."),
], status="live")
