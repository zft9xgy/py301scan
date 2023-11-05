import shutil
import os
import configparser


# delete directory and create again
def clear_cache(directory):
    try:
        shutil.rmtree(directory)
        os.mkdir(directory)
        print(f"Contents of the '{directory}' directory cleared successfully.")
    except Exception as e:
        print(f"Error clearing the '{directory}' directory: {str(e)}")


# Reset the CSV file
def reset_csv(file):
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

    # Clear the cache directory
    clear_cache(CACHE_PATH)

    # Reset the CSV file
    reset_csv(OUTPUT_RAW)

    # Reset the lists file
    reset_csv(INPUT_URLS_LIST)
    reset_csv(INPUT_SITEMAPS_LIST)
