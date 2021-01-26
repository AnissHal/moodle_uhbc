from bs4 import BeautifulSoup
import urllib.request

with urllib.request.urlopen('https://moodle.univ-chlef.dz/fr/course/index.php?categoryid=156') as fp:
    soup = BeautifulSoup(fp.read(), 'html.parser')

courses = soup.find_all(attrs= {"data-courseid" : True})

for course in courses:
    course_name = course.select('h3.coursename')
    course_link = course.select('a')
    print(course_name[0].string)
    print(course_link[0]['href'])