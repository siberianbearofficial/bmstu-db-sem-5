from sqlalchemy import create_engine, Column, Uuid, String, DateTime, ForeignKey, text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import uuid
from datetime import datetime

Base = declarative_base()


class Student(Base):
    __tablename__ = "student"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)


class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)


class Course(Base):
    __tablename__ = "course"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    teacher_id = Column(Uuid, ForeignKey(Teacher.id), nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
    teacher = relationship("Teacher")


class Enrollment(Base):
    __tablename__ = "enrollment"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    comment = Column(String)
    student_id = Column(Uuid, ForeignKey(Student.id), nullable=False)
    course_id = Column(Uuid, ForeignKey(Course.id), nullable=False)
    created_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    student = relationship("Student")
    course = relationship("Course")


class CoursePrerequisite(Base):
    __tablename__ = "course_prerequisite"
    course_id = Column(Uuid, ForeignKey(Course.id), primary_key=True)
    prerequisite_id = Column(Uuid, ForeignKey(Course.id), primary_key=True)


engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
Session = sessionmaker(bind=engine)

with Session() as session:
    # 1. Однотабличный
    students = session.query(Student).order_by(Student.created_at).limit(10).all()
    print("Все студенты:", *map(lambda s: s.first_name, students), sep="\n")

    # 2. Многотабличный
    results = (
        session.query(Student.first_name, Student.last_name, Enrollment.comment)
        .join(Enrollment, Student.id == Enrollment.student_id)
        .limit(10)
        .all()
    )
    print(
        "Имя студента и комментарий зачисления:",
        *map(lambda r: f"{r.first_name} - {r.comment}", results),
        sep="\n",
    )

    # 3. Добавление, изменение и удаление

    # Добавление
    new_student = Student(
        first_name="New", last_name="Student", created_at=datetime.now(tz=None)
    )
    session.add(new_student)
    session.commit()
    print("Добавлен студент:", new_student.first_name, new_student.last_name)

    # Изменение
    student_to_update = (
        session.query(Student).filter(Student.first_name == "New").first()
    )
    if student_to_update:
        student_to_update.last_name = "Updated"
        session.commit()
        print("Переименованный студент:", student_to_update.last_name)

    # Удаление
    enrollment_to_delete = (
        session.query(Enrollment).order_by(Enrollment.created_at).first()
    )
    if enrollment_to_delete:
        session.delete(enrollment_to_delete)
        session.commit()
        print(
            "Удаленное зачисление:",
            enrollment_to_delete.id,
            enrollment_to_delete.comment,
        )

    # 4. Получение доступа к данным через вызов хранимой процедуры
    session.execute(text("CALL print_all_students()"))
    print("Хранимая процедура вызвана")

    # 5*. Создать таблицу и проверить коммит
    session.execute(text("CREATE TABLE test3 (id uuid, test varchar)"))
    session.commit()
