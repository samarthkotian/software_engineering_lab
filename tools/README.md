# Report generation

The lab test dependencies are listed separately in each lab folder. The two
additional packages here are needed only to rebuild the PDF reports and output
images:

```powershell
python -m pip install -r tools/requirements-reports.txt
python tools/build_lab67_reports.py
```

Run from the repository root. The script reads the preserved UTF-8 logs in
`lab6/reports` and `lab7/reports`. It renders images of those logs and builds both
PDF reports. Lab 7 appendices read the current final application and tests.
Images are explicitly labeled as rendered output, not literal desktop captures.

The report builder does not run tests. Run the commands in each lab README to
verify the code. Do not overwrite saved baseline logs with runs of the fixed
application. Recreate the baseline in a temporary folder with the original
application and the completed final test suite, as described in `lab7/README.md`.
