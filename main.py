import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from icecream import ic

"""
Actualmente este scripts, funciona y hace su trabajo, pero es inviable para webs grandes.
Para una listado o sitemap (>100 urls) no lo recocomendario actualmente.
Es viable pero puede demorar en su ejecución. No esta al nivel de screaming frog.
"""


def uniques(list):

    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    return unique_list


def get_urls_from_sitemap_list_txt(sitemap_path):

    with open(sitemap_path, 'r') as file:
        sitemaps_list = file.read().splitlines()

    urls = []
    # extraccion de urls desde sitemaps
    for sitemap in sitemaps_list:
        print(sitemap)
        response = requests.get(sitemap)
        soup = BeautifulSoup(response.text, "xml")
        loc_tags = soup.find_all("loc")

        # ignore image files when getting href from sitemap
        extensions_to_ignore = [".jpg", ".png", ".jpeg", ".gif", ".webp"]

        for url in loc_tags:
            url = url.text.lower()
            if any(url.endswith(ext) for ext in extensions_to_ignore):
                continue
            urls.append(url)

    return urls


def get_urls_from_urls_list_txt(urls_path):
    with open(urls_path, 'r') as file:
        return file.read().splitlines()


def get_links_from_single_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    return links


def clean_links(links):
    output = []
    for link in links:
        href = link.get("href")
        if not href:
            continue
        if href.startswith("#"):
            continue
        if "mailto:" in href:
            continue
        if "tel:" in href:
            continue
        if "#" in href:
            continue
        output.append(link)
    return output


def get_link_main_location(link):
    if link.find_parent("header"):
        return "header"
    elif link.find_parent("footer"):
        return "footer"
    elif link.find_parent("body"):
        return "body"
    else:
        return "other"


def analyze_links(links):
    scan_output = []
    for link in tqdm(links, desc="links"):
        href = link.get("href")
        # False si href comienza con '#'

        if not href:
            continue
        if href.startswith("#"):
            continue
        if "mailto:" in href:
            continue
        if "tel:" in href:
            continue

        response_link = requests.head(href)
        response_code = response_link.status_code
        if response_code != 200:
            scan_output.append(["Source:", url, "Link:", href,
                               "Response code", response_code])
    return scan_output


def is_href_on_ingnore_list(href, ignore_200_set):
    return href in ignore_200_set


if __name__ == "__main__":
    start_time = time.time()

    # Si quieres extraer las urls desde un conjunto de sitemap, usa las siguientes lineas.
    sitemap_path = './input/sitemap_list.txt'
    urls = get_urls_from_sitemap_list_txt(sitemap_path)

    # En caso de no querer usar los sitemaps, y tienes una lista de url, comenta la parte anterior y usa esta.
    # urls = get_urls_from_urls_list_txt('./input/urls_list.txt')

    output_csv = './csv/raw_scan.csv'

    scan_output = []
    ignore_200_set = set()
    urls = uniques(urls)

    for url in tqdm(urls, desc="source_url", position=0):

        links = get_links_from_single_url(url)
        links = clean_links(links)

        for link in tqdm(links, desc="inner_links"):
            href = link.get("href")

            if is_href_on_ingnore_list(href, ignore_200_set):
                continue

            link_status = requests.head(href).status_code

            if link_status == 200:
                ignore_200_set.add(href)

                continue

            anchor_text = link.text.strip()
            link_location = get_link_main_location(link)

            scan_output.append(
                [link_status, url, href, f'"{anchor_text}"', link_location])

    # reset file
    try:
        open(output_csv, "w").close()
    except Exception as e:
        print(f"Error resetting the '{output_csv}' file: {str(e)}")

    with open(output_csv, 'a', encoding='utf-8') as file:
        file.write("status_code,source_url,link,anchor,tag_location")
        file.write('\n')
        for row in scan_output:
            file.write(','.join(str(e) for e in row))
            file.write('\n')

    # Marca de tiempo al final del script
    finish_time = time.time()

    # Calcular la diferencia de tiempo
    print(f"Ejecución completada, puede encontrar su archivo en {output_csv}")
    print(f"Time {finish_time - start_time} s")
