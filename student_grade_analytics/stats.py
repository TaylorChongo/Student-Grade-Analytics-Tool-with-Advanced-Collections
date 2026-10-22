"""Statistics: mean, median, mode, percentile ranks and grade trends."""

from collections import defaultdict, deque
from typing import Dict, List, Optional

from student_grade_analytics.aggregators import grade_distribution
from student_grade_analytics.models import Student


def all_scores(students: List[Student]) -> List[float]:
    """Return every score of every student in one list."""
    scores = []
    for student in students:
        for grade in student.grades:
            scores.append(grade.score)
    return scores


def mean(scores: List[float]) -> float:
    """Return the average of the scores, or 0.0 if there are none."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def median(scores: List[float]) -> float:
    """Return the middle score, or 0.0 if there are none."""
    if not scores:
        return 0.0
    ordered = sorted(scores)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def mode(students: List[Student]) -> str:
    """Return the most common letter grade, or "" if there are no grades."""
    counts = grade_distribution(students)
    if not counts:
        return ""
    return counts.most_common(1)[0][0]


def percentile_ranks(students: List[Student]) -> Dict[str, float]:
    """Return, for each student, the percentage of other students they beat."""
    averages: Dict[str, float] = {}
    for student in students:
        avg = student.average()
        if avg is not None:
            averages[student.name] = avg

    total = len(averages)
    ranks: Dict[str, float] = {}
    for name, avg in averages.items():
        if total == 1:
            ranks[name] = 100.0
            continue
        lower = 0
        for other_avg in averages.values():
            if other_avg < avg:
                lower += 1
        ranks[name] = round(lower / (total - 1) * 100, 1)
    return ranks


def grade_trend(student: Student) -> Optional[float]:
    """Return latest semester average minus the previous one, or None."""
    scores_by_semester: defaultdict[str, List[float]] = defaultdict(list)
    for grade in student.grades:
        scores_by_semester[grade.semester].append(grade.score)

    last_two: deque[float] = deque(maxlen=2)
    for semester in sorted(scores_by_semester):
        last_two.append(mean(scores_by_semester[semester]))

    if len(last_two) < 2:
        return None
    return last_two[1] - last_two[0]
