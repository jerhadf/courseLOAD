from bs4 import BeautifulSoup # python web scraping library
import urllib3 # tool for opening URLs with HTTP requests
from pprint import pprint # pretty print
import json

# list of department codes
departments = ['AAAS', 'AMEL', 'AMES', 'ANTH', 'ARAB', 'ARTH', 'ASCL', 'ASTR', 'BIOL', 'CHEM', 'CHIN', 'CLST', 'COCO', 'COGS', 'COLT', 'COSC', 'CRWT', 'EARS', 'ECON', 'EDUC', 'ENGL', 'ENGS', 'ENVS', 'FILM', 'FREN', 'FRIT', 'GEOG', 'GERM', 'GOVT', 'GRK', 'HEBR', 'HIST', 'HUM', 'INTS', 'ITAL', 'JAPN', 'JWST', 'LACS', 'LAT', 'LATS', 'LING', 'MATH', 'MES', 'MUS',
'NAS', 'PBPL', 'PHIL', 'PHYS', 'PORT', 'PSYC', 'QSS', 'REL', 'RUSS', 'SART', 'SOCY', 'SPAN', 'SPEE', 'SSOC', 'THEA', 'TUCK', 'WGSS', 'WRIT']

def get_courses(department):
    """
    Grabs the course list info for the given department
    @arg department -- the academic department (ex/ "COSC")
    """
    
    http = urllib3.PoolManager()

    url = f'https://www.layuplist.com/search?q={department}'
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data)
    page_source = soup.prettify()

    # save the BeautifulSoup page source to a txt file
    with open(f"sources/{department}_source.txt", 'w') as fp:
        json.dump(page_source, fp)

    # function to remove <td> tags from a string
    clean_td = lambda element : element.replace("<td>", "").replace("</td>", "").strip()

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
        distribs = clean_td(children[2]).split() # saves the distributives for this course

        # save the data to the course dictionary 
        course_dict[course_code] = { 
            "course_desc": course_desc, 
            "offered" : offered, 
            "url": url,
            "distribs": distribs
        }

        pprint(course_dict)
        return course_dict

for department in departments: 
    course_info = get_courses(department)
    print(f"\n COURSE INFO FOR {department}: \n")
    pprint(course_info)
# Take out the <div> of name and get its value
# name_box = soup.find(‘h1’, attrs={‘class’: ‘name’})

# # specify the layuplist url - searching for COSC courses
# layuplist = "https://www.layuplist.com/search?q=COSC"

# # query the website and return the html to the variable ‘page’
# page = urllib3.urlopen(layuplist)

# # parse the html using beautiful soup and store in variable `soup`
# soup = BeautifulSoup(page, 'html.parser')

# print(page)