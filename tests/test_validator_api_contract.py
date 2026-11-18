"""API-level contract regression tests using temporary, synthetic data."""

import csv
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "validate_submission.py"
SPEC = importlib.util.spec_from_file_location("validator_api_contract", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class ApiContractTests(unittest.TestCase):
    def test_uppercase_expected_digest_is_accepted(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "submission.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["protein_id", "label_0"])
                writer.writerow(["P001", "1"])
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            report = VALIDATOR.validate_submission(
                path, expected_rows=1, labels=1, expected_sha256=digest.upper()
            )
            self.assertTrue(report["valid"])
            self.assertEqual(report["expected_sha256"], digest)

    def test_boolean_dimensions_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "submission.csv"
            path.write_text("protein_id,label_0\nP001,1\n", encoding="utf-8")
            for option in ({"expected_rows": True}, {"labels": True}):
                with self.subTest(option=option):
                    with self.assertRaisesRegex(ValueError, "positive integer"):
                        VALIDATOR.validate_submission(path, **option)

    def test_invalid_digest_format_is_rejected_before_reading(self):
        with tempfile.TemporaryDirectory() as directory:
            missing_path = Path(directory) / "missing.csv"
            with self.assertRaisesRegex(ValueError, "64 hexadecimal"):
                VALIDATOR.validate_submission(missing_path, expected_sha256="not-a-digest")


if __name__ == "__main__":
    unittest.main()
