import libcache
import link_scanner
import list_helper as helper

# extract the url from sitemap and save it to urls_where_search
# helper.save_urls_from_sitemaps_to_list()

# create cache
libcache.save_url_list_to_cache("./input/urls_where_search.txt")

# find for 301 links inside each url in the list
# link_scanner.analyze_list()
