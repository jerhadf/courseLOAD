from bs4 import BeautifulSoup # python web scraping library
import urllib3 # tool for opening URLs with HTTP requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from pprint import pprint # pretty print
import json

url_list = 