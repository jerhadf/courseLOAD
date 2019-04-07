from bs4 import BeautifulSoup # python web scraping library
import urllib3 # tool for opening URLs with HTTP requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from pprint import pprint # pretty print
import json
import mechanize
import urllib2 
import cookielib

# login to LayupList


def get_course_urls(dept): 
    """ 
    Returns a list of all the course urls in the given department
    """
    with open(f"data\{dept}_dict.json", 'r') as fp:
        dept_dict = json.load(fp)
        dept_urls = [k['url'] for k in list(dept_dict.values())]
        return dept_urls

def get_prof_urls(course_url):
    """
    Get all the professor review urls for the given course url
    """
    http = urllib3.PoolManager()
    response = http.request('GET', course_url) # open the course url page
    soup = BeautifulSoup(response.data, features="html.parser")
    page_source = soup.prettify()

    prof_urls = []
    for element in soup.find_all('tr'): 
        onclick = element.get("onclick")
        if (onclick is not None) and ("review_search" in onclick):
            prof_url = onclick.split("'")[1].replace(" ", "%20")
            prof_urls.append(
                f"https://www.layuplist.com{prof_url}")

    return prof_urls

def get_prof_reviews(prof_url): 
    #! YOU NEED TO BE LOGGED IN TO SEE REVIEWS .... UGH
    http = urllib3.PoolManager()
    response = http.request('GET', prof_url) # open the course url page
    soup = BeautifulSoup(response.data, features="html.parser")
    page_source = soup.prettify()

    print(prof_url)

    for element in soup.find_all('td'): 
        print(element)

cosc_urls = get_course_urls("COSC")
CS1_url = cosc_urls[0]
CS1_prof_urls = get_prof_urls(CS1_url)
get_prof_reviews(CS1_prof_urls[0])

# get a list of all the course urls in the COSC department


