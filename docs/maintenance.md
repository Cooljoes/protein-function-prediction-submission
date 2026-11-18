# Maintenance and validation / 维护与验证

Updated: **2026-11-18**.

This guide provides executable checks for downloaded prediction files and a
precise map of the published artifacts. The checker uses only the Python standard
library. It validates the submission contract; model quality requires separate
ground-truth labels and evaluation evidence.

[Project overview](../README.md) · [Analysis report](README.md) ·
[Contributing](../CONTRIBUTING.md) ·
[Validation workflow](../.github/workflows/submission-validation.yml)

## 1. 校验提交文件

环境要求：**Python 3.11+**。从仓库根目录执行，无需安装额外包：

```bash
python3 tools/validate_submission.py /path/to/predictions.csv
python3 tools/validate_submission.py /path/to/predictions.csv --json
```

默认契约如下：

| 检查项 | 要求 |
| --- | --- |
| 编码 | UTF-8，可带 BOM |
| 表头 | `protein_id`，随后依次为 `label_0` 至 `label_499` |
| 数据行数 | 28,450 行，不含表头 |
| 列数 | 每行 501 列 |
| 蛋白质 ID | 非空且唯一 |
| 预测标签 | 每个单元格必须是精确的 `0` 或 `1`；空值、概率和 `0.0` 等表示均不接受 |

工具计算并报告文件原始字节的 SHA-256。文件名相同并不保证内容相同，哈希可用于
识别实际下载的版本。UTF-8 BOM 和换行字节也属于文件内容，会影响哈希。

### 与模板核对

```bash
python3 tools/validate_submission.py /path/to/predictions.csv \
  --template /path/to/submit_template_v1.csv --json
```

模板应采用相同表头，ID 非空且唯一，行数与预期一致。工具逐行核对 ID 顺序。
模板中的标签单元格允许为空，其标签内容不参与预测正确性的判断。未提供模板时，
格式通过只表示内部结构符合要求，不能据此确认 ID 集合就是竞赛要求的测试集。

### 对照 V5 发布文件的哈希

现有 V5 Release 中的独立 CSV 为 `pairgogpt_v2_allkbag2.csv`：

```bash
python3 tools/validate_submission.py /path/to/pairgogpt_v2_allkbag2.csv \
  --expected-sha256 b8c4ebe55c066217a1ffb3fd3b3da99092de729d29534f999e67c128d1519c48 \
  --json
```

哈希来源为 [V5 manifest](https://github.com/Cooljoes/protein-function-prediction-submission/releases/download/v5.0.0/V5_manifest.json)
及 GitHub Release 资产元数据。本轮维护核对了这两处记录，不将元数据读取写成
对该独立 CSV 的再次下载和逐行执行。

### 小规模数据与自动化

工具也支持显式指定其他行数或标签数，便于验证小规模合成样例：

```bash
python3 tools/validate_submission.py /path/to/synthetic.csv \
  --expected-rows 2 --labels 3 --json
```

这种覆盖参数的结果只适用于指定契约。正式 500 标签提交应使用项目默认值。
JSON 报告包括 `valid`、`rows`、`labels`、`sha256`、`error_count` 和 `errors`。
错误明细最多保留 20 条，`error_count` 记录发现的违规总数；同一条记录包含多个
非二元标签时，只记录该行遇到的第一处非二元值。

| 退出码 | 含义 |
| --- | --- |
| `0` | 所请求的格式、模板及哈希检查通过 |
| `1` | 校验失败，可查看错误明细 |
| `2` | 命令参数无效或文件无法读取 |

## 2. 区分两个预测产物

历史分析报告、原源码包和 V5 独立发布文件属于不同的证据来源：

| 产物 | 所在位置 | 本地日志中的 dev / clean（Macro-F1 × 100） |
| --- | --- | --- |
| `pairgogpt_v2_allbag2.csv` | 原源码 ZIP 内的 `release/submission/` | 62.724 / 62.679 |
| `pairgogpt_v2_allkbag2.csv` | V5 Release 独立 CSV 附件 | 62.761 / 62.720 |

对应 SHA-256：

```text
allbag2:
6414a57bdb4a9d1afe9fa225624af538a386b10a48bb30f583da775103781d20

allkbag2:
b8c4ebe55c066217a1ffb3fd3b3da99092de729d29534f999e67c128d1519c48

V5 原源码 ZIP:
2e29c298513d269d40fd1da9efb2d0fa6bc907aad1278736c169bc7808b4b421
```

上述对应关系记录在已发布的 V5 manifest 中。现有 Release 将 64.3818 记录为
所有者于 2026-10-17 确认的 `allkbag2` 排行榜成绩；原报告将其历史 `allbag2`
与 64.38/64.3818 关联。两者的来源说明应同时保留，不能仅凭相同分数推断 CSV
相同，或将某个版本的本地指标移到另一个文件上。

本轮维护没有重新查询排行榜或重算这两组模型指标。完整来源说明见
[V5 Release](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0)
和 [README 的结果历史](../README.md#results-and-development-history)。

## 3. 可复现范围

| 层级 | 当前入口与限制 |
| --- | --- |
| 提交文件结构与完整性 | 本仓库的 [CSV 校验工具](../tools/validate_submission.py)，可直接运行 |
| 校验工具的行为回归 | [标准库测试](../tests/test_validate_submission.py)，使用临时合成 CSV |
| 原始图表与分析说明 | [报告章节](README.md)、[图集](figures.md)、[表格](tables.md)及来源清单 |
| 历史 `allbag2` 训练流程 | V5 源码包中的 README、脚本和日志；完整运行还需要竞赛数据、权重及大型缓存 |
| V5 `allkbag2` 的完整重建 | 原包未包含新增 `gogptq` 特征的完整生成步骤及历史约定，现有材料不足以承诺逐值重现 |

dev、clean、确认集和排行榜是不同的评估来源。原报告的跨层集成并非已经完成
严格的全流程嵌套交叉验证；只凭最终融合阶段的划分，不能证明所有上游特征都与
确认集隔离。引用结果时请沿用[现有评估说明](../README.md#evaluation-protocol)。

## 4. 维护验证记录

新增工具的回归检查命令：

```bash
python3 -m unittest discover -s tests -p 'test_validate_submission.py' -v
git diff --check
```

本轮在 Linux x86_64 / Python 3.12.14 下实际完成了以下检查：

| 检查 | 结果与适用范围 |
| --- | --- |
| 校验器回归用例 | 26 项通过；包括错误表头、行列数、ID、标签值、模板、哈希、BOM、损坏 CSV 和命令行返回码 |
| 原 ZIP 内的历史 `allbag2` | 28,450 行、500 标签，格式通过且 SHA-256 匹配上述 `6414a57b…`；未提供独立测试模板，未验证竞赛 ID 顺序 |
| 两种产物的区分 | 用 V5 `allkbag2` 哈希检查历史 `allbag2` 时，正确返回校验失败（退出码 1） |
| V5 独立 `allkbag2` | 仅核对现有 Release 的文件名、哈希和 manifest；本轮未对其 CSV 本体重新逐行运行 |
| 模型训练、排行榜与模型效果 | 本轮未执行或重新核验 |

GitHub Actions 对工具、测试或工作流变更运行 Python 3.11 / 3.12 的同一组检查。
该工作流只执行校验器的行为测试，使用临时合成数据；不包含模型下载或训练步骤。

实际验证结论应同时注明命令、文件 SHA-256、输入类型和执行环境。校验器测试通过
与 CSV 结构通过分别说明工具行为和文件契约；历史 64.3818 的模型效果仍以其
既有成绩来源为依据。

## 5. 后续维护重点

优先修复能够提供具体输入和回归用例的问题，例如模板行序错位、损坏 CSV、版本
文件混淆或复现说明缺项。新增模型实验应单独记录数据划分、特征生成范围、依赖
版本、完整命令和原始结果，方便后续评审与复查。
