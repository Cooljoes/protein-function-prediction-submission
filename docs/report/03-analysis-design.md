# Analysis Design and Evaluation Plan

[Report guide](../README.md) · [Figures](../figures.md) · [Tables](../tables.md)

This chapter outlines the three-stage ensemble and the report's evaluation plan: five folds grouping identical sequences, thresholds tuned on other folds, a confirmation set, and a clean-row subset. It also records the hardware constraints and checkpointing approach used during feature generation.

Original report section: **3 分析方案的设计**. [Download the source DOCX](https://github.com/Cooljoes/protein-function-prediction-submission/releases/download/v5.0.0/protein_function_prediction_report.docx).

The original report describes the historical `allbag2` workflow. The current [V5.0.0 release](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) uses the separately supplied `allkbag2` CSV, with the owner-confirmed leaderboard score **64.3818**. Original figure labels and table values are retained.

原报告描述历史 `allbag2` 方案；当前 [V5.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) 使用单独提供的 `allkbag2`，项目所有者确认的排行榜成绩为 **64.3818**。原图标注与表格数值保持原样。

## 3 分析方案的设计

### 3.1 总体技术路线

围绕第 1 章提出的五个问题，方案按“数据整理—信息源构建—三层融合—严格验证”展开（图 1）。三类信息源相互独立地提取特征；基础层只使用比赛数据与通用蛋白质语言模型；第二层用逐标签逻辑回归吸收注释预训练模型的信号；第三层用配对 stacker 学习跨模型、跨标签的修正。

[![Figure 1 — Overall Modeling Workflow](../../assets/figures/report/figure-01-overall-workflow.png)](../../assets/figures/report/figure-01-overall-workflow.png)

*图 1  总体技术路线*

Historical workflow: 15 prediction inputs and local Macro-F1 62.72; the V5 `allkbag2` variant adds a GO-GPT score-space kNN input.

历史流程包含 15 项预测输入，本地 Macro-F1 为 62.72；V5 的 `allkbag2` 增加了 GO-GPT 分数空间 kNN 输入。

### 3.2 评估方案设计

每天只有一次提交机会，排行榜反馈稀缺且噪声大，因此方案的核心是一套可信的本地评估体系：

- 分组 5 折交叉验证：测试集是先随机划分、再把与训练集序列完全相同的蛋白移回训练集得到的，因此折划分时同一序列的蛋白必须落在同一折，避免“记住序列”带来的虚高。

- honest 口径：所有模型输出折外预测（OOF）；每一折的 500 个阈值只用其余 4 折调优，再在本折上计分。

- 确认集：在大规模拟合开始前随机留出 5,000 个蛋白，不参与任何训练、特征选择和调参，只在两次关键版本跳跃时各打开一次。

- 干净行口径：部分候选 GO 术语是用 8,292 个蛋白的标签挑选的，这些蛋白从“干净行”中剔除，用来检验选择偏差（实测仅 0.04–0.12 分）。

- 晋级规则：新版本必须在 dev 与干净行上同时提升 ≥ 0.15–0.3，且 5 折中至少 4 折提升，才替换现有版本，以控制多次比较带来的乐观偏差。

- 排行榜校准：用已提交版本的排行榜得分校准本地分数（两次提交分别为 +1.75 与 +1.66，排行榜 ≈ 本地 honest + 1.7），据此预估新版本的表现。

### 3.3 计算资源与工程约束

全部计算在一台笔记本工作站完成（RTX 4060 8 GB 显存、32 线程、16 GB 内存）。GO-GPT 对 14.2 万个蛋白的打分约需 10–12 GPU 小时，采用分块保存、断点续跑；GPU 任务均设置显存上限，避免显存溢出导致的成倍降速；内存受限的步骤（如 15 个模型输入的配对 stacker，峰值约 8 GB）串行执行。

[← Background and Related Methods](02-background.md) · [Features and Analytical Methods →](04-features-and-methods.md)
