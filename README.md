# py301scan

This script is intended to help the user find links with status codes other than 200, and to help locate them on the web so they can be rectified at source.

## Disclaimer

This project was made with a particular case in mind and for the purpose of learning python, so many parts of the code may not be optimised.

Also, the code is not stable and is not efficient for websites with more than 100 urls.

Full development will be continued in the indefinite future.

## Installation

```sh
git clone https://github.com/zft9xgy/py301scan.git
cd py301scan
pip3 install -r requirements.txt
python3 init.py
```

## Usage

The script is intended to take a list of sitemaps from the `input/sitemap_list.txt` file, one on each line. If you only have one, you can leave only one.

To run the script:

```sh
python3 main.py
```

## Result

You can find a csv file in `csv/raw_scan.csv` with the following header

```csv
status_code,source_url,link,anchor,tag_location
```

## TL;DR

In the first version of this script, I tried to go too far and add, or wanted to add, too much functionality so that users without programming skills could use it, but that led to the failure of the project, because I didn't have the experience and knowledge to meet my expectations.

Simplifying this project has allowed me to close it and continue with the next one so I can come back here in the future and develop it as it should be.

If you have read this far and would like to comment or discuss further, feel free to open an issue or write to me at zft9xgy@proton.me.
