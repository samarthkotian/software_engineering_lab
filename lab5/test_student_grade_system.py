"""Regression tests for grade management and the repaired security paths."""

import copy
import hashlib
import importlib
import io
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import student_grade_system as grades


class GradeSystemTests(unittest.TestCase):
    """Exercise meaningful behavior beyond the three static analyzers."""

    def setUp(self):
        self.original_gradebook = copy.deepcopy(grades.gradebook)

    def tearDown(self):
        grades.gradebook.clear()
        grades.gradebook.update(self.original_gradebook)

    def test_score_validation_and_independent_audit_logs(self):
        first_log, second_log = [], []
        self.assertTrue(grades.add_grade("S01", 95, first_log))
        self.assertTrue(grades.add_grade("S02", 70, second_log))
        self.assertEqual(len(first_log), 1)
        self.assertEqual(len(second_log), 1)
        self.assertIn("S01", first_log[0])
        self.assertIn("S02", second_log[0])
        self.assertEqual(grades.add_grade.__defaults__, (None,))
        before = copy.deepcopy(grades.gradebook)
        for student, mark in [("missing", 80), ("S01", -1), ("S01", 101)]:
            self.assertFalse(grades.add_grade(student, mark))
        self.assertEqual(grades.gradebook, before)

    def test_attendance_rejects_unknown_and_out_of_range_updates(self):
        self.assertTrue(grades.record_attendance("S02", 2))
        self.assertEqual(grades.gradebook["S02"]["attendance"], 76)
        for student, days in [("missing", 2), ("S02", -1), ("S02", 25)]:
            self.assertFalse(grades.record_attendance(student, days))
        self.assertEqual(grades.gradebook["S02"]["attendance"], 76)

    def test_passing_boundary_and_missing_marks(self):
        self.assertTrue(grades.check_passing_status("S01"))
        self.assertFalse(grades.check_passing_status("S03"))
        self.assertFalse(grades.check_passing_status("missing"))
        grades.gradebook["S03"]["marks"] = [50]
        self.assertTrue(grades.check_passing_status("S03"))
        grades.gradebook["S03"]["marks"] = []
        self.assertFalse(grades.check_passing_status("S03"))

    def test_gpa_preserves_the_demo_and_accepts_numeric_scaling(self):
        grades.add_grade("S01", 95)
        self.assertAlmostEqual(grades.compute_weighted_gpa("S01"), 4.35)
        self.assertAlmostEqual(grades.compute_weighted_gpa("S01", 25), 3.48)

    def test_gpa_rejects_code_strings_invalid_scales_and_missing_marks(self):
        for scale in ["avg_score / 20", "__import__('os')", 0, -1,
                      float("inf"), float("nan")]:
            with self.subTest(scale=scale), self.assertRaises(ValueError):
                grades.compute_weighted_gpa("S01", scale)
        with self.assertRaises(ValueError):
            grades.compute_weighted_gpa("missing")
        grades.gradebook["S01"]["marks"] = []
        with self.assertRaises(ValueError):
            grades.compute_weighted_gpa("S01")

    def test_hash_is_sha256(self):
        expected = hashlib.sha256(b"S01").hexdigest()
        self.assertEqual(grades.generate_student_hash("S01"), expected)
        self.assertNotEqual(expected, grades.generate_student_hash("S02"))

    def test_pin_uses_secrets_and_preserves_four_digit_bounds(self):
        for offset, expected in [(0, 1000), (8999, 9999)]:
            with patch.object(grades.secrets, "randbelow",
                              return_value=offset):
                self.assertEqual(grades.generate_registration_pin(), expected)

    def test_export_treats_shell_characters_as_filename_text(self):
        parent = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory(dir=parent) as directory:
            target = Path(directory) / "grades & echo.txt"
            with redirect_stdout(io.StringIO()):
                grades.export_grade_sheet(target)
            self.assertEqual(target.read_text(encoding="utf-8"),
                             str(grades.gradebook))
            self.assertEqual(list(Path(directory).iterdir()), [target])

    def test_main_never_prints_the_environment_token(self):
        output = io.StringIO()
        parent = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory(dir=parent) as directory:
            target = Path(directory) / "grades.txt"
            real_export = grades.export_grade_sheet
            with patch.dict(grades.os.environ, {"GRADE_PORTAL_TOKEN": "demo"}):
                with patch.object(grades, "export_grade_sheet",
                                  side_effect=lambda: real_export(target)):
                    with redirect_stdout(output):
                        grades.main()
        self.assertIn("Calculated GPA: 4.35", output.getvalue())
        self.assertIn("Portal token active: True", output.getvalue())
        self.assertNotIn("demo", output.getvalue())

    def test_import_has_no_output_or_export_side_effect(self):
        output = io.StringIO()
        with patch("builtins.open") as mock_open, redirect_stdout(output):
            importlib.reload(grades)
        mock_open.assert_not_called()
        self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
