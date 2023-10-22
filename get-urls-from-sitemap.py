import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import configparser

# Leer el archivo config
config = configparser.ConfigParser()
config.read('config.ini')

# URL del sitemap desde el archivo config
SITEMAP_URL = config['DEFAULT']['SITEMAP_URL']
URLS_FILE = config['DEFAULT']['URLS_FILE']


def get_total_urls_in_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, "xml")
    return len(soup.find_all("loc"))


def main():
    # Informar al usuario sobre la URL del sitemap que se utilizará.
    print(f"Current sitemap URL: {SITEMAP_URL}")

    # Pedir confirmación para usar la URL o introducir una nueva.
    decision = input(
        "To use another sitemap URL, paste it here or press ENTER to continue with the current one: ")

    if decision:
        sitemap_url = decision.strip()  # limpiar espacios en blanco
    else:
        sitemap_url = SITEMAP_URL

    # Preguntar al usuario sobre excluir URLs de imágenes (por defecto sí)
    exclude_images = input(
        "By default, Yoast SEO generated sitemaps contain many images. Do you want to exclude URLs containing '/wp-content/'? (yes/no [default: yes]): ")
    if exclude_images.lower() not in ['no', 'n']:
        exclude_images = True
    else:
        exclude_images = False

    # Preguntar al usuario si quiere agregar o regenerar la lista
    append_to_list = input(
        "Do you want to append the extracted URLs to the end of the list? (yes/no [default: yes][no:regenerate list]): ")
    if append_to_list.lower() in ['no', 'n']:
        mode = 'w'
    else:
        mode = 'a'

    # Obtener el total de URLs en el sitemap
    total_urls = get_total_urls_in_sitemap(sitemap_url)
    print(f"Fetching {total_urls} URLs from the sitemap...")

    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, "xml")

    loc_tags = soup.find_all("loc")

    # Extraer las URLs con barra de progreso y escribir en el archivo
    with open(URLS_FILE, mode) as file:
        for loc in tqdm(loc_tags, total=total_urls, desc="Extracting URLs"):
            url = loc.text
            if exclude_images and '/wp-content/' in url:
                continue
            file.write(url + "\n")

    print(f"URLs have been saved to {URLS_FILE}.")


if __name__ == "__main__":
    main()
