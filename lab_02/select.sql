-- 1. Инструкция SELECT, использующая предикат сравнения
SELECT first_name, last_name
FROM student
WHERE created_at > '2024-01-01 00:00:00';

-- 2. Инструкция SELECT, использующая предикат BETWEEN
SELECT title, created_at
FROM course
WHERE created_at BETWEEN '2024-09-12 19:00:31.700000' AND '2024-09-12 19:00:31.800000';

-- 3. Инструкция SELECT, использующая предикат LIKE
SELECT first_name, email
FROM teacher
WHERE email LIKE 'a%';

-- 4. Инструкция SELECT, использующая предикат IN с вложенным подзапросом
SELECT title
FROM course
WHERE teacher_id IN (SELECT id
                     FROM teacher
                     WHERE last_name = 'Самойлов');

-- 5. Инструкция SELECT, использующая предикат EXISTS с вложенным подзапросом
SELECT first_name, last_name
FROM student s
WHERE EXISTS (SELECT 1
              FROM enrollment e
              WHERE e.student_id = s.id);

-- 6. Инструкция SELECT, использующая предикат сравнения с квантором
SELECT first_name, last_name
FROM teacher t
WHERE created_at < ALL (SELECT created_at
                        FROM course
                        WHERE teacher_id = t.id);

-- 7. Инструкция SELECT, использующая агрегатные функции в выражениях столбцов
SELECT course_id, COUNT(course_id) AS total_students, MAX(created_at) AS last_enrollment
FROM enrollment
GROUP BY course_id;

-- 8. Инструкция SELECT, использующая скалярные подзапросы в выражениях столбцов
SELECT id,
       title,
       (SELECT COUNT(course_id)
        FROM enrollment
        WHERE course_id = c.id) AS total_enrollments
FROM course c;

-- 9. Инструкция SELECT, использующая простое выражение CASE
SELECT first_name,
       last_name,
       CASE
           WHEN deleted_at IS NULL THEN 'Active'
           ELSE 'Deleted'
           END AS status
FROM student;

-- 10. Инструкция SELECT, использующая поисковое выражение CASE
SELECT title,
       CASE teacher_id
           WHEN '65f9eb07-f28b-4d2c-bf8f-162e096cfe05' THEN 'Главный преподаватель'
           WHEN '67194da4-f4f8-4e99-9e64-b4f2bbf599a6' THEN 'Помощник главного преподавателя'
           ELSE 'Обычный преподаватель'
           END AS teacher_name
FROM course;

-- 11. Создание новой временной локальной таблицы из результирующего набора данных инструкции SELECT
CREATE TEMP TABLE temp_course_students AS
SELECT c.id        AS course_id,
       c.title,
       COUNT(e.id) AS total_students
FROM course c
         LEFT JOIN enrollment e ON c.id = e.course_id
GROUP BY c.id;

-- 12. Инструкция SELECT, использующая вложенные коррелированные подзапросы в качестве производных таблиц в предложении FROM
SELECT t.first_name,
       t.last_name,
       avg_enrollments.total_enrollments
FROM teacher t
         JOIN (SELECT c.teacher_id,
                      AVG(enroll_count) AS total_enrollments
               FROM (SELECT course_id,
                            COUNT(course_id) AS enroll_count
                     FROM enrollment
                     GROUP BY course_id) e
                        JOIN course c ON c.id = e.course_id
               GROUP BY c.teacher_id) avg_enrollments ON avg_enrollments.teacher_id = t.id;

-- 13. Инструкция SELECT, использующая вложенные подзапросы с уровнем вложенности 3
SELECT s.first_name,
       s.last_name,
       (SELECT COUNT(e.id)
        FROM enrollment e
        WHERE e.student_id = s.id
          AND e.course_id IN (SELECT id
                              FROM course
                              WHERE teacher_id = (SELECT id
                                                  FROM teacher
                                                  WHERE id = 'ceab6709-dd07-4fe3-9a77-509e795caae6'))) AS courses_with_selected_teacher
FROM student s;

-- 14. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY, но без предложения HAVING
SELECT teacher_id, COUNT(teacher_id) AS total_courses
FROM course
GROUP BY teacher_id;

-- 15. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY и предложения HAVING
SELECT teacher_id, COUNT(teacher_id) AS total_courses
FROM course
GROUP BY teacher_id
HAVING COUNT(teacher_id) > 3;

-- 16. Однострочная инструкция INSERT, выполняющая вставку в таблицу одной строки значений
INSERT INTO student (id, first_name, last_name, created_at)
VALUES ('11111111-1111-1111-1111-111111111111', 'Иван', 'Иванов', CURRENT_TIMESTAMP);

-- 17. Многострочная инструкция INSERT, выполняющая вставку в таблицу результирующего набора данных вложенного подзапроса
INSERT INTO enrollment (id, student_id, course_id, created_at, expires_at)
SELECT gen_random_uuid(),
       s.id,
       c.id,
       CURRENT_TIMESTAMP,
       CURRENT_TIMESTAMP + INTERVAL '1 year'
FROM student s
         JOIN course c ON c.teacher_id = 'e57b9e26-f593-4784-827c-b898cb09a1a7';

-- 18. Простая инструкция UPDATE
UPDATE student
SET first_name = 'Зинаида'
WHERE last_name = 'Русакова';

-- 19. Инструкция UPDATE со скалярным подзапросом в предложении SET
UPDATE course
SET teacher_id = (SELECT id
                  FROM teacher
                  WHERE email = 'rjurik1975@bmstu.ru')
WHERE id = '92acf599-28c5-4fd0-bfdd-0072cf2ea213';

-- 20. Простая инструкция DELETE
DELETE
FROM student
WHERE id = 'af275e6e-ccc7-48f6-a895-626e9fee3979';

-- 21. Инструкция DELETE с вложенным коррелированным подзапросом в предложении WHERE
DELETE
FROM enrollment
WHERE student_id IN (SELECT id
                     FROM student
                     WHERE deleted_at IS NOT NULL);

-- 22. Инструкция SELECT, использующая простое обобщенное табличное выражение
WITH recent_enrollments AS (SELECT student_id, course_id, MAX(created_at) AS last_enrollment
                            FROM enrollment
                            GROUP BY student_id, course_id)
SELECT s.first_name, s.last_name, re.last_enrollment
FROM student s
         JOIN recent_enrollments re ON s.id = re.student_id;

-- 23. Инструкция SELECT, использующая рекурсивное обобщенное табличное выражение
WITH RECURSIVE prerequisite_hierarchy AS (SELECT prerequisite_id,
                                                 course_id
                                          FROM course_prerequisite
                                          WHERE course_id = '26264fe3-0b5a-4b26-96bc-9a4201d3a022'

                                          UNION ALL

                                          SELECT cp.prerequisite_id,
                                                 cp.course_id
                                          FROM course_prerequisite cp
                                                   INNER JOIN prerequisite_hierarchy ph
                                                              ON cp.course_id = ph.prerequisite_id)
SELECT DISTINCT prerequisite_id
FROM prerequisite_hierarchy;

-- 24. Оконные функции. Использование конструкций MIN/MAX/AVG OVER()
SELECT course_id,
       created_at,
       COUNT(course_id) OVER (PARTITION BY course_id)                     AS total_students,
       AVG(EXTRACT(EPOCH FROM (expires_at - created_at)) / 86400) OVER () AS avg_days_valid
FROM enrollment;

-- 25. Оконные функции для устранения дублей
DELETE
FROM enrollment
WHERE id IN (SELECT id
             FROM (SELECT id,
                          ROW_NUMBER() OVER (PARTITION BY student_id, course_id ORDER BY created_at DESC) AS row_num
                   FROM enrollment) subquery
             WHERE row_num > 1);
