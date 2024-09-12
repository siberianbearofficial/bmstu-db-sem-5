import csv
from os import makedirs

from fake_course import Course
from fake_enrollment import Enrollment
from fake_student import Student
from fake_teacher import Teacher


def write_students(students: list[Student]) -> None:
    print('Writing students...')
    with open('data/students.csv', 'w') as file:
        writer = csv.writer(file)
        for student_list in map(lambda el: el.list(), students):
            writer.writerow(student_list)


def write_teachers(teachers: list[Teacher]) -> None:
    print('Writing teachers...')
    with open('data/teachers.csv', 'w') as file:
        writer = csv.writer(file)
        for teacher_list in map(lambda el: el.list(), teachers):
            writer.writerow(teacher_list)


def write_courses(courses: list[Course]) -> None:
    print('Writing courses...')
    with open('data/courses.csv', 'w') as file:
        writer = csv.writer(file)
        for course_list in map(lambda el: el.list(), courses):
            writer.writerow(course_list)


def write_enrollments(enrollments: list[Enrollment]) -> None:
    print('Writing enrollments...')
    with open('data/enrollments.csv', 'w') as file:
        writer = csv.writer(file)
        for enrollment_list in map(lambda el: el.list(), enrollments):
            writer.writerow(enrollment_list)


makedirs('data', exist_ok=True)
