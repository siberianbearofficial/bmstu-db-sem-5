from datetime import datetime
from dataclasses import dataclass
from py_linq import Enumerable


@dataclass
class Student:
    id: str
    first_name: str
    last_name: str
    created_at: datetime


@dataclass
class Enrollment:
    id: str
    comment: str
    student_id: str
    course_id: str
    created_at: datetime
    expires_at: datetime

    def __gt__(self, other):
        return self.created_at > other.created_at


students = Enumerable(
    [
        Student("1", "John", "Doe", datetime(2021, 1, 1)),
        Student("2", "Alice", "Smith", datetime(2021, 2, 1)),
        Student("3", "Bob", "Brown", datetime(2021, 3, 1)),
    ]
)

enrollments = Enumerable(
    [
        Enrollment(
            "10", "Excellent", "1", "C1", datetime(2021, 4, 1), datetime(2022, 4, 1)
        ),
        Enrollment("11", "Good", "2", "C2", datetime(2021, 5, 1), datetime(2022, 5, 1)),
        Enrollment(
            "12", "Average", "1", "C3", datetime(2021, 6, 1), datetime(2022, 6, 1)
        ),
    ]
)


query1 = students.where(lambda s: s.first_name == "John").to_list()
print(f'Студенты с first_name = "John": {query1}')

query2 = students.select(lambda s: f"{s.first_name} {s.last_name}").to_list()
print(f"Полное имя каждого студента: {query2}")

query3 = students.order_by_descending(lambda s: s.last_name).to_list()
print(f"Сортируем студентов по фамилии в обратном порядке: {query3}")

query4 = students.join(
    enrollments,
    outer_key=lambda s: s.id,
    inner_key=lambda e: e.student_id,
    result_func=lambda res: f"Student {res[0].first_name} {res[0].last_name} enrolled course {res[1].course_id} with comment: {res[1].comment}",
).to_list()
print(f"Результаты зачислений студентов: {query4}")

query5 = (
    enrollments.group_by(["student_id"], key=lambda e: e.student_id)
    .select(
        lambda grp: f"Student with id {grp.key.student_id} enrolled to {grp.count()} courses"
    )
    .to_list()
)
print(f"Считаем общее число зачислений на курсы для каждого студента: {query5}")
