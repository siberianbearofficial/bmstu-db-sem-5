CREATE TABLE student_profile
(
    id           uuid PRIMARY KEY,
    student_id   uuid      NOT NULL REFERENCES student (id),
    profile_data jsonb,
    created_at   timestamp NOT NULL,
    updated_at   timestamp
);

-- Экспорт данных
COPY (
    SELECT json_agg(row_to_json(t))
    FROM (SELECT * FROM student) t
    ) TO '/var/liv/postgresql/data/student1.json';

COPY (
    SELECT json_agg(row_to_json(t))
    FROM (SELECT * FROM teacher) t
    ) TO '/var/liv/postgresql/data/teacher1.json';

COPY (
    SELECT json_agg(row_to_json(t))
    FROM (SELECT * FROM course) t
    ) TO '/var/liv/postgresql/data/course1.json';

COPY (
    SELECT json_agg(row_to_json(t))
    FROM (SELECT * FROM enrollment) t
    ) TO '/var/liv/postgresql/data/enrollment1.json';

COPY (
    SELECT json_agg(row_to_json(t))
    FROM (SELECT * FROM course_prerequisite) t
    ) TO '/var/liv/postgresql/data/course_prerequisite1.json';


-- Импорт данных
COPY student FROM '/var/liv/postgresql/data/student1.json';
COPY teacher FROM '/var/liv/postgresql/data/teacher1.json';
COPY course FROM '/var/liv/postgresql/data/course1.json';
COPY enrollment FROM '/var/liv/postgresql/data/enrollment1.json';
COPY course_prerequisite FROM '/var/liv/postgresql/data/course_prerequisite1.json';


-- Извлечение фрагмента JSON
SELECT student_id, profile_data -> 'address' AS address
FROM student_profile
WHERE profile_data IS NOT NULL;

-- Извлечение значения из JSON
SELECT student_id, profile_data ->> 'email' AS email
FROM student_profile
WHERE profile_data IS NOT NULL;

-- Проверка наличия ключа
SELECT student_id,
       profile_data ? 'phone'  AS has_phone,
       profile_data -> 'phone' AS phone_data
FROM student_profile
WHERE profile_data IS NOT NULL;

-- Обновление JSON данных
UPDATE student_profile
SET profile_data = jsonb_set(
        profile_data,
        '{address,country}',
        '"Россия"',
        true
                   )
WHERE student_id = 'ae3f8fae-ee2a-4de0-83e8-0bd146506be3';

-- Удаление ключа из JSON
UPDATE student_profile
SET profile_data = profile_data - 'phone'
WHERE student_id = 'ae3f8fae-ee2a-4de0-83e8-0bd146506be3';

-- Разворачиваем JSON-массив
WITH json_data AS (SELECT profile_data -> 'achievements' AS data
                   FROM student_profile
                   WHERE id = '33333333-3333-3333-3333-333333333333')
SELECT
    jsonb_array_elements(data) ->> 'title' AS achievement
FROM json_data;
