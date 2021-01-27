from bs4 import BeautifulSoup
import urllib.request
import webbrowser
import questionary
import time

with urllib.request.urlopen('https://moodle.univ-chlef.dz/fr/') as fp:
    soup = BeautifulSoup(fp.read(), 'html.parser')



def get_category_names(soup):
    faculty_choices = []
    main_categroies = soup.select('h3.categoryname')
    for d in main_categroies:
        fac_names = d.select('a')[0].string
        faculty_choices.append(fac_names + ' ->')
    
    return faculty_choices


def get_category_links(soup):
    main_categroies = soup.select('h3.categoryname')
    faculty_links = []

    for d in main_categroies:
        links = d.select('a')[0]["href"]
        faculty_links.append(links)

    return faculty_links


links = get_category_links(soup)
choices = get_category_names(soup)


choosen_fac = questionary.select(
    "CHOOSE YOUR FACULTY",
    choices=choices
).ask()



with urllib.request.urlopen(links[choices.index(choosen_fac)]) as fp:
    soup = BeautifulSoup(fp.read(), 'html.parser')



links = get_category_links(soup)
choices = get_category_names(soup)


choosen_fac = questionary.select(
    "CHOOSE YOUR DEPERTEMENT",
    choices=choices
).ask()

with urllib.request.urlopen(links[choices.index(choosen_fac)]) as fp:
    soup = BeautifulSoup(fp.read(), 'html.parser')

courses = soup.find_all(attrs= {"data-courseid" : True})


links = get_category_links(soup)
choices = get_category_names(soup)

course_name = []
course_link = []

def get_courses(courses):
    for course in courses:
        try:
            name = course.select('div.coursename')[0].string
            link = course.select('div.coursename')[0].select('a')[0]['href']
        except IndexError:
            name = course.select('h3.coursename')[0].string  
            link = course.select('h3.coursename')[0].select('a')[0]['href']
        course_name.append(name + ' [COURS]')
        course_link.append(link)



get_courses(courses)

choices.extend(course_name)
if choices:
    choosen_lesson = questionary.select(
    "CHOOSE YOUR LEVEL",
    choices=choices
    ).ask()

else: 
    print('NO LESSONS YET')
    time.sleep(2)
    exit()

if '->' in choosen_lesson:
    with urllib.request.urlopen(links[choices.index(choosen_lesson)]) as fp:
        soup = BeautifulSoup(fp.read(), 'html.parser')

    courses = soup.find_all(attrs= {"data-courseid" : True})

    course_name = []
    course_link = []
    get_courses(courses)

    course_name = []
    course_link = []
    get_courses(courses)
    choosen_lesson = questionary.select(
    "CHOOSE YOUR COURSE",
    choices=course_name
    ).ask()
    webbrowser.open(course_link[course_name.index(choosen_lesson)])
else:
    print(course_link[course_name.index(choosen_lesson)])
    webbrowser.open(course_link[course_name.index(choosen_lesson)])