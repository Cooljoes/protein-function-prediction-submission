# Background and Related Methods

[Report guide](../README.md) · [Figures](../figures.md) · [Tables](../tables.md)

This chapter introduces Gene Ontology, homology-based function transfer, protein language models, and models pretrained on functional annotations. It explains how stacking, label relationships, and per-label thresholds inform the proposed prediction pipeline.

Original report section: **2 相关理论综述**. [Download the source DOCX](https://github.com/Cooljoes/protein-function-prediction-submission/releases/download/v5.0.0/protein_function_prediction_report.docx).

## 2 相关理论综述

### 2.1 蛋白质功能注释与基因本体

基因本体（Gene Ontology, GO）以有向无环图组织功能术语，分为分子功能（MF）、生物学过程（BP）、细胞组分（CC）三个方面；注释遵循“真路径规则”，即一个蛋白被注释到某术语时，自动拥有其全部祖先术语[1](references.md#ref-1)。因此 GO 标签之间存在大量包含关系与高相关性，这既是多标签学习可以利用的结构，也意味着“注释深度”（一个蛋白有多少标签）会强烈影响逐标签的判定。CAFA 系列评测是该领域最具影响力的基准[11](references.md#ref-11)，其评测结果表明，同源迁移与机器学习方法的集成通常优于单一方法。

### 2.2 基于同源的功能迁移

进化上同源的蛋白往往保留相似功能。BLAST[2](references.md#ref-2) 与 MMseqs2[3](references.md#ref-3) 等序列比对工具可在大规模数据库中快速寻找同源序列，再按相似度加权投票迁移其功能标签（k 近邻）。该方法在高相似度区间非常准确，但在相似度低于约 40% 的“暮光区”与无同源序列的“孤儿蛋白”上效果显著下降。替换矩阵 BLOSUM62[4](references.md#ref-4) 描述了氨基酸之间的进化替换倾向，本研究在序列预处理中用它辅助确定字母编码映射。

### 2.3 蛋白质语言模型

蛋白质语言模型在数亿条无标注序列上以掩码语言建模方式自监督训练，学到的残基与序列表示蕴含结构与功能信息。ESM2[5](references.md#ref-5) 是其中代表，其嵌入可直接用于下游的近邻检索或轻量分类器。这类模型以标准氨基酸编码为输入，因此需要先完成问题 1 中的编码对齐。

### 2.4 以功能注释预训练的模型

另一类公开模型直接以 GO / EC 注释作为监督信号训练。ProteInfer[6](references.md#ref-6) 使用扩张残差卷积网络从序列预测约 3.2 万个 GO 术语与 EC 编号；GO-GPT（BioReason-Pro 的组成部分[7](references.md#ref-7)）以 ESM2 表示为条件，用自回归解码器逐个生成 GO 术语。这类模型的输出空间与本题标签同属 GO 体系，经过“匿名标签—GO 术语”的对应后，可以作为强特征。

### 2.5 多标签学习、堆叠集成与阈值优化

多标签学习可分为把问题拆成独立二分类的“问题转换法”与显式利用标签相关性的方法[12](references.md#ref-12)。堆叠泛化（Stacking）[8](references.md#ref-8) 以第一层模型的折外预测作为第二层模型的输入，能综合不同模型的长处；梯度提升决策树 LightGBM[9](references.md#ref-9) 在大规模表格数据上效率高，适合作为第二层学习器。由于 F1 不是概率的单调函数，最优决策阈值往往远低于 0.5，需要针对每个标签单独搜索[10](references.md#ref-10)；而阈值本身也会过拟合，必须在独立数据上调优与评估。

[← Objectives and Research Questions](01-objectives.md) · [Analysis Design and Evaluation Plan →](03-analysis-design.md)
