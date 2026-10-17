# Source Code Structure

[Report guide](../README.md) · [Figures](../figures.md) · [Tables](../tables.md)

This appendix maps the reported pipeline stages to their scripts and outputs. Its documented commands target the historical allbag2 workflow; the V5 notes identify the additional gogptq feature-generation step missing from the archive for complete allkbag2 reproduction.

Original report section: **附录 B 源码结构**. [Download the source DOCX](https://github.com/Cooljoes/protein-function-prediction-submission/releases/download/v5.0.0/protein_function_prediction_report.docx).

The original report describes the historical `allbag2` workflow. The current [V5.0.0 release](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) uses the separately supplied `allkbag2` CSV, with the owner-confirmed leaderboard score **64.3818**. Original figure labels and table values are retained.

原报告描述历史 `allbag2` 方案；当前 [V5.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) 使用单独提供的 `allkbag2`，项目所有者确认的排行榜成绩为 **64.3818**。原图标注与表格数值保持原样。

The original archive name `ht_source_code.zip` below is preserved from the report. The published package is named `protein_function_prediction_source.zip`; its reproduction commands cover `allbag2`.

下文 `ht_source_code.zip` 是原报告使用的历史包名，当前发布附件名为 `protein_function_prediction_source.zip`，包内复现命令针对 `allbag2`。

## 附录 B 源码结构

源码包 ht_source_code.zip 按流程编号组织，README.md 给出从原始数据到最终提交文件的完整命令与每一步的预期分数，MODELS.md 列出外部资源及校验值。主要脚本如下（common.py 提供数据读取、折划分与 honest 评估等公共函数）。

**表 9  流程步骤与对应脚本**

| 流程步骤 | 脚本 | 主要产出 |
| --- | --- | --- |
| 分组 5 折划分 | 02_make_folds.py | data/folds.csv |
| 字母编码映射 | 13_encoding_map.py | data/encoding_map.json |
| 序列统计特征 | 03_baseline_kmer.py、12_composition.py | kmer_ridge、comp |
| ESM2 嵌入与基础模型 | 04_embed.py、05_train_mlp.py、17_train_mlp_cond.py、06_knn.py | esm2_650m 嵌入，MLP / kNN 基础模型 |
| 同源检索 | 07_mmseqs_knn.py --mapped | mmseqsmap_{knn,max,k50,top1}、hitstats_map |
| 基础层堆叠 | 21_depth.py、09_stack.py、23_mlp_stack.py、08_blend.py | stack_depth、mlpstack、blend_sm |
| GO-GPT 打分与合并 | 20_gogpt.py、22_gogpt_eval.py、26_camber_prep.py、27_gogpt_merge.py | gogptm_v2_*（候选 GO 术语分数） |
| ProteInfer 特征 | 33_proteinfer.py、34_proteinfer_terms.py、40_pinf_ridge.py | 嵌入、候选 logit、岭回归头 |
| 逐标签融合 | 28_gogpt_fusion.py | gogptfus_v2_ntpi_k5 |
| 配对 stacker 与种子平均 | 35_pair_gogpt.py、41_avg.py | pairgogpt_v2_allbag2 |
| 提交文件生成与校验 | 38_make_sub.py | submissions/pairgogpt_v2_allbag2.csv |

[CSV 下载 / Download CSV](../../data/report-tables/table-09-pipeline-scripts.csv)

[← External Resources](appendix-a-resources.md)
