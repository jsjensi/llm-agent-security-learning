# MINJA 论文学习入口

对应论文：

*Memory Injection Attacks on LLM Agents via Query-Only Interaction*

## 论文原文

- 英文原文：`../../papers/OriginalText/Dong 等 - Memory Injection Attacks on LLM Agents via Query-Only Interaction.pdf`
- 中文翻译：`../../papers/ChineseTranslation/Dong 等 - Memory Injection Attacks on LLM Agents via Query-Only Interaction.no_watermark.zh-CN.mono.pdf`

## 学习顺序

1. [七天学习计划](../../plans/daily/README.md)
2. [Day 1：摘要与引言](../../journal/2026-09-05-day1.md)
3. [Day 2：相关工作与威胁模型](../../journal/2026-09-06-day2.md)
4. [Day 3：方法总览与桥接步骤](../../journal/2026-09-07-day3.md)
5. [MINJA 一页总结](minja-summary.md)
6. [最小复现所需 Python](python-minimum-for-minja.md)
7. 第 6 天后查看 [toy 参考实现](../../reference/minja-toy/README.md)

## 通用前置知识

- [LLM Agent 系统基础](../llm-agent-system/README.md)
- [记忆、RAG 与 Top-k 检索](../llm-agent-system/03-memory-and-rag.md)

## 当前学习边界

当前目标是理解 MINJA 的威胁模型、桥接步骤、指示提示和渐进缩短，并完成受控的最小机制复现。

直接在代码中插入恶意记录只能验证“恶意记忆影响后续检索和推理”，不能视为完整复现 query-only 注入。完整复现还需要由 Agent 根据攻击查询自主生成并保存目标记录。
