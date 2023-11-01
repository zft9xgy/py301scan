import configparser
import cachelib
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from tqdm import tqdm


def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


# FROM LISTA DE URLS CACHEADAS
# for Toma una a una las urls y las analiza.
# analiza una url, tomando la cache
# busca todos los enlaces
# analiza los codigos de estado
# si el codigo es 301, lo escribe en una lista


URLS_TO_FIND_DIR = "./input/urls_to_find.txt"
URLS_WHERE_SEARCH_DIR = "./input/urls_where_search.txt"


# Read the content of file txt with one url per line and return a python list
def read_file_to_list(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")
        return []
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {str(e)}")
        return []


def get_status_code(url):
    try:
        # Realiza una solicitud HEAD (no descarga el cuerpo)
        response = requests.head(url)
        status_code = response.status_code
        return status_code
    except requests.exceptions.RequestException:
        return None  # Manejo de errores en caso de problemas de conexión o URL no válida


# Return soup parser as lxml from the url in cache


def get_soup_from_url(url):
    html_file_dir = cachelib.get_filepath_hashmd5(url)
    with open(html_file_dir, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'lxml')
    return soup


def append_url_to_file(url, FILE_PATH="./urls_301.txt"):
    try:
        # Leer las URLs existentes del archivo
        with open(FILE_PATH, 'r') as file:
            existing_urls = file.read().splitlines()

        # Verificar si la URL ya existe en la lista
        if url not in existing_urls:
            # Si la URL no existe, añadirla al archivo
            with open(FILE_PATH, 'a') as file:
                file.write(url + '\n')
                print("URL añadida:", url)
        else:
            print("La URL ya existe en el archivo:", url)

    except FileNotFoundError:
        # Si el archivo no existe, crearlo y añadir la URL
        with open(FILE_PATH, 'w') as file:
            file.write(url)  # + '\n')
            print("Archivo y URL creados:", FILE_PATH, url)
    except Exception as e:
        print("Ocurrió un error al guardar la URL:", str(e))


def find_301_links_in_url(url):
    # Lee la configuración desde el archivo config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    excluded_prefixes = config.get(
        'FILTER_CRITERIA', 'excluded_prefixes').split(', ')
    contains_hash = config.getboolean('FILTER_CRITERIA', 'contains_hash')
    starts_with_hash = config.getboolean('FILTER_CRITERIA', 'starts_with_hash')

    if not cachelib.is_url_in_cache(url):
        cachelib.save_url_to_cache(url)
    soup = get_soup_from_url(url)

    links = soup.find_all('a')
    # for link in links:
    #     ahref = link.get('href')
    #     if not ahref:
    #         continue  # Saltar si el enlace es None o vacío

    #     if any(ahref.startswith(prefix) for prefix in excluded_prefixes) or (starts_with_hash and ahref.startswith("#")) or (contains_hash and "#" in ahref):
    #         continue  # Saltar enlaces que cumplan con los criterios

    #     # print(ahref)
    #     if get_status_code(ahref) == 301:
    #         print(get_status_code(ahref), ahref)
    #         append_url_to_file(ahref)
    # Crea una barra de progreso para el bucle interno
    with tqdm(total=len(links)) as pbar:
        for link in links:
            ahref = link.get('href')
            if not ahref:
                pbar.update(1)
                continue  # Saltar si el enlace es None o vacío

            if any(ahref.startswith(prefix) for prefix in excluded_prefixes) or (starts_with_hash and ahref.startswith("#")) or (contains_hash and "#" in ahref):
                pbar.update(1)
                continue  # Saltar enlaces que cumplan con los criterios

            if get_status_code(ahref) == 301:
                print(get_status_code(ahref), ahref)
                append_url_to_file(ahref)
            # Incrementa la barra de progreso en 1 unidad por cada enlace procesado
            pbar.update(1)

        # Aquí puedes procesar los enlaces que no se saltaron
        # Por ejemplo, imprimirlos o realizar alguna otra acción


# def analyze_list(URLS_WHERE_SEARCH_DIR="./input/urls_where_search.txt"):
#     urls_where_search_list = read_file_to_list(URLS_WHERE_SEARCH_DIR)

#     for url in urls_where_search_list:
#         find_301_links_in_url(url)


def analyze_list(URLS_WHERE_SEARCH_DIR="./input/urls_where_search.txt"):
    urls_where_search_list = read_file_to_list(URLS_WHERE_SEARCH_DIR)

    # Crea una barra de progreso para el bucle
    with tqdm(total=len(urls_where_search_list)) as pbar:
        for url in urls_where_search_list:
            find_301_links_in_url(url)
            # Incrementa la barra de progreso en 1 unidad por cada URL procesada
            pbar.update(1)


analyze_list()
