# 跑通 MINJA toy 实验所需的最少 Python

这不是完整 Python 教程，只覆盖阅读 `code/run_minja_toy.py` 所需内容。

## 1. 变量与基本类型

```python
top_k = 3                         # 整数
query = "Where is Orion?"         # 字符串
tokens = ["where", "orion"]       # 列表：有顺序
record = {"query": query}         # 字典：键值映射
is_poisoned = False               # 布尔值
```

## 2. 循环与条件

```python
for record in records:
    if record.poisoned:
        print(record.query)
```

`for` 逐个处理记录，`if` 只在条件为真时执行缩进代码。

## 3. 函数

```python
def cosine_similarity(left, right):
    return sum(value * right.get(token, 0.0)
               for token, value in left.items())
```

`def` 定义可重复调用的步骤；参数放在括号内；`return` 返回结果。

## 4. 类与数据类

```python
@dataclass(frozen=True)
class MemoryRecord:
    record_id: str
    query: str
    answer: str
```

`MemoryRecord` 把一条记忆的编号、查询和答案放在一起。`record.query` 用来读取字段。

## 5. JSON 与 CSV

- JSON 保存输入记录和场景配置，适合嵌套的列表、字典。
- CSV 保存每轮指标，每行是一轮实验，方便用 Excel 查看。
- 脚本用 `json.load()` 读取 JSON，用 `csv.DictWriter` 写 CSV。

## 6. 路径

```python
root = Path(__file__).resolve().parents[1]
data_path = root / "data" / "minja_toy_records.json"
```

`Path` 用相对于脚本的位置寻找文件，避免依赖当前电脑的绝对路径。

## 7. 虚拟环境与 pip

当前脚本只有标准库依赖，不需要安装包。以后安装真实 Embedding 模型时再使用：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install sentence-transformers
```

不要为了本周演示临时升级全部环境；先保证无依赖版本稳定运行。

## 8. 调试顺序

1. 看终端最后一行错误类型。
2. 检查是否在仓库根目录执行命令。
3. 单独运行 `python code/run_minja_toy.py`。
4. 再运行单元测试。
5. 不理解某个值时，在对应行前后临时加 `print()`，理解后删除。

