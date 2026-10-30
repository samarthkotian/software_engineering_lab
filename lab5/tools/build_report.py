"""Build the single consolidated Lab 5 PDF from the recorded evidence."""

from html import escape
from pathlib import Path
import re
import subprocess
import textwrap

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image, PageBreak, Paragraph, Preformatted,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/Lab5_PES1UG24CS406_Static_Code_Analysis.pdf"
INK = colors.black
WIDTH = A4[0] - 88
styles = getSampleStyleSheet()
styles.add(ParagraphStyle("TitleLab", fontName="Helvetica-Bold", fontSize=20,
                          leading=25, textColor=INK, spaceAfter=10))
styles.add(ParagraphStyle("Kicker", fontName="Helvetica-Bold", fontSize=10,
                          leading=14, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle("H1Lab", fontName="Helvetica-Bold", fontSize=14,
                          leading=18, textColor=INK, spaceAfter=10))
styles.add(ParagraphStyle("H2Lab", fontName="Helvetica-Bold", fontSize=11,
                          leading=15, textColor=INK, spaceBefore=10,
                          spaceAfter=6))
styles.add(ParagraphStyle("BodyLab", fontName="Helvetica", fontSize=10,
                          leading=14.2, textColor=INK, spaceAfter=9))
styles.add(ParagraphStyle("SmallLab", parent=styles["BodyLab"], fontSize=8.5,
                          leading=11.5, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle("CellLab", parent=styles["BodyLab"], fontSize=7.9,
                          leading=10.4, spaceAfter=0))
styles.add(ParagraphStyle("CellHeadLab", parent=styles["CellLab"],
                          fontName="Helvetica-Bold", textColor=INK))
styles.add(ParagraphStyle("CodeLab", fontName="Courier", fontSize=7.1,
                          leading=9.3, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle("CaptionLab", parent=styles["SmallLab"],
                          fontSize=8, leading=11, alignment=TA_CENTER))
story = []


def md_inline(text):
    """Convert only the simple inline Markdown used in local source notes."""
    text = escape(text)
    return re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)


def p(text, style="BodyLab"):
    return Paragraph(md_inline(text), styles[style])


def heading(text):
    story.append(p(text, "H1Lab"))


def table(headers, rows, widths):
    cells = [[p(text, "CellHeadLab") for text in headers]]
    cells += [[p(text, "CellLab") for text in row] for row in rows]
    result = Table(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
    result.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return result


def screenshot(name, max_height):
    filename = ROOT / "evidence" / name
    with PILImage.open(filename) as image:
        width, height = image.size
    ratio = min(WIDTH / width, max_height / height)
    story.append(Image(str(filename), width=width * ratio, height=height * ratio))
    story.append(Spacer(1, 8))


def raw_report(stage, tool):
    relative = f"reports/{stage}/{tool}_report.txt"
    story.append(p(f"{tool.upper()} - {stage.upper()}", "H2Lab"))
    story.append(p(relative, "SmallLab"))
    content = (ROOT / relative).read_text(encoding="utf-8")
    if not content:
        story.append(p("This report is empty (0 bytes). Flake8 exited with code "
                       "0 and produced no findings. No report text has been added."))
        return
    wrapped = []
    for line in content.expandtabs(4).splitlines():
        wrapped.extend(textwrap.wrap(line, width=116, replace_whitespace=False,
                                     drop_whitespace=False,
                                     break_on_hyphens=False) or [""])
    story.append(Preformatted("\n".join(wrapped), styles["CodeLab"]))


def page():
    story.append(PageBreak())


def footer(canvas, document):
    canvas.saveState()
    if document.page > 1:
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(INK)
        canvas.drawString(44, A4[1] - 23,
                          "Lab 5 - Static Code Analysis")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(INK)
    canvas.drawString(44, 27, "PES1UG24CS406  |  Software Engineering  |  Lab 5")
    canvas.drawRightString(A4[0] - 44, 27, str(document.page))
    canvas.restoreState()


story.append(p("SOFTWARE ENGINEERING / LAB 5", "Kicker"))
story.append(p("Static Code Analysis", "TitleLab"))
story.append(p("Student Grade System", "H1Lab"))
story.append(p("Samarth Kotian  |  PES1UG24CS406"))
story.append(p("30 October 2026", "SmallLab"))
story.append(Spacer(1, 14))
heading("1. Introduction and results")
story.append(p("Static code analysis examines source code without executing it "
               "to identify likely bugs, unsafe patterns, maintainability issues, "
               "and style violations. This lab applies three complementary tools "
               "to the assigned student grade and transcript manager."))
story.append(table(["Tool", "Purpose", "Before", "After"], [
    ["Pylint 4.1.3", "Code quality, likely errors, naming and maintainability",
     "5.51/10; 22 messages", "10.00/10; no messages"],
    ["Bandit 1.9.4", "Python security patterns and vulnerable API usage",
     "6 findings: 2 High, 1 Medium, 3 Low", "0 findings"],
    ["Flake8 7.5.0", "PEP 8 style, unused names and syntax checks",
     "8 findings", "0 findings; silent success"],
], [73, 188, 134, WIDTH - 395]))
story.append(Spacer(1, 12))
story.append(p("Verification: Python 3.12.14; all final analyzer exit codes "
               "are 0; all 10 regression tests pass. The sample GPA is still "
               "4.35 after recording S01's score of 95."))
story.append(p("Evidence included: a prioritized issue table, six before-and-after "
               "screenshots, complete contents of all six analyzer text reports, "
               "and four standard reflection answers."))
story.append(p("Assigned source: https://github.com/SETAPESU26/"
               "L5_42_student_grade_system", "SmallLab"))
story.append(p("Individual submission: https://github.com/samarthkotian/"
               "software_engineering_lab/tree/main/lab5", "SmallLab"))
story.append(p("Analysis uses default enabled checks. No warning suppressions, "
               "ignored rules, or `# nosec` comments were introduced.", "SmallLab"))

issues = []
for line in (ROOT / "issues.md").read_text(encoding="utf-8").splitlines():
    if line.startswith("| ") and not line.startswith("| Issue"):
        values = [value.strip() for value in line.strip("|").split("|")]
        if len(values) == 5:
            issues.append(values)
widths = [83, 66, 44, 136, WIDTH - 329]
page()
heading("2. Issue identification: security")
story.append(p("Original line numbers refer to the unchanged supplied source in "
               "`reports/before/student_grade_system.py`. High and Medium "
               "security findings appear first. Severity labels come from Bandit.",
               "SmallLab"))
story.append(table(["Issue", "Type", "Lines", "Description", "Fix approach"],
                   issues[:6], widths))
story.append(Spacer(1, 10))
story.append(p("All six Bandit findings were resolved. The shell call was removed "
               "entirely; GPA expressions were replaced by direct arithmetic. "
               "No unsafe call was retained behind a suppression."))

page()
heading("2. Issue identification: quality and style")
story.append(p("The following tool findings overlap in places. They are grouped "
               "by cause so the table describes the actual repair rather than "
               "counting each warning as an unrelated bug.", "SmallLab"))
story.append(table(["Issue", "Type", "Lines", "Description", "Fix approach"],
                   issues[6:], widths))
story.append(Spacer(1, 10))
story.append(p("Additional behavior checks", "H2Lab"))
story.append(p("Missing students and empty mark lists are handled deliberately. "
               "Scores and attendance updates have bounds. Invalid GPA scales "
               "raise clear errors. A main guard prevents output and grade-sheet "
               "creation during import. Equal weighting of marks is retained."))

page()
heading("3. Before screenshots: Pylint and Flake8")
story.append(p("Actual browser captures of the saved analyzer output. The "
               "surrounding report view labels the command and recorded exit "
               "status; the analyzer text is not rewritten.", "SmallLab"))
screenshot("pylint_before.png", 427)
story.append(p("Figure 1. Pylint before: 5.51/10 and 22 messages.", "CaptionLab"))
screenshot("flake8_before.png", 185)
story.append(p("Figure 2. Flake8 before: all eight findings.", "CaptionLab"))

page()
heading("3. Before screenshot: Bandit")
story.append(p("This screenshot shows the High and Medium findings. The complete "
               "Bandit output, including all three Low findings and metrics, "
               "appears in the report appendix.", "SmallLab"))
screenshot("bandit_before.png", 500)
story.append(p("Figure 3. Unsafe eval, weak MD5 and shell execution.", "CaptionLab"))
story.append(table(["Severity", "High", "Medium", "Low", "Total"],
                   [["Original findings", "2", "1", "3", "6"]],
                   [WIDTH - 280, 70, 70, 70, 70]))

page()
heading("4. After screenshots: Pylint and Flake8")
story.append(p("All checks were rerun on the final corrected file.", "SmallLab"))
screenshot("pylint_after.png", 245)
story.append(p("Figure 4. Pylint after: 10.00/10; exit code 0.", "CaptionLab"))
screenshot("flake8_after.png", 220)
story.append(p("Figure 5. Flake8 after: no output; exit code 0. The status "
               "message belongs to the report view; the raw file is empty.", "CaptionLab"))
story.append(p("Flake8 success is silent. The PDF explicitly represents the "
               "zero-byte after report without inventing analyzer output."))

page()
heading("4. After screenshot: Bandit and verification")
screenshot("bandit_after.png", 390)
story.append(p("Figure 6. Bandit after: no issues at any severity; exit code 0.",
               "CaptionLab"))
story.append(p("Functional verification", "H2Lab"))
story.append(p("Ten regression tests pass. They cover score validation and audit "
               "logs; attendance bounds; passing boundaries and missing marks; "
               "numeric GPA scaling; rejection of code strings and invalid "
               "scales; SHA-256; cryptographic PIN bounds; literal shell "
               "characters in export filenames; token redaction; and safe import."))
story.append(p("Final sample output", "H2Lab"))
program = (ROOT / "reports/after/program_output.txt").read_text(encoding="utf-8")
story.append(Preformatted(program.rstrip(), styles["CodeLab"]))
story.append(p("The PIN varies per run. The token status is False when no "
               "environment token is configured. The digest is an identifier "
               "hash, not encryption or a password-storage scheme.", "SmallLab"))

page()
heading("5. Reflection")
story.append(p("The supplied handout omits the reflection question text. The "
               "following four standard questions address its stated learning "
               "outcomes, as requested.", "SmallLab"))
reflection = (ROOT / "reflection.md").read_text(encoding="utf-8")
for section in reflection.split("\n## ")[1:]:
    question, answer = section.split("\n", 1)
    story.append(p(question, "H2Lab"))
    story.append(p(" ".join(answer.split()), "BodyLab"))

page()
heading("6. Commit record and reproducibility")
commits = subprocess.check_output(
    ["git", "log", "--reverse", "--format=%h|%s", "--",
     "student_grade_system.py"], cwd=ROOT, text=True
).strip().splitlines()
rows = [line.split("|", 1) for line in commits]
story.append(table(["Commit", "Purpose"], rows, [70, WIDTH - 70]))
story.append(Spacer(1, 12))
story.append(p("The baseline commit preserves the original source and initial "
               "reports. The next three separate commits contain Pylint, "
               "Bandit, and Flake8 fixes. Supporting documentation and the PDF "
               "are packaged separately after these fixes."))
story.append(p("Reproduce the analysis", "H2Lab"))
story.append(Preformatted(
    "python -m venv .venv\n"
    ".venv\\Scripts\\python.exe -m pip install -r requirements.txt\n"
    ".venv\\Scripts\\python.exe -m pylint --persistent=n student_grade_system.py\n"
    ".venv\\Scripts\\python.exe -m bandit -r student_grade_system.py\n"
    ".venv\\Scripts\\python.exe -m flake8 student_grade_system.py\n"
    ".venv\\Scripts\\python.exe -m unittest -v", styles["CodeLab"]))
story.append(p("Original sample output", "H2Lab"))
original_output = (ROOT / "reports/before/program_output.txt").read_text(
    encoding="utf-8")
story.append(Preformatted(original_output.rstrip(), styles["CodeLab"]))
story.append(p("The original export message appeared first because the shell "
               "and Python output streams were buffered differently. The final "
               "program prints directly without creating a shell.", "SmallLab"))
story.append(p("Capture method", "H2Lab"))
story.append(p("Each analyzer was run as a subprocess against the same target "
               "filename. The raw reports contain stdout followed by stderr; "
               "neither stream was filtered. Recorded exit codes are included "
               "in the repository. Bandit timestamps are UTC. Screenshots are "
               "browser views of the saved reports, rather than terminal captures. "
               "The appendix reproduces all six report contents."))

page()
heading("7. Complete report contents")
story.append(p("All six requested .txt reports are reproduced below. Long lines "
               "are wrapped for page width; no finding or report text is omitted. "
               "Raw originals remain in the Git repository.", "SmallLab"))
raw_report("before", "pylint")
page()
heading("7. Complete report contents / continued")
raw_report("before", "bandit")
page()
heading("7. Complete report contents / continued")
raw_report("before", "flake8")
raw_report("after", "pylint")
raw_report("after", "bandit")
raw_report("after", "flake8")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
document = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4, rightMargin=44, leftMargin=44,
    topMargin=42, bottomMargin=56,
    title="Lab 5 - Static Code Analysis - PES1UG24CS406",
    author="Samarth Kotian", subject="Pylint, Bandit and Flake8 lab submission",
)
document.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
