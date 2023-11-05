"""
Nombre del script: helper.py
Descripción: La idea con este scripts es proporcionar una libreria para trabajar con listas de python y ficheros de text con las urls.
Autor: Rafael Cosquiere - zft9xgy
Github: https://github.com/zft9xgy/py301scan
Fecha de creación: 31 de octubre de 2023
Última modificación: 31 de octubre de 2023
Versión: 1.0
"""

import requests
from bs4 import BeautifulSoup
import configparser

# append_single_url_to_file(url,file_dir)
# reset_file(file)
# get_list_from_file()

config = configparser.ConfigParser()
config.read('config.ini')

URLS_LIST = config['DEFAULT']['INPUT_URLS_LIST']
SITEMAPS_LIST = config['DEFAULT']['INPUT_SITEMAPS_LIST']


# Return True if url is found on file_dir, False if not
def is_url_in_file(url, file_dir=URLS_LIST):
    try:
        with open(file_dir, 'r') as file:
            existing_urls = file.read().splitlines()
        return url in existing_urls
    except FileNotFoundError:
        return False  # El archivo no existe, por lo que la URL tampoco puede estar presente
    except Exception as e:
        print("Ocurrió un error al verificar la URL:", str(e))
        return False


# Append url to the filelist, not checking if exsit or not. Just append.
# This function could be implemented with futures concurrence
def save_url_to_filelist(url, file_dir=URLS_LIST):
    try:
        with open(file_dir, 'a') as file:
            file.write(url.strip() + '\n')
            print("Added url:", url)

    except FileNotFoundError:
        # Si el archivo no existe, crearlo y añadir la URL
        with open(file_dir, 'w') as file:
            file.write(url + '\n')
            print(f"Archivo y URL creados: {file_dir} - {url}")

    except Exception as e:
        print(f"Ocurrió un error al guardar la URL: {str(e)}")



# Iterate line by line and save each url to filelist
def save_urls_to_filelist(urls, file_dir=URLS_LIST):
    for url in urls:
        save_url_to_filelist(url, file_dir)


# Load de extension to ignore from config file. 
# This extension will be use to filter when getting urls from sitemap or filelist of urls
def load_extensions_to_ignore():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'LIST_HELPER' in config:
        extensions = config['LIST_HELPER'].get('EXTENSIONS_TO_IGNORE', '')
        if extensions:
            return set(extensions.split(', '))
    return set()  # Devolver un conjunto vacío por defecto


# this function get a puython list which contain all the urls find the provide sitemap
# return a python list with all the urls from a given sitemap
def get_urls_from_sitemap_ignoring_extension(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, "xml")
    loc_tags = soup.find_all("loc")

    # Cargar la lista de extensiones a ignorar desde el archivo de configuración
    extensions_to_ignore = load_extensions_to_ignore()

    extracted_urls = []  # Crear una lista para almacenar las URLs extraídas

    for loc in loc_tags:
        url = loc.text.lower()  # Convertir a minúsculas para hacerlo case-insensitive
        if any(url.endswith(ext) for ext in extensions_to_ignore):
            continue  # Ignorar la URL si termina con una extensión prohibida
        extracted_urls.append(url)  # Agregar la URL a la lista
        print("Added url to the list:", url)

    return extracted_urls  # Devolver la lista de URLs extraídas


# this function get a puython list which contain all the urls find the provide sitemap
# return a python list with all the urls from a given sitemap
def get_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, "xml")
    loc_tags = soup.find_all("loc")

    extracted_urls = []  # Crear una lista para almacenar las URLs extraídas

    for loc in loc_tags:
        url = loc.text.lower()  # Convertir a minúsculas para hacerlo case-insensitive
        extracted_urls.append(url)  # Agregar la URL a la lista
        print("Added url to the list:", url)

    return extracted_urls  # Devolver la lista de URLs extraídas

# This function will take the sitemaps from the sitemap list one by one and extract the urls
def save_urls_from_sitemaps_file_to_file(sitemap_list_dir=SITEMAPS_LIST,url_list_dir=URLS_LIST):
    try:
        with open(sitemap_list_dir, 'r') as sitemaps_list:
            lines = sitemaps_list.readlines()
            for line in lines:
                sitemap_url = line.strip()
                if not sitemap_url or sitemap_url.startswith("#"):
                    # Si se trata de una linea en blanco o empieza con # ignora la linea y continua
                    continue
                urls = get_urls_from_sitemap_ignoring_extension(sitemap_url)
                save_urls_to_filelist(urls,url_list_dir)
    except FileNotFoundError:
        print(f"Error: El archivo '{sitemap_list_dir}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {str(e)}")


# Return a python list from a file, where each line is an element.
def get_list_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
        return lines
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")
        return []
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {str(e)}")
        return []

