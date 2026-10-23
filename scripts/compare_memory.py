"""Measure how much memory the project's data structures use.

Run from the project folder with:  python -m scripts.compare_memory
"""

import tempfile
import tracemalloc
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Union

from student_grade_analytics.io_utils import iter_rows, load_students
from student_grade_analytics.models import Course, Grade

COUNT = 100_000
MATH = Course(code="MATH101", name="Calculus", credits=3)


@dataclass(frozen=True)
class GradeNoSlots:
    """The same fields as Grade, but without slots=True (for comparison)."""

    course: Course
    semester: str
    score: float


def measure(build: Callable[[], object]) -> int:
    """Run `build` and return the peak memory it used, in bytes."""
    tracemalloc.start()
    result = build()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del result
    return peak


def to_mb(size: int) -> str:
    """Format a number of bytes as megabytes."""
    return f"{size / 1024 / 1024:.2f} MB"


# ---- Comparison 1: one grade stored in different ways ----

def grades_with_slots() -> List[Grade]:
    grades = []
    for i in range(COUNT):
        grades.append(Grade(course=MATH, semester="2025-S1", score=float(i % 100)))
    return grades


def grades_without_slots() -> List[GradeNoSlots]:
    grades = []
    for i in range(COUNT):
        grades.append(
            GradeNoSlots(course=MATH, semester="2025-S1", score=float(i % 100))
        )
    return grades


def grades_as_dicts() -> List[Dict[str, Union[Course, str, float]]]:
    grades: List[Dict[str, Union[Course, str, float]]] = []
    for i in range(COUNT):
        grades.append({"course": MATH, "semester": "2025-S1", "score": float(i % 100)})
    return grades


# ---- Comparison 2: one course stored in different ways ----

def courses_as_namedtuples() -> List[Course]:
    courses = []
    for i in range(COUNT):
        courses.append(Course(code="MATH101", name="Calculus", credits=i % 5))
    return courses


def courses_as_dicts() -> List[Dict[str, Union[str, int]]]:
    courses: List[Dict[str, Union[str, int]]] = []
    for i in range(COUNT):
        courses.append({"code": "MATH101", "name": "Calculus", "credits": i % 5})
    return courses


# ---- Comparison 3: reading a large CSV, list vs generator ----

def write_large_csv(path: Path) -> None:
    """Write a CSV with COUNT rows (10 grades for each student)."""
    with open(path, "w", newline="", encoding="utf-8") as file:
        file.write(
            "student_id,name,major,year,course_code,course_name,credits,semester,score\n"
        )
        for i in range(COUNT):
            student = i // 10
            file.write(
                f"S{student},Student{student},Math,{student % 4 + 1},"
                f"MATH101,Calculus,3,2025-S1,{i % 100}\n"
            )


def main() -> None:
    """Run every comparison and print the results."""
    print(f"Memory used to store {COUNT:,} objects\n")

    print("Grade (dataclass)")
    print(f"  slots=True (our Grade)   {to_mb(measure(grades_with_slots))}")
    print(f"  without slots            {to_mb(measure(grades_without_slots))}")
    print(f"  plain dict               {to_mb(measure(grades_as_dicts))}")

    print("\nCourse (NamedTuple)")
    print(f"  NamedTuple (our Course)  {to_mb(measure(courses_as_namedtuples))}")
    print(f"  plain dict               {to_mb(measure(courses_as_dicts))}")

    with tempfile.TemporaryDirectory() as folder:
        csv_path = Path(folder) / "large.csv"
        write_large_csv(csv_path)

        def total_with_list() -> float:
            total = 0.0
            for student in load_students(csv_path):
                for grade in student.grades:
                    total += grade.score
            return total

        def total_with_generator() -> float:
            total = 0.0
            for row in iter_rows(csv_path):
                total += float(row["score"])
            return total

        print(f"\nReading a CSV with {COUNT:,} rows (sum of all scores)")
        print(f"  load_students (list)     {to_mb(measure(total_with_list))}")
        print(f"  iter_rows (generator)    {to_mb(measure(total_with_generator))}")
        print(f"  same result? {total_with_list() == total_with_generator()}")


if __name__ == "__main__":
    main()
