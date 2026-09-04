# MINJA 一周每日学习安排

目标不是七天内照抄完整代码，而是能够向老师讲清论文、亲手实现关键模块，并诚实说明最小复现与论文完整实验的差别。

每天采用同一节奏：

1. 阅读指定论文内容。
2. 不看参考答案，先用自己的话回答检查题。
3. 亲手完成一个小练习。
4. 把不理解的问题记录下来。
5. 完成检查后再进入下一天。

## 第 1 天：问题背景与威胁模型

阅读：

- Abstract
- Section 1 Introduction
- Figure 1
- Section 3 Threat Model

必须理解：

- STM 与 LTM 的区别。
- 记忆记录 `(q, Rq)` 如何参与 Top-k 检索和上下文学习。
- victim term、target term、victim query、target reasoning 的含义。
- MINJA 与直接修改记忆库的攻击有什么区别。

亲手产出：

- 用自己的话画出“查询、检索、推理、写回记忆”的流程。
- 回答三个问题：攻击者有什么权限、没有什么权限、依赖系统的什么假设。

验收：不看论文，用两分钟讲清为什么 query-only 条件更现实也更困难。

## 第 2 天：Bridging Steps

阅读：

- Section 4 Method
- Section 4.1 Design Malicious Records with Bridging Steps

必须理解：

- victim 与 target 之间为什么存在 logic gap。
- `b_v,t` 为什么要放在恶意推理的开头。
- bridging steps 为什么必须对多种 victim query 都有效。

亲手产出：

- 为一个完全虚构的例子写出 victim、target、正常查询、目标查询和桥接步骤。
- 判断桥接步骤是否通用、是否显眼、能否诱导错误推理。

验收：能够区分“触发词”“桥接步骤”和“目标推理”。

## 第 3 天：Indication Prompt 与 Progressive Shortening

阅读：

- Section 4.2 Inject Malicious Records via Queries
- Algorithm 1

必须理解：

- indication prompt 如何让 Agent 自主生成目标记录。
- 为什么一次性删除提示通常会失败。
- 渐进缩短如何利用已经写入的恶意示例。
- 为什么最终查询越接近正常查询越容易被检索。

亲手产出：

- 针对第 2 天的虚构例子，写出三轮逐渐缩短的攻击查询。
- 对每轮标注：仍保留了什么、删除了什么、预期检索效果如何。

验收：可以按 Figure 1 从 Q1 讲到 Q3，不混淆“生成成功”和“检索成功”。

## 第 4 天：先写无攻击记忆检索

学习内容：

- Python 列表、字典、函数和循环。
- TF-IDF 或 Embedding 的基本含义。
- 余弦相似度和 Top-k 排序。

亲手编码：

- 创建 10 至 20 条虚构良性记忆。
- 输入一个查询，计算相似度并打印 Top-3。
- 至少测试 5 个正常查询。

约束：先不要看 `reference/minja-toy/` 的实现；遇到错误时只查看 Python 基础笔记。

验收：能逐行解释自己的检索函数，知道每个输入和输出的类型。

## 第 5 天：亲手加入最小记忆注入

亲手编码：

- 复制第 4 天的无攻击实验作为基线。
- 加入一个虚构恶意记录。
- 比较注入前后的 Top-3、排名和最终答案。
- 再实现三轮 progressive shortening 查询。

必须记录：

- 每轮恶意记录相似度。
- 每轮排名以及是否进入 Top-k。
- 注入前答案和注入后答案。

验收：能够解释变化来自检索记录改变，而不是偷偷修改受害查询。

## 第 6 天：实验、指标与论文对照

阅读：

- Section 5 Experimental Settings
- 论文中的 ISR、ASR、UD 定义和主要结果表。

亲手实验：

- 至少使用 3 组虚构 victim-target。
- 增加无注入对照和普通记忆干扰。
- 固定随机种子，保存 CSV 结果。
- 运行失败也要记录，不人为删除不理想结果。

验收：能够解释自己的简化 ISR/ASR 为什么不能与论文的 GPT-4 数值直接比较。

完成自己的版本后，才允许查看：

- `reference/minja-toy/code/`
- `reference/minja-toy/data/`

查看参考答案时只比较设计差异，不整段复制。

## 第 7 天：汇报与模拟考察

准备五分钟讲解：

- 30 秒：研究问题。
- 45 秒：威胁模型。
- 60 秒：bridging steps 与 progressive shortening。
- 90 秒：运行自己写的代码。
- 45 秒：展示指标。
- 30 秒：局限性和下一步。

必须能回答：

1. 为什么 MINJA 是 query-only？
2. 为什么 Agent 自己生成记录比直接写数据库困难？
3. bridging steps 与 progressive shortening 分别解决什么问题？
4. ISR、ASR、UD 分别衡量什么？
5. toy 复现不能证明什么？

最终验收：

- 断网状态下从头运行一次自己的代码。
- 不看笔记讲完整个 Figure 1。
- 请他人随机提问三次。
- 将自己的代码、结果和说明单独提交 Git。

## 学习纪律

- 前三天不看完整参考代码。
- 卡住 20 分钟后先描述问题，再寻求提示，不直接索要答案。
- 每天结束时写三句话：今天学会了什么、仍不理解什么、明天先做什么。
- 所有实验只使用本地虚构数据和自己控制的 toy agent。
