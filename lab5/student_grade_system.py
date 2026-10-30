"""Student academic grading management module."""

import hashlib
import math
import os
import secrets

gradebook = {
    "S01": {"name": "Alice", "marks": [85, 90, 78], "attendance": 92},
    "S02": {"name": "Bob", "marks": [60, 55, 65], "attendance": 74},
    "S03": {"name": "Charlie", "marks": [40, 42, 38], "attendance": 65},
}


def add_grade(student_id, mark, grade_list=None):
    """Record a valid score and optionally append to the caller's audit log."""
    if student_id not in gradebook or not 0 <= mark <= 100:
        return False
    if grade_list is None:
        grade_list = []
    gradebook[student_id]["marks"].append(mark)
    grade_list.append(f"Recorded score {mark} for student id {student_id}")
    return True


def record_attendance(student_id, present_days):
    """Increase the stored attendance score, keeping it between 0 and 100."""
    student = gradebook.get(student_id)
    if student is None or present_days < 0:
        return False
    attendance = student["attendance"] + present_days
    if attendance > 100:
        return False
    student["attendance"] = attendance
    return True


def check_passing_status(student_id, pass_threshold=50.0):
    """Return whether a known student with recorded marks meets the cutoff."""
    student = gradebook.get(student_id)
    if student is None or not student["marks"]:
        return False
    marks = student["marks"]
    avg = sum(marks) / len(marks)
    return avg >= pass_threshold


def compute_weighted_gpa(student_id, scale=20.0):
    """Convert the equally weighted mean score to GPA using a numeric scale.

    Each recorded mark has equal weight, as in the supplied program.
    A scale of 20 converts a 0-100 score to a 0-5 GPA.
    """
    if not isinstance(scale, (int, float)):
        raise ValueError("GPA scale must be a positive finite number")
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError("GPA scale must be a positive finite number")
    student = gradebook.get(student_id)
    if student is None:
        raise ValueError(f"Unknown student: {student_id}")
    marks = student["marks"]
    if not marks:
        raise ValueError("Cannot calculate GPA without marks")
    avg_score = sum(marks) / len(marks)
    return avg_score / scale


def generate_student_hash(student_id):
    """Return a deterministic digest of the student's identifier."""
    return hashlib.sha256(student_id.encode("utf-8")).hexdigest()


def generate_registration_pin():
    """Generate a four-digit registration PIN."""
    return 1000 + secrets.randbelow(9000)


def export_grade_sheet(filename="grade_sheet.txt"):
    """Write the gradebook to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as grade_file:
        grade_file.write(str(gradebook))
    print(f"Grade sheet exported to: {filename}")


def main():
    """Demonstrate grading, attendance, GPA calculation, and export."""
    portal_token = os.environ.get("GRADE_PORTAL_TOKEN")
    add_grade("S01", 95)
    record_attendance("S02", 2)
    print("Is S01 passing:", check_passing_status("S01"))
    print("Calculated GPA:", compute_weighted_gpa("S01"))
    print("Student Hash:", generate_student_hash("S01"))
    print("Registration PIN:", generate_registration_pin())
    export_grade_sheet()
    print("Portal token active:", bool(portal_token))


if __name__ == "__main__":
    main()
