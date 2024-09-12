CREATE TABLE student
(
    id         uuid,
    first_name varchar,
    last_name  varchar,
    created_at timestamp,
    deleted_at timestamp
);

CREATE TABLE teacher
(
    id          uuid,
    first_name  varchar,
    middle_name varchar,
    last_name   varchar,
    email       varchar,
    created_at  timestamp,
    deleted_at  timestamp
);

CREATE TABLE course
(
    id          uuid,
    title       varchar,
    description varchar,
    teacher_id  uuid,
    created_at  timestamp,
    deleted_at  timestamp
);

CREATE TABLE enrollment
(
    id         uuid,
    comment    varchar,
    student_id uuid,
    course_id  uuid,
    created_at timestamp,
    expires_at timestamp
);
