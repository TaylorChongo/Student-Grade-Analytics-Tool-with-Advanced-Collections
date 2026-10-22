"""The structure of the JSON report."""

from typing import Dict, Optional, TypedDict


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
