# Moodle Api
## Introduction
Not official api to access UHBC (Université de Hassiba benbouali) courses and list all faculties using webscraping since there's no official api
## Pre-requists
This library requires `BeautifulSoup` library to work and Python version `3.x`
## How it works
### Usage
```py
api = MoodleApi() # Create a new instance
faculties = api.get_faculties() # returns list of all faculties available in moodle
>>> [['Faculté de Technologie', 'https://moodle.univ-chlef.dz/fr/course/index.php?categoryid=2'], ...]
selected_faculty = api.select('technologie.electronique.l2') # Select faculty of science and technology of the departement of second year
courses = selected_faculty.get_courses() # returns a list of element Courses
courses = api.select('technologie.electronique.l2').get_courses() # You can chain methods
for course in courses:
  print(course.name) # Course name TP: Logique combinatoire et séquentielle 
  print(course.link) # Course link https://moodle.univ-chlef.dz/fr/course/view.php?id=396
  print(course.access) # see if the course is public or private or requires key password to access
  info = course.course_info() # this will start a fetch request | returns dict with all info course
  course.is_public() # returns True if the course is available to guest users and False if private or requires password
```
### Selector
The selector works like css selector it starts with faculty name to departemnt name to study year and separated by a `.`
selector are in french language and spaces are replaced with `_` and some faculties and departements had been truncated
you can read `id.txt` file to see all selectors possible
| Faculty name selector                              | Faculty name (French)                                                     |
|----------------------------------------------------|---------------------------------------------------------------------------|
| technologie                                        | Faculté de Technologie                                                    |
| langues_etrengeres                                 | Faculté des Langues Étrangères                                            |
| sciences_nature_vie                                | Faculté des Sciences de La Nature et de La Vie                            |
| genie_civil_architecture                           | Faculté de Génie Civil et D'Architecture                                  |
| sciences_exactes_informatique                      | Faculté des Sciences Exactes et Informatique                              |
| sciences_economiques_commerciales_sciences_gestion | Faculté des Sciences Économique, Commerciales, et des Sciences de Gestion |
| lettres_arts                                       | Faculté des Lettres et Arts                                               |
| sciences_humaines_sociales                         | Faculté des Sciences Humaines et Sociales                                 |
| droit_sciences_politiques                          | Faculté de Droit et des Sciences Politiques                               |
| education_physique_sportive                        | Institut d'Éducation Physique et Sportive                                 |
| intensif_langues                                   | Centre d'Enseignement Intensif des Langues                                |
#### Exemple
if we want courses of second year of english departement foreign languages
```py
api.select('langues_etrengers.anglais.l2').get_courses()
```
## Todo
- [x] Get Course information about author and if course public
- [ ] Course Content
## Licence
This library is licensed under the MIT.
