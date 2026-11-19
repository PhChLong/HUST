-- Star schema. Staging tables (stg_*) are created by run_pipeline.py from the CSV headers.

DROP TABLE IF EXISTS fact_student_term;
DROP TABLE IF EXISTS fact_enrollment;
DROP TABLE IF EXISTS fact_teaching_assignment;
DROP TABLE IF EXISTS dim_student;
DROP TABLE IF EXISTS dim_program;
DROP TABLE IF EXISTS dim_course;
DROP TABLE IF EXISTS dim_instructor;
DROP TABLE IF EXISTS dim_term;
DROP TABLE IF EXISTS dim_department;

CREATE TABLE dim_department (
    department_key  INTEGER PRIMARY KEY,
    department_id   TEXT UNIQUE NOT NULL,
    department_name TEXT
);

CREATE TABLE dim_term (
    term_key      INTEGER PRIMARY KEY,
    term_id       TEXT UNIQUE NOT NULL,
    academic_year TEXT,
    semester_no   INTEGER,
    start_date    TEXT,
    end_date      TEXT
);

CREATE TABLE dim_program (
    program_key    INTEGER PRIMARY KEY,
    program_id     TEXT UNIQUE NOT NULL,
    program_name   TEXT,
    department_key INTEGER REFERENCES dim_department  -- managing department
);

CREATE TABLE dim_student (
    student_key INTEGER PRIMARY KEY,
    student_id  TEXT UNIQUE NOT NULL,
    cohort_year INTEGER,
    program_key INTEGER REFERENCES dim_program
);

CREATE TABLE dim_course (
    course_key     INTEGER PRIMARY KEY,
    course_id      TEXT UNIQUE NOT NULL,
    course_name    TEXT,
    credits        INTEGER,
    department_key INTEGER REFERENCES dim_department  -- owning department
);

CREATE TABLE dim_instructor (
    instructor_key INTEGER PRIMARY KEY,
    instructor_id  TEXT UNIQUE NOT NULL,
    degree_level   TEXT,
    department_key INTEGER REFERENCES dim_department  -- home department
);

-- Grain: one student at the end of one semester
CREATE TABLE fact_student_term (
    student_key            INTEGER REFERENCES dim_student,
    term_key               INTEGER REFERENCES dim_term,
    program_department_key INTEGER REFERENCES dim_department,
    academic_status        TEXT,
    PRIMARY KEY (student_key, term_key)
);

-- Grain: one student in one section (a retake is a new row in another term)
CREATE TABLE fact_enrollment (
    student_key            INTEGER REFERENCES dim_student,
    section_id             TEXT,
    term_key               INTEGER REFERENCES dim_term,
    course_key             INTEGER REFERENCES dim_course,
    program_key            INTEGER REFERENCES dim_program,
    program_department_key INTEGER REFERENCES dim_department,
    course_department_key  INTEGER REFERENCES dim_department,
    result_status          TEXT,
    final_score            REAL,
    PRIMARY KEY (student_key, section_id)
);

-- Grain: one instructor in one section
CREATE TABLE fact_teaching_assignment (
    instructor_key        INTEGER REFERENCES dim_instructor,
    section_id            TEXT,
    term_key              INTEGER REFERENCES dim_term,
    course_key            INTEGER REFERENCES dim_course,
    home_department_key   INTEGER REFERENCES dim_department,
    course_department_key INTEGER REFERENCES dim_department,
    teaching_role         TEXT,
    assigned_periods      INTEGER,
    PRIMARY KEY (instructor_key, section_id)
);
