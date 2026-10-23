"""The structure of the JSON report, and the function that builds it."""

from collections import OrderedDict
from typing import Dict, List, Optional, TypedDict

from student_grade_analytics.aggregators import (
    grade_distribution,
    group_by_major,
    rank_students,
)
from student_grade_analytics.models import Student
from student_grade_analytics.stats import (
    all_scores,
    grade_trend,
    mean,
    median,
    mode,
    percentile_ranks,
)


class Statistics(TypedDict):
    """Mean and median of all scores, and the most common letter grade."""

    mean: float
    median: float
    mode: str


class Report(TypedDict):
    """The full report that is written to a JSON file."""

    total_students: int
    grade_distribution: Dict[str, int]
    students_per_major: Dict[str, int]
    ranking: Dict[str, float]
    percentiles: Dict[str, float]
    trends: Dict[str, Optional[float]]
    statistics: Statistics


def build_report(students: List[Student]) -> Report:
    """Calculate everything and put it together in one report."""
    
    students_per_major: Dict[str, int] = {}
    for major, group in group_by_major(students).items():
        students_per_major[major] = len(group)

    # OrderedDict keeps the ranking from best to worst in the report.
    ranking: OrderedDict[str, float] = OrderedDict()
    for name, avg in rank_students(students).items():
        ranking[name] = round(avg, 1)

    trends: Dict[str, Optional[float]] = {}
    for student in students:
        trend = grade_trend(student)
        if trend is None:
            trends[student.name] = None
        else:
            trends[student.name] = round(trend, 1)

    scores = all_scores(students)
    statistics: Statistics = {
        "mean": round(mean(scores), 1),
        "median": round(median(scores), 1),
        "mode": mode(students),
    }

    report: Report = {
        "total_students": len(students),
        "grade_distribution": dict(grade_distribution(students)),
        "students_per_major": students_per_major,
        "ranking": ranking,
        "percentiles": percentile_ranks(students),
        "trends": trends,
        "statistics": statistics,
    }
    return report
