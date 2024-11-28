ALTER TABLE student
    ADD CONSTRAINT pk_student_id primary key (id),
    ALTER COLUMN first_name SET NOT NULL,
    ALTER COLUMN last_name SET NOT NULL,
    ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE teacher
    ADD CONSTRAINT pk_teacher_id primary key (id),
    ALTER COLUMN first_name SET NOT NULL,
    ALTER COLUMN middle_name SET NOT NULL,
    ALTER COLUMN last_name SET NOT NULL,
    ALTER COLUMN email SET NOT NULL,
    ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE course
    ADD CONSTRAINT pk_course_id primary key (id),
    ALTER COLUMN title SET NOT NULL,
    ALTER COLUMN teacher_id SET NOT NULL,
    ADD CONSTRAINT fk_teacher_id foreign key (teacher_id) references teacher (id),
    ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE enrollment
    ADD CONSTRAINT pk_enrollment_id primary key (id),
    ALTER COLUMN student_id SET NOT NULL,
    ADD CONSTRAINT fk_student_id foreign key (student_id) references student (id),
    ALTER COLUMN course_id SET NOT NULL,
    ADD CONSTRAINT fk_course_id foreign key (course_id) references course (id),
    ALTER COLUMN created_at SET NOT NULL,
    ALTER COLUMN expires_at SET NOT NULL;

ALTER TABLE course_prerequisite
    ADD CONSTRAINT pk_course_prerequisite primary key (course_id, prerequisite_id),
    ADD CONSTRAINT fk_course foreign key (course_id) references course (id),
    ADD CONSTRAINT fk_prerequisite foreign key (prerequisite_id) references course (id),
    ALTER COLUMN course_id SET NOT NULL,
    ALTER COLUMN prerequisite_id SET NOT NULL;
