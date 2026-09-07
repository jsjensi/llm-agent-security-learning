class OpenaiConfig:
    def __init__(self, model_name="gpt-3.5-turbo"):
        # 初始化 OpenAI 配置
        self.api_key = "your_api_key"  # 替换为你的实际 OpenAI API 密钥
        self.model_name = model_name

    def __getitem__(self, item):
        # 支持通过字典访问配置
        return getattr(self, item)


# class Config:
#     def __init__(self):
#         # 初始化全局设置
#         self.data_path = "/egr/research-dselab/dongshe1/MMLU/data/data/test/high_school_chemistry_test.csv"
#         self.gold = "default"  # 答案选项（"default", "A", "B", "C", or "D"）
#         self.n_shots = 0  # Few-shot 示例数量，默认为 0（zero-shot）
#         self.cot = False  # 是否启用推理链（Chain of Thought）
#         self.mem_size = 1000  # 最大记忆数据大小
#         self.seed = 42  # 随机种子
