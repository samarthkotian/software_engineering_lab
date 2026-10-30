# Lab 5 - Standard reflection questions

The supplied three-page lab handout does not include the reflection question
text. These four standard questions address its stated learning outcomes.

## 1. How did Pylint, Bandit, and Flake8 help improve this program?

Pylint highlighted maintainability and reliability problems such as the shared
mutable default list, missing docstrings, unused code, and unmanaged file
handling. Flake8 identified concrete style and correctness issues, including a
bare exception, comparison with `None`, unused names, long lines, and the missing
final newline. Bandit focused on security: it identified unsafe `eval`, MD5,
shell execution, predictable PIN generation, an embedded token, and silent
exception handling. Their overlapping findings helped verify the same repairs
from different perspectives. The final results were Pylint 10.00/10, zero Bandit
findings, and zero Flake8 findings.

## 2. Which issues were most important, and how were they prioritized?

The two High findings were addressed first in the security review: MD5 was
replaced by SHA-256 and the shell command was removed. The Medium `eval` finding
was replaced by direct arithmetic with a validated numeric scale. The Low
security findings were also fixed: cryptographic randomness now generates the
PIN, the token comes from the environment and is never printed, and invalid
attendance updates are handled explicitly. Quality and formatting repairs
followed. A secure digest does not make low-entropy student identifiers private,
and a four-digit PIN still requires rate limiting in a real authentication system.

## 3. What was challenging about fixing the issues while preserving behavior?

The main challenge was removing `eval` without changing the demonstrated GPA.
The original string `avg_score / 20.0` is now a numeric scale with default 20.0.
After recording S01's score of 95, the GPA remains 4.35. Arbitrary expression
strings are intentionally rejected. Another important change was replacing the
shared list default with `None` while retaining caller-supplied audit logs.
Explicit tests checked attendance updates, passing boundaries, invalid inputs,
safe export filenames, import behavior, and token redaction. All ten tests passed.

## 4. What are the limitations of static analysis, and how would it be used again?

A clean report cannot prove functional correctness or complete security.
Static analysis does not establish that grading rules match institutional
policy, that attendance is modeled correctly, or that authentication has suitable
rate limits. Flake8 also marked `avg_score` as unused because its use was hidden
inside an evaluated string, showing why findings need interpretation. I would
combine all three tools with code review and behavior tests, and run them before
commits or in continuous integration. Small commits for each tool make fixes
easier to review. Reports should record tool versions, original line numbers,
and before-and-after results so the improvements can be reproduced.
