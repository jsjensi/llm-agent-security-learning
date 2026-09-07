import openai
from openai import OpenAI
import time 
class OpenaiEngine:
    def __init__(self, config):
        """
        初始化 OpenAI 引擎。
        :param config: 包含 API 密钥和模型名称的配置字典。
        """
        self.api_key = config["api_key"]
        self.model_name = config["model_name"]

        # 设置 OpenAI 的 API 密钥
        openai.api_key = self.api_key

    def generate(self, prompt, max_tokens=150, temperature=0.7):
        """
        调用 OpenAI API 生成文本。
        :param prompt: 输入提示语。
        :param max_tokens: 最大输出 token 数。
        :param temperature: 温度参数，控制生成的随机性。
        :return: 生成的响应文本。
        """
        retries = 0
        max_retries = 30
        while retries < max_retries:
            try:
                # 调用 OpenAI API 生成响应
                response = openai.Completion.create(
                    model=self.model_name,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                # 提取生成的文本
                text = response.choices[0].text.strip()
                return text
            except Exception as e:
                # 处理异常并重试
                print(f"发生错误：{e}。正在重试 {retries + 1}/{max_retries}...")
                time.sleep(1)
                retries += 1
                if retries == max_retries:
                    print("已达最大重试次数，执行失败。")
                    raise e
