# 蛋白质功能预测 | Protein Function Prediction

## 中文介绍

这是一个多标签蛋白质功能注释实验项目，结合蛋白质序列模型与基因本体（Gene Ontology，GO）映射，为蛋白质预测 500 个功能标签。仓库用版本化 GitHub Releases 保存预测文件与评估资料，并记录模型组合的开发历程和评估限制。

项目 Release 采用顺序版本号：**V1.0.0** 发布 V25 + GO 测试集预测 CSV；**V2.0.0** 记录后续 V25 + GO + V30 Pro 融合评估。V25、V30 Pro 和 V31 是研究过程中的模型/实验名称，与仓库 Release 版本号相互独立。

### 发布版本

| 版本 | 内容 | 本地选择集 Macro F1 |
|---|---|---:|
| [V1.0.0 — V25 + GO 测试集预测](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v1.0.0) | 28,450 条蛋白质 × 500 个二元标签的预测 CSV、校验清单和 SHA-256 校验值 | 0.481454 |
| [V2.0.0 — V25 + GO + V30 Pro 融合评估](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v2.0.0) | 开发报告、完整验证 JSON 和逐标签指标；没有 V2 测试集预测 CSV | 0.486082 |

### 创作与迭代历程

1. **V25 基线：**锁定候选模型在本地开发评估中得分为 0.434802。另一个 35M 融合候选得分为 0.435132，但未通过晋级门槛。
2. **V25 + 扩展 GO：**将扩展 GO 直接映射与 V25 组合，通过校准后采用 50/50 融合，在历史选择集上的 Macro F1 为 0.481454；测试集 CSV 发布在 [V1.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v1.0.0)。
3. **V25 + GO + V30 Pro：**在 V25 + GO 基础上加入升级后的 V30 Pro 预测，并采用经校准的 0.10 权重，所有标签的 Macro F1 达到 0.486082。原始 V30 模型没有参与该融合。此版本的测试集预测并未生成，[V2.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v2.0.0) 仅包含评估资料。

### 数据格式与评估说明

- V1 CSV 的列名为 `protein_id` 和 `label_0` 至 `label_499`，包含 28,450 行蛋白质记录及 500 个二元 `0`/`1` 预测。Release 中的 Manifest 记录 SHA-256 和格式校验信息。
- V1、V2 的 Macro F1 均为本地历史选择集结果（5,542 条记录）。该选择集在开发期间被重复使用，因此结果属于探索性比较，不是独立盲测。
- 校准使用了 1,683 条记录；记录的融合交叉拟合分数不等同于端到端的折外验证。
- 未读取审计标签。V1 CSV 尚未上传到比赛平台，因此没有平台得分。
- GO 预测器使用了外部 GO 注释，其是否符合比赛规则尚未确认。使用基于 GO 的模型前，请向赛事组织方核实。
- V2 分数对应融合评估，不是 V1 可下载 CSV 的比赛成绩。仓库不发布模型检查点。

## English

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
