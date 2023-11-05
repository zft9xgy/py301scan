import os
import configparser


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
    if not os.path.exists(CSV_PATH):
        os.mkdir(CSV_PATH)
        print("Creada CSV path:",CSV_PATH)

    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)
        print("Creada Cache path:",CACHE_PATH)

    if not os.path.exists(INPUT_PATH):
        os.mkdir(INPUT_PATH)
        print("Creada Input path:",INPUT_PATH)

    # Create default files
    if not os.path.exists(OUTPUT_RAW):
        with open(OUTPUT_RAW, "w") as file:
            print("Creado output csv file:",OUTPUT_RAW)
        with open(OUTPUT_RAW,"a") as file:
            file.write("status_code,link,source_url,anchor,tag_location" + "\n")
            print("Output csv file, inicializado.")
            return


    if not os.path.exists(INPUT_SITEMAPS_LIST):
        with open(INPUT_SITEMAPS_LIST, "w") as file:
            print("Creada lista de sitemaps:",INPUT_SITEMAPS_LIST)
            return

    if not os.path.exists(INPUT_URLS_LIST):
        with open(INPUT_URLS_LIST, "w") as file:
            print("Creada lista de urls:",INPUT_URLS_LIST)
            return


if __name__ == "__main__":
    main()
