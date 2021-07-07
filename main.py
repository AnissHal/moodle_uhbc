from typing import List
from bs4 import BeautifulSoup as bs
import urllib.request as request
import json


class Course:
    def __init__(self, name, link) -> None:
        self.name = name
        self.link = link

class MoodleApi:
    def __init__(self) -> None:
        self.__ids = []

    def get_faculties(self) -> List:
        with request.urlopen('https://moodle.univ-chlef.dz/fr') as fp:
            self.soup = bs(fp.read(), 'html.parser')
        faculties = []
        elements = self.soup.select('h3.categoryname')
        for element in elements:
            fac_names = element.select('a')[0].string
            link = element.select('a')[0]["href"]
            faculties.append([fac_names, link])

        return faculties

    def __search(self, arr, selector, n=0):
        matches = []
        for e in arr:
            if selector[n] in e:
                matches.append(e)
        if n+1 == len(selector):
            return matches[-1][-1]
        return self.__search(matches, selector, n+1)

    def select(self, selector) -> 'MoodleApi':
        """
        select faculty or departement or level
        
        :param selector(str): selector

        Returns:
            MoodleApi: return self
        """
        if not self.__ids:
            with open('id.txt', 'r') as f:
                self.__ids = json.load(f)
        self.__fetch(self.__search(self.__ids, selector.split('.')))
        return self

    def __fetch(self, id) -> None:
        with request.urlopen('https://moodle.univ-chlef.dz/fr/course/index.php?categoryid={}&perpage=100'.format(id)) as fp:
            self.soup = bs(fp.read(), 'html.parser')

    def get_courses(self) -> List:
        """
        return list of courses

        Returns:
            List: list containing all courses
        """
        courses = []
        elements = self.soup.find_all(attrs={"data-courseid": True})
        for element in elements:
            name = element.select('.coursename')[0].string
            link = element.select('.coursename')[0].select('a')[0]['href']
            courses.append(Course(name, link))
        return courses
