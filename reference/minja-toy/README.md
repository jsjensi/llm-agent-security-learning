# MINJA Toy 参考答案

这里保存此前生成的 CPU 离线最小复现，只作为第 6 天之后的对照材料。

学习期间请遵守：

1. 前三天不要阅读这里的代码。
2. 第 4、5 天先完成自己的版本。
3. 第 6 天再比较数据结构、检索实现、指标和实验记录方式。
4. 不要把参考答案的 1.00 指标当作论文完整实验结果。

参考实现使用纯 Python TF-IDF 和确定性 toy agent。由于没有真实 LLM，桥接推理生成由测试夹具模拟，只验证记忆写入、Top-k 检索和输出受影响的后半段链路。

运行方式：

```powershell
python reference/minja-toy/code/run_minja_toy.py
python -m unittest discover -s reference/minja-toy/code -p "test_*.py" -v
```
