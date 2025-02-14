-- Хранимая процедура без параметров
CREATE OR REPLACE PROCEDURE print_all_students()
    LANGUAGE plpgsql AS
$$
DECLARE
    student_record RECORD;
BEGIN
    RAISE NOTICE 'List of Students:';
    FOR student_record IN SELECT id, first_name, last_name FROM student
        LOOP
            RAISE NOTICE '% % %', student_record.id, student_record.first_name, student_record.last_name;
        END LOOP;
END;
$$;

CALL print_all_students();


-- Хранимая процедура с рекурсивным ОТВ
CREATE OR REPLACE PROCEDURE print_course_dependencies(course UUID)
    LANGUAGE plpgsql AS
$$
DECLARE
    prereq RECORD;
BEGIN
    FOR prereq IN
        WITH RECURSIVE dependency_chain AS (SELECT cp1.course_id, cp1.prerequisite_id
                                            FROM course_prerequisite cp1
                                            WHERE cp1.course_id = course
                                            UNION ALL
                                            SELECT cp2.course_id, cp2.prerequisite_id
                                            FROM course_prerequisite cp2
                                                     JOIN dependency_chain dc ON cp2.course_id = dc.prerequisite_id)
        SELECT *
        FROM dependency_chain
        LOOP
            RAISE NOTICE 'Course: %, Prerequisite: %', prereq.course_id, prereq.prerequisite_id;
        END LOOP;
END;
$$;

CALL print_course_dependencies('26264fe3-0b5a-4b26-96bc-9a4201d3a022');


-- Хранимая процедура с курсором
CREATE OR REPLACE PROCEDURE print_students_by_course(course UUID)
    LANGUAGE plpgsql AS
$$
DECLARE
    student_cursor CURSOR FOR
        SELECT s.id, s.first_name, s.last_name
        FROM student s
                 JOIN enrollment e ON s.id = e.student_id
        WHERE e.course_id = course;
    student_row RECORD;
BEGIN
    OPEN student_cursor;
    LOOP
        FETCH student_cursor INTO student_row;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'Student: % % %', student_row.id, student_row.first_name, student_row.last_name;
    END LOOP;
    CLOSE student_cursor;
END;
$$;

CALL print_students_by_course('b72c388e-7fae-4dd3-93e2-52ccd7779b79');


-- Хранимая процедура доступа к метаданным
CREATE OR REPLACE PROCEDURE print_all_tables()
    LANGUAGE plpgsql AS
$$
DECLARE
    table_row RECORD;
BEGIN
    FOR table_row IN
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        LOOP
            RAISE NOTICE 'Table: %', table_row.table_name;
        END LOOP;
END;
$$;

CALL print_all_tables();

-- Понадобилась для лр6, чтобы видеть результат выполнения процедуры в базе
CREATE OR REPLACE PROCEDURE add_student(
    p_id uuid,
    p_first_name varchar,
    p_last_name varchar,
    p_created_at timestamp
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO student (id, first_name, last_name, created_at, deleted_at)
    VALUES (p_id, p_first_name, p_last_name, p_created_at, NULL);
END;
$$;
