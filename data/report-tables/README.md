# Report Table Data

[Report guide](../../docs/README.md) · [Rendered tables](../../docs/tables.md)

These UTF-8 CSV files reproduce the nine tables in the analysis report. Headers and values retain the source wording and precision; the files contain aggregate report tables, not the competition training dataset.

The original report describes the historical `allbag2` workflow. The current [V5.0.0 release](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) uses the separately supplied `allkbag2` CSV, with the owner-confirmed leaderboard score **64.3818**. Original figure labels and table values are retained.

以下 UTF-8 CSV 对应报告全部 9 张表。表头、单元格文字和数值精度均按原报告保留；内容为报告汇总表，不是比赛训练数据。

原报告描述历史 `allbag2` 方案；当前 [V5.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) 使用单独提供的 `allkbag2`，项目所有者确认的排行榜成绩为 **64.3818**。原图标注与表格数值保持原样。

| Table | Description | CSV |
|---|---|---|
| 1 | Feature Groups and Their Roles<br>表 1  特征变量一览 | [table-01-feature-groups.csv](table-01-feature-groups.csv) |
| 2 | Modeling and Decision Methods<br>表 2  采用的数据分析方法 | [table-02-analysis-methods.csv](table-02-analysis-methods.csv) |
| 3 | Dataset Subsets and Evaluation Roles<br>表 3  数据集划分 | [table-03-dataset-subsets.csv](table-03-dataset-subsets.csv) |
| 4 | Descriptive Statistics for the Training and Test Sets<br>表 4  数据描述统计 | [table-04-descriptive-statistics.csv](table-04-descriptive-statistics.csv) |
| 5 | Five-Fold Honest Macro-F1 of Individual Models and the Base Ensemble<br>表 5  单一模型与基础层的 honest Macro-F1（5 折） | [table-05-base-model-results.csv](table-05-base-model-results.csv) |
| 6 | Incremental Model Ablations on Dev and Clean Rows<br>表 6  逐步改进的消融结果（dev / 干净行，honest Macro-F1） | [table-06-model-ablations.csv](table-06-model-ablations.csv) |
| 7 | Key Model Results Across Evaluation Subsets and the Leaderboard<br>表 7  关键版本在不同验证口径下的表现 | [table-07-evaluation-comparison.csv](table-07-evaluation-comparison.csv) |
| 8 | Public Pretrained Models and Third-Party Code<br>表 8  公开预训练权重与第三方代码 | [table-08-external-resources.csv](table-08-external-resources.csv) |
| 9 | Pipeline Stages, Scripts, and Outputs<br>表 9  流程步骤与对应脚本 | [table-09-pipeline-scripts.csv](table-09-pipeline-scripts.csv) |

## Provenance

[Table metadata and SHA-256](manifest.json)

[Original report](https://github.com/Cooljoes/protein-function-prediction-submission/releases/download/v5.0.0/protein_function_prediction_report.docx)
