# Protein Function Prediction

An experimental project for multilabel protein-function annotation. The workflow combines sequence-based predictions with Gene Ontology (GO) mapping and compares model versions using Macro F1 across 500 labels.

The repository preserves a downloadable V25 + GO test-prediction file and versioned evaluation records. Release notes distinguish prediction artifacts from local validation results so a model score is not mistaken for a competition score.

## Releases

| Version | Release | Contents | Local selection Macro F1 |
|---|---|---|---:|
| `v25-go-v1.0.0` | [V25 + GO test CSV](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v25-go-v1.0.0) | Full test predictions: 28,450 proteins × 500 binary labels, plus a checksum and validation manifest | 0.481454 |
| `v31.0.0` | [V31 fusion evaluation](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v31.0.0) | V25 + expanded GO + V30 Pro comparison, development history, full validation JSON, and per-label metrics; no V31 test CSV | 0.486082 |

## Development history

1. **V25 baseline:** the locked candidate reached 0.434802 in local development evaluation. A separate 35M fusion candidate reached 0.435132 on the same historical selection set but did not pass the promotion gate.
2. **V25 + expanded GO:** expanded GO direct mapping was evaluated alongside V25. A calibration-selected 50/50 fusion reached 0.481454 on the historical selection set. Its full test prediction CSV is the artifact in the V25 + GO release.
3. **V31 three-source fusion:** the V25 + GO result was used as the base and the upgraded V30 Pro predictions were added with a calibrated 0.10 fusion weight. The all-label result reached 0.486082; the original V30 model was not used. The V31 release contains evaluation artifacts only because V31 test predictions were not generated.

## Data format

The V25 + GO CSV contains a header of `protein_id` followed by `label_0` through `label_499`. It has 28,450 protein rows and binary `0`/`1` predictions. The release manifest records the SHA-256 checksum and format-validation status.

## Evaluation and limitations

- The V25 + GO and V31 fusion scores are local Macro F1 measurements on a 5,542-row historical selection set. That set was reused during development, so these comparisons are exploratory and are not independent blind validation.
- Calibration used 1,683 rows. The recorded fusion cross-fit score is not end-to-end out-of-fold validation.
- No audit labels were read. The V25 + GO CSV was generated but was not uploaded to the competition platform; no platform score is available.
- The GO predictor was trained using external GO annotations. Whether that use is allowed by the competition rules has not been confirmed. Check with the organizers before submitting a GO-based model.
- The V31 score is an evaluation result, not the score of the downloadable V25 + GO CSV. The V31 release contains reports and metrics, not model checkpoints; no model checkpoints are published in this repository.

## Repository contents

- `submission_GO_V25_fusion_048145.csv` — the V25 + expanded GO test-prediction artifact; this is the same file attached to the V25 + GO release.
- `README.md` — project overview, version history, artifact map, and evaluation limits.
- GitHub Releases — version-specific CSV, manifest, validation, and per-label results.
