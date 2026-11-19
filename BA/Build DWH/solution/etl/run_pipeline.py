"""Run: python3 etl/run_pipeline.py  (from the solution folder)"""
import csv
import json
import re
import sqlite3
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parent.parent
SOURCE: Path = ROOT.parent / "HUST_Source_Data_EN"
DB: Path = ROOT / "output" / "hust_dwh.sqlite"
TABLES: list[str] = ["departments", "programs", "terms", "students", "student_terms", "instructors",
                     "courses", "sections", "enrollments", "teaching_assignments"]


def load_staging(con: sqlite3.Connection) -> None:
    for name in TABLES:
        with open(SOURCE / f"{name}.csv", encoding="utf-8-sig", newline="") as f:
            rows: list[list[str]] = list(csv.reader(f))
        header: list[str] = rows[0]
        con.execute(f"DROP TABLE IF EXISTS stg_{name}")
        con.execute(f"CREATE TABLE stg_{name} ({', '.join(c + ' TEXT' for c in header)})")
        #? Empty values (missing final_score) become NULL
        data: list[list[str | None]] = [[v if v != "" else None for v in r] for r in rows[1:]]
        con.executemany(f"INSERT INTO stg_{name} VALUES ({', '.join('?' * len(header))})", data)


def sql_blocks(file: str) -> list[tuple[str, str, str]]:
    #@ Split a .sql file into (tag, description, query) blocks that start with "-- @tag  description"
    text: str = (ROOT / "sql" / file).read_text(encoding="utf-8")
    parts: list[str] = re.split(r"^-- @", text, flags=re.M)[1:]
    blocks: list[tuple[str, str, str]] = []
    for part in parts:
        head, query = part.split("\n", 1)
        tag, _, desc = head.partition("  ")
        blocks.append((tag.strip(), desc.strip(), query.strip()))
    return blocks


def run_once() -> tuple[list[tuple[str, str, str, str]], dict[str, list[dict]]]:
    DB.parent.mkdir(exist_ok=True)
    con: sqlite3.Connection = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    load_staging(con)
    con.executescript((ROOT / "sql" / "1_schema.sql").read_text(encoding="utf-8"))
    con.executescript((ROOT / "sql" / "2_load.sql").read_text(encoding="utf-8"))
    con.commit()

    checks: list[tuple[str, str, str, str]] = []
    for expected, desc, query in sql_blocks("4_checks.sql"):
        actual: str = str(con.execute(query).fetchone()[0])
        checks.append((desc, expected, actual, "PASS" if actual == expected else "FAIL"))

    charts: dict[str, list[dict]] = {}
    for name, _, query in sql_blocks("3_charts.sql"):
        cur: sqlite3.Cursor = con.execute(query)
        cols: list[str] = [c[0] for c in cur.description]
        charts[name] = [dict(zip(cols, r)) for r in cur.fetchall()]
    charts["terms"] = [r[0] for r in con.execute("SELECT term_id FROM dim_term ORDER BY term_id")]
    charts["depts"] = [r[0] for r in con.execute("SELECT department_id FROM dim_department ORDER BY 1")]
    charts["programs"] = [dict(id=r[0], dept=r[1]) for r in con.execute(
        "SELECT p.program_id, d.department_id FROM dim_program p JOIN dim_department d USING (department_key)")]
    con.close()
    return checks, charts


checks, charts = run_once()
#? Rerun on the same input and make sure checks and chart data do not change
checks2, charts2 = run_once()
checks.append(("Rerun with the same input gives identical checks and chart data", "True",
               str(checks == checks2 and charts == charts2), "PASS" if (checks == checks2 and charts == charts2) else "FAIL"))

lines: list[str] = ["| Check | Expected | Actual | Result |", "|---|---|---|---|"]
lines += [f"| {d} | {e} | {a} | {s} |" for d, e, a, s in checks]
(ROOT / "output" / "checks.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))

template: str = (ROOT / "dashboards" / "template.html").read_text(encoding="utf-8")
for page in ["student", "instructor"]:
    html: str = template.replace("__DATA__", json.dumps(charts)).replace("__PAGE__", page)
    (ROOT / "dashboards" / f"{page}_dashboard.html").write_text(html, encoding="utf-8")
print("Dashboards written to dashboards/")
