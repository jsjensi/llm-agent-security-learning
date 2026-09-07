# 学习笔记分类

本目录按照“论文专属内容”和“跨论文通用基础”分类。

## 按论文分类

### MINJA

目录：[`minja/`](minja/)

对应论文：

*Memory Injection Attacks on LLM Agents via Query-Only Interaction*

当前内容包括论文摘要、逐节精读、威胁模型、最小复现所需 Python，以及 toy 实验入口。

### 自进化 LLM Agent 安全

目录：[`lin-self-evolving-agent-safety/`](lin-self-evolving-agent-safety/)

对应论文：

*Safety in Self-Evolving LLM Agent Systems: Threats, Amplification, and Case Studies*

目前已建立入口，独立精读笔记尚未开始。

## 通用基础

目录：[`llm-agent-system/`](llm-agent-system/)

这里保存两篇论文都可能用到的知识，例如：

- LLM 与 LLM Agent 的区别；
- Agent 系统架构；
- 短期记忆与长期记忆；
- Embedding、RAG 与 Top-k 检索；
- 工具调用和任务规划。

## 分类原则

- 只服务于一篇论文的内容，放入对应论文目录。
- 两篇论文都会使用的概念，放入 `llm-agent-system/`。
- 每日学习过程仍保存在 `journal/`，再由论文目录建立链接。
- 可运行参考实现仍保存在 `reference/`，避免移动后破坏命令和数据路径。
