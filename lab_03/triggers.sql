-- Триггер AFTER
CREATE TABLE student_log
(
    id       UUID PRIMARY KEY,
    action   VARCHAR,
    log_time TIMESTAMP
);

CREATE FUNCTION log_student_insert()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO student_log (id, action, log_time)
    VALUES (NEW.id, 'INSERT', CURRENT_TIMESTAMP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_student_insert
    AFTER INSERT
    ON student
    FOR EACH ROW
EXECUTE FUNCTION log_student_insert();

INSERT INTO student (id, first_name, last_name, created_at)
VALUES (gen_random_uuid(), 'Петр', 'Петров', CURRENT_TIMESTAMP);

SELECT *
FROM student_log;


-- Триггер INSTEAD OF
CREATE VIEW student_course_view AS
SELECT s.id AS student_id, c.id AS course_id, e.comment
FROM student s
         JOIN enrollment e ON s.id = e.student_id
         JOIN course c ON e.course_id = c.id;

CREATE FUNCTION insert_into_enrollment()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO enrollment (id, student_id, course_id, comment, created_at, expires_at)
    VALUES (gen_random_uuid(), NEW.student_id, NEW.course_id, NEW.comment, CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP + INTERVAL '1 year');
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER instead_of_student_course_insert
    INSTEAD OF INSERT
    ON student_course_view
    FOR EACH ROW
EXECUTE FUNCTION insert_into_enrollment();

INSERT INTO student_course_view (student_id, course_id, comment)
VALUES ('ec03bbbd-7928-41c8-99c5-b2f339ceb110', 'c90c23ff-c56f-43f7-93dd-e5a2b5c0813a', 'Занятия по средам');

SELECT *
FROM enrollment e
WHERE e.student_id = 'ec03bbbd-7928-41c8-99c5-b2f339ceb110'
  AND e.course_id = 'c90c23ff-c56f-43f7-93dd-e5a2b5c0813a'
  AND e.comment = 'Занятия по средам';
