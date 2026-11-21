# Report generation

The lab test dependencies are listed separately in each lab folder. The two
additional packages here are needed only to rebuild the PDF reports:

```powershell
python -m pip install -r tools/requirements-reports.txt
python tools/build_lab67_reports.py
```

Run from the repository root. The script embeds the existing six real terminal
screenshots from `lab6/evidence` and `lab7/evidence`. It never redraws their
contents or replaces them with generated images. Source appendices read the
current final test files and application.

The report builder does not run tests. Run the commands in each lab README to
verify the code. Do not overwrite saved baseline logs with runs of the fixed
application. Recreate the baseline in a temporary folder with the original
application and the completed final test suite, as described in `lab7/README.md`.

## Screenshot provenance

The six PNG files are browser screenshots taken through the computer-use
capture API while xterm.js displayed fresh output from the real Python
processes. They are screenshots of a browser terminal, rather than native
Windows Terminal windows. No output text, percentages or test outcomes are
painted into the images by the report builder.

`capture_terminal_evidence.py` runs the commands, stores transcripts and waits
for the capture controller between stages. `live_terminal_capture.py` streams
that output into the read-only xterm display on localhost. It does not accept
commands through the browser. The original Lab 7 program is copied into an
isolated directory and tested with the same completed final suite.

For a new capture session, use the Python test environment, place xterm.js 6.0.0
`lib/xterm.js` and `css/xterm.css` in `live_terminal_control/` beside this checkout's
lab workspace, and run `python tools/live_terminal_capture.py`. Open
`http://localhost:8766`, capture each stage, and create its `<stage>.continue`
file in that control directory. The six stage names are `line_coverage`,
`branch_coverage`, `before_application`, `before_fuzz`, `after_application`, and
`after_fuzz`. The optional `LAB_CAPTURE_ONLY` environment variable selects one
stage for recapture. Close the local server after saving the screenshots.
