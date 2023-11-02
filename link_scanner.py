import configparser
import libcache
import list_helper
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from tqdm import tqdm
import time


config = configparser.ConfigParser()
config.read('config.ini')

URLS_WHERE_SEARCH_DIR = config['LINK_SCANNER']['URLS_WHERE_SEARCH_DIR']
OUTPUT_SCAN_LIST_DIR = config['LINK_SCANNER']['OUTPUT_SCAN_LIST_DIR']


# This function extract the domain for a given url
def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain

# Read the content of file txt with one url per line and return a python list


def get_status_code(url):
    try:
        # Realiza una solicitud HEAD (no descarga el cuerpo)
        response = requests.head(url)
        status_code = response.status_code
        return status_code
    except requests.exceptions.RequestException:
        return None  # Manejo de errores en caso de problemas de conexión o URL no válida


# Return soup parser as lxml from the url in cache

# Asuming the url is in cache already.
# Da error si la url no esta en cache, comtemplar esto #todo
def get_soup_from_url(url):

    # si no url en cahce, la crea.
    if not libcache.is_url_in_cache(url):
        libcache.save_url_to_cache(url)

    # get html dir
    html_file_dir = libcache.get_filepath_hashmd5(url)
    with open(html_file_dir, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'lxml')
    return soup


# Analizar lista - main
#  urls = get_urls_from_filelist(lista.txt)
# for url in urls
#   links = get_all_links_from_url(url) # lista con todos los links en esa url
#   for link in links
#       ahref = link.get('href')
#       if not ahref_already_existe_in_file
#           f.write(get_status_code(href),href)

def is_href_contain_blacklist_elements(href):
    # Lee la configuración desde el archivo config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    excluded_prefixes = config.get(
        'FILTER_CRITERIA', 'excluded_prefixes').split(', ')
    contains_hash = config.getboolean('FILTER_CRITERIA', 'contains_hash')
    starts_with_hash = config.getboolean('FILTER_CRITERIA', 'starts_with_hash')

    # Devuelve False si linea vacia
    if (not href):
        return True

    # False si href start with '#'
    if (starts_with_hash and href.startswith("#")):
        return True

    # False si contiene '#'
    if (contains_hash and "#" in href):
        return True

    # False si empieza con alguno de los elementos de la lista, como mailto: o tel:
    if any(href.startswith(prefix) for prefix in excluded_prefixes):
        return True

    return False


def get_links_from_url(url):
    links = []
    soup = get_soup_from_url(url)
    links = soup.find_all('a')
    return links


# appen
def append_link_to_file(link):
    filepath = OUTPUT_SCAN_LIST_DIR
    with open(filepath, 'a', encoding='utf-8') as file:
        file.write(str(get_status_code(link.get('href'))))
        file.write(",")
        file.write(link.get('href'))
        file.write("\n")


def is_href_already_in_file(href):
    filepath = OUTPUT_SCAN_LIST_DIR
    # print("Filepath:", filepath)
    with open(filepath, 'r', encoding='utf-8') as file:
        line = file.read().splitlines()
        for row in line:
            row = row.split(',')
            if href == row[1]:
                return True
        # if not found, return false
        return False


def analyze_filelist(file_dir):
    urls = list_helper.get_list_from_file(file_dir)
    print("Analizando fichero:", file_dir)
    print("Total de urls a analizar:", len(urls), "\n")

    for url in tqdm(urls, desc="Total progress", position=0):
        # print("Analizando url:", url)
        links = get_links_from_url(url)
        # print("Total de link encontrados en la url:", len(links), "\n")

        for link in tqdm(links, desc="Inner progress", position=1, leave=False):
            href = link.get('href')
            if is_href_contain_blacklist_elements(href):
                # print("skipping:blacklist", href)
                continue
            if is_href_already_in_file(href):
                # print("skipping:already in list", href)
                continue
            # print(href)
            append_link_to_file(link)


if __name__ == "__main__":
    analyze_filelist(URLS_WHERE_SEARCH_DIR)
