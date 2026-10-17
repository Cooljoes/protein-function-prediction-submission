# Report Abstract

[Report guide](../README.md) · [Project overview](../../README.md)

The original report presents a three-stage ensemble for predicting 500 protein-function labels. Its abstract records the historical `allbag2` results and the observations that motivated the feature and evaluation design.

The original report describes the historical `allbag2` workflow. The current [V5.0.0 release](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) uses the separately supplied `allkbag2` CSV, with the owner-confirmed leaderboard score **64.3818**. Original figure labels and table values are retained.

原报告描述历史 `allbag2` 方案；当前 [V5.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) 使用单独提供的 `allkbag2`，项目所有者确认的排行榜成绩为 **64.3818**。原图标注与表格数值保持原样。

## 摘要

蛋白质功能注释是生命科学与生物医药研发的基础工作，但依赖湿实验的注释成本高、周期长。本报告围绕“仅凭氨基酸序列预测蛋白质的 500 个基因本体（GO）功能标签”这一多标签分类任务，以标签平均的 Macro-F1 为评价指标，建立了一套从数据整理、探索性分析到多层集成建模与严格验证的完整分析流程。

竞赛序列采用非标准的字母编码。在序列预处理阶段，我们依据竞赛训练集内部的序列比对统计并结合标准替换矩阵，确定了字母与标准氨基酸编码之间的映射，映射后的序列仅作为预训练模型的输入。随后融合三类信息源：训练集内部的 MMseqs2 同源检索、ESM2 蛋白质语言模型嵌入，以及以 GO 注释预训练的 GO-GPT 与 ProteInfer 模型。建模采用三层结构：11 个基础模型经 LightGBM 配对堆叠与 MLP 堆叠得到基础层（honest Macro-F1 47.69）；逐标签逻辑回归融合注释预训练模型的输出（56.02）；最后以 LightGBM“蛋白 × 标签”配对 stacker 学习跨标签、跨模型的修正，得到最终模型（62.72）。

评估全程采用按序列分组的 5 折交叉验证，阈值只在其他折上调优（honest 口径），并设置 5,000 个蛋白的留出确认集与“干净行”口径控制选择偏差。本地分数与排行榜高度一致（排行榜 ≈ 本地 honest + 1.7）：中间版本本地 60.39、排行榜 62.14；最终模型本地 62.72、排行榜 64.38。分析还发现：序列完全相同的蛋白之间标签吻合度仅 23.3（F1），说明标签中存在不可由序列解释的注释深度差异；而功能注释预训练模型与跨标签上下文是提升的主要来源。

关键词：蛋白质功能预测；基因本体；蛋白质语言模型；多标签分类；堆叠集成；LightGBM；Macro-F1

[Objectives and research questions →](01-objectives.md)
