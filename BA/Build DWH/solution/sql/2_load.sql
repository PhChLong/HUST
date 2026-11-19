-- Load staging -> warehouse (full reload: 1_schema.sql recreates empty tables first).

INSERT INTO dim_department (department_id, department_name)
SELECT department_id, department_name FROM stg_departments;

INSERT INTO dim_term (term_id, academic_year, semester_no, start_date, end_date)
SELECT term_id, academic_year, semester_no, start_date, end_date FROM stg_terms ORDER BY term_id;

INSERT INTO dim_program (program_id, program_name, department_key)
SELECT p.program_id, p.program_name, d.department_key
FROM stg_programs p JOIN dim_department d ON d.department_id = p.department_id;

INSERT INTO dim_student (student_id, cohort_year, program_key)
SELECT s.student_id, s.cohort_year, p.program_key
FROM stg_students s JOIN dim_program p ON p.program_id = s.program_id;

INSERT INTO dim_course (course_id, course_name, credits, department_key)
SELECT c.course_id, c.course_name, c.credits, d.department_key
FROM stg_courses c JOIN dim_department d ON d.department_id = c.department_id;

INSERT INTO dim_instructor (instructor_id, degree_level, department_key)
SELECT i.instructor_id, i.degree_level, d.department_key
FROM stg_instructors i JOIN dim_department d ON d.department_id = i.department_id;

INSERT INTO fact_student_term
SELECT s.student_key, t.term_key, p.department_key, x.academic_status
FROM stg_student_terms x
JOIN dim_student s ON s.student_id = x.student_id
JOIN dim_program p ON p.program_key = s.program_key
JOIN dim_term t    ON t.term_id = x.term_id;

INSERT INTO fact_enrollment
SELECT s.student_key, e.section_id, t.term_key, c.course_key, p.program_key,
       p.department_key, c.department_key, e.result_status, e.final_score
FROM stg_enrollments e
JOIN stg_sections sec ON sec.section_id = e.section_id
JOIN dim_student s    ON s.student_id = e.student_id
JOIN dim_program p    ON p.program_key = s.program_key
JOIN dim_term t       ON t.term_id = sec.term_id
JOIN dim_course c     ON c.course_id = sec.course_id;

INSERT INTO fact_teaching_assignment
SELECT i.instructor_key, a.section_id, t.term_key, c.course_key,
       i.department_key, c.department_key, a.teaching_role, a.assigned_periods
FROM stg_teaching_assignments a
JOIN stg_sections sec  ON sec.section_id = a.section_id
JOIN dim_instructor i  ON i.instructor_id = a.instructor_id
JOIN dim_term t        ON t.term_id = sec.term_id
JOIN dim_course c      ON c.course_id = sec.course_id;
