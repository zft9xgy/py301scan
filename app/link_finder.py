"""
aun no se ha desarrollado este scripts
"""

# import requests
# from bs4 import BeautifulSoup
# import csv
# from tqdm import tqdm
# from concurrent.futures import ThreadPoolExecutor
# import hashlib
# import os
# import configparser

# # Script description:
# # This script searches for a specific URL within a list of web pages.
# # If the URL is found, details are saved in a CSV file.

# config = configparser.ConfigParser()
# config.read('config.ini')

# URL_TO_FIND = config['DEFAULT']['URL_TO_FIND']
# INPUT_FILE = config['DEFAULT']['URLS_FILE']
# CACHE_DIR = config['DEFAULT']['CACHE_DIR']
# CSV_DIR = config['DEFAULT']['CSV_FOLDER']
# CSV_DEFAULT_NAME = config['DEFAULT']['CSV_DEFAULT_NAME']


# def get_from_cache(url):
#     """Recuperar contenido de la caché si está disponible."""
#     filename = hashlib.md5(url.encode()).hexdigest() + ".html"
#     filepath = os.path.join(CACHE_DIR, filename)
#     if os.path.exists(filepath):
#         with open(filepath, 'r', encoding='utf-8') as file:
#             return file.read()
#     return None


# def find_matching_links(url, URL_TO_FIND):
#     content = get_from_cache(url)

#     if not content:
#         try:
#             response = requests.get(url, timeout=3)
#             response.raise_for_status()  # Asegurarse de que la respuesta fue exitosa
#             content = response.text

#             # Guardamos en caché
#             filename = hashlib.md5(url.encode()).hexdigest() + ".html"
#             filepath = os.path.join(CACHE_DIR, filename)
#             with open(filepath, 'w', encoding='utf-8') as file:
#                 file.write(content)

#         except requests.Timeout:
#             print(f"Timeout al intentar acceder a {url}")
#             return "timeout"
#         except requests.RequestException:
#             return []

#     soup = BeautifulSoup(content, 'lxml')
#     links = soup.find_all("a", href=True)
#     matching_links = [(url, link['href'], link.string if link.string else "empty", get_location(
#         link, soup)) for link in links if URL_TO_FIND in link['href']]
#     return matching_links


# def get_location(link, soup):
#     if link.find_parent("header"):
#         return "header"
#     elif link.find_parent("footer"):
#         return "footer"
#     elif link.find_parent("body"):
#         return "body"
#     else:
#         return "other"


# # Lee las URLs desde el archivo de entrada
# with open(INPUT_FILE, "r") as file:
#     urls_to_analyze = file.read().splitlines()

# # Información para el usuario antes de la ejecución
# print(f"Se intentará encontrar la URL: {URL_TO_FIND}")
# print(f"Se analizarán las URLs del archivo: {INPUT_FILE}")
# print(f"El archivo contiene {len(urls_to_analyze)} URLs.")
# response = input(
#     "Presione 'Enter' para continuar o escriba 'no' para finalizar: ")
# if response.lower().strip() == 'no':
#     print("Ejecución finalizada por el usuario.")
#     exit()

# # Solicita al usuario el nombre para el archivo CSV
# csv_filename_input = input(
#     f"Introduzca el nombre del archivo CSV (presione 'Enter' para usar '{CSV_DEFAULT_NAME}' por defecto): ")


# # Solicita al usuario el nombre para el archivo CSV
# csv_filename = csv_filename_input if csv_filename_input else CSV_DEFAULT_NAME

# # Asegurarse de que el nombre del archivo termine con ".csv"
# if not csv_filename.endswith(".csv"):
#     csv_filename += ".csv"

# # Combinar el directorio y el nombre del archivo
# full_csv_path = os.path.join(CSV_DIR, csv_filename)

# # Asegurarse de que el directorio para el archivo CSV exista
# if not os.path.exists(CSV_DIR):
#     os.makedirs(CSV_DIR)


# # Preguntar cuántos hilos/núcleos usar
# num_threads = int(input(
#     "Introduzca el número de hilos/núcleos a usar (presione 'Enter' para usar por defecto el número de núcleos de su máquina): ") or 0)

# # Lista para almacenar las coincidencias
# all_matching_links = []

# # Usar ThreadPoolExecutor para analizar URLs en paralelo
# consecutive_timeouts = 0
# with ThreadPoolExecutor(max_workers=num_threads or None) as executor:
#     results = list(tqdm(executor.map(lambda url: find_matching_links(
#         url, URL_TO_FIND), urls_to_analyze), total=len(urls_to_analyze), desc="Procesando URLs"))

#     for matching_links in results:
#         if matching_links == "timeout":
#             consecutive_timeouts += 1
#             if consecutive_timeouts == 3:
#                 print("3 timeouts consecutivos. Finalizando la ejecución.")
#                 exit()
#             continue
#         consecutive_timeouts = 0  # Reset the counter
#         all_matching_links.extend(matching_links)

# # Escribe los resultados en un archivo CSV
# with open(full_csv_path, mode='w', newline='') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(["Source", "Link", "Anchor", "Link Position"])
#     for match in all_matching_links:
#         writer.writerow([match[0], match[1], match[2], match[3]])

# print(f"Se encontraron y registraron las coincidencias en {full_csv_path}")
