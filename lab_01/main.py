from faker import Faker

from lab_01.fake_course import CourseFaker
from lab_01.fake_enrollment import EnrollmentFaker
from lab_01.fake_student import StudentFaker
from lab_01.fake_teacher import TeacherFaker

from write_csv import write_students, write_teachers, write_courses, write_enrollments


def main():
    faker = Faker('ru')

    student_faker = StudentFaker(faker)
    teacher_faker = TeacherFaker(faker)
    course_faker = CourseFaker(faker)
    enrollment_faker = EnrollmentFaker(faker)

    students = student_faker.create_students(count=5000)
    teachers = teacher_faker.create_teachers(count=2000)
    courses = course_faker.create_courses(
        count=10000,
        teacher_ids=[t.id for t in teachers]
    )
    enrollments = enrollment_faker.create_enrollments(
        count=100000,
        student_ids=[s.id for s in students],
        course_ids=[c.id for c in courses]
    )

    write_students(students)
    write_teachers(teachers)
    write_courses(courses)
    write_enrollments(enrollments)


if __name__ == '__main__':
    main()
