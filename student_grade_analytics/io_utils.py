"""Read students from a CSV file and write reports to a JSON file."""

import csv
import json
from pathlib import Path
from typing import Dict, List, Union

from student_grade_analytics.models import Course, Grade, Student
from student_grade_analytics.reports import Report


def load_students(path: Union[str, Path]) -> List[Student]:
    """Read a CSV file (one row per grade) and return the list of students."""
    path = Path(path)
    students_by_id: Dict[str, Student] = {}

    try:
        with open(path, newline="", encoding="utf-8") as file: 
            reader = csv.DictReader(file)
            for row in reader:
                student_id = row["student_id"]
                if student_id not in students_by_id:
                    students_by_id[student_id] = Student(
                        student_id=student_id,
                        name=row["name"],
                        major=row["major"],
                        year=int(row["year"]),
                    )

                course = Course(
                    code=row["course_code"],
                    name=row["course_name"],
                    credits=int(row["credits"]),
                )
                grade = Grade(
                    course=course,
                    semester=row["semester"],
                    score=float(row["score"]),
                )
                students_by_id[student_id].grades.append(grade)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return []
    except PermissionError:
        print(f"No permission to read: {path}")
        return []

    return list(students_by_id.values())


def write_report(report: Report, path: Union[str, Path]) -> None:
    """Write the report to a JSON file, creating the folder if needed."""
    path = Path(path)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)
    except PermissionError:
        print(f"No permission to write: {path}")
