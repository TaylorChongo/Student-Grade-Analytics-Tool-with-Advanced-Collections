"""Shared test data, available to every test file."""

from typing import List

import pytest

from student_grade_analytics.models import Course, Grade, Student

MATH = Course(code="MATH101", name="Calculus", credits=3)
CS = Course(code="CS101", name="Programming", credits=4)
BIO = Course(code="BIO101", name="Cell Biology", credits=3)


@pytest.fixture
def students() -> List[Student]:
    """Three small students whose results are easy to check by hand.

    Scores: Ama 90, 80 | Kofi 70 | Esi 95, 100
    Averages: Esi 97.5, Ama 85.0, Kofi 70.0
    """
    ama = Student(student_id="S1", name="Ama", major="Math", year=2)
    ama.grades.append(Grade(course=MATH, semester="2025-S1", score=90))
    ama.grades.append(Grade(course=CS, semester="2025-S2", score=80))

    kofi = Student(student_id="S2", name="Kofi", major="Biology", year=1)
    kofi.grades.append(Grade(course=BIO, semester="2025-S1", score=70))

    esi = Student(student_id="S3", name="Esi", major="Math", year=3)
    esi.grades.append(Grade(course=MATH, semester="2025-S1", score=95))
    esi.grades.append(Grade(course=CS, semester="2025-S2", score=100))

    return [ama, kofi, esi]
