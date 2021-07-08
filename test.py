from main import MoodleApi

api = MoodleApi()
faculties = api.get_faculties()
print(faculties)
courses = api.select('technologie.electronique.l2').get_courses()
for course in courses:
  print(course.course_info())