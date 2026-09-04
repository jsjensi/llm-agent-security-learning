# MINJA CPU 最小复现

## 复现目标

本实验复现 MINJA 的最小检索链路：历史交互被写入记忆库，受害查询检索出恶意记录，确定性 toy agent 因 Top-1 记录而改变答案。

它不复现 GPT-4/GPT-4o 的推理生成过程，也不使用 WebShop、MIMIC-III、eICU 或 MMLU，因此不能把本实验的指标与论文数值直接比较。

## 环境

- Python 3.10 或更高版本（已在 Python 3.13 上验证）
- 无第三方 Python 依赖
- 普通 CPU，运行时间通常少于 1 秒

## 一键运行

在仓库根目录执行：

```powershell
python code/run_minja_toy.py
```

预期摘要：

```text
Mean baseline accuracy: 1.00
Mean simplified ISR: 1.00
Mean simplified ASR: 1.00
Mean utility retention: 1.00
```

运行回归测试：

```powershell
python -m unittest discover -s code -p "test_*.py" -v
```

也可以在 PyCharm 中打开 `minja_minimal_demo.ipynb`，按顺序运行单元格。若本机没有 Notebook 支持，直接运行脚本即可，实验内容相同。

## 输入与输出

- 输入：`../data/minja_toy_records.json`
- 逐轮指标：`../data/results/minja_metrics.csv`
- 汇总：`../data/results/summary.json`
- 攻击链路图：`../assets/minja_pipeline.png`（另保留可编辑 SVG）
- 渐进缩短结果图：`../assets/minja_metrics.svg`

脚本参数：

```powershell
python code/run_minja_toy.py --top-k 3 --seed 42
```

`--data` 可指定另一份同结构 JSON，`--output-dir` 可指定结果目录。

## 代码阅读顺序

1. `tokenize()`：把文本切成词。
2. `tfidf_vectors()`：生成透明、可解释的 TF-IDF 稀疏向量。
3. `TfidfMemory.search()`：用余弦相似度完成 Top-k 检索。
4. `ToyAgent.answer()`：采用 Top-1 记忆的答案。
5. `run_experiment()`：依次运行基线、三轮注入、ISR/ASR 和正常效用对照。

## 指标定义

- 基线准确率：注入前 Top-1 是否是场景指定的正确记录。
- 简化 ISR：最后写入的恶意记录是否进入 Top-k。
- 简化 ASR：恶意记录是否排名 Top-1 并被 toy agent 采用。
- 正常效用保持率：注入前后，无关查询的 Top-1 记录保持不变的比例。

## 方法限制

论文中的攻击者只提交查询，真实 LLM 根据 indication prompt、bridging steps 和已有恶意示例生成新记录。本实验没有可用 LLM，`store_simulated_interaction()` 使用确定性测试夹具提供“模拟 LLM 轨迹”，只隔离验证记忆写入与检索部分。

此外，TF-IDF 是 `all-MiniLM-L6-v2` 的离线降级方案，只能表示词面重叠，不能代表真实语义向量。三个场景均为教学用合成数据，1.00 的结果只说明测试夹具按预期工作，不说明真实系统攻击成功率为 100%。

