# Lab 7 - Fuzz Testing: Salon Booking

**Samarth Kotian | PES1UG24CS406 | 5G**

The completed Hypothesis suite tests all three assigned functions:
`parse_booking`, `duration_average`, and `payable_bill`.

| Application version | Result with the same completed tests |
| --- | --- |
| Original | 38 failed, 4 passed |
| Fixed | 42 passed |

The six generated properties each complete 300 passing examples (1,800 total).
There are also 35 invalid-input regression cases and one documented-example
test. Generation is deterministic; the test database and per-example deadline
are disabled. Complete example counts and any discarded draws are recorded in
`reports/after_fuzz.txt`.

## Deliverables

- [salon_booking.py](salon_booking.py): repaired application.
- [test_processor.py](test_processor.py): completed Hypothesis and regression
  suite, using the handout's generic test filename.
- [test_salon_booking.py](test_salon_booking.py): compatibility entry point for
  the assigned test filename; normal discovery runs only the canonical suite.
- [Lab 7 PDF](output/pdf/Lab7_PES1UG24CS406_Fuzz_Testing.pdf): before/after output
  images, bugs and fixes, reflections and complete final source appendices.
- [evidence](evidence/): original application, failing tests, fixed application,
  and passing tests, captured from the live xterm browser terminal during fresh
  local runs. Matching transcripts are in `reports/screenshot_*.txt`.
- [reports](reports/): full logs, original tracebacks and final Hypothesis statistics.
- `original/`: unchanged application and incomplete assigned test skeleton.

## Run

From this `lab7` directory, using Python 3.12+:

```powershell
python -m pip install -r requirements.txt
python salon_booking.py
python -m pytest test_processor.py -v --hypothesis-show-statistics
```

For the application prompts, try `haircut:45`, `30,45,60`, and `800|100`.
Results are `('Haircut', 45.0)`, `45`, and `844.0`.
For invalid input, try a blank booking, `1,,3`, and `nan|0`.
The program reports each error and continues instead of raising a traceback.

## Contract and fixes

Invalid helper input returns `None`. Non-string or blank input, malformed
separators, empty CSV fields, unknown services, negative values, non-finite
numbers and numeric overflow are rejected. Text longer than 10,000 characters
is rejected before parsing. EOF and cancellation end the interactive program
cleanly.

Valid service names are haircut, colour and spa, with case and surrounding
whitespace normalized. Durations are nonnegative; CSV durations are integers
and their average retains the original floor division. Billing retains
`max(bill * 1.18 - discount, 0)` and the original float API. Zero values are
valid, and a discount above the taxed bill produces zero.

## Replay baseline failures

Create an empty temporary directory and copy these two files into it:

1. `original/salon_booking.py`
2. The completed `test_processor.py` from this directory.

Run `python -m pytest test_processor.py -v --tb=short` there. Expect 38 failures
and 4 passes. The original incomplete test skeleton is kept as source evidence;
it is not a runnable baseline test suite. The fixed code and original code are
always tested with the same completed tests.

See the [overall checklist](../Lab6_Lab7_README.md).
