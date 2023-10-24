import os
import requests
import hashlib
import configparser
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import shutil

# Leer configuración desde config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Variables de configuración
cache_dir = config['DEFAULT']['CACHE_DIR']
URLS_FILE = config['DEFAULT']['URLS_FILE']
MAX_WORKERS_DEFAULT = os.cpu_count()

# input url, return bool


def is_url_in_cache(url):
    filename = hashlib.md5(url.encode()).hexdigest() + ".html"
    filepath = os.path.join(cache_dir, filename)
    return os.path.exists(filepath)


# Asegurarse de que el directorio cache existe
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)


def save_content_to_cache(url):
    """ Save URL content to cache directory """
    filename = hashlib.md5(url.encode()).hexdigest() + ".html"
    filepath = os.path.join(cache_dir, filename)

    if os.path.exists(filepath):
        return  # If the file already exists, just return (it's already cached)

    content = requests.get(url).text
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)


# Read the URL list
with open(URLS_FILE, "r") as file:
    urls = file.read().splitlines()

print(f"URLs to cache from: {URLS_FILE}")
print(f"Number of URLs to cache: {len(urls)}")

# Confirm execution
confirm = input(
    "Do you want to proceed with caching? (press enter for yes/no): ")
if confirm.lower() == "no":
    print("Operation cancelled.")
    exit()

# Ask if the user wants to reset the cache
reset_cache = input(
    "Do you want to reset the cache? (yes/press enter for no): ")
if reset_cache.lower() == "yes":
    shutil.rmtree(cache_dir)  # Remove the entire cache directory
    os.makedirs(cache_dir)  # Create an empty cache directory

# Ask the user for the number of workers
try:
    max_workers = int(input(
        f"Enter the number of workers (press enter for default {MAX_WORKERS_DEFAULT}): "))
except ValueError:
    max_workers = MAX_WORKERS_DEFAULT

# Use concurrency to save the URLs to cache
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Display progress bar with tqdm
    list(tqdm(executor.map(save_content_to_cache, urls),
         total=len(urls), desc="Caching URLs"))

print("Cache created.")
