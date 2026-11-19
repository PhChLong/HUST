-- Validation checks. Format: "-- @<expected value>  <description>", then one query.

-- @6=6  departments: source rows = dim_department rows
SELECT (SELECT COUNT(*) FROM stg_departments) || '=' || (SELECT COUNT(*) FROM dim_department);

-- @12=12  programs: source = target
SELECT (SELECT COUNT(*) FROM stg_programs) || '=' || (SELECT COUNT(*) FROM dim_program);

-- @6=6  terms: source = target
SELECT (SELECT COUNT(*) FROM stg_terms) || '=' || (SELECT COUNT(*) FROM dim_term);

-- @480=480  students: source = target
SELECT (SELECT COUNT(*) FROM stg_students) || '=' || (SELECT COUNT(*) FROM dim_student);

-- @36=36  instructors: source = target
SELECT (SELECT COUNT(*) FROM stg_instructors) || '=' || (SELECT COUNT(*) FROM dim_instructor);

-- @36=36  courses: source = target
SELECT (SELECT COUNT(*) FROM stg_courses) || '=' || (SELECT COUNT(*) FROM dim_course);

-- @1760=1760  student_terms: source = fact_student_term
SELECT (SELECT COUNT(*) FROM stg_student_terms) || '=' || (SELECT COUNT(*) FROM fact_student_term);

-- @6690=6690  enrollments: source = fact_enrollment
SELECT (SELECT COUNT(*) FROM stg_enrollments) || '=' || (SELECT COUNT(*) FROM fact_enrollment);

-- @540=540  teaching_assignments: source = fact_teaching_assignment
SELECT (SELECT COUNT(*) FROM stg_teaching_assignments) || '=' || (SELECT COUNT(*) FROM fact_teaching_assignment);

-- @0  Duplicate keys at the declared grain (all 3 facts)
SELECT (SELECT COUNT(*) FROM (SELECT 1 FROM fact_student_term GROUP BY student_key, term_key HAVING COUNT(*) > 1))
     + (SELECT COUNT(*) FROM (SELECT 1 FROM fact_enrollment GROUP BY student_key, section_id HAVING COUNT(*) > 1))
     + (SELECT COUNT(*) FROM (SELECT 1 FROM fact_teaching_assignment GROUP BY instructor_key, section_id HAVING COUNT(*) > 1));

-- @0  Foreign key violations
SELECT COUNT(*) FROM pragma_foreign_key_check;

-- @0  GRADED without a score, or non-GRADED with a score
SELECT COUNT(*) FROM fact_enrollment
WHERE (result_status = 'GRADED') <> (final_score IS NOT NULL);

-- @0  Sections where the sum of assigned periods <> planned periods
SELECT COUNT(*) FROM stg_sections s
WHERE s.planned_periods <> (SELECT SUM(assigned_periods) FROM fact_teaching_assignment f
                            WHERE f.section_id = s.section_id);

-- @L2024-1-012: 2 rows, 30+15=45  Co-taught section example (lead + co)
SELECT section_id || ': ' || COUNT(*) || ' rows, ' || GROUP_CONCAT(assigned_periods, '+') || '='
       || SUM(assigned_periods)
FROM (SELECT * FROM fact_teaching_assignment WHERE section_id = 'L2024-1-012' ORDER BY teaching_role DESC);

-- @1  G4 counts that co-taught section once (it is one row in the per-section subquery)
SELECT COUNT(*) FROM (SELECT section_id FROM fact_teaching_assignment
                      WHERE section_id = 'L2024-1-012' GROUP BY section_id);

-- @SV20220119  An ACTIVE student with no enrollments in 2024-1
SELECT MIN(s.student_id) FROM fact_student_term f
JOIN dim_student s ON s.student_key = f.student_key
JOIN dim_term t    ON t.term_key = f.term_key
WHERE t.term_id = '2024-1' AND f.academic_status = 'ACTIVE'
  AND NOT EXISTS (SELECT 1 FROM fact_enrollment e WHERE e.student_key = f.student_key AND e.term_key = f.term_key);

-- @1  That student is counted in S1 for 2024-1
SELECT COUNT(*) FROM fact_student_term f
JOIN dim_student s ON s.student_key = f.student_key
JOIN dim_term t    ON t.term_key = f.term_key
WHERE s.student_id = 'SV20220119' AND t.term_id = '2024-1' AND f.academic_status = 'ACTIVE';

-- @621  Student-course pairs taken more than once (retakes kept as separate rows)
SELECT COUNT(*) FROM (SELECT 1 FROM fact_enrollment GROUP BY student_key, course_key HAVING COUNT(*) > 1);

-- @466  Benchmark 2024-1: active students
SELECT COUNT(*) FROM fact_student_term f JOIN dim_term t ON t.term_key = f.term_key
WHERE t.term_id = '2024-1' AND f.academic_status = 'ACTIVE';

-- @1743 graded, 1543 passed  Benchmark 2024-1: graded and passing enrollments
SELECT SUM(result_status = 'GRADED') || ' graded, ' || SUM(final_score >= 4.0) || ' passed'
FROM fact_enrollment f JOIN dim_term t ON t.term_key = f.term_key WHERE t.term_id = '2024-1';

-- @36  Benchmark 2024-1: instructors with assignments
SELECT COUNT(DISTINCT instructor_key) FROM fact_teaching_assignment f
JOIN dim_term t ON t.term_key = f.term_key WHERE t.term_id = '2024-1';

-- @3240 periods, 72 sections  Benchmark 2024-1: assigned periods and sections
SELECT SUM(assigned_periods) || ' periods, ' || COUNT(DISTINCT section_id) || ' sections'
FROM fact_teaching_assignment f JOIN dim_term t ON t.term_key = f.term_key WHERE t.term_id = '2024-1';
