import os
import configparser

# Load the configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Read URLs from the specified URLS_FILE
with open(config['DEFAULT']['URLS_FILE'], "r") as file:
    urls = file.read().splitlines()

# Dictionary to map URL prefixes to lists and directories
url_lists = dict(config.items('URL_PREFIXES'))

# Default list for URLs that do not match the specified prefixes
default_list = config['DEFAULT']['DEFAULT_LIST']

# Function to append URL to an existing list or create one if it doesn't exist


def append_to_list(url, list_filename):
    # Ensure it's not the cache directory
    if os.path.isdir(list_filename):
        print(
            f"Error: {list_filename} is a directory, not a valid file. Skipping...")
        return

    # If directory does not exist, create it
    if not os.path.exists(os.path.dirname(list_filename)):
        os.makedirs(os.path.dirname(list_filename))

    with open(list_filename, "a") as list_file:
        list_file.write(url + "\n")


# Classify URLs into corresponding lists
for url in urls:
    categorized = False
    for prefix, list_filename in url_lists.items():
        if prefix in url:
            append_to_list(url, list_filename)
            categorized = True
            break
    if not categorized:
        append_to_list(url, default_list)

# Print the number of URLs in each list
for list_filename in url_lists.values():
    if os.path.isfile(list_filename):  # Check if it's a file and not a directory
        with open(list_filename, "r") as list_file:
            num_urls = sum(1 for _ in list_file)
            print(f"{list_filename}: {num_urls} URL(s)")

# You can access the individual URL lists using the files in the specified directories.
