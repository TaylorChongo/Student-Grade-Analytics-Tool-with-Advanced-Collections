"""Tests for the collection-based aggregators."""

from typing import List

from student_grade_analytics.aggregators import (
    RollingAverage,
    grade_distribution,
    group_by_major,
    group_by_year,
    rank_students,
)
from student_grade_analytics.models import Student


# Counter
def test_grade_distribution(students: List[Student]) -> None:
    counts = grade_distribution(students)
    assert counts["A"] == 3
    assert counts["B"] == 1
    assert counts["C"] == 1
    assert counts["F"] == 0


# defaultdict
def test_group_by_major(students: List[Student]) -> None:
    groups = group_by_major(students)
    math_names = []
    for student in groups["Math"]:
        math_names.append(student.name)
    assert math_names == ["Ama", "Esi"]
    assert len(groups["Biology"]) == 1


def test_group_by_year(students: List[Student]) -> None:
    groups = group_by_year(students)
    assert sorted(groups) == [1, 2, 3]
    assert groups[1][0].name == "Kofi"


# OrderedDict
def test_rank_students_best_first(students: List[Student]) -> None:
    ranking = rank_students(students)
    assert list(ranking) == ["Esi", "Ama", "Kofi"]
    assert ranking["Esi"] == 97.5


def test_rank_students_skips_students_without_grades() -> None:
    student = Student(student_id="S1", name="Ama", major="Math", year=1)
    assert len(rank_students([student])) == 0


# deque
def test_rolling_average_drops_oldest_value() -> None:
    rolling = RollingAverage(3)
    rolling.add(50)
    rolling.add(60)
    rolling.add(70)
    assert rolling.average() == 60
    rolling.add(90)  # 50 is dropped
    assert list(rolling.values) == [60, 70, 90]


def test_rolling_average_empty_is_none() -> None:
    assert RollingAverage(3).average() is None
