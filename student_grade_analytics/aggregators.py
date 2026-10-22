"""Collection-based aggregators (Counter, defaultdict, OrderedDict, deque)."""

from collections import Counter, OrderedDict, defaultdict, deque
from typing import Dict, List, Optional

from student_grade_analytics.models import Student


def grade_distribution(students: List[Student]) -> Counter[str]:
    """Count how many of each letter grade (A, B, C, D, F) there are."""
    letters = []
    for student in students:
        for grade in student.grades:
            letters.append(grade.letter)
    return Counter(letters)


def group_by_major(students: List[Student]) -> Dict[str, List[Student]]:
    """Group students by their major."""
    groups: defaultdict[str, List[Student]] = defaultdict(list)
    for student in students:
        groups[student.major].append(student)
    return dict(groups)


def group_by_year(students: List[Student]) -> Dict[int, List[Student]]:
    """Group students by their year of study."""
    groups: defaultdict[int, List[Student]] = defaultdict(list)
    for student in students:
        groups[student.year].append(student)
    return dict(groups)


def rank_students(students: List[Student]) -> OrderedDict[str, float]:
    """Return student names and averages, from highest to lowest average."""
    pairs = []
    for student in students:
        avg = student.average()
        if avg is not None:
            pairs.append((avg, student.name))
    pairs.sort(reverse=True)

    ranking: OrderedDict[str, float] = OrderedDict()
    for avg, name in pairs:
        ranking[name] = avg
    return ranking


class RollingAverage:
    """Average of only the last few values added."""

    def __init__(self, size: int) -> None:
        """Keep at most `size` values; older ones are dropped automatically."""
        self.values: deque[float] = deque(maxlen=size)

    def add(self, value: float) -> None:
        """Add a new value."""
        self.values.append(value)

    def average(self) -> Optional[float]: 
        """Return the average of the stored values, or None if empty."""
        if not self.values:
            return None
        return sum(self.values) / len(self.values)
