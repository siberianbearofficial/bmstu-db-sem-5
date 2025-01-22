-- Скалярная функция
CREATE OR REPLACE FUNCTION get_student_full_name(student_id UUID) RETURNS VARCHAR AS $$
BEGIN
    RETURN (
        SELECT first_name || ' ' || last_name
        FROM student
        WHERE id = student_id
    );
END;
$$ LANGUAGE plpgsql;

SELECT get_student_full_name('ec03bbbd-7928-41c8-99c5-b2f339ceb110');


-- Подставляемая табличная функция
CREATE OR REPLACE FUNCTION get_courses_by_teacher(teacher UUID)
RETURNS TABLE(course_id UUID, title VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.title
    FROM course c
    WHERE c.teacher_id = teacher;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_courses_by_teacher('1e6717dc-7935-4ea8-ab0e-8a7167f427e8');


-- Многооператорная табличная функция
CREATE OR REPLACE FUNCTION get_students_by_course(course UUID)
RETURNS TABLE(student_id UUID, full_name TEXT, comment VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.id,
        s.first_name || ' ' || s.last_name AS full_name,
        e.comment
    FROM student s
    JOIN enrollment e ON s.id = e.student_id
    WHERE e.course_id = course;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_students_by_course('b72c388e-7fae-4dd3-93e2-52ccd7779b79');


-- Функция с рекурсивным ОТВ
CREATE OR REPLACE FUNCTION get_course_prerequisites(course UUID)
RETURNS TABLE(course_id UUID, prerequisite_id UUID) AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE prerequisite_chain AS (
        SELECT cp1.course_id, cp1.prerequisite_id
        FROM course_prerequisite cp1
        WHERE cp1.course_id = course
        UNION ALL
        SELECT cp2.course_id, cp2.prerequisite_id
        FROM course_prerequisite cp2
        JOIN prerequisite_chain pc ON cp2.course_id = pc.prerequisite_id
    )
    SELECT * FROM prerequisite_chain;
END;
$$ LANGUAGE plpgsql;

SELECT distinct prerequisite_id FROM get_course_prerequisites('26264fe3-0b5a-4b26-96bc-9a4201d3a022');
