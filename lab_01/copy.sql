COPY student FROM '/var/liv/postgresql/data/students.csv' DELIMITER ',' CSV HEADER;

COPY teacher FROM '/var/liv/postgresql/data/teachers.csv' DELIMITER ',' CSV HEADER;

COPY course FROM '/var/liv/postgresql/data/courses.csv' DELIMITER ',' CSV HEADER;

COPY enrollment FROM '/var/liv/postgresql/data/enrollments.csv' DELIMITER ',' CSV HEADER;
