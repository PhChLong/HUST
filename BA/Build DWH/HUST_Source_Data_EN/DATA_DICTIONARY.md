# HUST Source Data Dictionary

All records, IDs, and departments are synthetic. The source systems listed below represent the academic and administrative functions in the exercise.

## File Formats and Keys

- Open `hust_source.sqlite` directly or import the 10 CSV files into your chosen database system. Both formats contain the same records.
- CSV files use UTF-8 with a BOM, comma delimiters, a header row, and a decimal point. Dates use YYYY-MM-DD.
- Import empty `final_score` values as NULL. All other fields are required. SQLite stores dates as ISO date strings.
- PK means primary key and FK means foreign key. Multiple fields marked PK in the same table form a composite key.
- If you enforce foreign keys during CSV import, load the tables in the order shown below.

## Relationship Rules

- Use `sections.term_id` to identify the semester for enrollments and teaching assignments.
- Each student has one status snapshot per semester from their entry year onward. Only students marked ACTIVE can have section enrollments. Some ACTIVE students have none.
- A student may retake the same course in a different semester. Within a semester, a student can enroll in at most one section of a course.
- Every section has one lead instructor and may have a co-instructor. The assigned periods sum to the scheduled periods for that section.
- The program-managing department, instructor home department, and course-owning department are three roles of the same department directory. Students may take courses outside their program's department, and instructors may teach sections outside their home department.

## `departments`

Simulated source **Academic Catalog**. Row grain **One department**. Row count **6**.

| Column | Logical Type | Key | Nullable | Definition |
| --- | --- | --- | --- | --- |
| `department_id` | `TEXT` | PK | No | Department ID. |
| `department_name` | `TEXT` | — | No | Synthetic department name. |

## `programs`

Simulated source **Academic Administration**. Row grain **One academic program**. Row count **12**.

| Column | Logical Type | Key | Nullable | Definition |
| --- | --- | --- | --- | --- |
| `program_id` | `TEXT` | PK | No | Academic program ID. |
| `program_name` | `TEXT` | — | No | Synthetic program name. |
| `department_id` | `TEXT` | FK → `departments.department_id` | No | Department that manages the program. |

## `terms`

Simulated source **Academic Administration**. Row grain **One semester**. Row count **6**.

| Column | Logical Type | Key | Nullable | Definition |
| --- | --- | --- | --- | --- |
| `term_id` | `TEXT` | PK | No | Semester ID, for example 2024-1. |
| `academic_year` | `TEXT` | — | No | Academic year, for example 2024–2025. |
| `semester_no` | `INTEGER` | — | No | Semester number within the academic year, either 1 or 2. |
| `start_date` | `DATE` | — | No | First day of the semester. |
| `end_date` | `DATE` | — | No | Last day of the semester and the date of the status snapshot. |

## `students`

Simulated source **Student Records**. Row grain **One student**. Row count **480**.

| Column | Logical Type | Key | Nullable | Definition |
| --- | --- | --- | --- | --- |
| `student_id` | `TEXT` | PK | No | Synthetic student ID. |
| `cohort_year` | `INTEGER` | — | No | Entry year used to identify the student's cohort. |
| `program_id` | `TEXT` | FK → `programs.program_id` | No | Student's academic program, which stays the same throughout this exercise. |

## `student_terms`

Simulated source **Student Records**. Row grain **One student in one semester**. Row count **1,760**.

| Column | Logical Type | Key | Nullable | Definition |
| --- | --- | --- | --- | --- |
| `student_id` | `TEXT` | PK + FK → `students.student_id` | No | Student ID. |
| `term_id` | `TEXT` | PK + FK → `terms.term_id` | No | Semester of the status snapshot. |
| `academic_status` | `TEXT` | — | No | ACTIVE means enrolled and LEAVE means on leave at semester end. |

## `instructors`

Simulated source **Instructor Records**. Row grain **One instructor**. Row count **36**.

| Column | Logical Type | Key | Nullable | Definition |
| --- | --- | --- | --- | --- |
| `instructor_id` | `TEXT` | PK | No | Synthetic instructor ID. |
| `department_id` | `TEXT` | FK → `departments.department_id` | No | Instructor's home department. |
| `degree_level` | `TEXT` | — | No | Degree level, either MASTER (master's degree) or PHD (doctorate). |

## `courses`

Simulated source **Academic Catalog**. Row grain **One course**. Row count **36**.

| Column | Logical Type | Key | Nullable | Definition |
| --- | --- | --- | --- | --- |
| `course_id` | `TEXT` | PK | No | Course ID. |
| `course_name` | `TEXT` | — | No | Synthetic course name. |
| `department_id` | `TEXT` | FK → `departments.department_id` | No | Department that owns the course. |
| `credits` | `INTEGER` | — | No | Number of credits for the course. |

## `sections`

Simulated source **Section Scheduling**. Row grain **One course section offered**. Row count **432**.

| Column | Logical Type | Key | Nullable | Definition |
| --- | --- | --- | --- | --- |
| `section_id` | `TEXT` | PK | No | Section ID, unique across all semesters. |
| `term_id` | `TEXT` | FK → `terms.term_id` | No | Semester in which the section is offered. |
| `course_id` | `TEXT` | FK → `courses.course_id` | No | Course taught in the section. |
| `planned_periods` | `INTEGER` | — | No | Scheduled teaching periods for the section. Each period is 45 minutes. |

## `enrollments`

Simulated source **Enrollment and Grades**. Row grain **One student's enrollment in one section**. Row count **6,690**.

| Column | Logical Type | Key | Nullable | Definition |
| --- | --- | --- | --- | --- |
| `student_id` | `TEXT` | PK + FK → `students.student_id` | No | Student ID. |
| `section_id` | `TEXT` | PK + FK → `sections.section_id` | No | Section in which the student enrolled. |
| `result_status` | `TEXT` | — | No | GRADED means a grade is available, WITHDRAWN means the student withdrew, and PENDING means a grade is pending. |
| `final_score` | `DECIMAL(3,1)` | — | Yes | Final grade on a 0–10 scale. Present only when the status is GRADED. |

## `teaching_assignments`

Simulated source **Teaching Assignments**. Row grain **One instructor's assignment to one section**. Row count **540**.

| Column | Logical Type | Key | Nullable | Definition |
| --- | --- | --- | --- | --- |
| `section_id` | `TEXT` | PK + FK → `sections.section_id` | No | Section ID. |
| `instructor_id` | `TEXT` | PK + FK → `instructors.instructor_id` | No | Instructor ID. |
| `teaching_role` | `TEXT` | — | No | LEAD means lead instructor and CO means co-instructor. |
| `assigned_periods` | `INTEGER` | — | No | Number of scheduled periods assigned to the instructor for this section. |
