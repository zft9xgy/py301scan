import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import csv
import os
import concurrent.futures
from configparser import ConfigParser

# Script que buscara urls con codigos de error 301 en todas las urls proporcionadas en la lista urls.txt.
