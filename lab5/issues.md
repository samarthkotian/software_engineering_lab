# Lab 5 - Issue identification and fixes

All line numbers below refer to the original supplied file, preserved at
`reports/before/student_grade_system.py`. Security severity is Bandit's reported
severity. Quality/style priorities are descriptive, not invented Bandit ratings.
Every listed issue is resolved in the final file without disabling checks.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| B324: weak MD5 hash | Security - High | 49 | MD5 is unsuitable for security-sensitive hashing. | Use `hashlib.sha256` with UTF-8 input. This is an identifier digest, not password storage. |
| B605: shell execution | Security - High | 60 | A filename is concatenated into an `os.system` command, allowing shell metacharacters to be interpreted. | Remove the shell invocation and print the completion message directly. |
| B307 / W0123: `eval` | Security - Medium | 44 | Evaluating a supplied GPA expression can execute arbitrary Python code. | Replace expression evaluation with validated numeric scaling: mean score divided by a positive finite scale. Update the demo call. |
| B110 / W0702 / E722: bare exception and silent `pass` | Security - Low / reliability | 26-27 | All exceptions, including programming errors, are silently swallowed. | Validate student membership and attendance bounds explicitly; return a success flag. Unexpected programming errors remain visible. |
| B311: predictable PIN generation | Security - Low | 53 | `random.randint` is not suitable for generating security-sensitive PINs. | Use `secrets.randbelow(9000) + 1000` to preserve the four-digit range. |
| B105: hardcoded portal token | Security - Low | 64, 72 | An embedded credential is also printed to the console. | Read optional `GRADE_PORTAL_TOKEN` from the environment and print only its Boolean presence. |
| W0102: mutable default list | Bug / quality | 15 | The same default audit list is shared across function calls. | Default to `None` and allocate a fresh list inside `add_grade`. Caller-provided lists remain supported. |
| W1514 / R1732: unsafe resource handling | Reliability / quality | 57-59 | The file has no explicit encoding and may stay open if writing raises an error. | Use a context manager with explicit UTF-8 encoding. File errors propagate to the caller. |
| C0103 / C0116: naming and missing docstrings | Maintainability | 15, 23, 30, 41, 48, 52, 56, 63 | The function name `addGrade` violates snake_case and functions lack documentation. | Rename it to `add_grade`, update the caller, and document each function. |
| W0611 / F401 / W0612 / F841: unused code | Quality / style | 6, 31, 43 | `json` and `grace_marks` are unused. `avg_score` is only referenced dynamically inside `eval`, so analyzers cannot see its use. | Remove the unused import and variable; use `avg_score` directly in numeric GPA calculation. |
| C0121 / E711 / R1703 / R1705: comparisons and branching | Quality / style | 32, 35-38 | Equality comparison with `None` and unnecessary `if/else` obscure simple logic. | Use `is None`, guard missing/empty records, and return the comparison directly. |
| C0209 / E501 / C0304 / W292: formatting | Style | 19, 34, 75 | Old string formatting, two lines over 79 characters, and a missing final newline reduce consistency. | Use an f-string, split the long calculation using local variables, and end the file with a newline. |

## Additional behavior checks

- Reject scores outside 0-100 and invalid attendance increments without mutation.
- Return `False` for passing-status checks on unknown students or empty marks.
- Raise clear `ValueError` exceptions for unknown students, empty marks, and
  invalid GPA scales rather than evaluating a string or dividing by zero.
- Guard `main()` so importing the module does not print or write a grade sheet.
- Keep the original equal weighting of scores: after adding 95 to S01,
  `(85 + 90 + 78 + 95) / 4 / 20 = 4.35`.
- Ten regression tests verify these behaviors, secure PIN generation, SHA-256,
  literal treatment of shell characters in filenames, and token redaction.

## Verified results

| Tool | Before | After |
|---|---|---|
| Pylint 4.1.3 | 5.51/10, 22 messages, exit 28 | 10.00/10, no messages, exit 0 |
| Bandit 1.9.4 | 6 findings: 2 High, 1 Medium, 3 Low; exit 1 | No findings; exit 0 |
| Flake8 7.5.0 | 8 findings; exit 1 | No output; empty report; exit 0 |

Reports contain stdout followed by stderr, without filtering or suppression.
The final Flake8 report is intentionally zero bytes because success is silent.
