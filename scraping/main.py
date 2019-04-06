from bs4 import BeautifulSoup # python web scraping library
import urllib3 # tool for opening URLs with HTTP requests
from pprint import pprint # pretty print
import json

http = urllib3.PoolManager()

url = 'https://www.layuplist.com/search?q=COSC'
response = http.request('GET', url)
soup = BeautifulSoup(response.data)
page_source = soup.prettify()

# print(page_source)
print(soup.title)

for link in soup.find_all('a'):
    print(link.get('href'))

with open("page_souce.txt", 'w') as fp:
    json.dump(page_source)
    

# Take out the <div> of name and get its value
# name_box = soup.find(‘h1’, attrs={‘class’: ‘name’})

# # specify the layuplist url - searching for COSC courses
# layuplist = "https://www.layuplist.com/search?q=COSC"

# # query the website and return the html to the variable ‘page’
# page = urllib3.urlopen(layuplist)

# # parse the html using beautiful soup and store in variable `soup`
# soup = BeautifulSoup(page, 'html.parser')

# print(page)