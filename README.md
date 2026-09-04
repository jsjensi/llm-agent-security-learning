# 大语言模型智能体安全

本目录用于整理大语言模型智能体安全相关论文，以及阅读、复现过程中积累的知识和实验资料。

## 目录说明

- `papers/`：论文原文。
- `plans/`：学习路线与阶段性规划。
- `notes/`：论文摘要、核心知识点和阅读笔记。
- `questions/`：阅读与复现过程中遇到的问题、假设和待验证事项。
- `code/`：论文复现代码、实验脚本和 Notebook。
- `data/`：实验输入、数据集、运行结果和日志。
- `assets/`：论文插图、流程图、截图及其他静态资源。

## 当前论文

1. *Memory Injection Attacks on LLM Agents via Query-Only Interaction*
2. *Safety in Self-Evolving LLM Agent Systems: Threats, Amplification, and Case Studies*

## 一周复现成果

已完成一个普通 CPU 可离线运行的 MINJA 最小机制实验：

- 运行说明：`code/README.md`
- 现场演示：`code/minja_minimal_demo.ipynb`
- 可重复脚本：`code/run_minja_toy.py`
- 合成输入：`data/minja_toy_records.json`
- 实验结果：`data/results/`
- 一页论文笔记：`notes/minja-summary.md`
- 五分钟汇报稿：`notes/minja-demo-script.md`

快速运行：

```powershell
python code/run_minja_toy.py
python -m unittest discover -s code -p "test_*.py" -v
```

该实验只复现记忆写入、Top-k 检索与输出受影响的链路。由于没有真实 LLM，桥接推理生成由测试夹具模拟，不能将结果当作论文完整复现。

## 整理建议

- 笔记、问题、代码和数据文件使用论文简称作为前缀，方便关联检索。
- 原始论文只保存在 `papers/`，避免产生重复副本。
- 大体积数据和模型文件应记录来源、版本及生成方式。
- 实验结果应注明运行环境、参数、随机种子和对应代码版本。

