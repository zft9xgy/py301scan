#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Nombre del script: list_helper.py
Descripción: Este script proporciona las funciones necesarias para extraer las urls desde una lista de sitemaps.xml
Autor: Rafael Cosquiere - zft9xgy
Github: https://github.com/zft9xgy/py301scan
Fecha de creación: 31 de octubre de 2023
Última modificación: 31 de octubre de 2023
Versión: 1.0
"""

import requests
from bs4 import BeautifulSoup
import configparser


#  Save the urls to the list.
def urls_to_list(urls):
    for url in urls:
        save_url_to_list(url)


def save_url_to_list(url, URL_LIST_DIR="./input/urls_where_search.txt"):
    try:
        # Leer las URLs existentes del archivo
        with open(URL_LIST_DIR, 'r') as file:
            existing_urls = file.read().splitlines()

        # Verificar si la URL ya existe en la lista
        if url not in existing_urls:
            # Si la URL no existe, añadirla al archivo
            with open(URL_LIST_DIR, 'a') as file:
                file.write(url + '\n')
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


def load_extensions_to_ignore():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'LIST_HELPER' in config:
        extensions = config['LIST_HELPER'].get('EXTENSIONS_TO_IGNORE', '')
        if extensions:
            return set(extensions.split(', '))
    return set()  # Devolver un conjunto vacío por defecto


def extract_urls_from_sitemap(sitemap_url):
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
def get_urls_from_sitemap_list(SITEMAP_LIST_DIR="./input/sitemap_list.txt"):
    try:
        with open(SITEMAP_LIST_DIR, 'r') as sitemaps_list:
            lines = sitemaps_list.readlines()
            for line in lines:
                sitemap_url = line.strip()
                if not sitemap_url or sitemap_url.startswith("#"):
                    # print("Ignorando sitemap:", sitemap_url)
                    continue
                # Procesa la URL aquí, por ejemplo, imprímela
                print("Analizando sitemap:", sitemap_url)
                urls = extract_urls_from_sitemap(sitemap_url)
                urls_to_list(urls)
    except FileNotFoundError:
        print(f"Error: El archivo '{SITEMAP_LIST_DIR}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {str(e)}")


if __name__ == "__main__":
    print("Empezando")
    get_urls_from_sitemap_list()
