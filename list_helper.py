#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Nombre del script: list_helper.py
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

URLS_WHERE_SEARCH_DIR = config['LINK_SCANNER']['URLS_WHERE_SEARCH_DIR']


def is_url_in_file(url, file_dir):
    try:
        with open(file_dir, 'r') as file:
            existing_urls = file.read().splitlines()
        return url in existing_urls
    except FileNotFoundError:
        return False  # El archivo no existe, por lo que la URL tampoco puede estar presente
    except Exception as e:
        print("Ocurrió un error al verificar la URL:", str(e))
        return False


def save_url_to_filelist(url, URL_LIST_DIR="./input/urls_where_search.txt"):
    try:
        # Leer las URLs existentes del archivo
        with open(URL_LIST_DIR, 'r') as file:
            existing_urls = file.read().splitlines()

        # Verificar si la URL ya existe en la lista
        if url not in existing_urls:
            # Si la URL no existe, añadirla al archivo
            with open(URL_LIST_DIR, 'a') as file:
                file.write(url.strip() + '\n')
                print("Added url:", url)
        else:
            print("skip: url already on list:", url)

    except FileNotFoundError:
        # Si el archivo no existe, crearlo y añadir la URL
        with open(URL_LIST_DIR, 'w') as file:
            file.write(url + '\n')
            print(f"Archivo y URL creados: {URL_LIST_DIR} - {url}")
    except Exception as e:
        print(f"Ocurrió un error al guardar la URL: {str(e)}")


def save_urls_to_filelist(urls, file_dir=URLS_WHERE_SEARCH_DIR):
    for url in urls:
        save_url_to_filelist(url, file_dir)


def load_extensions_to_ignore():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'LIST_HELPER' in config:
        extensions = config['LIST_HELPER'].get('EXTENSIONS_TO_IGNORE', '')
        if extensions:
            return set(extensions.split(', '))
    return set()  # Devolver un conjunto vacío por defecto


# this function get a puython list which contain all the urls find the provide sitemap
def get_urls_from_sitemap(sitemap_url):
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

    return extracted_urls  # Devolver la lista de URLs extraídas


# This function will take the sitemaps from the sitemap list one by one and extract the urls
def save_urls_from_sitemaps_to_list(SITEMAP_FILELIST_PATH="./input/sitemap_list.txt"):
    try:
        with open(SITEMAP_FILELIST_PATH, 'r') as sitemaps_list:
            lines = sitemaps_list.readlines()
            for line in lines:
                sitemap_url = line.strip()
                if not sitemap_url or sitemap_url.startswith("#"):
                    # print("Ignorando sitemap:", sitemap_url)
                    continue
                # Procesa la URL aquí, por ejemplo, imprímela
                print("Analizando sitemap:", sitemap_url)
                urls = get_urls_from_sitemap(sitemap_url)
                save_urls_to_filelist(urls)
    except FileNotFoundError:
        print(f"Error: El archivo '{SITEMAP_FILELIST_PATH}' no se encontró.")
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


# if __name__ == "__main__":
