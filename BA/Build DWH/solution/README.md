The script:
1. Loads `../HUST_Source_Data_EN/*.csv` into staging tables in `output/hust_dwh.sqlite`.
2. Builds the warehouse (`sql/1_schema.sql`, `sql/2_load.sql`).
3. Runs the pipeline a second time to check that the results stay the same.
4. Runs the checks (`sql/4_checks.sql`) and writes them to `output/checks.md`.
5. Creates `dashboards/student_dashboard.html` and `dashboards/instructor_dashboard.html` from `dashboards/template.html` and the queries in `sql/3_charts.sql`.

To view the dashboards, open the HTML files in a browser. Adding `#2024-1` to the end of the URL selects only that semester.
