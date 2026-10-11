# Protein Function Prediction

An experimental project for multilabel protein-function annotation. The workflow combines sequence-based predictions with Gene Ontology (GO) mapping and compares candidate versions using Macro F1 across 500 labels.

This repository documents two milestones in the project. Release versions use a simple, chronological sequence: **V1.0.0** is the V25 + GO test-prediction artifact, and **V2.0.0** records the later V25 + GO + V30 Pro fusion evaluation. The model-family names (V25, V30 Pro, and V31) describe the research lineage; they are distinct from the repository's release numbers.

## Releases

| Release | Contents | Local selection Macro F1 |
|---|---|---:|
| [V1.0.0 — V25 + GO test predictions](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v1.0.0) | Test CSV for 28,450 proteins × 500 binary labels, checksum, and validation manifest | 0.481454 |
| [V2.0.0 — V25 + GO + V30 Pro fusion evaluation](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v2.0.0) | Development report, validation JSON, and per-label metrics; no V2 test CSV | 0.486082 |

## Development history

1. **V25 baseline:** the locked candidate reached 0.434802 in local development evaluation. A separate 35M fusion candidate reached 0.435132 on the same historical selection set but did not pass the promotion gate.
2. **V25 + expanded GO:** expanded GO direct mapping was evaluated alongside V25. A calibration-selected 50/50 fusion reached 0.481454 on the historical selection set. Its full test-prediction CSV is the artifact in [V1.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v1.0.0).
3. **V25 + GO + V30 Pro:** the V25 + GO result was used as the base and upgraded V30 Pro predictions were added with a calibrated 0.10 fusion weight. The all-label result reached 0.486082; the original V30 model was not used. This milestone is documented in [V2.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v2.0.0). V2 test predictions were not generated, so this release contains evaluation artifacts only.

## Data format

The CSV attached to V1.0.0 has a header of `protein_id` followed by `label_0` through `label_499`. It has 28,450 protein rows and binary `0`/`1` predictions. The release manifest records the SHA-256 checksum and format-validation status.

## Evaluation and limitations

- The V1 and V2 scores are local Macro F1 measurements on a 5,542-row historical selection set. That set was reused during development, so these comparisons are exploratory and are not independent blind validation.
- Calibration used 1,683 rows. The recorded fusion cross-fit score is not end-to-end out-of-fold validation.
- No audit labels were read. The V1 CSV was generated but was not uploaded to the competition platform; no platform score is available.
- The GO predictor was trained using external GO annotations. Whether that use is allowed by the competition rules has not been confirmed. Check with the organizers before submitting a GO-based model.
- The V2 score is an evaluation result, not the score of the downloadable V1 CSV. The V2 release contains reports and metrics, not model checkpoints; no model checkpoints are published in this repository.

## Repository contents

- V1.0.0 test-prediction CSV, distributed as a Release asset and not committed to the `main` branch.
- `README.md` — project overview, release history, artifact map, and evaluation limits.
- GitHub Releases — version-specific CSV, manifest, validation, and per-label results.
