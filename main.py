from typing import List
import urllib.request as request
from urllib import parse
import json
import re
from bs4 import BeautifulSoup as bs


class Course:
    def __init__(self, name, link, access) -> None:
        self.name = name
        self.link = link
        self.access = access
        self.author = None
        self.desc = None
        self.__soup = None
        self.course_id = re.search(r"\d+", self.link).group(0)

    def __fetch(self):
        data = parse.urlencode({'courseid': self.course_id, 'type': 1}).encode()
        req = request.Request(
            'https://moodle.univ-chlef.dz/fr/course/category.ajax.php', data=data)
        with request.urlopen(req) as body:
            # fixme: Fix Unicode problem with special caracters, request returns javascript caracters coding
            body = str(body.read()).replace('\\', '').replace('u00e9', 'é').replace(
                'u00e8', 'è').replace('u00e0', 'à').replace('u2019', "'")
            self.__soup = bs(body.encode('utf8'), 'html.parser')

    def course_info(self):
        """
            Start a Fetch request to get cousre info

        Returns:
            dict: all course infos
        """
        if self.__soup is None:
            self.__fetch()

        for p_element in self.__soup.find_all('p'):
            self.desc = p_element.getText()

        self.author = self.__soup.select('a')[0].getText()
        return ({'id': self.course_id,
                 'name': self.name,
                 'link': self.link,
                 'access': self.access,
                 'author': self.author,
                 'description': self.desc})


class MoodleApi:
    def __init__(self) -> None:
        self.__ids = []
        self.__soup = None

    def get_faculties(self) -> List:
        with request.urlopen('https://moodle.univ-chlef.dz/fr') as body:
            self.__soup = bs(body.read(), 'html.parser')
        faculties = []
        elements = self.__soup.select('h3.categoryname')
        for element in elements:
            fac_names = element.select('a')[0].string
            link = element.select('a')[0]["href"]
            faculties.append([fac_names, link])

        return faculties

    def __search(self, arr, selector, n=0):
        matches = []
        for element in arr:
            if selector[n] in element:
                matches.append(element)
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
            with open('id.txt', 'r') as file:
                self.__ids = json.load(file)
        self.__fetch(self.__search(self.__ids, selector.split('.')))
        return self

    def __fetch(self, id) -> None:
        with request.urlopen('https://moodle.univ-chlef.dz/fr/course/index.php?categoryid={}&perpage=100'.format(id)) as body:
            self.__soup = bs(body.read(), 'html.parser')

    def __parse_access(self, links):
        if links:
            for link in links:
                return 'password' if 'withpassword' in link['src'] else 'public'
        else:
            return 'private'

    def get_courses(self) -> List:
        """
        return list of courses

        Returns:
            List: list containing all courses
        """
        courses = []
        elements = self.__soup.find_all(attrs={"data-courseid": True})
        for element in elements:
            name = element.select('.coursename')[0].string
            link = element.select('.coursename')[0].select('a')[0]['href']
            access = element.select('div.enrolmenticons>img')
            courses.append(Course(name, link, self.__parse_access(access)))
        return courses
