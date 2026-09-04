# MINJA 五分钟汇报与现场演示

## 0:00–0:30 问题背景

“带长期记忆的 Agent 会保存过去的查询和推理，并把相似记录作为后续任务的示例。MINJA 说明攻击者不需要直接修改数据库，只通过普通查询也可能诱导 Agent 自己写入恶意记录。”

## 0:30–1:15 威胁模型

展示 `assets/minja_pipeline.svg`，说明：

1. 攻击者只有 query-only 权限。
2. Agent 会把交互写入长期记忆。
3. 新查询用相似度检索 Top-k 记忆。
4. 恶意记录被检索后会作为错误示例影响输出。

强调实验只使用本地虚构数据，不连接第三方系统。

## 1:15–2:15 论文方法

“Bridging steps 负责把 victim 与 target 连接成一段看似连贯的推理。Indication prompt 先明确指导 Agent 生成这段推理。Progressive shortening 再逐轮删除明显提示，依靠已写入的恶意记录维持目标轨迹，使最后记录更像正常 victim query，更容易进入 Top-k。”

本实验把“LLM 生成轨迹”替换为确定性测试夹具，因为当前只有 CPU、无模型 API。复现重点是可独立验证的记忆写入、相似检索和输出改变。

## 2:15–3:45 现场运行

在仓库根目录执行：

```powershell
python code/run_minja_toy.py
```

然后打开：

- `data/results/summary.json`：对比每个场景的基线答案和注入后答案。
- `data/results/minja_metrics.csv`：查看每轮恶意记录相似度、排名和 Top-k 命中。
- `assets/minja_metrics.svg`：展示最终缩短记录相似度上升。

解释四个汇总值：

- Baseline accuracy = 1.00：注入前能检索到正确记录。
- Simplified ISR = 1.00：最终恶意记录进入 Top-k。
- Simplified ASR = 1.00：最终恶意记录排名 Top-1，输出转向 target。
- Utility retention = 1.00：五个无关查询的 Top-1 没有变化。

## 3:45–4:30 结果解释

“三个虚构场景中，最后一轮记录与 victim query 词面最接近，因此排名 Top-1。结果说明：只要恶意记录能够被写入，检索增强记忆就可能把它放大为后续行为。但 1.00 是合成测试结果，不是论文真实攻击率。”

## 4:30–5:00 局限与下一步

当前限制：

1. TF-IDF 只表示词面重叠，不是语义 Embedding。
2. 没有真实 LLM，所以没有验证它能否仅凭查询自主生成桥接步骤。
3. 数据规模小，简化 ISR/ASR 与论文指标不可直接比较。

下一步依次是：接入 `all-MiniLM-L6-v2`；获得 API 后替换测试夹具；最后对照官方 QA Agent 代码，在 MMLU 子集上运行。

## 老师可能追问

### 为什么叫 query-only？

论文攻击者不直接写数据库，只发查询。Agent 按自身记忆策略保存交互。本 toy 实验模拟了这个接口和后半段链路，但生成轨迹由夹具代替，所以必须称“最小机制复现”，不能称完整 query-only 攻击复现。

### Bridging steps 与 progressive shortening 有什么区别？

Bridging steps 解决 victim 如何在推理上转向 target；progressive shortening 解决如何逐步去掉显眼指令，同时让最终记录更接近受害查询并容易被检索。

### 为什么不直接跑官方代码？

官方实验包含 GPT-4/GPT-4o、复杂 Agent 和 WebShop、医疗数据库或 MMLU 等数据。在 CPU、无 API、一周且 Python 零基础的条件下，先隔离复现核心机制更可验证，也更容易诚实说明偏差。

### ISR、ASR、UD 分别是什么？

ISR 衡量恶意记录是否成功注入；ASR 衡量受害查询是否产生攻击目标行为；UD 衡量攻击对正常任务效用的损害。本实验用 Top-k 命中、Top-1 恶意记录和无关查询 Top-1 保持率近似它们。

### 你的实验能证明真实 Agent 可被攻击吗？

不能单独证明。它证明检索层存在必要的传播链路：一旦恶意记录被写入且相似度足够高，后续输出会受影响。真实可攻击性还取决于 LLM 是否生成并保存恶意轨迹、记忆过滤策略和提示结构。
