# Labs 6 and 7 - deliverables checklist

**Samarth Kotian | PES1UG24CS406 | 5G | 21 November 2026**

Assigned source:
[SETAPESU26/L6_L7_42_salon_booking](https://github.com/SETAPESU26/L6_L7_42_salon_booking).
The lab handouts determine the requirements. The layout was also checked against
[Satyam's submission](https://github.com/satyamgoyal06/SE-Labs-PES1UG24CS424):
separate Lab 6 suites with coverage images, and a Lab 7 report plus repaired
application and Hypothesis tests. Our tests and fixes target our assigned Salon
Booking module; the reference submission uses a different assigned project.

## Lab 6: Code and Branch Coverage

| Handout requirement | Location / result |
| --- | --- |
| Run initial line and branch analysis | `lab6/reports/initial_*` |
| Separate line-coverage test file | `lab6/CodeCoverageTest_salon_booking.py` - 14 tests, 37/37 statements (100%) |
| Separate branch-coverage test file | `lab6/BranchCoverageTest_salon_booking.py` - 71 tests, 26/26 branch exits and 37/37 statements (100%) |
| At least 90% line coverage | 100%; see `lab6/reports/line_coverage.json` |
| At least 90% branch coverage | 100%; see `lab6/reports/branch_coverage.json` |
| Final coverage output images only after reaching the threshold | `lab6/evidence/line_coverage.png` and `branch_coverage.png` |
| Separate line and branch commits | `cf1151f` (line) and `881c31d` (branch) |

The handout requests terminal-output screenshots. The included images render
the actual saved terminal output and are labeled accordingly; they are not
desktop captures. If literal desktop screenshots are required by the evaluator,
capture the commands in [lab6/README.md](lab6/README.md) and replace the images.

[Consolidated Lab 6 PDF](lab6/output/pdf/Lab6_PES1UG24CS406_Coverage.pdf).
The Lab 6 application is unchanged. Run both independent suites from `lab6/`.

## Lab 7: Fuzzing for Input Validation Bugs

| Handout requirement | Location / result |
| --- | --- |
| Original application output | `lab7/reports/before_application.txt` and `before_invalid_application.txt` |
| Complete Hypothesis tests for all three functions | `lab7/test_processor.py`; assigned filename `test_salon_booking.py` is a compatibility entry point |
| Capture failing tests before repair | `lab7/reports/before_fuzz.txt` - 38 failed, 4 passed |
| Repair the application | `lab7/salon_booking.py`; original retained in `lab7/original/` |
| Fixed application output | `lab7/reports/after_application.txt` and `after_invalid_application.txt` |
| Re-run the same completed tests | `lab7/reports/after_fuzz.txt` - 42 passed; 1,800 generated passing examples across six properties |
| PDF with before-and-after output images | [Lab 7 PDF](lab7/output/pdf/Lab7_PES1UG24CS406_Fuzz_Testing.pdf) |
| Fixed Python script and updated tests | Included directly in `lab7/` and in the PDF appendices |

The four Lab 7 evidence images are in `lab7/evidence/`. They render the recorded
outputs; complete tracebacks and Hypothesis statistics are retained in the raw
logs. The PDF also includes a bug/fix discussion, reflection answers and the
final source code. Those explanatory sections supplement the handout's listed
deliverables.

## Reproduce

Use Python 3.12 or newer. Follow the per-lab READMEs to install test dependencies
and run commands. Use separate processes for the two lab directories to avoid
mixing their identically named `salon_booking` modules.

No submission form has been filled or coursework uploaded to a submission portal.
