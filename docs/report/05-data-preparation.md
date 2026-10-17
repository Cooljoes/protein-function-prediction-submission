# Data Preparation

[Report guide](../README.md) · [Figures](../figures.md) · [Tables](../tables.md)

This chapter documents missing derived features, long and duplicate sequences, nonstandard residues, numerical issues, and sequence-encoding alignment. It also explains feature transformations, dimensionality reduction, and the roles of the dev, clean, confirmation, and test subsets.

Original report section: **5 数据的整理**. [Download the source DOCX](https://github.com/Cooljoes/protein-function-prediction-submission/releases/download/v5.0.0/protein_function_prediction_report.docx).

## 5 数据的整理

### 5.1 数据缺失

标签矩阵与序列本身没有缺失值。缺失主要出现在派生特征中：GO-GPT 的打分分批完成，最终覆盖了全部 113,796 个训练蛋白与 28,450 个测试蛋白；其中 ESM2-3B 表示与解码器状态有 3,292 个训练蛋白早期未保存，测试集则未计算，因此这两类表示只用于探索，不进入最终模型，从源头避免训练—测试分布不一致。对少数无同源命中的蛋白（训练 7.7%、测试 7.3%），同源一致度记为 0 并作为显式特征，由模型学习其含义。

### 5.2 异常值筛选

- 极端长度：序列长度 3–35,375，10.7% 超过 ESM2 的 1,022 残基窗口。长序列用 4 个窗口的嵌入平均（ESM2-650M）或截断（GO-GPT 取前 1,022 个）处理；分析表明 GO-GPT 在长蛋白上的增益并不比短蛋白低（+0.038 对 +0.022–0.034），无需额外处理。

- 非标准残基：按 ProteInfer 的约定，U→C、O→X，B / Z 在两种氨基酸间平均分配，X 均匀分配。

- 数值异常：ProteInfer 在 GPU 半精度下出现溢出（非有限值），改用单精度，与 CPU 结果的相对误差仅 8×10⁻⁴；所有特征写出前检查有限性。

- 重复序列：训练集中有 2,613 组共 5,816 个序列完全相同的蛋白，它们被约束在同一折，避免验证分数虚高。

### 5.3 数据转换

- 字母编码映射：统计竞赛训练集内部序列比对中的字母替换频率，与标准替换矩阵 BLOSUM62 对齐，确定 20 个字母与标准氨基酸编码之间的一一映射（相关系数 0.966）。映射全程只使用竞赛训练集，未使用任何外部序列或数据库，映射后的序列仅作为预训练模型的输入；映射后 ESM2 的掩码预测损失为 2.39，处于天然蛋白的正常范围（映射前为 2.89）。

- 概率变换：GO-GPT 分数取对数并量化到 0–255（覆盖 10⁻⁶–1 的 6 个数量级）；各模型概率在融合前转为 logit；连续特征在每折训练部分上标准化。

- 格式转换：序列转为 one-hot（ProteInfer）或分词编码（ESM2）；多标签结果按“蛋白 × 标签”展开为 5,000 余万行的配对表供 LightGBM 使用（训练时按规则采样）。

### 5.4 数据集划分

**表 3  数据集划分**

| 数据子集 | 蛋白数 | 用途 |
| --- | --- | --- |
| 训练集（全部） | 113,796 | 5 折分组交叉验证 |
| 其中：dev 行 | 108,796 | 模型训练与 honest 评估 |
| 其中：干净行 | 100,504 | 排除候选术语挑选所用蛋白后的评估 |
| 其中：确认集 | 5,000 | 留出，只打开两次做关键版本确认 |
| 测试集 | 28,450 | 提交预测，排行榜评分 |

[CSV 下载 / Download CSV](../../data/report-tables/table-03-dataset-subsets.csv)

### 5.5 数据降维

高维表示在进入下游模型前进行压缩：ESM2-3B 的 2,560 维平均嵌入经 PCA 降到 512 维（保留 86% 方差），GO-GPT 解码器 3 × 900 维起始状态降到 256 维（85%）；候选 GO 术语的筛选把 GO-GPT 的 10,303 维与 ProteInfer 的 32,102 维输出分别压缩到 1,821 维与 882 维，再在每个标签上只保留 2–5 个最相关的术语。由于 ProteInfer 的输出层是线性的，相关性可以直接由嵌入的协方差投影得到，无需显式计算每个蛋白的 3.2 万个 logit。

[← Features and Analytical Methods](04-features-and-methods.md) · [Exploratory Data Analysis →](06-exploratory-analysis.md)
