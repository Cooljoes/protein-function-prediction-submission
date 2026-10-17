# External Resources

[Report guide](../README.md) · [Figures](../figures.md) · [Tables](../tables.md)

This appendix lists the pretrained models and third-party code used in the reported workflow, together with their stated sources, licenses, and roles. The source archive's MODELS.md provides the corresponding resource details and checksums.

Original report section: **附录 A 外部资源清单**. [Download the source DOCX](https://github.com/Cooljoes/protein-function-prediction-submission/releases/download/v5.0.0/protein_function_prediction_report.docx).

## 附录 A 外部资源清单

训练、评估与预测只使用竞赛提供的数据；未引入任何额外数据集，未用序列查询外部数据库或在线服务。使用的公开预训练权重与第三方代码如下（均来自公开仓库，以模型权重或代码形式使用，下载后校验 SHA256，详见源码包 MODELS.md）。

**表 8  公开预训练权重与第三方代码**

| 资源 | 来源 | 许可 | 用途 |
| --- | --- | --- | --- |
| ESM2-650M | facebook/esm2_t33_650M_UR50D | MIT | 通用蛋白质语言模型嵌入 |
| ESM2-3B（前 30 层） | facebook/esm2_t36_3B_UR50D | MIT | GO-GPT v1 的蛋白编码器 |
| GO-GPT v1 | wanglab/gogpt | Apache-2.0 | 生成式 GO 术语打分 |
| ProteInfer ×4 | samirchar/proteinfertorch-{go,ec}-{random,clustered} | Apache-2.0 | GO / EC logit 与嵌入 |
| GO-GPT 模型结构代码 | github.com/bowang-lab/BioReason-Pro（单个文件） | MIT | 加载 GO-GPT 解码器 |
| MMseqs2 | github.com/soedinglab/MMseqs2 | GPL-3.0 | 训练集内部同源检索 |

[CSV 下载 / Download CSV](../../data/report-tables/table-08-external-resources.csv)

[← References](references.md) · [Source Code Structure →](appendix-b-source-structure.md)
