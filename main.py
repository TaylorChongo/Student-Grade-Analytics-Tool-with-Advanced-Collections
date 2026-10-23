"""Run the tool: load the CSV, build the report and save it as JSON."""

from pathlib import Path

from student_grade_analytics.io_utils import load_students, write_report
from student_grade_analytics.reports import build_report

DATA_FILE = Path("data") / "students.csv"
OUTPUT_FILE = Path("output") / "report.json"


def main() -> None:
    """Load the students, build the report, save it and print a summary."""
    students = load_students(DATA_FILE)
    if not students:
        return

    report = build_report(students)
    write_report(report, OUTPUT_FILE)

    stats = report["statistics"]
    print(f"Students: {report['total_students']}")
    print(f"Mean: {stats['mean']}  Median: {stats['median']}  Mode: {stats['mode']}")

    print("Top 3 students:")
    position = 1
    for name, avg in report["ranking"].items():
        if position > 3:
            break
        print(f"  {position}. {name} ({avg})")
        position += 1

    print(f"Report saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
