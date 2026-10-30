# Evidence scripts

Run these from the `lab5` directory. Analysis dependencies are pinned in
`../requirements.txt` (relative to this document).

- `python tools/capture_analysis.py after` runs the final program and the three
  analyzers, preserving both output streams and exit codes. Use the environment
  containing the pinned Pylint, Bandit, and Flake8 packages.
- `node tools/capture_report_screenshots.cjs` uses the Node `playwright` package
  and a headless Chromium browser to capture six views of the saved report text.
  Install Playwright and its Chromium browser with `npm install playwright` and
  `npx playwright install chromium` if not already available. Alternatively set
  `LAB5_BROWSER_EXE` to an installed Chrome executable. It uses a fresh browser
  process without personal browser sessions. The Bandit-before image is clearly
  labeled as an excerpt; the complete output is retained in text and PDF.
- `python tools/build_report.py` uses `reportlab` and `Pillow` to assemble the
  consolidated PDF from saved text, documentation, screenshots, and Git history.
  Install those authoring packages with `python -m pip install reportlab Pillow`
  if needed. They are not required by the corrected grading program.

The original `before` reports are baseline evidence and should not be overwritten
by analysis of the corrected program. Raw analyzer files are never edited to
replace warnings or insert success messages.
