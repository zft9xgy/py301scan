"""
Nombre del script: cachelib.py
Descripción: El objetivo de esta libreria es proporcionar las funciones necesarias para manejar la cache.
Autor: Rafael Cosquiere - zft9xgy
Fecha de creación: 31 de octubre de 2023
Última modificación: 31 de octubre de 2023
Versión: 1.0
"""

# is_url_in_cache(url)
# get_filepath_hashmd5(url, CACHE_DIR="./cache")
# save_url_to_cache(url)
# delete_url_from_cache(url)
# save_url_list_to_cache(url_list_dir, skip_existing=True)
# reset_cache(CACHE_DIR="./cache")

import os
import requests
import hashlib
from tqdm import tqdm
import shutil


# It will if url is already in cache.
def is_url_in_cache(url):
    filepath = get_filepath_hashmd5(url)
    return os.path.exists(filepath)


# Get filepath with hashmd5 name on filename
# Ex. input = "https://zft9xgy.github.io/zero/"
# Ex. onput = "./cache/cd75740daf42600b2e4a89099cfe1542.html"
def get_filepath_hashmd5(url, CACHE_DIR="./cache"):
    filename = hashlib.md5(url.encode()).hexdigest() + ".html"
    filepath = os.path.join(CACHE_DIR, filename)
    return filepath


# Save url to cache, not checking if already exist, just create. If exist, it will override it.
# this function will also
def save_url_to_cache(url):
    content = requests.get(url).text
    filepath = get_filepath_hashmd5(url)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)


# Check if urls exist, if so, delete it from cache
# TO DO hacerla mas robusta teniendo en cuenta windows, linux y mac
def delete_url_from_cache(url):
    if is_url_in_cache(url):
        os.system(f"rm {get_filepath_hashmd5(url)}")


# This function will read line by line the file.list were the urls are store
# By default it will check if url is already in cache, if so, it will skip.
# If not, it will save url to cache.
def save_url_list_to_cache(url_list_dir, skip_existing=True):
    try:
        with open(url_list_dir, 'r') as file_list:
            lines = file_list.readlines()
            for line in lines:
                url = line.strip()
                # Procesa la URL aquí, por ejemplo, imprímela
                if skip_existing and is_url_in_cache(url):
                    print("Skipping: url already in cache:", url)
                    continue
                else:
                    save_url_to_cache(url)
                    print("Added to cache:", url)
    except FileNotFoundError:
        print(f"Error: El archivo '{url_list_dir}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {str(e)}")

# It will delete the conent of the cache directory files and subdirectories included.
# This funcion will only work in unix env.


def reset_cache(CACHE_DIR="./cache"):
    try:
        shutil.rmtree(CACHE_DIR)
        os.mkdir(CACHE_DIR)
        print(f"Contents of the '{CACHE_DIR}' directory cleared successfully.")
    except Exception as e:
        print(f"Error clearing the '{CACHE_DIR}' directory: {str(e)}")
