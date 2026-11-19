| Check | Expected | Actual | Result |
|---|---|---|---|
| departments: source rows = dim_department rows | 6=6 | 6=6 | PASS |
| programs: source = target | 12=12 | 12=12 | PASS |
| terms: source = target | 6=6 | 6=6 | PASS |
| students: source = target | 480=480 | 480=480 | PASS |
| instructors: source = target | 36=36 | 36=36 | PASS |
| courses: source = target | 36=36 | 36=36 | PASS |
| student_terms: source = fact_student_term | 1760=1760 | 1760=1760 | PASS |
| enrollments: source = fact_enrollment | 6690=6690 | 6690=6690 | PASS |
| teaching_assignments: source = fact_teaching_assignment | 540=540 | 540=540 | PASS |
| Duplicate keys at the declared grain (all 3 facts) | 0 | 0 | PASS |
| Foreign key violations | 0 | 0 | PASS |
| GRADED without a score, or non-GRADED with a score | 0 | 0 | PASS |
| Sections where the sum of assigned periods <> planned periods | 0 | 0 | PASS |
| Co-taught section example (lead + co) | L2024-1-012: 2 rows, 30+15=45 | L2024-1-012: 2 rows, 30+15=45 | PASS |
| G4 counts that co-taught section once (it is one row in the per-section subquery) | 1 | 1 | PASS |
| An ACTIVE student with no enrollments in 2024-1 | SV20220119 | SV20220119 | PASS |
| That student is counted in S1 for 2024-1 | 1 | 1 | PASS |
| Student-course pairs taken more than once (retakes kept as separate rows) | 621 | 621 | PASS |
| Benchmark 2024-1: active students | 466 | 466 | PASS |
| Benchmark 2024-1: graded and passing enrollments | 1743 graded, 1543 passed | 1743 graded, 1543 passed | PASS |
| Benchmark 2024-1: instructors with assignments | 36 | 36 | PASS |
| Benchmark 2024-1: assigned periods and sections | 3240 periods, 72 sections | 3240 periods, 72 sections | PASS |
| Rerun with the same input gives identical checks and chart data | True | True | PASS |
