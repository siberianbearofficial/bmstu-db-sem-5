from datetime import datetime
from random import choice, randint
from uuid import uuid4, UUID

from faker import Faker


class Enrollment:
    def __init__(
        self,
        student_id: UUID,
        course_id: UUID,
        expires_at: datetime,
        comment: str | None = None,
    ):
        self.id = uuid4()
        self.student_id = student_id
        self.course_id = course_id
        self.comment = comment
        self.expires_at = expires_at
        self.created_at = datetime.now(tz=None)
        self.deleted_at = None

    def __str__(self):
        if self.comment:
            return f"{self.student_id} - {self.course_id} ({self.comment})"
        return f"{self.student_id} - {self.course_id}"

    def __repr__(self):
        return self.__str__()

    def list(self):
        return [
            self.id,
            self.comment,
            self.student_id,
            self.course_id,
            self.created_at,
            self.expires_at,
        ]


class EnrollmentFaker:
    def __init__(self, faker: Faker | None = None):
        self.__faker = faker or Faker("ru")

    def create_enrollment(self, student_id: UUID, course_id: UUID) -> Enrollment:
        expires_at = self.__faker.date_time_this_decade(before_now=False)
        comment = None if randint(1, 10) < 4 else self.__faker.text(max_nb_chars=30)
        return Enrollment(student_id, course_id, expires_at, comment)

    def create_enrollments(
        self, student_ids: list[UUID], course_ids: list[UUID], count: int = 100
    ) -> list[Enrollment]:
        return [
            self.create_enrollment(choice(student_ids), choice(course_ids))
            for _ in range(count)
        ]
