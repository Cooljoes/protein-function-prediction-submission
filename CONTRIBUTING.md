# Contributing / 参与维护

This repository hosts project documentation, published artifact references, and
small validation tools. The historical training implementation is distributed
in the [V5 source archive](https://github.com/Cooljoes/protein-function-prediction-submission/releases/tag/v5.0.0).
Keep each change focused and identify the exact artifact and evaluation protocol
it affects.

## 开发环境

维护提交校验工具使用 **Python 3.11+**，不需要额外 Python 包、模型权重或 GPU。
在仓库根目录运行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

GitHub Actions 在 Linux 上运行 Python 3.11、3.12，并在 macOS、Windows 上运行
Python 3.12。每个任务都发现 `tests/` 下全部 `test_*.py` 用例，同时检查
[离线合成样例](examples/README.md)。测试使用合成 CSV，不需要竞赛数据或模型接口。

新增测试文件请沿用 `test_*.py` 命名。修改 `tests/` 或 `examples/` 下任意文件都会
触发工作流；不要将测试发现规则缩小到单个文件，否则会遗漏其他模块。

## 修改约定

- 工具处理用户指定的本地文件，默认只输出报告。保持流式 CSV 读取，避免将整份
  预测矩阵加载到内存；ID 去重允许保留 ID 集合。
- 修复格式校验问题时，加入能体现错误输入及预期行为的回归用例，尤其关注标签
  顺序、ID 对齐、重复 ID、非二元值、错误行宽、模板和哈希。
- 保持命令行退出码约定：`0` 为校验通过，`1` 为校验失败，`2` 为参数或文件读取错误。
  改变参数、JSON 字段或退出码时同步更新测试和[维护指南](docs/maintenance.md)。
- 更新结果说明时注明文件名、完整 SHA-256、数据划分、指标标度和结果来源。
  本地 dev/clean、确认集、平台成绩应分别记录。
- 图表或表格变更应同步维护已有来源清单：
  [figure manifest](assets/figures/report/manifest.json) 与
  [table manifest](data/report-tables/manifest.json)。
- 原始数据、模型权重、完整特征缓存和机器路径日志不属于本仓库的日常维护提交。
  训练源码及第三方资源的使用条件以发布包中的说明和许可为准。

## 提交前检查

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tools/validate_submission.py examples/submission.csv --expected-rows 2 --labels 3 --template examples/template.csv --json
git diff --check
git diff --stat
```

在提交说明中写清问题、修改后的行为、实际执行的验证以及未覆盖的范围。
例如，CSV 校验可以证明文件符合提交契约；模型效果仍需对应真值和评估记录。
格式工具维护不应被描述为重新训练或复现历史排行榜成绩。

提交使用与本人 GitHub 账号关联的邮箱。协作者使用自己的身份；不要复制别人的
作者信息。历史 Release 中的文件与成绩来源可从
[V5 manifest](https://github.com/Cooljoes/protein-function-prediction-submission/releases/download/v5.0.0/V5_manifest.json)
追溯。
