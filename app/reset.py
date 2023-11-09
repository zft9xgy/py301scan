"""
Nombre del script: reset.py
Descripción: Este script elimina los directorios y los archivos y los vuelve a crear.
Autor: Rafael Cosquiere aka zft9xgy
Github: https://github.com/zft9xgy/py301scan
Fecha de creación: 09 de noviembre de 2023
Última modificación: 09 de noviembre de 2023
Versión: 1.0
"""

import configparser


# Reset the CSV file
def clean_file(file):
    try:
        open(file, "w").close()
        print(f"File '{file}' reset successfully.")
    except Exception as e:
        print(f"Error resetting the '{file}' file: {str(e)}")


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('./config.ini')

    CACHE_PATH = config['DEFAULT']['CACHE_PATH']
    INPUT_URLS_LIST = config['DEFAULT']['INPUT_URLS_LIST']
    INPUT_SITEMAPS_LIST = config['DEFAULT']['INPUT_SITEMAPS_LIST']
    OUTPUT_RAW = config['DEFAULT']['OUTPUT_RAW']


    # Reset the CSV file
    clean_file(OUTPUT_RAW)

    # Reset the lists file
    clean_file(INPUT_URLS_LIST)
    clean_file(INPUT_SITEMAPS_LIST)
