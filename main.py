import libcache
import link_scanner

# extract the url from sitemap and save it to urls_where_search
# gsmap.get_urls_from_sitemap_list()


# create cache
# cachelib.save_url_list_to_cache("./input/urls_where_search.txt")


# find for 301 links inside each url in the list
link_scanner.analyze_list()
