import cachelib
import get_urls_from_sitemap_list as gsmap
import scan_301

# extract the url from sitemap and save it to urls_where_search
# gsmap.get_urls_from_sitemap_list()


# create cache
# cachelib.save_url_list_to_cache("./input/urls_where_search.txt")


# find for 301 links inside each url in the list
scan_301.analyze_list()
