# Software Engineering Labs 6 and 7 - Salon Booking

Samarth Kotian | PES1UG24CS406 | 5G | 21 November 2026

Assigned source: https://github.com/SETAPESU26/L6_L7_42_salon_booking

## Results

- Lab 6: line suite 14 passed, 37/37 statements (100%). Branch suite 71 passed,
  26/26 branch exits and 37/37 statements (100%). Application unchanged.
- Lab 7: the same completed suite changes from 38 failed / 4 passed on the
  original to 42 passed on the fixed code. Six Hypothesis properties each run
  300 examples. All three application functions are tested.

## Deliverables

Each lab contains code, tests, `original/`, captured `reports/`, `evidence/`
images, and its final PDF under `output/pdf/`. The evidence images are honest
renderings of recorded process output, not desktop screenshots. Full logs are
preserved, including tracebacks and generated-example statistics.

Lab 6 has separate `CodeCoverageTest_salon_booking.py` and
`BranchCoverageTest_salon_booking.py` suites. Lab 7's canonical suite is
`test_processor.py`; the assigned `test_salon_booking.py` remains an entry point.

## Run

Use Python 3.12+ and install `pytest`, `coverage`, and `hypothesis`. Run each
lab from its own folder, because the assigned modules have the same name.

From `Lab 6`:

```powershell
python -m coverage run --source=salon_booking -m pytest CodeCoverageTest_salon_booking.py
python -m coverage report -m --fail-under=90
python -m coverage run --branch --source=salon_booking -m pytest BranchCoverageTest_salon_booking.py
python -m coverage report -m --fail-under=90
```

From `Lab 7`:

```powershell
python salon_booking.py
python -m pytest test_processor.py -v --hypothesis-show-statistics
```

In this workspace an isolated interpreter is available at
`../.venv-lab67/Scripts/python.exe` relative to the repository root. The source
code needs no third-party packages at runtime.

Lab 7 returns `None` for invalid helper input, and the interactive app prints
a validation error. Known services are haircut, colour and spa. Finite,
nonnegative values are required; CSV durations use integers. Inputs longer
than 10,000 characters are rejected. The original floor-average, tax rate,
and zero bill floor are preserved.

## Baseline replay

Create a separate temporary folder, copy `Lab 7/original/salon_booking.py`
and the completed `Lab 7/test_processor.py` into it, then run the same pytest
command. Expect failures. The incomplete original test is preserved for
provenance, and excluded from discovery. The Lab 6 baseline uses its original
two tests, retained as `test_salon_booking.py`.

The required line and branch changes are recorded in separate local commits.
Nothing has been pushed or uploaded for submission.
