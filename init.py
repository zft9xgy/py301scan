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


# Reset the file
def clean_file(file):
    try:
        open(file, "w").close()
        # print(f"File '{file}' reset successfully.")
    except Exception as e:
        print(f"Error resetting the '{file}' file: {str(e)}")


def create_dir_if_not_exist(dir_dir):
    if not os.path.exists(dir_dir):
        os.mkdir(dir_dir)
        # print("Creada CSV path:",dir_dir)


def create_file_if_not_existe(file_dir):
    if not os.path.exists(file_dir):
        with open(file_dir, "w") as file:
            # print("Creado output csv file:",file_dir)
            return


def main():

    CSV_PATH = "./csv"
    INPUT_PATH = "./input"
    INPUT_URLS_LIST = "./input/urls_list.txt"
    INPUT_SITEMAPS_LIST = "./input/sitemap_list.txt"
    OUTPUT_RAW = "./csv/raw_scan.csv"

    # Create directories
    create_dir_if_not_exist(CSV_PATH)
    create_dir_if_not_exist(INPUT_PATH)

    create_file_if_not_existe(OUTPUT_RAW)
    create_file_if_not_existe(INPUT_SITEMAPS_LIST)
    create_file_if_not_existe(INPUT_URLS_LIST)

    clean_file(INPUT_URLS_LIST)
    clean_file(OUTPUT_RAW)

    # escribe cabecera en csv si no existe ya
    if os.stat(OUTPUT_RAW).st_size == 0:
        with open(OUTPUT_RAW, "a") as file:
            file.write("status_code,link,source_url,anchor,tag_location" + "\n")

    print("Ready to go...")


if __name__ == "__main__":
    main()
