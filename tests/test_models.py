"""Tests for Course, Grade and Student."""

import pytest

from student_grade_analytics.models import Course, Grade, Student

MATH = Course(code="MATH101", name="Calculus", credits=3)


def test_letter_grades() -> None:
    assert Grade(course=MATH, semester="S1", score=90).letter == "A"
    assert Grade(course=MATH, semester="S1", score=89.9).letter == "B"
    assert Grade(course=MATH, semester="S1", score=70).letter == "C"
    assert Grade(course=MATH, semester="S1", score=60).letter == "D"
    assert Grade(course=MATH, semester="S1", score=59).letter == "F"


def test_score_out_of_range_raises() -> None:
    with pytest.raises(ValueError):
        Grade(course=MATH, semester="S1", score=101)
    with pytest.raises(ValueError):
        Grade(course=MATH, semester="S1", score=-1)


def test_year_out_of_range_raises() -> None:
    with pytest.raises(ValueError):
        Student(student_id="S1", name="Ama", major="Math", year=5)


def test_average_with_no_grades_is_none() -> None:
    student = Student(student_id="S1", name="Ama", major="Math", year=1)
    assert student.average() is None


def test_average() -> None:
    student = Student(student_id="S1", name="Ama", major="Math", year=1)
    student.grades.append(Grade(course=MATH, semester="S1", score=80))
    student.grades.append(Grade(course=MATH, semester="S2", score=90))
    assert student.average() == 85


def test_grade_for() -> None:
    student = Student(student_id="S1", name="Ama", major="Math", year=1)
    grade = Grade(course=MATH, semester="S1", score=80)
    student.grades.append(grade)
    assert student.grade_for("MATH101") == grade
    assert student.grade_for("BIO101") is None
