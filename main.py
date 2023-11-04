import libcache
import link_scanner
import list_helper as helper


def main():
    # Explicar al usuario que debe de introducir varias urls en el archivo ./input/sitemap_list.txt
    # o la lista de urls_where_search.txt
    print("Este programa analizara un conjunto de URLs dado para encontrar en cada una de esas URLs, enlaces con codigos de errores 301.")
    # print("Para ello, introduzca las URls a analizar en el archivo 'input/urls_where_search.txt'")
    print("Para ello, introduzca las url/s del sitemap/s en el archivo 'input/sitemap_list.txt'", "\n")
    print("Se extraeran todas las urls contenidas en el/los sitemaps.")

    # Confirm execution
    confirm = input(
        "Pulse Enter para continuar o 'salir' para salir: ")
    print("\n")
    if confirm.lower() == "salir":
        print("Operación cancelada.")
        exit()

    # extract the url from sitemap and save it to urls_where_search
    print("\n", "#####################################", "\n")
    helper.save_urls_from_sitemaps_to_list()
    print("\n", "#####################################", "\n")
    url_list_dir = "input/urls_where_search.txt"

    # create cache
    print("Se va a proceder con creación de la cache, tenga en cuenta que esto puede demorar un poco dependiendo del numero de urls", "\n")
    print("Número de URls que se van a cachear:", len(
        helper.get_list_from_file(url_list_dir)))

    # Confirm execution
    print("Desea resetear la cache?")
    confirm = input(
        "Introduzca 'reset' para resetear o Enter para continuar: ")

    if confirm.lower() == "reset":
        print("\n", "#####################################", "\n")
        libcache.reset_cache()
        print("\n", "#####################################", "\n")
        print("Cache reseteada.")

    print("\n", "#####################################", "\n")
    libcache.save_url_list_to_cache(url_list_dir)
    print("\n", "#####################################", "\n")

    print("Se va a proceder con el analisis:", "\n")
    # Confirm execution
    confirm = input(
        "Pulse Enter para continuar o 'salir' para salir: ")
    if confirm.lower() == "salir":
        print("Operación cancelada.")
        exit()

    # find for 301 links inside each url in the list
    print("\n", "#####################################", "\n")
    link_scanner.analyze_filelist(url_list_dir)
    print("\n", "#####################################", "\n")

    # link_scanner_futures.analyze_filelist(url_list_dir)


if __name__ == "__main__":
    main()
