"""Tests for reading the CSV file and writing the JSON report."""

import json
from pathlib import Path
from typing import List

from student_grade_analytics.io_utils import load_students, write_report
from student_grade_analytics.models import Student
from student_grade_analytics.reports import build_report

SAMPLE_CSV = Path(__file__).parent.parent / "data" / "students.csv"


def test_load_sample_data() -> None:
    students = load_students(SAMPLE_CSV)
    assert len(students) == 10
    assert students[0].name == "Ama"
    assert len(students[0].grades) == 3
    assert students[0].grades[0].score == 88.0


def test_load_small_csv(tmp_path: Path) -> None:
    csv_file = tmp_path / "small.csv"
    csv_file.write_text(
        "student_id,name,major,year,course_code,course_name,credits,semester,score\n"
        "S1,Ama,Math,2,MATH101,Calculus,3,2025-S1,88\n"
        "S1,Ama,Math,2,CS101,Programming,4,2025-S2,92\n",
        encoding="utf-8",
    )
    students = load_students(str(csv_file))  # a str path works too
    assert len(students) == 1
    assert students[0].year == 2
    assert students[0].grades[1].course.credits == 4


def test_missing_file_returns_empty_list(tmp_path: Path) -> None:
    assert load_students(tmp_path / "missing.csv") == []


def test_write_report_creates_json(
    tmp_path: Path, students: List[Student]
) -> None:
    out_file = tmp_path / "new_folder" / "report.json"
    write_report(build_report(students), out_file)

    with open(out_file, encoding="utf-8") as file:
        data = json.load(file)
    assert data["total_students"] == 3
    assert data["statistics"]["mode"] == "A"
