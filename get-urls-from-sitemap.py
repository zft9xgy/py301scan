import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import configparser

# Leer el archivo config
config = configparser.ConfigParser()
config.read('config.ini')

# Default Execution options
sitemap_url = config['DEFAULT']['SITEMAP_URL']
url_list = config['DEFAULT']['URLS_FILE']
exclude_wpcontent = config['GETFROMSITEMAP']['EXCLUDE_WPCONTENT']
mode = config['GETFROMSITEMAP']['MODE']


def set_options():
    global mode, sitemap_url, mode

    # show current sitemap and ask for change.
    print(f"Current sitemap URL: {sitemap_url}")
    decision = input(
        "To use another sitemap URL, paste it here or press ENTER to continue with the current one: ")

    if decision:
        sitemap_url = decision.strip()
    else:
        sitemap_url = sitemap_url

    # Preguntar al usuario sobre excluir URLs de imágenes (por defecto sí)
    exclude_wpcontent = input(
        "By default, Yoast SEO generated sitemaps contain many images. Do you want to exclude URLs containing '/wp-content/'? (yes/no) [press enter to default: yes]: ")
    if exclude_wpcontent.lower() not in ['no', 'n']:
        exclude_wpcontent = True
    else:
        exclude_wpcontent = False

    # Preguntar al usuario si quiere agregar o regenerar la lista
    append_to_list = input(
        "Do you want to append the extracted URLs to the end of the list? (yes/no) [press enter to default: yes][no:regenerate list]): ")
    if append_to_list.lower() in ['no', 'n']:
        mode = 'w'
    else:
        mode = 'a'


def main():

    set_options()

    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, "xml")
    loc_tags = soup.find_all("loc")
    total_urls = len(loc_tags)

    print(f"Fetching {total_urls} URLs from the sitemap...")

    # Extraer las URLs con barra de progreso y escribir en el archivo
    with open(url_list, mode) as file:
        for loc in tqdm(loc_tags, total=total_urls, desc="Extracting URLs"):
            url = loc.text
            if exclude_wpcontent and '/wp-content/' in url:
                continue
            file.write(url + "\n")

    print(f"URLs have been saved to {url_list}.")


if __name__ == "__main__":
    main()
