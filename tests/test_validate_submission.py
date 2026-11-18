"""Behavioral checks for submission format validation, using synthetic CSVs."""

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "validate_submission.py"
SPEC = importlib.util.spec_from_file_location("submission_validator", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class SubmissionValidationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def write_csv(self, name="submission.csv", rows=None, *, labels=2, header=None, bom=False):
        path = self.root / name
        if rows is None:
            rows = [["P001", "0", "1"], ["P002", "1", "0"]]
        if header is None:
            header = ["protein_id"] + [f"label_{index}" for index in range(labels)]
        with path.open("w", encoding="utf-8-sig" if bom else "utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
            writer.writerows(rows)
        return path

    def validate(self, path, **options):
        arguments = {"expected_rows": 2, "labels": 2}
        arguments.update(options)
        return VALIDATOR.validate_submission(path, **arguments)

    def assert_invalid(self, result):
        self.assertFalse(result["valid"])
        self.assertGreater(result["error_count"], 0)
        self.assertTrue(result["errors"])

    def run_cli(self, path, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(path), "--expected-rows", "2", "--labels", "2", *arguments],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )

    def test_default_schema_has_500_labels(self):
        path = self.write_csv(rows=[["P001"] + ["0"] * 500, ["P002"] + ["1"] * 500], labels=500)
        result = VALIDATOR.validate_submission(path, expected_rows=2)
        self.assertTrue(result["valid"])
        self.assertEqual(result["rows"], 2)
        self.assertEqual(result["labels"], 500)
        self.assertEqual(result["error_count"], 0)

    def test_configurable_small_schema(self):
        path = self.write_csv(rows=[["P001", "0", "1", "0"], ["P002", "1", "1", "1"]], labels=3)
        result = self.validate(path, labels=3)
        self.assertTrue(result["valid"])
        self.assertEqual(result["labels"], 3)

    def test_utf8_bom_is_accepted_and_included_in_hash(self):
        path = self.write_csv(bom=True)
        result = self.validate(path)
        self.assertTrue(result["valid"])
        self.assertEqual(result["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())

    def test_header_names_and_label_order_are_strict(self):
        headers = [
            ["id", "label_0", "label_1"],
            ["protein_id", "label_1", "label_0"],
            ["protein_id", "label_0", "label_0"],
            ["protein_id", "label_0"],
        ]
        for header in headers:
            with self.subTest(header=header):
                self.assert_invalid(self.validate(self.write_csv(header=header)))

    def test_exact_row_count_is_required(self):
        path = self.write_csv()
        for expected in [1, 3]:
            with self.subTest(expected=expected):
                self.assert_invalid(self.validate(path, expected_rows=expected))

    def test_short_long_and_blank_rows_are_rejected(self):
        for row in [["P002", "1"], ["P002", "1", "0", "1"], []]:
            with self.subTest(row=row):
                path = self.write_csv(rows=[["P001", "0", "1"], row])
                self.assert_invalid(self.validate(path))

    def test_empty_and_whitespace_ids_are_rejected(self):
        for identifier in ["", "   "]:
            with self.subTest(identifier=identifier):
                path = self.write_csv(rows=[["P001", "0", "1"], [identifier, "1", "0"]])
                self.assert_invalid(self.validate(path))

    def test_duplicate_ids_are_rejected(self):
        path = self.write_csv(rows=[["P001", "0", "1"], ["P001", "1", "0"]])
        self.assert_invalid(self.validate(path))

    def test_labels_require_literal_zero_or_one(self):
        for value in ["0.5", "", "1 ", "True", "2", "NaN"]:
            with self.subTest(value=value):
                path = self.write_csv(rows=[["P001", "0", "1"], ["P002", value, "0"]])
                self.assert_invalid(self.validate(path))

    def test_template_allows_blank_prediction_values(self):
        path = self.write_csv()
        template = self.write_csv("template.csv", rows=[["P001", "", ""], ["P002", "", ""]])
        self.assertTrue(self.validate(path, template=template)["valid"])

    def test_template_requires_exact_id_order(self):
        path = self.write_csv()
        template = self.write_csv("template.csv", rows=[["P002", "", ""], ["P001", "", ""]])
        self.assert_invalid(self.validate(path, template=template))

    def test_template_with_missing_row_is_rejected(self):
        path = self.write_csv()
        template = self.write_csv("template.csv", rows=[["P001", "", ""]])
        self.assert_invalid(self.validate(path, template=template))

    def test_template_with_duplicate_ids_is_rejected(self):
        path = self.write_csv()
        template = self.write_csv("template.csv", rows=[["P001", "", ""], ["P001", "", ""]])
        self.assert_invalid(self.validate(path, template=template))

    def test_template_header_is_validated(self):
        path = self.write_csv()
        template = self.write_csv("template.csv", header=["id", "label_0", "label_1"])
        self.assert_invalid(self.validate(path, template=template))

    def test_template_shape_and_nonempty_ids_are_validated(self):
        path = self.write_csv()
        for row in [["P002", ""], ["", "", ""]]:
            with self.subTest(row=row):
                template = self.write_csv("template.csv", rows=[["P001", "", ""], row])
                self.assert_invalid(self.validate(path, template=template))

    def test_matching_sha256_is_accepted(self):
        path = self.write_csv()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertTrue(self.validate(path, expected_sha256=digest)["valid"])

    def test_wrong_sha256_is_rejected(self):
        self.assert_invalid(self.validate(self.write_csv(), expected_sha256="0" * 64))

    def test_malformed_quoted_csv_is_rejected(self):
        path = self.root / "broken.csv"
        path.write_text('protein_id,label_0,label_1\nP001,0,1\nP002,"1,0\n', encoding="utf-8")
        self.assert_invalid(self.validate(path))

    def test_error_details_are_bounded_but_total_is_retained(self):
        path = self.write_csv(rows=[[f"P{index:03}", "0.5", "0"] for index in range(30)])
        result = self.validate(path, expected_rows=30)
        self.assert_invalid(result)
        self.assertLessEqual(len(result["errors"]), 20)
        self.assertGreaterEqual(result["error_count"], 30)

    def test_validation_does_not_modify_inputs_or_create_files(self):
        path = self.write_csv()
        before = path.read_bytes()
        names = set(self.root.iterdir())
        self.assertTrue(self.validate(path)["valid"])
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(set(self.root.iterdir()), names)

    def test_cli_json_success(self):
        result = self.run_cli(self.write_csv(), "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["valid"])
        self.assertEqual(report["rows"], 2)

    def test_cli_text_success(self):
        result = self.run_cli(self.write_csv())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.strip())

    def test_cli_validation_failure_still_outputs_json(self):
        path = self.write_csv(rows=[["P001", "0", "1"], ["P001", "1", "0"]])
        result = self.run_cli(path, "--json")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assert_invalid(json.loads(result.stdout))

    def test_cli_missing_input_has_io_error_exit_code(self):
        result = self.run_cli(self.root / "absent.csv", "--json")
        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stderr.strip())

    def test_cli_missing_template_has_io_error_exit_code(self):
        result = self.run_cli(self.write_csv(), "--template", str(self.root / "absent-template.csv"))
        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stderr.strip())

    def test_cli_rejects_invalid_arguments(self):
        path = self.write_csv()
        for arguments in [("--labels", "0"), ("--expected-rows", "-1"), ("--expected-sha256", "not-a-hash")]:
            with self.subTest(arguments=arguments):
                result = self.run_cli(path, *arguments)
                self.assertEqual(result.returncode, 2)
                self.assertTrue(result.stderr.strip())


if __name__ == "__main__":
    unittest.main()
