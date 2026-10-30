# Lab 5 - Static Code Analysis: Student Grade System

**Student:** Samarth Kotian

**SRN:** PES1UG24CS406

**Date:** 30 October 2026

**Assigned source:** https://github.com/SETAPESU26/L5_42_student_grade_system

**Individual repository:** https://github.com/samarthkotian/software_engineering_lab

The final program scores **10.00/10 in Pylint**, with **zero Bandit findings**
and **zero Flake8 findings**. All ten regression tests pass.

## Contents

- `student_grade_system.py`: corrected program; no third-party runtime imports.
- `issues.md`: twelve issue groups, original lines, fixes, and measured results.
- `reflection.md`: four standard reflection answers, as the handout omits them.
- `reports/before/` and `reports/after/`: all six complete analysis reports,
  program output, and recorded exit codes; the original source is retained.
- `evidence/`: screenshots of saved analyzer output before and after fixes.
- `output/pdf/Lab5_PES1UG24CS406_Static_Code_Analysis.pdf`: the single consolidated
  submission PDF, including screenshots and all six report contents.
- `test_student_grade_system.py`: regression tests.
- `tools/`: scripts for collecting analysis and assembling evidence.

## Run and verify

Use Python 3.12 or newer. From this `lab5` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe student_grade_system.py
.\.venv\Scripts\python.exe -m pylint --persistent=n student_grade_system.py
.\.venv\Scripts\python.exe -m bandit -r student_grade_system.py
.\.venv\Scripts\python.exe -m flake8 student_grade_system.py
.\.venv\Scripts\python.exe -m unittest -v
```

To regenerate the final raw reports, run
`.\.venv\Scripts\python.exe tools/capture_analysis.py after`.
Do not overwrite the saved `before` evidence with the corrected source.
Reports were captured with Python 3.12.14, Pylint 4.1.3, Bandit 1.9.4,
and Flake8 7.5.0, using the default enabled checks.

## Behavior and API changes

- `addGrade` becomes `add_grade`, with `grade_list=None` and score bounds.
- `compute_weighted_gpa(student_id, scale=20.0)` replaces the unsafe expression
  string parameter. Equal mark weights preserve the supplied program's behavior.
- The sample GPA remains 4.35; S02's attendance increases from 74 to 76.
- Invalid attendance updates return `False`; GPA validation raises `ValueError`.
- The student digest is SHA-256 and registration PINs use `secrets`.
- `GRADE_PORTAL_TOKEN` is optional. Output shows only whether it is configured.
- Grade-sheet export retains the supplied text representation with UTF-8 and a
  context manager. No shell is started. Importing the module has no side effects.

## Submission

The history contains a baseline evidence commit followed by separate **Pylint**,
**Bandit**, and **Flake8** fix commits. Some findings overlap between tools;
the issue table explains these overlaps rather than disabling rules.

Upload **only the consolidated PDF** to the professor's submission form:
https://forms.gle/kEdMtbTUJa64a1fZ7 . The raw `.txt` reports are retained here for
reproducibility and are embedded in the PDF; they are not separate Drive uploads.
