"""The structure of the JSON report."""

from typing import Dict, TypedDict


class Statistics(TypedDict):
    """Mean, median and mode of all scores."""

    mean: float
    median: float
    mode: float


class Report(TypedDict):
    """The full report that is written to a JSON file."""

    total_students: int
    grade_distribution: Dict[str, int]
    students_per_major: Dict[str, int]
    ranking: Dict[str, float]
    statistics: Statistics
