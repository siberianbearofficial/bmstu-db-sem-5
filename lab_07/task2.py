import json

from datetime import datetime
from py_linq import Enumerable

with open("../lab_01/data/student1.json") as f:
    students = json.load(f)

students_enum = Enumerable(students)


def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")


query1 = (
    students_enum.where(
        lambda s: s["first_name"] == "София"
        and parse_date(s["created_at"]) > datetime(2023, 1, 1)
    )
    .order_by_descending(lambda s: parse_date(s["created_at"]))
    .to_list()
)

print(
    f"Студенты с именем София, созданные после 1 января 2023 в порядке убывания даты создания: {json.dumps(query1, indent=4, ensure_ascii=False)}"
)

to_update = students_enum.where(
    lambda s: parse_date(s["created_at"]) < datetime(2021, 3, 1)
).to_list()

for student in to_update:
    student["last_name"] = f"{student['last_name']} (new)"

print(
    f"Обновляем фамилию студентов, созданных раньше 1 марта 2021: {json.dumps(students, indent=4, ensure_ascii=False)}"
)

new_student = {
    "id": "5",
    "first_name": "Тестик",
    "last_name": "Тестов",
    "created_at": "2021-05-10T10:10:10.101010",
}
students.append(new_student)

print(
    f"Добавляем нового студента: {json.dumps(students, indent=4, ensure_ascii=False)}"
)
