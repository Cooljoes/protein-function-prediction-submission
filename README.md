# 蛋白质功能预测 | Protein Function Prediction

## 中文介绍

这是一个多标签蛋白质功能注释实验项目，结合蛋白质序列模型与基因本体（Gene Ontology，GO）映射，为蛋白质预测 500 个功能标签。仓库用版本化 GitHub Releases 保存预测文件与评估资料，并记录模型组合的开发历程和评估限制。

项目 Release 采用顺序版本号：**V1.0.0** 发布 V25 + GO 测试集预测 CSV；**V2.0.0** 记录 V25 + GO + V30 Pro 融合评估；**V3.0.0** 记录 V36 的受控 GO 特征试验；**V4.0.0** 发布 V41-PairGO GO 优化预测 CSV。V25、V30 Pro、V31 和 V36 是研究过程中的模型/实验名称，与仓库 Release 版本号相互独立。

### 发布版本

| 版本 | 内容 | 评估口径与 Macro F1 |
|---|---|---:|
| [V1.0.0 — V25 + GO 测试集预测](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v1.0.0) | 28,450 条蛋白质 × 500 个二元标签的预测 CSV、校验清单和 SHA-256 校验值 | 0.481454 |
| [V2.0.0 — V25 + GO + V30 Pro 融合评估](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v2.0.0) | 开发报告、完整验证 JSON 和逐标签指标；没有 V2 测试集预测 CSV | 0.486082 |
| [V3.0.0 — V36 受控 GO 特征试验](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v3.0.0) | 三折双种子 pilot 指标、预设 protocol 和验证报告；未通过晋级门槛，没有模型或测试集 CSV | 0.387896（pilot CV；不可与上方 selection 分数直接比较） |
| [V4.0.0 — V41-PairGO GO 优化预测](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v4.0.0) | 28,450 × 500 预测 CSV 和 SHA-256 格式清单 | 未报告独立评估分数 |

### 创作与迭代历程

1. <strong>V25 基线：</strong> 锁定候选模型在本地开发评估中得分为 0.434802。另一个 35M 融合候选得分为 0.435132，但未通过晋级门槛。
2. <strong>V25 + 扩展 GO：</strong> 将扩展 GO 直接映射与 V25 组合，通过校准后采用 50/50 融合，在历史选择集上的 Macro F1 为 0.481454；测试集 CSV 发布在 [V1.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v1.0.0)。
3. <strong>V25 + GO + V30 Pro：</strong> 在 V25 + GO 基础上加入升级后的 V30 Pro 预测，并采用经校准的 0.10 权重，所有标签的 Macro F1 达到 0.486082。原始 V30 模型没有参与该融合。此版本的测试集预测并未生成，[V2.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v2.0.0) 仅包含评估资料。
4. <strong>V36 受控特征试验：</strong> 比较方差筛选 GO、标签感知 GO、标签感知 GO 加序列编码三条路线。路线 B 得到最高 pilot CV Macro F1 0.387896，比同轮路线 A 高 0.003406，但未达到预设 +0.01 晋级门槛。该轮提前停止，没有做融合或 selection 评估；详见 [V3.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v3.0.0)。
5. <strong>V41-PairGO：</strong> 以 `pairgogpt_v2_pi.csv` 为主要预测结果，并对部分高置信度项目使用 GO、V30 Pro 和 V40 输出进行修正。V4.0.0 发布 CSV 和格式清单；目前未报告独立评估分数。

### 数据格式与评估说明

- V1 CSV 的列名为 `protein_id` 和 `label_0` 至 `label_499`，包含 28,450 行蛋白质记录及 500 个二元 `0`/`1` 预测。Release 中的 Manifest 记录 SHA-256 和格式校验信息。
- V1、V2 的 Macro F1 均为本地历史选择集结果（5,542 条记录）。该选择集在开发期间被重复使用，因此结果属于探索性比较，不是独立盲测。
- V3 的 0.387896 是 V36 三折双种子 pilot CV 结果；路线比较使用了该轮 CV 结果，分组按精确序列而非同源簇进行。它与 V1、V2 的历史 selection 分数口径不同，不可直接比较，也不构成独立确认。
- 校准使用了 1,683 条记录；记录的融合交叉拟合分数不等同于端到端的折外验证。
- 未读取审计标签。V1 CSV 尚未上传到比赛平台，因此没有平台得分。
- GO 预测器使用了外部 GO 注释，其是否符合比赛规则尚未确认。使用基于 GO 的模型前，请向赛事组织方核实。
- V2 分数对应融合评估，不是 V1 可下载 CSV 的比赛成绩。V3 未晋级，不包含 V36 模型检查点或测试集预测。仓库不发布模型检查点。

## English

An experimental project for multilabel protein-function annotation. The workflow combines sequence-based predictions with Gene Ontology (GO) mapping and compares candidate versions using Macro F1 across 500 labels.

This repository documents four milestones in the project. Release versions use a simple, chronological sequence: **V1.0.0** is the V25 + GO test-prediction artifact, **V2.0.0** records the V25 + GO + V30 Pro fusion evaluation, **V3.0.0** documents the V36 controlled feature pilot, and **V4.0.0** publishes the V41-PairGO GO-optimized prediction CSV. The model-family names (V25, V30 Pro, V31, and V36) describe the research lineage; they are distinct from the repository's release numbers.

## Releases

| Release | Contents | Evaluation and Macro F1 |
|---|---|---:|
| [V1.0.0 — V25 + GO test predictions](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v1.0.0) | Test CSV for 28,450 proteins × 500 binary labels, checksum, and validation manifest | 0.481454 |
| [V2.0.0 — V25 + GO + V30 Pro fusion evaluation](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v2.0.0) | Development report, validation JSON, and per-label metrics; no V2 test CSV | 0.486082 |
| [V3.0.0 — V36 controlled GO feature pilot](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v3.0.0) | Three-fold, two-seed pilot metrics, protocol, and validation report; gate not passed, no model or test CSV | 0.387896 (pilot CV; not directly comparable to selection scores) |
| [V4.0.0 — V41-PairGO GO-optimized predictions](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v4.0.0) | 28,450 × 500 prediction CSV and SHA-256 format manifest | No independent evaluation score reported |

## Development history

1. **V25 baseline:** the locked candidate reached 0.434802 in local development evaluation. A separate 35M fusion candidate reached 0.435132 on the same historical selection set but did not pass the promotion gate.
2. **V25 + expanded GO:** expanded GO direct mapping was evaluated alongside V25. A calibration-selected 50/50 fusion reached 0.481454 on the historical selection set. Its full test-prediction CSV is the artifact in [V1.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v1.0.0).
3. **V25 + GO + V30 Pro:** the V25 + GO result was used as the base and upgraded V30 Pro predictions were added with a calibrated 0.10 fusion weight. The all-label result reached 0.486082; the original V30 model was not used. This milestone is documented in [V2.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v2.0.0). V2 test predictions were not generated, so this release contains evaluation artifacts only.
4. **V36 controlled feature pilot:** variance-selected GO, label-aware GO, and label-aware GO plus sequence embedding were compared. Route B reached the best pilot CV Macro F1 of 0.387896, +0.003406 over route A, below the predeclared +0.01 promotion gate. The branch stopped without fusion or a selection evaluation; see [V3.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v3.0.0).
5. **V41-PairGO:** `pairgogpt_v2_pi.csv` is the primary prediction artifact, with limited corrections to selected high-confidence entries using GO, V30 Pro, and V40 outputs. V4.0.0 publishes the CSV and format manifest; no independent evaluation score is reported.

## Data format

The V1.0.0 and V4.0.0 CSVs use the header `protein_id` followed by `label_0` through `label_499`. Each has 28,450 protein rows and binary `0`/`1` predictions. Each release manifest records the SHA-256 checksum and format-validation status.

## Evaluation and limitations

- The V1 and V2 scores are local Macro F1 measurements on a 5,542-row historical selection set. That set was reused during development, so these comparisons are exploratory and are not independent blind validation.
- V3's 0.387896 is a three-fold, two-seed V36 pilot CV result. The route comparison used these CV results and grouped exact sequences rather than homology clusters. It uses a different evaluation protocol from the V1/V2 historical-selection scores and must not be compared directly or treated as independent confirmation.
- Calibration used 1,683 rows. The recorded fusion cross-fit score is not end-to-end out-of-fold validation.
- No audit labels were read. The V1 CSV was generated but was not uploaded to the competition platform; no platform score is available.
- The GO predictor was trained using external GO annotations. Whether that use is allowed by the competition rules has not been confirmed. Check with the organizers before submitting a GO-based model.
- The V2 score is an evaluation result, not the score of the downloadable V1 CSV. The V2 release contains reports and metrics, not model checkpoints; no model checkpoints are published in this repository.
- V3 did not pass its promotion gate and contains no V36 checkpoint or test-prediction CSV.
- V4.0.0 publishes a prediction artifact, but no independent validation score or competition result is reported for it.

## Repository contents

- V1.0.0 and V4.0.0 test-prediction CSVs, distributed as Release assets and not committed to the `main` branch.
- `README.md` — project overview, release history, artifact map, and evaluation limits.
- GitHub Releases — version-specific CSV, manifest, validation, and per-label results.
