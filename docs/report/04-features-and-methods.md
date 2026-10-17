# Features and Analytical Methods

[Report guide](../README.md) · [Figures](../figures.md) · [Tables](../tables.md)

This chapter catalogs sequence statistics, homology signals, ESM2 representations, GO-GPT and ProteInfer outputs, and protein–label context features. It describes candidate-term selection, base predictors, logistic fusion, pair stacking, and threshold optimization.

Original report section: **4 特征变量的选取与数据分析方法**. [Download the source DOCX](https://github.com/Cooljoes/protein-function-prediction-submission/releases/download/v5.0.0/protein_function_prediction_report.docx).

## 4 特征变量的选取与数据分析方法

### 4.1 特征变量

特征按信息来源分为六组（表 1）。所有监督式特征（如候选 GO 术语的挑选）都只在当前折的训练部分上计算，验证折不参与。

**表 1  特征变量一览**

| 特征组 | 内容 | 维度 / 形式 | 用途 |
| --- | --- | --- | --- |
| 序列统计 | 长度（对数）、氨基酸组成、k-mer TF-IDF | 1 + 20 + 9,709 维（稀疏） | k-mer 岭回归、堆叠的蛋白层特征 |
| 同源检索 | MMseqs2 近邻标签投票（k 近邻 / 最大 / top-1 / k=50）、最佳命中一致度等统计 | 500 × 4 + 4 维 | 基础模型与各层的同源可信度特征 |
| 蛋白质语言模型 | ESM2-650M 最后一层与中间层的残基平均嵌入 | 1,280 + 1,280 维 | kNN、MLP、条件 MLP |
| GO-GPT | 候选 GO 术语的最大生成概率（对数量化）、各方面生成术语数 | 1,821 + 3 维 | 逐标签融合、配对 stacker |
| ProteInfer | 4 个模型的均值池化嵌入及其 GO/EC logit；嵌入上的 kNN 与岭回归预测 | 4 × 1,100 维；882/717 等候选 logit | 逐标签融合、配对 stacker 直接特征 |
| 蛋白 / 标签上下文 | 蛋白预测总量与形状（计数、熵、分位数、标签内排名）、相关标签与父子标签的预测、折内标签先验、标签编号 | 每个（蛋白, 标签）约 60 维 | 配对 stacker |

[CSV 下载 / Download CSV](../../data/report-tables/table-01-feature-groups.csv)

### 4.2 特征选择方法

标签是匿名的，无法直接知道每个标签对应哪个 GO 术语。我们在每一折的训练部分上计算“候选术语分数—标签”的皮尔逊相关系数，为每个标签挑选相关性最高的 k 个术语（GO-GPT 取 5 个、ProteInfer 每个模型取 2–5 个）作为该标签的专属特征。候选池先从 10,303 个 GO-GPT 术语中缩减为 1,821 个（每个标签前 16 个），从 32,102 个 ProteInfer 术语中缩减为 882 个（每个标签前 8 个）。对 ProteInfer 候选池的复核表明，5 折内重新挑选的全部 12,500 个 top-5 术语都已在候选池内，候选池本身不引入偏差。

### 4.3 数据分析方法

**表 2  采用的数据分析方法**

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

[CSV 下载 / Download CSV](../../data/report-tables/table-02-analysis-methods.csv)

[← Analysis Design and Evaluation Plan](03-analysis-design.md) · [Data Preparation →](05-data-preparation.md)
