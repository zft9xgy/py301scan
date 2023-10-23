# py301scan

The `py301scan` project aims to help users manage and rectify URLs on large or multilingual websites. It assists in extracting all URLs from a website, identifying those with 301 redirects, and subsequently locating these URLs in the original list to facilitate their correction.

> **Notice:**
> The project is still very new and may have some bugs, I would greatly appreciate if you could add an issue or contact me by email zft9xgy@proton.me if you find any bugs, errors or would like to add new features.

## **Project Stages:**

1. **URL Extraction:**

   - Manually: by directly adding to `urls.txt`.
   - Using the `get-urls-from-sitemap.py` script: Extract all URLs from a website's sitemap.

2. **Broken Links Identification:**

   - Pending Development: A script will find links that return 301 error codes and list them.

3. **Localization and Correction:**
   - Use the `alpha-find.py` script: Find specific URLs in the original list.

## **Installation & Setup:**

### **1. Installation:**

1. Ensure you have [Python 3](https://www.python.org/downloads/) installed on your computer.
2. Clone the `py301scan` project to your local machine.
3. Navigate to the project folder in your terminal or command prompt.
4. Install necessary packages.

   ```bash

   git clone https://github.com/zft9xgy/py301scan.git
   cd py301scan
   pip3 install -r requirements.txt
   ```

### **2. Configuration:**

1. Modify the `config.ini` to set necessary parameters, like:
   - `CACHE_DIR`: Where the cached content will be stored.
   - `URLS_FILE`: Name of the file that will contain the list of URLs.
   - `DEFAULT_LIST`: Default list of URLs.
   - `SITEMAP_URL`: The sitemap URL from which to extract links.
   - `URL_TO_FIND`: Specific URL you want to search for.
   - `CSV_DEFAULT_NAME`: Default name for CSV outputs.
   - `CSV_FOLDER`: Directory where CSV files will be stored.

### **3. Usage:**

1. If you don't have a list of URLs and want to generate one from a sitemap:

   ```bash
   python3 get-urls-from-sitemap.py
   ```

2. To cache the webpages locally for faster repeated checks, use:

   ```bash
   python3 create-cache.py
   ```

3. To search for a specific URL within your list:

   ```bash
   python3 alpha-find.py
   ```

4. (Pending) Once the 301 checker is developed, it will be added to the usage steps.

## **Additional Notes:**

- **Understanding the Config File:** The `config.ini` file allows you to set parameters without having to delve into the code. Ensure the sections in this file match your needs. If unfamiliar, it's best to stick to the provided defaults.

- **Cache Management:** The `create-cache.py` script caches web pages to speed up repeated checks. Make sure to have enough storage, as large websites can take up significant space.

- **About the Project:** This tool was developed to address specific needs for large or multilingual websites. As the project grows, more functionalities will be added to enhance its scope and efficiency.

## Note about urls-clasify.py

### Purpose:

This script is designed to handle multilingual websites. When given a list of URLs from a website, it segregates them based on the language or specific prefix in the URL. This categorization facilitates language-specific analysis later on, especially when using the alpha-find script.

### How to Use:

- 1 Make sure you have a file named urls.txt containing the URLs of the multilingual website you wish to analyze.
- 2 Run the urls-clasify.py script.
- 3 Based on the defined prefixes or language indicators in the URL, the script will categorize and save them into separate files. For instance, URLs with a "/es/" prefix indicating Spanish content might be saved to urls/es.txt.

Note: The use of this script is specific and might not be necessary for every user. It's a custom solution designed for the specific needs of handling URLs from multilingual websites. After categorizing, when using the alpha-find script, one can easily switch to the URL list of a specific language.

## TODO

- develop 301 link finder
- alpha-find.py, ask for cache use.
- cache directory, one cache directory per website maybe?
