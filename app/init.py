"""
Nombre del script: init.py
Descripción: Este script cumprueba que los ficheros y directorios existan y en caso de que no existan, los crea.
Autor: Rafael Cosquiere aka zft9xgy
Github: https://github.com/zft9xgy/py301scan
Fecha de creación: 09 de noviembre de 2023
Última modificación: 09 de noviembre de 2023
Versión: 1.0
"""

import os
import configparser


# Reset the file
def clean_file(file):
    try:
        open(file, "w").close()
        #print(f"File '{file}' reset successfully.")
    except Exception as e:
        print(f"Error resetting the '{file}' file: {str(e)}")


def create_dir_if_not_exist(dir_dir):
    if not os.path.exists(dir_dir):
        os.mkdir(dir_dir)
        #print("Creada CSV path:",dir_dir)


def create_file_if_not_existe(file_dir):
    if not os.path.exists(file_dir):
        with open(file_dir, "w") as file:
            #print("Creado output csv file:",file_dir)
            return




def main():

    config = configparser.ConfigParser()
    config.read('config.ini')

    CACHE_PATH = config['DEFAULT']['CACHE_PATH']
    CSV_PATH = config['DEFAULT']['CSV_PATH']
    INPUT_PATH = config['DEFAULT']['INPUT_PATH']
    INPUT_URLS_LIST = config['DEFAULT']['INPUT_URLS_LIST']
    INPUT_SITEMAPS_LIST = config['DEFAULT']['INPUT_SITEMAPS_LIST']
    OUTPUT_RAW = config['DEFAULT']['OUTPUT_RAW']

    # Create directories
    create_dir_if_not_exist(CSV_PATH)
    create_dir_if_not_exist(CACHE_PATH)
    create_dir_if_not_exist(INPUT_PATH)

    create_file_if_not_existe(OUTPUT_RAW)
    create_file_if_not_existe(INPUT_SITEMAPS_LIST)
    create_file_if_not_existe(INPUT_URLS_LIST)

    clean_file(INPUT_URLS_LIST)
    clean_file(OUTPUT_RAW)


    # escribe cabecera en csv si no existe ya
    if os.stat(OUTPUT_RAW).st_size == 0:
        with open(OUTPUT_RAW,"a") as file:
            file.write("status_code,link,source_url,anchor,tag_location" + "\n")

    print("Ready to go...")



if __name__ == "__main__":
    main()