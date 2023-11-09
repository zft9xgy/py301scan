"""
Nombre del script: link_scanner.py
Autor: Rafael Cosquiere aka zft9xgy
Github: https://github.com/zft9xgy/py301scan
Fecha de creación: 09 de noviembre de 2023
Última modificación: 09 de noviembre de 2023
Versión: 1.0
Descrición:
            Este scipt tiene como objetivo analizar una lista de urls una a una, para dar como resultado un csv que reporte los codigos de estado 
            de cada una.
            Es decir:

            parametros de entrada, una file_dir con la lista de urls a analizar
            parametros de salido. escribe el resultado del analisis en csv/raw_scan.csv

            Para ello toma las urls del fichero, una por linea y las almacena en una lista.
            Itera por ellas analizando cada url, tomando el contenido de esta de la cache.
            Buscar internamente todos los enlaces (links) que esta url contiene en su codigo html.
            Y reporta los codigos de error de los mismos.


            Consideraciones: 
            - reporta todos los codigos de error, no solo los 301.
            - no incluye links repetidos, ya que se entiende que un mismo link tendra el mismo codigo de estado en una url o en otra, aunque el anchor pueda ser diferente


"""

import configparser
import libcache
import helper
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import time
from icecream import ic


# Se obtienen los direciones de las lista de entrada y la direccion del csv de salida
config = configparser.ConfigParser()
config.read('config.ini')

URLS_DIR = config['DEFAULT']['INPUT_URLS_LIST']
OUTPUT_SCAN_DIR = config['DEFAULT']['OUTPUT_RAW']

# Crear el filtro
FILTER_CRITERIO = {
    'excluded_prefixes': config.get('FILTER_CRITERIA', 'excluded_prefixes'),
    'contains_hash': config.getboolean('FILTER_CRITERIA', 'contains_hash'),
    'starts_with_hash': config.getboolean('FILTER_CRITERIA', 'starts_with_hash')
}



# Esta funcion devuelte el codigo de estado de una url dada como un 'int'abs
# para ello realiza una request solo del head para optimizar el tiempo de ejecucion
# todo: contemplar timeout reponse
def get_status_code(url):
    try:
        # Realiza una solicitud HEAD (no descarga el cuerpo)
        response = requests.head(url)
        status_code = response.status_code
        return status_code
    except requests.exceptions.RequestException:
        return None  # Manejo de errores en caso de problemas de conexión o URL no válida


# Asuming the url is in cache already.
# todo: Da error si la url no esta en cache, comtemplar esto.
def get_soup_from_cache_url(url):

    # get html dir
    html_file_dir = libcache.get_filepath_hashmd5(url)
    with open(html_file_dir, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'lxml')

    return soup


def is_href_contain_blacklist_elements(href, filter_criteria=FILTER_CRITERIO):
    excluded_prefixes = filter_criteria.get('excluded_prefixes').split(', ')
    contains_hash = filter_criteria.get('contains_hash')
    starts_with_hash = filter_criteria.get('starts_with_hash')


    # Devuelve False si línea vacía
    if not href:
        return True

    # False si href comienza con '#'
    if starts_with_hash and href.startswith("#"):
        return True

    # False si contiene '#'
    if contains_hash and "#" in href:
        return True

    # False si empieza con alguno de los elementos de la lista, como mailto: o tel:
    if any(href.startswith(prefix) for prefix in excluded_prefixes):
        return True

    return False



# Devuelve una lista con todos los links encontrados en una url dada.
def get_links_from_url(url):
    links = []
    soup = get_soup_from_cache_url(url)
    links = soup.find_all('a')
    return links



# Devuelve la localizacion del link dentro del direcotira dom, outputs: header, footer, body
# todo: crear a modificar esta funcion para que reporte el location path del dom tree para que sea
# mas facil identificarlo
def get_link_main_location(link):
    if link.find_parent("header"):
        return "header"
    elif link.find_parent("footer"):
        return "footer"
    elif link.find_parent("body"):
        return "body"
    else:
        return "other"




# append link infgormaicon to the output csv
# source url, url que se esta analizando
# link, enlace encontrado en el contenido de esa url
# todo: crear funcion que obtenga el anchor, a veces link.text esta vacio
# todo: usar modulo csv 
# todo: posibilidad de crear objeto link para que sea mas simple el codigo
def append_link_data_to_file(link,source_url,output_dir=OUTPUT_SCAN_DIR):
    filepath = output_dir
    with open(filepath, 'a', encoding='utf-8') as file:
        file.write(str(get_status_code(link.get('href'))))
        file.write(",")
        file.write(link.get('href'))
        file.write(",")
        file.write(source_url)
        file.write(",")
        file.write(f'"{link.text.strip()}"')
        file.write(",")
        file.write(get_link_main_location(link))
        file.write("\n")

        #"status_code,link,source_url,anchor,tag_location"


def is_href_already_in_outputfile(href,file_dir):
    # print("Filepath:", filepath)
    with open(file_dir, 'r', encoding='utf-8') as file:
        line = file.read().splitlines()
        for row in line:
            row = row.split(',')
            if href == row[1]:
                return True
        # if not found, return false
        return False


def analyze_filelist(file_dir,output_dir=OUTPUT_SCAN_DIR):
    urls = helper.get_list_from_file(file_dir)
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
            # if is_href_already_in_outputfile(href,output_dir):
            #     print("skipping:already in list", href)
            #     continue
            #debug_url(link,url)
            append_link_data_to_file(link,url)


if __name__ == "__main__":
    analyze_filelist(URLS_DIR)
