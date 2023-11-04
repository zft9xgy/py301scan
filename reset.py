import shutil
import os


# Clear the cache directory
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

    # Cache directory path
    cache_directory = "./cache"
    # Clear the cache directory
    clear_cache(cache_directory)

    # CSV file path to reset
    csv_file = "./csv/raw_scan.csv"
    # Reset the CSV file
    reset_csv(csv_file)

    # File list file path to reset
    list_file = "./input/urls_where_search.txt"
    # Reset the CSV file
    reset_csv(list_file)
