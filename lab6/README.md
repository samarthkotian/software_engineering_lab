# Lab 6 - Code and Branch Coverage: Salon Booking

**Samarth Kotian | PES1UG24CS406 | 5G**

The assigned application is unchanged. All three functions are tested:
`extra_time_charge`, `can_book`, and `arrival_status`.

| Run | Tests passed | Application coverage |
| --- | ---: | --- |
| Starter tests | 2 | 14/37 statements (38% rounded); combined statement/branch score 32% |
| Line suite | 14 | 37/37 statements (100%) |
| Branch suite | 71 | 37/37 statements and 26/26 branch exits (100%) |

`coverage report` in branch mode shows a combined statement-and-branch score;
the branch-only result here is independently 26/26 exits. The final application
has no missing statements or partial branches.

## Files

- [CodeCoverageTest_salon_booking.py](CodeCoverageTest_salon_booking.py): line suite.
- [BranchCoverageTest_salon_booking.py](BranchCoverageTest_salon_booking.py):
  decision outcomes and boundary cases.
- [evidence](evidence/): final line and branch output images, rendered from saved
  process logs and labeled as such.
- [reports](reports/): complete initial/final logs and machine-readable coverage JSON.
- [PDF report](output/pdf/Lab6_PES1UG24CS406_Coverage.pdf): results, interpretation,
  test design and final evidence.
- `original/`: preserved assigned files; excluded from test discovery.

## Run

From this `lab6` directory, using Python 3.12+:

```powershell
python -m pip install -r requirements.txt
python -m coverage run --source=salon_booking -m pytest CodeCoverageTest_salon_booking.py -v
python -m coverage report -m --fail-under=90
python -m coverage run --branch --source=salon_booking -m pytest BranchCoverageTest_salon_booking.py -v
python -m coverage report -m --fail-under=90
```

Coverage is restricted to the application rather than including the test code.
`python -m pytest -q` runs the starter, line and branch suites together: 87 tests.
To reproduce the two-test baseline, substitute `test_salon_booking.py` in the
coverage command. Initial logs are retained without baseline evidence images,
as the handout requests images only after reaching at least 90%.

## Coverage decisions

Tests cross the member allowance and service exclusions, junior/senior rates,
extra-time thresholds 0/1/60/61, unknown services and negative durations. Booking
tests cross the party limits 2 and 4 and service limit 2. Arrival tests cover
both sides of each weekday/weekend and colour/non-colour cutoff, including the
inclusive late boundary. Expected-value assertions check the result as well as
executing each path.

The required line and branch work is recorded in separate commits (`cf1151f`
and `881c31d`). See the [overall checklist](../Lab6_Lab7_README.md).
