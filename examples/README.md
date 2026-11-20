# Offline examples / 离线使用示例

These tiny synthetic CSVs demonstrate the validator without competition data,
model downloads, or extra packages. Run every command from the repository root.

需要 Python 3.11 或更新版本；只使用标准库。以下文件均为 **2 行、3 个标签的
合成示例**，ID 为演示用名称，不代表真实蛋白质、模型输出或比赛成绩。
完整提交文件的默认要求仍是 28,450 行和 500 个标签。

| 文件 | 用途 |
| --- | --- |
| [submission.csv](submission.csv) | 符合演示契约的二元标签文件 |
| [template.csv](template.csv) | 同一组 ID 及顺序，标签单元格为空的模板 |
| [invalid-submission.csv](invalid-submission.csv) | 第二条记录的 `label_1` 故意使用 `0.5`，演示失败报告 |

## 1. 运行成功示例

在仓库根目录执行；Windows 上如使用 `python` 启动 Python，可将 `python3`
替换为 `python`。命令写在一行，避免不同终端的换行转义差异。

```bash
python3 tools/validate_submission.py examples/submission.csv --expected-rows 2 --labels 3 --template examples/template.csv --json
```

预期退出码为 **0**。JSON 报告中应出现以下字段：

```json
{
  "valid": true,
  "rows": 2,
  "labels": 3,
  "template_rows": 2,
  "id_order_checked": true,
  "error_count": 0,
  "errors": []
}
```

这里展示的是报告节选；完整输出还包含路径、SHA-256 和校验范围等字段。
模板校验检查 ID 是否完全相同且顺序一致，模板的空标签不作为预测值检查。

## 2. 查看格式错误

```bash
python3 tools/validate_submission.py examples/invalid-submission.csv --expected-rows 2 --labels 3 --template examples/template.csv --json
```

该文件故意不合格，预期退出码为 **1**，`valid` 为 `false`，`error_count` 为 `1`。
`errors` 会指出第二条数据记录的 `label_1` 必须为精确的 `0` 或 `1`，当前值为 `0.5`。
工具只报告问题，不会改写输入文件，也不会为概率值自动选择阈值。

## 3. 区分文件读取错误

下面的路径未随仓库提供，用于演示缺失文件：

```bash
python3 tools/validate_submission.py examples/missing.csv --expected-rows 2 --labels 3 --json
```

预期退出码为 **2**，错误信息写入标准错误流（stderr）。此时标准输出（stdout）
不包含 JSON；调用脚本应先检查退出码，再决定是否解析输出。

| 退出码 | 输出与处理方式 |
| --- | --- |
| `0` | 校验通过；使用 `--json` 时，可解析 stdout 中的报告 |
| `1` | 文件内容、模板或哈希校验失败；使用 `--json` 时，stdout 仍为报告，检查 `errors` |
| `2` | 命令参数无效或文件无法读取；查看 stderr，勿把 stdout 当作 JSON |

## 常见问题

| 现象 | 排查方法 |
| --- | --- |
| 小样例提示行数或表头不符 | 补上 `--expected-rows 2 --labels 3`；这些覆盖参数仅适用于演示样例 |
| `protein_id order differs from template` | 核对预测文件与模板的 ID 及逐行顺序；重新导出时保持每个 ID 与自己的预测向量绑定 |
| `SHA-256 mismatch` | 核对文件版本和完整哈希；BOM、换行变化也会改变字节哈希，不能据此直接推断预测内容相同 |
| `not a complete UTF-8 CSV` | 检查编码、引号是否闭合及文件是否截断；保存为完整 UTF-8 CSV 后重新校验 |
| 退出码 `2` 或找不到文件 | 确认当前目录为仓库根目录、路径正确且文件可读；带空格的路径需加引号 |
| 格式通过，但还不知道模型效果 | 文件契约不包含准确率评估；需要对应真值和完整评估协议 |

正式预测文件的哈希、默认契约和历史产物来源见[维护与验证指南](../docs/maintenance.md)。
后续修改与测试命令见[贡献说明](../CONTRIBUTING.md)。
