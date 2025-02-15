-- 1. Определяемая пользователем скалярная функция CLR
CREATE OR REPLACE FUNCTION get_student_full_name(s_id uuid)
    RETURNS text
    LANGUAGE plpython3u AS
$$
    q = "SELECT id, first_name, last_name FROM student"
    results = plpy.execute(q)
    if results:
        for result in results:
            if result["id"] == s_id:
                return result["first_name"] + ' ' + result["last_name"]
    return None
$$;

SELECT get_student_full_name('a5fd67a7-d0a5-424c-b67a-495d34e62075');

-- 2. Пользовательская агрегатная функция CLR
CREATE OR REPLACE FUNCTION get_student_count_with_first_name(s_name varchar)
    RETURNS integer
    LANGUAGE plpython3u AS
$$
    q = "SELECT first_name FROM student"
    result = plpy.execute(q)
    if result:
        count = 0
        for s in result:
            if s["first_name"] == s_name:
                count += 1
        return count
    else:
        return 0
$$;

SELECT get_student_count_with_first_name('New');

-- 3. Определяемая пользователем табличная функция CLR
CREATE OR REPLACE FUNCTION get_courses_with_teacher()
    RETURNS TABLE
            (
                course_id         uuid,
                course_title      varchar,
                teacher_full_name varchar
            )
    LANGUAGE plpython3u
AS
$$
    courses_sql = "SELECT id, title, teacher_id, deleted_at FROM course"
    teachers_sql = "SELECT id, first_name, middle_name, last_name, deleted_at FROM teacher"

    courses = plpy.execute(courses_sql)
    teachers = plpy.execute(teachers_sql)

    teacher_dict = dict()
    for teacher in teachers:
        if not teacher["deleted_at"]:
            full_name = teacher["first_name"] + ' ' + teacher["middle_name"] + ' ' + teacher["last_name"]
            teacher_dict[teacher["id"]] = full_name

    result = []
    for course in courses:
        teacher_id = course["teacher_id"]
        if not course["deleted_at"] and teacher_id in teacher_dict:
            result.append((course["id"], course["title"], teacher_dict[teacher_id]))

    return result
$$;

SELECT *
FROM get_courses_with_teacher();

-- 4.Хранимая процедура CLR
CREATE OR REPLACE PROCEDURE enroll_student(s_id uuid, c_id uuid, comment text)
    LANGUAGE plpython3u AS
$$
    import uuid
    from datetime import datetime, timedelta

    new_id = str(uuid.uuid4())
    created_at = datetime.now()
    expires_at = created_at + timedelta(days=30)

    plan = plpy.prepare(
        "INSERT INTO enrollment (id, student_id, course_id, comment, created_at, expires_at) VALUES ($1, $2, $3, $4, $5, $6)",
        ["uuid", "uuid", "uuid", "text", "timestamp", "timestamp"]
    )
    plpy.execute(plan, [new_id, s_id, c_id, comment, created_at, expires_at])
    plpy.notice("Student enrolled successfully")
$$;

CALL enroll_student('45b42ff4-75d3-4b89-a379-e5a35345befa', '5903a06b-7ab3-440e-b6ef-c50d91ca6c47',
                    'Комментарий к зачислению TEST TEST');

-- 5. Триггер CLR
CREATE OR REPLACE FUNCTION check_prerequisite_self()
    RETURNS trigger
    LANGUAGE plpython3u AS
$$
    new_row = TD["new"]
    if new_row["course_id"] == new_row["prerequisite_id"]:
        plpy.error("Курс не должен быть пререквизитом для самого себя")
    return new_row
$$;

CREATE TRIGGER trg_check_prerequisite_self
    BEFORE INSERT OR UPDATE
    ON course_prerequisite
    FOR EACH ROW
EXECUTE FUNCTION check_prerequisite_self();

INSERT INTO course_prerequisite (course_id, prerequisite_id)
VALUES ('43f5cf85-fd7f-4268-b4f5-15f6c2c70fee', '43f5cf85-fd7f-4268-b4f5-15f6c2c70fee');

-- 6. Определяемый пользователем тип данных CLR
CREATE TYPE student_summary AS
(
    full_name        text,
    enrollment_count integer
);

CREATE OR REPLACE VIEW v_student_summary AS
SELECT s.id,
       (s.first_name || ' ' || s.last_name,
        COALESCE(count(e.id), 0)
           )::student_summary AS student_info
FROM student s
         LEFT JOIN enrollment e ON s.id = e.student_id
GROUP BY s.id, s.first_name, s.last_name;

CREATE OR REPLACE FUNCTION get_students_with_high_enrollment_python()
    RETURNS SETOF text
    LANGUAGE plpython3u AS
$$
    query = "SELECT * FROM v_student_summary"
    result = plpy.execute(query)

    high_enrollment_names = []

    for row in result:
        student_info = row["student_info"]
        if student_info["enrollment_count"] > 30:
            high_enrollment_names.append(student_info["full_name"])

    return high_enrollment_names
$$;

SELECT *
FROM get_students_with_high_enrollment_python();

CREATE TABLE student_summary_table (
    id uuid PRIMARY KEY,
    student_info student_summary
);

INSERT INTO student_summary_table (id, student_info)
SELECT
    s.id,
    (s.first_name || ' ' || s.last_name, COUNT(e.id))::student_summary
FROM student s
LEFT JOIN enrollment e ON s.id = e.student_id
GROUP BY s.id, s.first_name, s.last_name;

SELECT (s.student_info).full_name
FROM student_summary_table s
WHERE (s.student_info).enrollment_count > 30;
