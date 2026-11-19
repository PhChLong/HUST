-- Chart queries. Each returns rows grouped by the filter columns (term, department ...);
-- the dashboard sums the rows that match the selected filters.

-- @s1  Active students by semester, cohort, program-managing department
SELECT t.term_id, d.department_id, s.cohort_year, COUNT(*) AS active
FROM fact_student_term f
JOIN dim_term t       ON t.term_key = f.term_key
JOIN dim_student s    ON s.student_key = f.student_key
JOIN dim_department d ON d.department_key = f.program_department_key
WHERE f.academic_status = 'ACTIVE'
GROUP BY 1, 2, 3;

-- @s2  Graded count and score sum by semester and program (average = score_sum / graded)
SELECT t.term_id, p.program_id, COUNT(*) AS graded, SUM(f.final_score) AS score_sum
FROM fact_enrollment f
JOIN dim_term t    ON t.term_key = f.term_key
JOIN dim_program p ON p.program_key = f.program_key
WHERE f.result_status = 'GRADED'
GROUP BY 1, 2;

-- @s3  Graded and passed by semester, course, course-owning department
SELECT t.term_id, d.department_id, c.course_id,
       COUNT(*) AS graded, SUM(f.final_score >= 4.0) AS passed
FROM fact_enrollment f
JOIN dim_term t       ON t.term_key = f.term_key
JOIN dim_course c     ON c.course_key = f.course_key
JOIN dim_department d ON d.department_key = f.course_department_key
WHERE f.result_status = 'GRADED'
GROUP BY 1, 2, 3;

-- @s4  Enrollments by semester, program-managing department, status
SELECT t.term_id, d.department_id, f.result_status, COUNT(*) AS enrollments
FROM fact_enrollment f
JOIN dim_term t       ON t.term_key = f.term_key
JOIN dim_department d ON d.department_key = f.program_department_key
GROUP BY 1, 2, 3;

-- @g1  Distinct instructors with assignments by semester, home department, degree
SELECT t.term_id, d.department_id, i.degree_level, COUNT(DISTINCT f.instructor_key) AS instructors
FROM fact_teaching_assignment f
JOIN dim_term t       ON t.term_key = f.term_key
JOIN dim_instructor i ON i.instructor_key = f.instructor_key
JOIN dim_department d ON d.department_key = f.home_department_key
GROUP BY 1, 2, 3;

-- @g2  Assigned periods by semester and home department
SELECT t.term_id, d.department_id, SUM(f.assigned_periods) AS periods
FROM fact_teaching_assignment f
JOIN dim_term t       ON t.term_key = f.term_key
JOIN dim_department d ON d.department_key = f.home_department_key
GROUP BY 1, 2;

-- @g3  Assigned periods by semester and instructor (top 10 is picked in the dashboard)
SELECT t.term_id, d.department_id, i.instructor_id, SUM(f.assigned_periods) AS periods
FROM fact_teaching_assignment f
JOIN dim_term t       ON t.term_key = f.term_key
JOIN dim_instructor i ON i.instructor_key = f.instructor_key
JOIN dim_department d ON d.department_key = f.home_department_key
GROUP BY 1, 2, 3;

-- @g4  Sections by number of instructors (first count instructors per section, then count sections)
SELECT term_id, department_id,
       CASE WHEN n = 1 THEN '1 instructor' ELSE '2+ instructors' END AS grp,
       COUNT(*) AS sections
FROM (SELECT t.term_id, d.department_id, f.section_id, COUNT(*) AS n
      FROM fact_teaching_assignment f
      JOIN dim_term t       ON t.term_key = f.term_key
      JOIN dim_department d ON d.department_key = f.course_department_key
      GROUP BY 1, 2, 3)
GROUP BY 1, 2, 3;
