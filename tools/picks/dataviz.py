import add_picks

add_picks.CHECKED = "2026-10-09"


def r(user, name, best_for, title, rating, reviews, price, path, why, watch_out=""):
    return dict(user=user, name=name, best_for=best_for, title=title, rating=rating, reviews=reviews,
                level="Vetted Pro", price=price, url=path, why=why, watch_out=watch_out)


add_picks.put("data/data-visualization", [
    r("nitinrungta", "Nitin Rungta", "Best overall for business data dashboards",
      "I will do ai ml hrms lovable powerbi looker dashboard analytics", "5.0", "266", "100",
      "/nitinrungta/analyze-visualize-and-summarize-your-data",
      "A Vetted Pro with a perfect rating across 266 reviews who builds Power BI and Looker dashboards. The entry package covers one or two charts in two days; larger packages visualize a whole business area, such as sales or stock data, with web embedding and interactive visuals.",
      "The jump from the entry package to a full business-area dashboard is large."),
    r("gaineselmore", "Gaines E", "Best budget pick for Tableau dashboards",
      "I will build world class dashboards and visuals in tableau", "5.0", "81", "100",
      "/gaineselmore/create-dashboards-and-visualizations-in-tableau",
      "A Vetted Pro with a perfect rating across 81 reviews who builds interactive Tableau dashboards. The basic package is one dashboard with up to four visuals from one data source, delivered in one day.",
      "The basic package includes only one revision."),
    r("ciocirlieionut", "Ciocirlie I.", "Best for maps and location data",
      "I will do expert gis mapping, geospatial and satellite analysis", "5.0", "81", "500",
      "/ciocirlieionut/gis-and-cartography-work-for-you",
      "A Vetted Pro with a perfect rating across 81 reviews who makes GIS maps and spatial analysis. Packages range from one essential map to several maps with remote sensing and web visualization.",
      "Specialist mapping work with a higher starting price than chart dashboards."),
    r("vaskar_dutta", "Avangard AI", "Best for Looker Studio dashboards",
      "Our agency will create or fix looker studio aka google data studio dashboard", "5.0", "31", "100",
      "/vaskar_dutta/create-your-google-data-studio-dashboard",
      "A Vetted Pro agency with a perfect rating that builds or fixes Looker Studio dashboards, for example from analytics, search or ad data. Packages go from a one-page dashboard to multi-page dashboards using up to four data sources.",
      "The seller asks you to get in touch before ordering for a custom price."),
    r("alex_nunes", "Alex Nunes", "Best for interactive Excel dashboards",
      "I will create interactive dashboard and reports in excel", "4.8", "205", "225",
      "/alex_nunes/create-interactive-dashboard-and-reports-in-excel",
      "A Vetted Pro with 205 reviews who builds interactive dashboards inside Excel. Higher packages also organize your data tables and add simple data entry, so the dashboard can keep updating.",
      "Delivery takes six to ten days, longer than most others here."),
    r("tableau_jedi", "Nimit", "Best for Tableau or Power BI with data prep",
      "I will create interactive and beautiful tableau and power bi dashboards", "4.8", "168", "100",
      "/tableau_jedi/create-complex-elegant-and-robust-dashboards-and-solutions",
      "A Vetted Pro with 168 reviews who builds dashboards in Tableau or Power BI. Packages run from a single visualization to a complex dashboard with advanced data preparation.",
      "Only the top package lists a revision, so agree on changes before ordering."),
], status="live")
