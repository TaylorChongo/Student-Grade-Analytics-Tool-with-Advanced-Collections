"""Tests for build_report."""

from typing import List

from student_grade_analytics.models import Student
from student_grade_analytics.reports import build_report


def test_build_report(students: List[Student]) -> None:
    report = build_report(students)
    assert report["total_students"] == 3
    assert report["grade_distribution"] == {"A": 3, "B": 1, "C": 1}
    assert report["students_per_major"] == {"Math": 2, "Biology": 1}
    assert list(report["ranking"]) == ["Esi", "Ama", "Kofi"]
    assert report["percentiles"]["Esi"] == 100.0
    assert report["trends"]["Kofi"] is None
    assert report["statistics"] == {"mean": 87.0, "median": 90.0, "mode": "A"}
