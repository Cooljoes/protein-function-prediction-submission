# Analysis Report Guide

[Project overview](../README.md) · [Figure gallery](figures.md) · [Report tables](tables.md) · [Table CSVs](../data/report-tables/README.md)

Read the report on GitHub through its abstract, eight chapters, references, and two appendices. Each chapter starts with an English overview followed by the original Chinese text. All 10 embedded figures and 9 tables retain their original numbering.

The original report describes the historical `allbag2` workflow. The current [V5.0.0 release](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) uses the separately supplied `allkbag2` CSV, with the owner-confirmed leaderboard score **64.3818**. Original figure labels and table values are retained.

按原报告结构阅读摘要、八个章节、参考文献和两个附录。每章先给出英文概述，再保留中文正文；全部 10 张原图和 9 张表沿用原编号。

原报告描述历史 `allbag2` 方案；当前 [V5.0.0](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0) 使用单独提供的 `allkbag2`，项目所有者确认的排行榜成绩为 **64.3818**。原图标注与表格数值保持原样。

## Contents

| Section | Report content | Figures / tables |
|---|---|---|
| [Abstract](report/00-summary.md) | 摘要 | — |
| [Objectives and Research Questions](report/01-objectives.md) | 1 分析目标与分析问题 | — |
| [Background and Related Methods](report/02-background.md) | 2 相关理论综述 | — |
| [Analysis Design and Evaluation Plan](report/03-analysis-design.md) | 3 分析方案的设计 | [Fig. 1](figures.md#figure-01) |
| [Features and Analytical Methods](report/04-features-and-methods.md) | 4 特征变量的选取与数据分析方法 | [Table 1](tables.md#table-01), [Table 2](tables.md#table-02) |
| [Data Preparation](report/05-data-preparation.md) | 5 数据的整理 | [Table 3](tables.md#table-03) |
| [Exploratory Data Analysis](report/06-exploratory-analysis.md) | 6 数据的探索性分析 | [Fig. 2](figures.md#figure-02), [Fig. 3](figures.md#figure-03), [Fig. 4](figures.md#figure-04), [Fig. 5](figures.md#figure-05), [Fig. 6](figures.md#figure-06), [Fig. 7](figures.md#figure-07), [Table 4](tables.md#table-04) |
| [Model Development and Evaluation](report/07-modeling-and-evaluation.md) | 7 分析模型的构建与评估 | [Fig. 8](figures.md#figure-08), [Fig. 9](figures.md#figure-09), [Fig. 10](figures.md#figure-10), [Table 5](tables.md#table-05), [Table 6](tables.md#table-06), [Table 7](tables.md#table-07) |
| [Findings, Limitations, and Conclusions](report/08-findings-and-conclusions.md) | 8 数据发现与结论 | — |
| [References](report/references.md) | 参考文献 | — |
| [External Resources](report/appendix-a-resources.md) | 附录 A 外部资源清单 | [Table 8](tables.md#table-08) |
| [Source Code Structure](report/appendix-b-source-structure.md) | 附录 B 源码结构 | [Table 9](tables.md#table-09) |

## How to read the results

- Original figures 1 and 8–10 and tables 6–7 describe the historical report workflow; their embedded labels are preserved.
- Figure 10 reports mean per-protein F1; Figure 9 averages label F1 within prevalence groups. These are different aggregations.
- Dev, clean, confirmation-set, and leaderboard scores are kept separate. The report's historical leaderboard offsets are observations from those submissions, not a forecast for other models.
- The original report text is reproduced as source material. Read the current [evaluation protocol](../README.md#evaluation-protocol) and [reproduction notes](../README.md#files-and-reproduction) alongside it, including the candidate-pool selection context, incomplete nested cross-fitting, and missing `gogptq` generation step for `allkbag2`.

## 图表阅读说明

- 图 1、图 8–10 与表 6–7 记录历史报告方案，保留原标注。
- 图 10 为每蛋白平均 F1；图 9 为按标签阳性率分组后的平均标签 F1，统计单位不同。
- dev、clean、确认集与排行榜成绩分别列示，报告中的历史分数差不代表未来模型的固定偏移。
- 章节正文为原报告转录。请同时参阅当前 README 的[评估说明](../README.md#评估方式与结果边界)与[复现说明](../README.md#下载内容与复现)，了解候选池选择、嵌套交叉拟合及 `allkbag2` 新增特征生成步骤的限制。

## Source and extraction

[Original DOCX](https://github.com/Cooljoes/protein-function-prediction-submission/releases/download/v5.0.0/protein_function_prediction_report.docx) · [Figure provenance](../assets/figures/report/manifest.json) · [Table provenance](../data/report-tables/manifest.json)

Figures are byte-identical copies of the embedded PNG files. Tables retain their cell values in Markdown and UTF-8 CSV. The chapter conversion omits the blank cover-page team fields, page breaks, and Word-generated page-number table of contents; links replace page navigation.

图像为内嵌 PNG 的逐字节副本。表格在 Markdown 和 UTF-8 CSV 中保留原始单元格值。章节转换省略封面空白队伍字段、分页符及 Word 自动生成的页码目录，改用 GitHub 链接导航。
