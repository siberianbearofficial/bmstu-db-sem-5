from datetime import datetime
from uuid import uuid4

from faker import Faker


class Student:
    def __init__(self, first_name: str, last_name: str):
        self.id = uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.now(tz=None)
        self.deleted_at = None

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return self.__str__()

    def list(self):
        return [
            self.id,
            self.first_name,
            self.last_name,
            self.created_at,
            self.deleted_at,
        ]


class StudentFaker:
    def __init__(self, faker: Faker | None = None):
        self.__faker = faker or Faker("ru")

    def create_student(self) -> Student:
        while True:
            try:
                first_name, middle_name, last_name = self.__faker.name().split()
                break
            except:
                print("Сгенерировалось невалидное имя, попробуем снова")
        return Student(first_name, last_name)

    def create_students(self, count: int = 100) -> list[Student]:
        return [self.create_student() for _ in range(count)]
