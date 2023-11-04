import os


def main():

    # Create directories
    if not os.path.exists("./csv"):
        os.mkdir("./csv")

    if not os.path.exists("./cache"):
        os.mkdir("./cache")

    if not os.path.exists("./input"):
        os.mkdir("./input")

    # Create default files
    if not os.path.exists("./csv/raw_scan.csv"):
        with open("./csv/raw_scan.csv", "w") as archivo:
            # This will create the file.
            return

    if not os.path.exists("./input/sitemap_list.txt"):
        with open("./input/sitemap_list.txt", "w") as archivo:
            # This will create the file.
            return

    if not os.path.exists("./input/urls_where_search.csv"):
        with open("./input/urls_where_search.txt", "w") as archivo:
            # This will create the file.
            return


if __name__ == "__main__":
    main()
