# Objectives and Research Questions

[Report guide](../README.md) · [Figures](../figures.md) · [Tables](../tables.md)

This chapter defines the task of predicting 500 anonymous GO-related labels from protein sequences, using 113,796 labeled proteins and 28,450 test proteins. It frames the main questions around sequence encoding, complementary information sources, ensemble design, evaluation, and annotation variability.

Original report section: **1 分析目标与分析问题**. [Download the source DOCX](https://github.com/Cooljoes/protein-function-prediction-submission/releases/download/v5.0.0/protein_function_prediction_report.docx).

## 1 分析目标与分析问题

### 1.1 研究背景

蛋白质是生命活动的主要执行者，准确知道一个蛋白质“做什么”（分子功能）、“参与什么过程”（生物学过程）以及“在哪里起作用”（细胞组分），是药物靶点发现、酶工程与疾病机制研究的前提。公共数据库中已测序的蛋白质数以亿计，但经过实验验证功能注释的比例不足 1%。依靠湿实验逐个注释成本高、周期长，因此利用计算方法从序列直接预测功能，具有显著的科研与产业价值。

本赛题共提供 142,246 个蛋白质，其中 113,796 个为带标签的训练集、28,450 个为测试集。每个蛋白需要预测 500 个匿名化的 GO 标签是否成立，属于典型的大规模多标签分类问题；评价指标为 500 个标签各自 F1 的算术平均（Macro-F1），对稀有标签与常见标签一视同仁。

### 1.2 分析目标

在仅使用比赛数据与公开预训练模型权重的前提下，构建一个对测试集具有最高 Macro-F1 的预测模型，并保证评估结论可信、可复现；同时从数据中提炼对功能注释业务有指导意义的发现。

### 1.3 分析问题

- 问题 1（序列表示）：竞赛序列采用非标准的字母编码，而公开的蛋白质预训练模型以标准氨基酸编码为输入。如何在只使用竞赛数据的前提下完成编码对齐？

- 问题 2（信息来源）：同源序列、通用蛋白质语言模型、以功能注释预训练的模型，各自对 500 个标签提供多少信息？是否互补？

- 问题 3（模型融合）：如何把数十个来源、数万维的信号组合成 500 个标签的最终决策，并利用标签之间的结构关系？

- 问题 4（评估可信度）：每天只有一次提交机会，如何设计本地验证，使本地分数可靠地反映排行榜表现、避免过拟合？

- 问题 5（性能边界）：误差主要来自哪里？是否存在仅凭序列无法逾越的上限？

[Background and Related Methods →](02-background.md)
