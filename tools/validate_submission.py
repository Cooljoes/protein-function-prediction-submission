#!/usr/bin/env python3
"""Validate a protein-label submission CSV without loading models or changing files.

The checks establish file integrity and the submission contract, not prediction
accuracy. Requires Python 3.11+ and only the standard library.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from itertools import zip_longest
from pathlib import Path
import re
import sys


DEFAULT_ROWS = 28_450
DEFAULT_LABELS = 500
MAX_ERRORS = 20


class _Errors:
    def __init__(self) -> None:
        self.count = 0
        self.messages: list[str] = []

    def add(self, message: str) -> None:
        self.count += 1
        if len(self.messages) < MAX_ERRORS:
            self.messages.append(message)


def _scan_csv(
    path: Path, *, labels: int, expected_rows: int, errors: _Errors, is_template: bool = False
) -> tuple[int, list[str]]:
    kind = "template" if is_template else "submission"
    expected_header = ["protein_id"] + [f"label_{number}" for number in range(labels)]
    seen: set[str] = set()
    ids: list[str] = []
    rows = 0
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            header = next(reader, None)
            if header != expected_header:
                errors.add(
                    f"{kind} header must be protein_id followed by label_0 through label_{labels - 1} "
                    f"in order ({labels + 1} columns)"
                )
            for row in reader:
                rows += 1
                protein_id = row[0] if row else ""
                ids.append(protein_id)
                if not protein_id.strip():
                    errors.add(f"{kind} record {rows} has an empty protein_id")
                elif protein_id in seen:
                    errors.add(f"{kind} record {rows} repeats protein_id {protein_id[:80]!r}")
                else:
                    seen.add(protein_id)
                if len(row) != labels + 1:
                    errors.add(f"{kind} record {rows} has {len(row)} columns; expected {labels + 1}")
                    continue
                if not is_template:
                    for number, value in enumerate(row[1:]):
                        if value not in ("0", "1"):
                            errors.add(
                                f"submission record {rows}, label_{number} must be exactly 0 or 1; "
                                f"found {value[:80]!r}"
                            )
                            # One binary-value violation per record keeps diagnostics concise.
                            break
    except (csv.Error, UnicodeError) as error:
        errors.add(f"{kind} is not a complete UTF-8 CSV: {error}")
    if rows != expected_rows:
        errors.add(f"{kind} has {rows} readable data records; expected {expected_rows}")
    return rows, ids


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_submission(
    path: str | Path,
    *,
    expected_rows: int = DEFAULT_ROWS,
    labels: int = DEFAULT_LABELS,
    template: str | Path | None = None,
    expected_sha256: str | None = None,
) -> dict[str, object]:
    """Return a validation report; raise OSError for I/O and ValueError for arguments.

    CSV content is processed a record at a time. Only protein IDs are retained
    for duplicate and optional template-order checks, never the prediction matrix.
    SHA-256 covers the original bytes, including a BOM or line-ending differences.
    Error counts include every detected violation, with one non-binary diagnostic
    per affected record and at most MAX_ERRORS messages retained.
    """
    for name, value in (("expected_rows", expected_rows), ("labels", labels)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if expected_sha256 is not None:
        if not isinstance(expected_sha256, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256):
            raise ValueError("expected_sha256 must contain exactly 64 hexadecimal characters")
        expected_sha256 = expected_sha256.lower()

    path = Path(path)
    errors = _Errors()
    checksum = _digest(path)
    if expected_sha256 is not None and checksum != expected_sha256:
        errors.add(f"SHA-256 mismatch: expected {expected_sha256}, got {checksum}")
    rows, ids = _scan_csv(path, labels=labels, expected_rows=expected_rows, errors=errors)

    template_rows = None
    if template is not None:
        template = Path(template)
        template_rows, template_ids = _scan_csv(
            template, labels=labels, expected_rows=expected_rows, errors=errors, is_template=True
        )
        missing = object()
        for number, (actual, required) in enumerate(zip_longest(ids, template_ids, fillvalue=missing), start=1):
            if actual is missing or required is missing:
                errors.add("submission and template contain different numbers of protein IDs")
                break
            if actual != required:
                errors.add(f"protein_id order differs from template at record {number}")

    return {
        "schema_version": 1,
        "valid": errors.count == 0,
        "path": str(path),
        "rows": rows,
        "expected_rows": expected_rows,
        "labels": labels,
        "sha256": checksum,
        "expected_sha256": expected_sha256,
        "template": str(template) if template is not None else None,
        "template_rows": template_rows,
        "id_order_checked": template is not None,
        "error_count": errors.count,
        "errors": errors.messages,
        "scope": "CSV structure and optional byte integrity / ID order only; prediction accuracy is not evaluated.",
    }


def _positive_integer(value: str) -> int:
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a positive integer") from error
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def _sha256_argument(value: str) -> str:
    if not re.fullmatch(r"[0-9a-fA-F]{64}", value):
        raise argparse.ArgumentTypeError("must contain exactly 64 hexadecimal characters")
    return value.lower()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path, help="submission CSV to inspect")
    parser.add_argument("--expected-rows", type=_positive_integer, default=DEFAULT_ROWS,
                        help=f"required number of data records (default: {DEFAULT_ROWS})")
    parser.add_argument("--labels", type=_positive_integer, default=DEFAULT_LABELS,
                        help=f"required number of label columns (default: {DEFAULT_LABELS})")
    parser.add_argument("--template", type=Path,
                        help="optional template with the same header and required protein-ID order; label values are ignored")
    parser.add_argument("--expected-sha256", type=_sha256_argument,
                        help="optional expected SHA-256 of the CSV's original bytes")
    parser.add_argument("--json", action="store_true", help="print the validation result as JSON")
    args = parser.parse_args(argv)
    try:
        report = validate_submission(
            args.csv_path, expected_rows=args.expected_rows, labels=args.labels,
            template=args.template, expected_sha256=args.expected_sha256,
        )
    except (OSError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("VALID" if report["valid"] else "INVALID")
        print(f"File: {report['path']}")
        print(f"Data records: {report['rows']} (expected {report['expected_rows']}); labels: {report['labels']}")
        print(f"SHA-256: {report['sha256']}")
        if report["id_order_checked"]:
            print(f"Template checked: {report['template']}")
        for message in report["errors"]:
            print("- " + message)
        if report["error_count"] > len(report["errors"]):
            print(f"Showing {len(report['errors'])} of {report['error_count']} detected violations.")
        print(report["scope"])
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
