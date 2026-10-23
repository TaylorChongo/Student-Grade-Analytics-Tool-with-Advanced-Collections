# Student Grade Analytics Tool

A command-line tool that reads student grades from a CSV file, calculates statistics (averages, grade distribution, rankings, percentiles, semester trends) and saves a report as JSON.

It is built with Python's advanced collections (`Counter`, `defaultdict`, `OrderedDict`, `deque`), `dataclasses` and `NamedTuple`, and type hints throughout (checked with `mypy --strict`).


---

## Setup

Requires **Python 3.11+** (developed with 3.14).

Repository: [Student-Grade-Analytics-Tool-with-Advanced-Collections](https://github.com/TaylorChongo/Student-Grade-Analytics-Tool-with-Advanced-Collections)

```bash
git clone <repo-link>

cd Student-Grade-Analytics-Tool-with-Advanced-Collections

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

| Command | What it does |
|---|---|
| `python main.py` | Reads `data/students.csv`, prints a summary, writes `output/report.json` |
| `python -m pytest` | Runs the tests |
| `python -m mypy main.py student_grade_analytics tests scripts` | Type check (strict mode) |
| `python -m scripts.compare_memory` | Runs the memory comparison (see [Performance notes](#performance-notes)) |

---

## Project structure

```
student-grade-analytics/
├── main.py                      # entry point
├── data/students.csv            # sample input
├── output/report.json           # sample output
├── scripts/compare_memory.py    # memory comparison
├── student_grade_analytics/
│   ├── models.py                # Course (NamedTuple), Grade, Student (dataclasses)
│   ├── aggregators.py           # Counter, defaultdict, OrderedDict, deque
│   ├── stats.py                 # mean, median, mode, percentiles, trends
│   ├── reports.py               # Report / Statistics (TypedDict), build_report
│   └── io_utils.py              # CSV reading, JSON writing, iter_rows generator
└── tests/                       # pytest tests
```

### Where each collection is used

| Collection | Where | Why |
|---|---|---|
| `Counter` | `grade_distribution()` | Counts how many A, B, C, D, F grades; `most_common()` gives the mode |
| `defaultdict(list)` | `group_by_major()`, `group_by_year()`, `grade_trend()` | Groups items without checking if the key exists first |
| `OrderedDict` | `rank_students()`, `ranking` in the report | Keeps students in order, best to worst |
| `deque(maxlen=...)` | `RollingAverage`, `grade_trend()` | Keeps only the last N values; older ones drop out automatically |
| `NamedTuple` | `Course` | A course never changes, so a light, immutable tuple is enough |
| `dataclass(slots=True)` | `Grade` (also `frozen`), `Student` | Structured data with validation and lower memory use |
| `TypedDict` | `Report`, `Statistics` | Describes the shape of the JSON report so mypy can check it |

---

## Sample input

`data/students.csv` has one row per grade. A student with several grades appears on several rows.

```csv
student_id,name,major,year,course_code,course_name,credits,semester,score
S001,Ama,Math,2,MATH101,Calculus,3,2025-S1,88
S001,Ama,Math,2,CS101,Programming,4,2025-S2,92
S001,Ama,Math,2,PHY101,Physics,3,2025-S2,95
S002,Kofi,Biology,1,BIO101,Cell Biology,3,2025-S1,74
S002,Kofi,Biology,1,ENG101,English,2,2025-S2,68
...
```

The sample file has 10 students, 3 majors and 22 grades over 2 semesters.

## Sample output

Terminal:

```
Students: 10
Mean: 77.7  Median: 80.5  Mode: A
Top 3 students:
  1. Esi (94.0)
  2. Adwoa (93.5)
  3. Ama (91.7)
Report saved to output\report.json
```

### JSON report example

`output/report.json`:

```json
{
  "total_students": 10,
  "grade_distribution": {"B": 5, "A": 6, "C": 4, "D": 4, "F": 3},
  "students_per_major": {"Math": 3, "Biology": 4, "Computer Science": 3},
  "ranking": {
    "Esi": 94.0, "Adwoa": 93.5, "Ama": 91.7, "Kojo": 83.5, "Abena": 83.5,
    "Kwame": 81.5, "Kofi": 71.0, "Yaw": 63.0, "Kweku": 62.0, "Akosua": 53.5
  },
  "percentiles": {
    "Ama": 77.8, "Kofi": 33.3, "Esi": 100.0, "Yaw": 22.2, "Abena": 55.6,
    "Kwame": 44.4, "Akosua": 0.0, "Kojo": 55.6, "Adwoa": 88.9, "Kweku": 11.1
  },
  "trends": {
    "Ama": 5.5, "Kofi": -6.0, "Esi": -6.0, "Yaw": 12.0, "Abena": 3.0,
    "Kwame": 5.0, "Akosua": 17.0, "Kojo": -13.0, "Adwoa": -11.0, "Kweku": 8.0
  },
  "statistics": {"mean": 77.7, "median": 80.5, "mode": "A"}
}
```

(The real file uses one value per line; it is shortened here.)

### What each field means

| Field | Meaning |
|---|---|
| `total_students` | Number of students loaded |
| `grade_distribution` | How many grades of each letter (A ≥ 90, B ≥ 80, C ≥ 70, D ≥ 60, F < 60) |
| `students_per_major` | Number of students in each major |
| `ranking` | Each student's average, best to worst |
| `percentiles` | Percentage of other students each student beats (100 = top, 0 = bottom) |
| `trends` | Latest semester average minus the previous one. Positive = improving, negative = dropping, `null` = only one semester |
| `statistics` | Mean and median of all scores, and the most common letter grade (mode) |

---

## Error handling

- **Missing CSV file:** prints `File not found: <path>` and stops, without a crash.
- **No permission to read or write:** prints a clear message instead of crashing.
- **Invalid data:** a score outside 0–100 or a year outside 1–4 raises a `ValueError` when the object is created.
- The output folder is created automatically if it does not exist.
- All files are opened with `with open(...)`, so they are always closed, even if an error happens.

---

## Performance notes

`scripts/compare_memory.py` measures the project's real classes with `tracemalloc`. Each approach stores the same data 100,000 times, and the peak memory used is compared.

Run it with:

```bash
python -m scripts.compare_memory
```

### Results

| What is stored (100,000 times) | Approach | Memory |
|---|---|---|
| Grade | `dataclass(slots=True)` (**our `Grade`**) | **8.39 MB** |
| Grade | `dataclass` without slots | 12.21 MB |
| Grade | plain `dict` | 20.59 MB |
| Course | `NamedTuple` (**our `Course`**) | **8.39 MB** |
| Course | plain `dict` | 18.30 MB |

| Reading a 100,000-row CSV (sum of all scores) | Memory |
|---|---|
| `load_students()` (builds a full list) | 33.24 MB |
| `iter_rows()` (generator) | **0.16 MB** |

Both CSV methods give the same total. Exact numbers vary a little between machines and Python versions.

### What the results mean

- **`slots=True` saves memory.** A normal object keeps its fields in a hidden dictionary. With `slots=True`, each object only has fixed spaces for its fields. Our `Grade` uses about 30% less memory than without slots, and about 60% less than a dict. The only downside is that you cannot add new attributes to an object later, which `Grade` never needs.
- **`NamedTuple` saves memory.** The field names are stored once in the class, not in every object. `Course` uses about half the memory of a dict. It cannot be changed after creation, which is fine because a course never changes.
- **A `dict` is the most flexible but the heaviest.** Each dict stores its own keys and keeps extra space so it can grow. That is useful for the JSON report, but wasteful for thousands of records with the same fields.
- **Generators keep memory flat.** `load_students()` holds every student, grade and course in memory at once. `iter_rows()` gives one row at a time and forgets it, so memory stays tiny however large the file is.

### When to use which

- Use **`load_students()`** for reports. Ranking and percentiles need all students at once, and the dataset fits in memory.
- Use **`iter_rows()`** for very large files that only need to be read once from start to end, for example summing or counting scores.
- **`Counter`** and **`defaultdict`** count and group in a single pass through the data, so the work grows with the number of grades (O(n)).
- **`deque(maxlen=...)`** adds and drops values in constant time. A list would need to remove its first item, which is slow on large lists.

---

## Testing

```bash
python -m pytest
```

The 28 tests cover:

- **Models:** letter grades, average, `grade_for`, invalid score or year
- **Collections:** one test group each for `Counter`, `defaultdict`, `OrderedDict`, `deque`
- **Statistics:** mean, median (odd and even counts), mode, percentiles, trends
- **Files:** loading the sample CSV, a missing file, the `iter_rows` generator, writing the JSON report
- **Report:** every field of `build_report`

Shared test data lives in `tests/conftest.py`. File tests use pytest's `tmp_path`, so they never change the real `data/` or `output/` folders.
