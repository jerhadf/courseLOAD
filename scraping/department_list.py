from bs4 import BeautifulSoup # python web scraping library
import urllib3 # tool for opening URLs with HTTP requests
from pprint import pprint # pretty print
import json
# find dartmouth page with the department code list and scrape it into a list

# list of data types for departments
dept_names = [] # full name of dept
dept_codes = [] # code for the dept
course_nums = [] # number of courses offered for the dept
dept_dict = {}

def get_dept_names():
    """
    Grabs the dept name info for the given department code
    @arg department -- the academic department (ex/ "COSC")
    """
    
    http = urllib3.PoolManager()

    url = "https://www.layuplist.com/departments"
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features="html.parser")
    page_source = soup.prettify()

    # function to remove <td> tags from a string
    remove_tags = lambda element : element.replace("<td><a>", "").replace("</a></td>", "").strip()

    # finds all the <tr> elements in the page source
    for element in soup.find_all('tr'):
        """
        Save department codes to a list
        """
        # grabs the <td> children of the <tr> element and cleans them up 
        children = list(element.findChildren("td" , recursive=False))
        children = list(map(str, children)) # convert elements to str

        # grabs each value and cleans it up
        deptcode = remove_tags(children[0]) # gets the code
        deptname = remove_tags(children[1])
        coursenum = remove_tags(children[2])

        # if it doesn't have a department name, use the department code as the name
        if deptname == "<td></td>": 
            deptname = deptcode

        # save the data to the department dictionary ///////////EDIT
        dept_codes.append(deptcode)
        dept_names.append(deptname)
        course_nums.append(coursenum)

        dept_dict[deptcode] = {
            "dept_name" : deptname, # the full name of department
            "course_num" : course_nums # the number of courses offered in department
        }
        
        return dept_dict

pprint(get_dept_names())

# for department in departments: 
#     course_info = get_courses(department)
#     print(f"\n COURSE INFO FOR {department}: \n")
#     pprint(course_info)
