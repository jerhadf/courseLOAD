from bs4 import BeautifulSoup # python web scraping library
import urllib3 # tool for opening URLs with HTTP requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from pprint import pprint # pretty print
import json

# get the department dictionary from the json
with open('data/departments.json') as json_file:  
    dept_data = json.load(json_file)

dept_codes = list(dept_data.keys())

def get_courses(department):
    """
    Grabs the course list info for the given department
    @arg department -- the academic department (ex/ "COSC")
    """
    
    http = urllib3.PoolManager()

    url = f'https://www.layuplist.com/search?q={department}'
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features="html.parser")
    page_source = soup.prettify()

    # save the BeautifulSoup page source to a txt file
    with open(f"sources/{department}_source.txt", 'w') as fp:
        json.dump(page_source, fp)

    # function to remove <td> tags from a string
    remove_tags = lambda element : (element
        .replace("<td><a>", "")
        .replace("</a></td>", "")
        .replace("<td>", "")
        .replace("</td>", "")
        .strip())

    # keeps track of course offerings for given departments
    course_dict = {}     # course_code : course_desc, distribs, offered, url

    # finds all the <tr> elements in the page source
    for element in soup.find_all('tr'):
        """
        1. get all the <tr> elements
        2. grab the onclick attribute as string and save it 
        3. grab the course URL from it: e.g. `/course/681` for COSC 1 
        4. save the course urls as dictionary with key-value pairs of 
        "COURSE NAME" : "URL" ex/ "COSC 1" : "/course/681"
        4. loop through all of the course URLs and navigate to them iteratively 
        5. scrape each of the course webpages for medians/prof reviews/boolean of whether offered 19S
        """
        # grabs the <td> children of the <tr> element and cleans them up 
        children = list(element.findChildren("td" , recursive=False))
        children = list(map(str, children)) # convert elements to str

        # grabs each value and cleans it up 
        name = children[0].split('<')[2].split(': ') # gets the full course name

        course_desc = name[1]
        course_code = name[0][2:]
        offered = True if "Offered" in children[1] else False # gets whether it's offered in term
        url = element.get("onclick").split("=")[1][1:-2] # grabs the url of the course (ex/ '/course/681')
        url = f"https://www.layuplist.com{url}" # saves the full layuplist url
        distribs = remove_tags(children[2]).split() # saves the distributives for this course

        # save the data to the course dictionary 
        course_dict[course_code] = { 
            "course_desc": course_desc, 
            "offered" : offered, 
            "url": url,
            "distribs": distribs
        }

    return course_dict
    
all_course_urls = []

for department in dept_codes: 
    # don't know why but this department doesn't have a course list
    if department == "SSOC": continue  
    # save course info for every department
    print(f"\n **** COURSE INFO FOR {department} ****: \n")
    course_info = get_courses(department)
    urls = [key['url'] for key in list(course_info.values())]
    all_course_urls += urls

    # # saves the department dict to a json file
    # with open(f'data/{department}_dict.json', 'w') as fp:
    #     json.dump(course_info, fp)

all_courses_dict = {
    "all_courses" : all_course_urls
}

with open(f'all_course_urls.json', 'w') as fp:
    json.dump(all_courses_dict, fp)  