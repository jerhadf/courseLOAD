from bs4 import BeautifulSoup # python web scraping library
import urllib3 # tool for opening URLs with HTTP requests
from pprint import pprint # pretty print
import json

http = urllib3.PoolManager()

departments = ["COSC", "PHIL", "HIST", "ENGS", "MATH"] # list of departments 

url = f'https://www.layuplist.com/search?q={departments[0]}'
response = http.request('GET', url)
soup = BeautifulSoup(response.data)
page_source = soup.prettify()

# save the BeautifulSoup page source to a txt file
with open("page_source.txt", 'w') as fp:
    json.dump(page_source, fp)

# 1. get all the <tr> elements
# 2. grab the onclick attribute as string and save it 
# 3. grab the course URL from it: e.g. `/course/681` for COSC 1 
# 4. save the course urls as dictionary with key-value pairs of 
# "COURSE NAME" : "URL" ex/ "COSC 1" : "/course/681"
# 4. loop through all of the course URLs and navigate to them iteratively 
# 5. scrape each of the course webpages for medians/prof reviews/boolean of whether offered 19S

url_list = []

course_dict = {"COSC 01": {"url":"/course/680", "desc":"Introduction to Programming and Computation", "offered19S": True, "distrib":"TLA", }}

for element in soup.find_all('tr'):
    children = list(element.findChildren("td" , recursive=False))
    url = element.get("onclick").split("=")[1][1:-2] # grabs the url of the course (ex/ '/course/681')
    url_list.append(url)

print(url_list)

# Take out the <div> of name and get its value
# name_box = soup.find(‘h1’, attrs={‘class’: ‘name’})

# # specify the layuplist url - searching for COSC courses
# layuplist = "https://www.layuplist.com/search?q=COSC"

# # query the website and return the html to the variable ‘page’
# page = urllib3.urlopen(layuplist)

# # parse the html using beautiful soup and store in variable `soup`
# soup = BeautifulSoup(page, 'html.parser')

# print(page)