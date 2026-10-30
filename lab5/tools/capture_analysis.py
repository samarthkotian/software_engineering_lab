"""Save unfiltered analysis output and exit codes for a lab evidence stage."""

import json
from pathlib import Path
import subprocess
import sys


def main():
    """Capture the supplied program and all three analyzers."""
    stage = sys.argv[1]
    destination = Path("reports") / stage
    destination.mkdir(parents=True, exist_ok=True)
    commands = {
        "program": ["student_grade_system.py"],
        "pylint": ["-m", "pylint", "--persistent=n", "student_grade_system.py"],
        "bandit": ["-m", "bandit", "-r", "student_grade_system.py"],
        "flake8": ["-m", "flake8", "student_grade_system.py"],
    }
    metadata = {}
    for name, arguments in commands.items():
        command = [sys.executable, "-X", "utf8", *arguments]
        result = subprocess.run(
            command, capture_output=True, text=True, encoding="utf-8",
            errors="replace", check=False,
        )
        filename = "program_output.txt" if name == "program" else name + "_report.txt"
        content = result.stdout + result.stderr
        (destination / filename).write_text(content, encoding="utf-8")
        metadata[name] = {"command": arguments, "exit_code": result.returncode}
        print(f"{name}: exit code {result.returncode}")
        print(content)
    (destination / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
