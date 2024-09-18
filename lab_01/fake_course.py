from datetime import datetime
from random import choice
from uuid import uuid4, UUID

from faker import Faker


class Course:
    def __init__(self, title: str, description: str, teacher_id: UUID):
        self.id = uuid4()
        self.title = title
        self.description = description
        self.teacher_id = teacher_id
        self.created_at = datetime.now(tz=None)
        self.deleted_at = None

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.__str__()

    def list(self):
        return [
            self.id,
            self.title,
            self.description,
            self.teacher_id,
            self.created_at,
            self.deleted_at,
        ]


class CourseFaker:
    def __init__(self, faker: Faker | None = None):
        self.__faker = faker or Faker("ru")

    def create_course(self, teacher_id: UUID) -> Course:
        title = self.__faker.word().capitalize()
        description = self.__faker.text(max_nb_chars=80)
        return Course(title, description, teacher_id)

    def create_courses(self, teacher_ids: list[UUID], count: int = 100) -> list[Course]:
        return [self.create_course(choice(teacher_ids)) for _ in range(count)]
