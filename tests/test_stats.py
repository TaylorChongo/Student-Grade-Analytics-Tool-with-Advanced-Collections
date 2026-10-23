"""Tests for the statistics functions."""

from typing import List

from student_grade_analytics.models import Student
from student_grade_analytics.stats import (
    all_scores,
    grade_trend,
    mean,
    median,
    mode,
    percentile_ranks,
)


def test_all_scores(students: List[Student]) -> None:
    assert all_scores(students) == [90, 80, 70, 95, 100]


def test_mean() -> None:
    assert mean([90, 80, 70, 95, 100]) == 87
    assert mean([]) == 0.0


def test_median_odd_count() -> None:
    assert median([90, 80, 70, 95, 100]) == 90


def test_median_even_count() -> None:
    assert median([10, 40, 20, 30]) == 25


def test_median_empty() -> None:
    assert median([]) == 0.0


def test_mode_is_most_common_letter(students: List[Student]) -> None:
    assert mode(students) == "A"
    assert mode([]) == ""


def test_percentile_ranks(students: List[Student]) -> None:
    ranks = percentile_ranks(students)
    assert ranks["Esi"] == 100.0
    assert ranks["Ama"] == 50.0
    assert ranks["Kofi"] == 0.0


def test_grade_trend(students: List[Student]) -> None:
    ama, kofi, esi = students
    assert grade_trend(ama) == -10  # 90 then 80
    assert grade_trend(esi) == 5  # 95 then 100
    assert grade_trend(kofi) is None  # only one semester
