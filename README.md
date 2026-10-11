# Protein Function Prediction Submission

This repository stores a protein function prediction CSV and versioned evaluation records.

## Current CSV

- `submission_GO_V25_fusion_048145.csv` — a 28,450-protein, 500-label test prediction file from the earlier V25 + expanded GO direct-mapping fusion. Its historical local selection Macro F1 was 0.481454. The file was generated locally and was not uploaded to the competition platform.

## Evaluation release

- [V31.0.0 — V25 + GO + V30 Pro fusion results](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v31.0.0) — local historical-selection Macro F1 0.486082, with the development history, validation JSON, and per-label results. This is not a platform score or an independent blind evaluation. V31 test predictions were not generated, so the repository CSV above is not a V31 submission.

## Format

The CSV header is `protein_id` followed by `label_0` through `label_499`. Rows contain protein IDs and binary label values.
