from datetime import datetime
from uuid import uuid4

from faker import Faker


class Teacher:
    def __init__(self, first_name: str, middle_name: str, last_name: str, email: str):
        self.id = uuid4()
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.created_at = datetime.now(tz=None)
        self.deleted_at = None

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'

    def __repr__(self):
        return self.__str__()

    def list(self):
        return [self.id, self.first_name, self.middle_name, self.last_name, self.email, self.created_at, self.deleted_at]


class TeacherFaker:
    def __init__(self, faker: Faker | None = None):
        self.__faker = faker or Faker('ru')

    def create_teacher(self) -> Teacher:
        while True:
            try:
                first_name, middle_name, last_name = self.__faker.name().split()
                break
            except:
                print('Сгенерировалось невалидное имя, попробуем снова')
        email = self.__faker.email(safe=True, domain='bmstu.ru')
        return Teacher(first_name, middle_name, last_name, email)

    def create_teachers(self, count: int = 100) -> list[Teacher]:
        return [self.create_teacher() for _ in range(count)]
