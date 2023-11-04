import asyncio
import configparser
import libcache
import list_helper
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from tqdm import tqdm

config = configparser.ConfigParser()
config.read('config.ini')

URLS_WHERE_SEARCH_DIR = config['LINK_SCANNER']['URLS_WHERE_SEARCH_DIR']
OUTPUT_SCAN_LIST_DIR = config['LINK_SCANNER']['OUTPUT_SCAN_LIST_DIR']

# This function extract the domain for a given URL
def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain

def get_status_code(url):
    try:
        response = requests.head(url)
        status_code = response.status_code
        return status_code
    except requests.exceptions.RequestException:
        return None

async def get_soup_from_url_async(url):
    if not libcache.is_url_in_cache(url):
        libcache.save_url_to_cache(url)

    html_file_dir = libcache.get_filepath_hashmd5(url)
    with open(html_file_dir, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'lxml')
    return soup

def is_href_contain_blacklist_elements(href):
    config = configparser.ConfigParser()
    config.read('config.ini')
    excluded_prefixes = config.get('FILTER_CRITERIA', 'excluded_prefixes').split(', ')
    contains_hash = config.getboolean('FILTER_CRITERIA', 'contains_hash')
    starts_with_hash = config.getboolean('FILTER_CRITERIA', 'starts_with_hash')

    if not href:
        return True

    if starts_with_hash and href.startswith("#"):
        return True

    if contains_hash and "#" in href:
        return True

    if any(href.startswith(prefix) for prefix in excluded_prefixes):
        return True

    return False

async def get_links_from_url_async(url):
    links = []
    soup = await get_soup_from_url_async(url)
    links = soup.find_all('a')
    return links

def append_link_to_file(link):
    filepath = OUTPUT_SCAN_LIST_DIR
    with open(filepath, 'a', encoding='utf-8') as file:
        file.write(str(get_status_code(link.get('href'))))
        file.write(",")
        file.write(link.get('href'))
        file.write("\n")

def is_href_already_in_file(href):
    filepath = OUTPUT_SCAN_LIST_DIR
    with open(filepath, 'r', encoding='utf-8') as file:
        line = file.read().splitlines()
        for row in line:
            row = row.split(',')
            if href == row[1]:
                return True
    return False

async def process_url(url):
    links = await get_links_from_url_async(url)
    for link in links:
        href = link.get('href')
        if is_href_contain_blacklist_elements(href) or is_href_already_in_file(href):
            continue
        append_link_to_file(link)

async def analyze_filelist_async(file_dir):
    urls = list_helper.get_list_from_file(file_dir)
    print("Analizando fichero:", file_dir)
    print("Total de URLs a analizar:", len(urls), "\n")

    tasks = [process_url(url) for url in urls]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(analyze_filelist_async(URLS_WHERE_SEARCH_DIR))
