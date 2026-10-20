"""Data models: Student, Course and Grade."""

from dataclasses import dataclass, field
from typing import List, NamedTuple, Optional


class Course(NamedTuple):
    """A school subject. It never changes, so a light NamedTuple is enough."""

    code: str
    name: str
    credits: int


@dataclass(frozen=True, slots=True)
class Grade:
    """A student's grade in a specific course and semester."""

    course: Course
    semester: str
    score: float

    def __post_init__(self) -> None:
        """Check the score is between 0 and 100 when the grade is created."""
        if not (0 <= self.score <= 100):
            raise ValueError(f"Score must be between 0 and 100, got {self.score}.")

    @property  # helps access the letter with the dot notation.
    def letter(self) -> str:
        """Return the letter grade corresponding to the score."""
        if self.score >= 90:
            return 'A'
        elif self.score >= 80:
            return 'B'
        elif self.score >= 70:
            return 'C'
        elif self.score >= 60:
            return 'D'
        else:
            return 'F'


@dataclass(slots=True)
class Student:
    """A student with a name and a list of grades."""

    student_id: str
    name: str
    major: str
    year: int
    # we use default_factory to create a new list for each instance of Student.
    grades: List[Grade] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Check the year is between 1 and 4 when the student is created."""
        if self.year < 1 or self.year > 4:
            raise ValueError(f"Year must be between 1 and 4, got {self.year}.")

    def average(self) -> Optional[float]:
        """Return the average score, or None if the student has no grades."""
        if not self.grades:
            return None
        return sum(grade.score for grade in self.grades) / len(self.grades)

    def grade_for(self, course_code: str) -> Optional[Grade]:
        """Return the grade for a specific course code, or None if not found."""
        for grade in self.grades:
            if grade.course.code == course_code:
                return grade
        return None
