import datetime
import uuid

from psycopg2._psycopg import connection


def task1(con: connection):
    """
    Выполнить скалярный запрос: получить общее количество студентов.
    """
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM student;")
    count = cur.fetchone()[0]
    print("Общее количество студентов:", count)


def task2(con: connection):
    """
    Выполнить запрос с несколькими соединениями (JOIN):
    для каждого курса вывести название, ФИО преподавателя и количество записей на курс.
    """
    cur = con.cursor()
    cur.execute(
        """
        SELECT 
            c.title AS course_title,
            CONCAT(t.first_name, ' ', t.last_name) AS teacher_name,
            COUNT(e.id) AS enrollment_count
        FROM course c
        JOIN teacher t ON c.teacher_id = t.id
        LEFT JOIN enrollment e ON c.id = e.course_id
        GROUP BY c.id, t.first_name, t.last_name, c.title;
    """
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)


def task3(con: connection):
    """
    Выполнить запрос с ОТВ (CTE) и оконными функциями:
    получить список курсов с количеством записей и их рангом по числу записей (топ-100).
    """
    cur = con.cursor()
    cur.execute(
        """
        WITH course_enrollments AS (
            SELECT 
                c.id, 
                c.title, 
                COUNT(e.id) AS enrollment_count
            FROM course c
            LEFT JOIN enrollment e ON c.id = e.course_id
            GROUP BY c.id, c.title
        )
        SELECT 
            id, 
            title, 
            enrollment_count,
            RANK() OVER (ORDER BY enrollment_count DESC) AS rank
        FROM course_enrollments
        ORDER BY rank DESC 
        LIMIT 100;
    """
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)


def task4(con: connection):
    """
    Выполнить запрос к метаданным: вывести список всех таблиц из information_schema.
    """
    cur = con.cursor()
    cur.execute(
        """
        SELECT table_schema, table_name, table_type
        FROM information_schema.tables
        ORDER BY table_schema, table_name;
    """
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)


def task5(con: connection):
    """
    Вызвать скалярную функцию.
    Получает полное имя студента.
    """
    cur = con.cursor()
    cur.execute("SELECT get_student_full_name('83cde84d-1f93-4700-8eb0-b600f55f955e');")
    result = cur.fetchone()[0]
    print("Результат скалярной функции get_student_full_name():", result)


def task6(con: connection):
    """
    Вызвать табличную (или многооператорную) функцию.
    Получение курсов указанного преподавателя.
    """
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM get_courses_by_teacher('08443b1a-3216-4ec7-8a75-99f3e8853f72');"
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)


def task7(con: connection):
    """
    Вызвать хранимую процедуру.
    Добавляет нового студента в таблицу student.
    """
    first_name = input("Введите имя студента: ")
    last_name = input("Введите фамилию студента: ")
    student_id = str(uuid.uuid4())
    cur = con.cursor()
    cur.execute(
        "CALL add_student(%s, %s, %s, %s);",
        (student_id, first_name, last_name, datetime.datetime.now()),
    )
    con.commit()
    print("Студент успешно добавлен.")


def task8(con: connection):
    """
    Вызвать системную функцию: вывести имя текущей базы данных.
    """
    cur = con.cursor()
    cur.execute("SELECT current_database();")
    current_db = cur.fetchone()[0]
    print(f"Имя текущей базы данных: {current_db}")


def task9(con: connection):
    """
    Создать таблицу в базе данных, соответствующую тематике.
    Создается таблица course_review для хранения отзывов по курсам.
    """
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE course_review (
            review_id uuid PRIMARY KEY,
            course_id uuid NOT NULL,
            review_text text,
            rating integer,
            created_at timestamp NOT NULL,
            CONSTRAINT fk_course_review FOREIGN KEY (course_id) REFERENCES course (id)
        );
    """
    )
    con.commit()
    print("Таблица course_review успешно создана.")


def task10(con: connection):
    """
    Выполнить вставку данных в созданную таблицу с использованием инструкции COPY.
    Принимает имя файла, содержащего данные в CSV-формате с заголовком.
    """
    filename = input("Введите имя файла для загрузки данных в course_review: ")
    cur = con.cursor()
    cur.execute(f"COPY course_review FROM '{filename}' DELIMITER ',' CSV HEADER;")
    con.commit()
    print("Данные успешно вставлены в таблицу course_review.")
