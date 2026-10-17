# Report Tables

[Report guide](README.md) · [Figures](figures.md) · [CSV downloads](../data/report-tables/README.md)

The nine original Word tables are reproduced below with their cell text and numerical precision retained. CSV downloads contain the same rows.

The original report describes the historical `allbag2` workflow. The current [V5.0.0 release](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) uses the separately supplied `allkbag2` CSV, with the owner-confirmed leaderboard score **64.3818**. Original figure labels and table values are retained.

以下保留全部 9 张 Word 表格的单元格内容及数值精度，并提供相同数据的 CSV 下载。

原报告描述历史 `allbag2` 方案；当前 [V5.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) 使用单独提供的 `allkbag2`，项目所有者确认的排行榜成绩为 **64.3818**。原图标注与表格数值保持原样。

<a id="table-01"></a>

## Table 1 — Feature Groups and Their Roles

表 1  特征变量一览

| 特征组 | 内容 | 维度 / 形式 | 用途 |
| --- | --- | --- | --- |
| 序列统计 | 长度（对数）、氨基酸组成、k-mer TF-IDF | 1 + 20 + 9,709 维（稀疏） | k-mer 岭回归、堆叠的蛋白层特征 |
| 同源检索 | MMseqs2 近邻标签投票（k 近邻 / 最大 / top-1 / k=50）、最佳命中一致度等统计 | 500 × 4 + 4 维 | 基础模型与各层的同源可信度特征 |
| 蛋白质语言模型 | ESM2-650M 最后一层与中间层的残基平均嵌入 | 1,280 + 1,280 维 | kNN、MLP、条件 MLP |
| GO-GPT | 候选 GO 术语的最大生成概率（对数量化）、各方面生成术语数 | 1,821 + 3 维 | 逐标签融合、配对 stacker |
| ProteInfer | 4 个模型的均值池化嵌入及其 GO/EC logit；嵌入上的 kNN 与岭回归预测 | 4 × 1,100 维；882/717 等候选 logit | 逐标签融合、配对 stacker 直接特征 |
| 蛋白 / 标签上下文 | 蛋白预测总量与形状（计数、熵、分位数、标签内排名）、相关标签与父子标签的预测、折内标签先验、标签编号 | 每个（蛋白, 标签）约 60 维 | 配对 stacker |

[Download CSV](../data/report-tables/table-01-feature-groups.csv) · [Report chapter](report/04-features-and-methods.md)

<a id="table-02"></a>

## Table 2 — Modeling and Decision Methods

表 2  采用的数据分析方法

| 层次 | 方法 | 要点 |
| --- | --- | --- |
| 基础模型 | k-mer TF-IDF + 岭回归 | 线性基线，捕捉短序列片段 |
| 基础模型 | 余弦 k 近邻（ESM2、ProteInfer、GO-GPT 分数空间） | softmax 相似度加权投票，k 与温度在折外预测上选择 |
| 基础模型 | 多层感知机（MLP）/ 条件 MLP | BCE 损失；条件 MLP 显式建模父子标签 |
| 基础模型 | 岭回归多标签头 | 在 ProteInfer 嵌入上闭式求解，绕过逐标签选词 |
| 第一层堆叠 | LightGBM 配对堆叠、跨标签 MLP 堆叠 | 输入 11 个基础模型折外预测 + 蛋白层特征，2:1 混合 |
| 第二层 | 逐标签逻辑回归 | C = 0.3，标准化；含同源一致度交互项 |
| 第三层 | LightGBM 配对 stacker | 以融合 logit 为 init_score 学习修正；负例按 5% 采样并加权；2 个随机种子平均 |
| 决策 | 逐标签阈值搜索 | 阈值网格 0.02–0.80，平滑 + 收缩，跨折调优 |

[Download CSV](../data/report-tables/table-02-analysis-methods.csv) · [Report chapter](report/04-features-and-methods.md)

<a id="table-03"></a>

## Table 3 — Dataset Subsets and Evaluation Roles

表 3  数据集划分

| 数据子集 | 蛋白数 | 用途 |
| --- | --- | --- |
| 训练集（全部） | 113,796 | 5 折分组交叉验证 |
| 其中：dev 行 | 108,796 | 模型训练与 honest 评估 |
| 其中：干净行 | 100,504 | 排除候选术语挑选所用蛋白后的评估 |
| 其中：确认集 | 5,000 | 留出，只打开两次做关键版本确认 |
| 测试集 | 28,450 | 提交预测，排行榜评分 |

[Download CSV](../data/report-tables/table-03-dataset-subsets.csv) · [Report chapter](report/05-data-preparation.md)

<a id="table-04"></a>

## Table 4 — Descriptive Statistics for the Training and Test Sets

表 4  数据描述统计

| 指标 | 训练集 | 测试集 |
| --- | --- | --- |
| 蛋白数 | 113,796 | 28,450 |
| 序列长度：最小 / 中位数 / 均值 / 最大 | 3 / 410 / 553.2 / 35,375 | 6 / 414 / 555.4 / 35,213 |
| 长度 &gt; 1,022 的比例 | 10.7% | — |
| 每个蛋白的标签数：均值 / 中位数 / 范围 | 25.42 / 17 / 1–273 | — |
| 标签阳性率：最低 / 中位数 / 最高 | 1.13% / 2.36% / 65.51% | — |
| 每个标签的阳性样本数：最少 / 中位数 / 最多 | 1,287 / 2,688 / 74,546 | — |
| 标签矩阵密度 | 5.08% | — |
| 无同源命中 / 最佳命中一致度 ≥ 95% | 7.7% / 13.0%（折外） | 7.3% / 14.5% |

[Download CSV](../data/report-tables/table-04-descriptive-statistics.csv) · [Report chapter](report/06-exploratory-analysis.md)

<a id="table-05"></a>

## Table 5 — Five-Fold Honest Macro-F1 of Individual Models and the Base Ensemble

表 5  单一模型与基础层的 honest Macro-F1（5 折）

| 模型 | 信息来源 | honest Macro-F1 |
| --- | --- | --- |
| k-mer 岭回归 | 序列片段 | 31.12 |
| MLP（ESM2 最后层） | 通用语言模型 | 37.79 |
| MLP（ESM2 最后层 + 中间层） | 通用语言模型 | 39.10 |
| 条件 MLP / 边际 MLP | 通用语言模型 + 标签层级 | 39.60 / 39.65 |
| kNN（ESM2） | 通用语言模型 | 40.54 |
| 岭回归头（ProteInfer 嵌入） | 注释预训练模型 | 40.67 |
| MMseqs2 同源 kNN | 同源检索 | 41.91 |
| kNN（GO-GPT 分数空间） | 注释预训练模型 | 43.14 |
| kNN（ProteInfer 嵌入） | 注释预训练模型 | 43.53 |
| LightGBM 配对堆叠 stack_depth | 11 个基础模型 | 47.32 |
| MLP 堆叠 mlpstack | 11 个基础模型 | 45.76 |
| 基础层 blend_sm | 2:1 混合 | 47.69 |

[Download CSV](../data/report-tables/table-05-base-model-results.csv) · [Report chapter](report/07-modeling-and-evaluation.md)

<a id="table-06"></a>

## Table 6 — Incremental Model Ablations on Dev and Clean Rows

表 6  逐步改进的消融结果（dev / 干净行，honest Macro-F1）

| 版本 | 改动 | dev | 干净行 | 增量 |
| --- | --- | --- | --- | --- |
| blend_sm | 基础层 | 47.69 | 47.59 | — |
| gogptfus_v2_nt_k5 | + GO-GPT 逐标签逻辑回归融合 | 53.93 | 53.83 | +6.24 |
| gogptfus_v2_ntpi_k5 | + ProteInfer（GO 随机划分）logit | 56.02 | 55.94 | +2.09 |
| pairgogpt_v2_pi | + LightGBM 配对 stacker（含标签结构） | 60.39 | 60.32 | +4.37 |
| pid | + ProteInfer logit 直接进入 stacker | 62.10 | 62.05 | +1.71 |
| pid4 | + 全部 4 个 ProteInfer 模型 | 62.15 | 62.10 | +0.05 |
| pid4rs | + 岭回归头 + 蛋白内形状特征 | 62.29 | 62.24 | +0.14 |
| all | + 全部基础模型 + ProteInfer kNN | 62.66 | 62.61 | +0.37 |
| allbag2（最终） | 2 个随机种子平均 | 62.72 | 62.68 | +0.06 |

[Download CSV](../data/report-tables/table-06-model-ablations.csv) · [Report chapter](report/07-modeling-and-evaluation.md)

Historical `allbag2` results are retained in this table.

本表保留报告中历史 `allbag2` 的结果。

<a id="table-07"></a>

## Table 7 — Key Model Results Across Evaluation Subsets and the Leaderboard

表 7  关键版本在不同验证口径下的表现

| 版本 | dev | 干净行 | 确认集 | 排行榜 |
| --- | --- | --- | --- | --- |
| 基础层 blend_sm | 47.69 | 47.59 | 47.52 | — |
| v1：GO-GPT 逐标签融合（3,292 个已打分蛋白训练） | — | — | 53.08 | 54.87 |
| GO-GPT + ProteInfer 逻辑回归融合 | 56.02 | 55.94 | 55.79 | — |
| pairgogpt_v2_pi（配对 stacker） | 60.39 | 60.32 | 60.59 | 62.14 |
| 最终模型 allbag2 | 62.72 | 62.68 | — | 64.38 |

[Download CSV](../data/report-tables/table-07-evaluation-comparison.csv) · [Report chapter](report/07-modeling-and-evaluation.md)

Historical `allbag2` results are retained in this table.

本表保留报告中历史 `allbag2` 的结果。

<a id="table-08"></a>

## Table 8 — Public Pretrained Models and Third-Party Code

表 8  公开预训练权重与第三方代码

| 资源 | 来源 | 许可 | 用途 |
| --- | --- | --- | --- |
| ESM2-650M | facebook/esm2_t33_650M_UR50D | MIT | 通用蛋白质语言模型嵌入 |
| ESM2-3B（前 30 层） | facebook/esm2_t36_3B_UR50D | MIT | GO-GPT v1 的蛋白编码器 |
| GO-GPT v1 | wanglab/gogpt | Apache-2.0 | 生成式 GO 术语打分 |
| ProteInfer ×4 | samirchar/proteinfertorch-{go,ec}-{random,clustered} | Apache-2.0 | GO / EC logit 与嵌入 |
| GO-GPT 模型结构代码 | github.com/bowang-lab/BioReason-Pro（单个文件） | MIT | 加载 GO-GPT 解码器 |
| MMseqs2 | github.com/soedinglab/MMseqs2 | GPL-3.0 | 训练集内部同源检索 |

[Download CSV](../data/report-tables/table-08-external-resources.csv) · [Report chapter](report/appendix-a-resources.md)

<a id="table-09"></a>

## Table 9 — Pipeline Stages, Scripts, and Outputs

表 9  流程步骤与对应脚本

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

[Download CSV](../data/report-tables/table-09-pipeline-scripts.csv) · [Report chapter](report/appendix-b-source-structure.md)
