"""Additional CLI regression tests for the public CSV validation interface."""

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "validate_submission.py"


class CliContractTests(unittest.TestCase):
    def test_utf8_bom_json_report_and_expected_digest(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "bom.csv"
            with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["protein_id", "label_0"])
                writer.writerow(["P001", "1"])
            expected = hashlib.sha256(csv_path.read_bytes()).hexdigest()
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(csv_path),
                 "--expected-rows", "1", "--labels", "1",
                 "--expected-sha256", expected.upper(), "--json"],
                capture_output=True, text=True, check=False, timeout=15,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = json.loads(completed.stdout)
            self.assertTrue(report["valid"])
            self.assertEqual(report["sha256"], expected)
            self.assertEqual(report["expected_sha256"], expected)
            self.assertEqual(report["rows"], 1)
            self.assertEqual(report["labels"], 1)
            self.assertEqual(report["schema_version"], 1)

    def test_cli_rejects_zero_labels_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "input.csv"
            csv_path.write_text("protein_id,label_0\nP001,1\n", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(csv_path), "--labels", "0"],
                capture_output=True, text=True, check=False, timeout=15,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("positive integer", completed.stderr)
            self.assertNotIn("Traceback", completed.stderr)


if __name__ == "__main__":
    unittest.main()
