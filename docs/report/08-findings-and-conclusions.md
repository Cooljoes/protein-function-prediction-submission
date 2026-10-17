# Findings, Limitations, and Conclusions

[Report guide](../README.md) · [Figures](../figures.md) · [Tables](../tables.md)

This chapter summarizes the reported contributions of encoding alignment, annotation-pretrained models, and cross-label context, alongside annotation variability and computational costs. It discusses potential uses and future work, including fully nested cross-fitting across ensemble layers.

Original report section: **8 数据发现与结论**. [Download the source DOCX](https://github.com/Cooljoes/protein-function-prediction-submission/releases/download/v5.0.0/protein_function_prediction_report.docx).

The original report describes the historical `allbag2` workflow. The current [V5.0.0 release](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) uses the separately supplied `allkbag2` CSV, with the owner-confirmed leaderboard score **64.3818**. Original figure labels and table values are retained.

原报告描述历史 `allbag2` 方案；当前 [V5.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) 使用单独提供的 `allkbag2`，项目所有者确认的排行榜成绩为 **64.3818**。原图标注与表格数值保持原样。

## 8 数据发现与结论

### 8.1 主要发现

- 编码对齐是使用预训练模型的前提：竞赛序列采用非标准字母编码，依据训练集内部统计完成编码映射后，蛋白质语言模型与功能注释预训练模型才得以按设计使用。

- 信息来源的价值排序：功能注释预训练模型（GO-GPT +6.2、ProteInfer +2.1 并在第三层再贡献约 +1.8）&gt; 同源检索 ≈ 通用语言模型；三者显著互补。

- 跨标签上下文是第二大杠杆：逐标签模型看不到“这个蛋白整体有多少功能”，配对 stacker 引入蛋白层上下文与标签结构后提升 4.4 分。

- 阈值已接近最优：逐标签阈值的理论上限只比 honest 高约 0.35，进一步提升必须依靠更好的排序信号，而不是调阈值。

- 存在序列无法解释的标签噪声：相同序列蛋白之间标签吻合度仅 23.3，注释深度主要取决于物种与条目，仅凭序列的模型存在硬上限。

### 8.2 分析结果的使用与决策支持

- 功能注释流水线：模型可对新测序蛋白批量给出 500 个功能的概率，作为数据库自动注释或人工审核前的初筛，显著降低人工成本。

- 湿实验优先级排序：对药物靶点发现或酶工程项目，可按预测概率与同源可信度对候选蛋白排序，把有限的实验预算优先投入“高概率、低同源”（模型增益最大、现有工具最难判断）的蛋白。

- 按业务目标调节阈值：本方案对每个功能单独设定阈值。若业务更看重召回（如安全性筛查），可整体下调阈值；若更看重精确（如自动入库），可上调阈值或只采信高同源区间的结果。

- 模型治理：本地 honest 评估与排行榜高度一致（偏差稳定在约 1.7），说明这套验证流程可直接用于上线前的效果预估与版本迭代决策。

### 8.3 局限与改进方向

- 外部资源的使用边界：训练与评估只使用竞赛提供的数据。ESM2、GO-GPT、ProteInfer 均以公开发布的预训练权重形式使用，仅在本地对竞赛序列做前向推理并把输出作为特征，未获取或使用其原始训练数据；各模型的来源、版本与许可见附录 A。为便于区分各信息源的作用，报告同时给出了不含功能注释预训练模型的基础层结果（47.69）。

- 计算成本：生成式模型打分耗时较长（GO-GPT v1 约 10–12 GPU 小时，v2 约 12 小时），未来可通过限制解码步数、批量推理优化降低成本。

- 改进方向：以嵌套交叉拟合完全隔离各层的折外特征；引入更多 k 值的功能空间近邻投票；在更充裕算力下集成 GO-GPT v2 与更大的语言模型。

### 8.4 结论

本研究针对“序列采用非标准字母编码、标签匿名、指标为 Macro-F1”的蛋白质功能多标签预测任务，先完成序列编码对齐，再融合同源检索、蛋白质语言模型与功能注释预训练模型三类信息源，构建“基础层—逐标签融合—配对 stacker”三层集成模型。在严格的分组交叉验证与留出确认下，最终模型 honest Macro-F1 达到 62.72，较基础层提升 15.0 分；最终提交的排行榜得分为 64.38，与本地预估一致。分析同时揭示了标签中存在的、由注释深度造成的不可约噪声，为蛋白质功能注释的自动化与实验资源分配提供了数据依据。

[← Model Development and Evaluation](07-modeling-and-evaluation.md) · [References →](references.md)
