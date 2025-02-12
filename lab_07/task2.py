import json

from datetime import datetime
from py_linq import Enumerable

json_document = """
{
    "students": [
        {"id": "1", "first_name": "John", "last_name": "Doe", "created_at": "2021-01-01T00:00:00"},
        {"id": "2", "first_name": "Alice", "last_name": "Smith", "created_at": "2021-02-15T00:00:00"},
        {"id": "3", "first_name": "Bob", "last_name": "Brown", "created_at": "2021-03-20T00:00:00"},
        {"id": "4", "first_name": "Alice", "last_name": "Jones", "created_at": "2021-04-01T00:00:00"}
    ]
}
"""

data = json.loads(json_document)
students = data["students"]
students_enum = Enumerable(students)


def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")


query1 = (
    students_enum.where(
        lambda s: s["first_name"] == "Alice"
        and parse_date(s["created_at"]) > datetime(2021, 2, 1)
    )
    .order_by_descending(lambda s: parse_date(s["created_at"]))
    .to_list()
)

print(
    f"Студенты Alice, созданные после 1 февраля 2021 в порядке убывания даты создания: {json.dumps(query1, indent=4)}"
)

to_update = students_enum.where(
    lambda s: parse_date(s["created_at"]) < datetime(2021, 3, 1)
).to_list()

for student in to_update:
    student["last_name"] = f"{student['last_name']} (new)"

print(
    f"Обновляем фамилию студентов, созданных раньше 1 марта 2021: {json.dumps(data, indent=4)}"
)

new_student = {
    "id": "5",
    "first_name": "Eve",
    "last_name": "Green",
    "created_at": "2021-05-10T00:00:00",
}
data["students"].append(new_student)

print(f"Добавляем нового студента: {json.dumps(data, indent=4)}")
