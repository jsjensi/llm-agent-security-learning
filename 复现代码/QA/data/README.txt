本文件包含我们多任务评测所用的 dev、val 和 test 数据。
dev 数据集用于少样本学习，以便为模型提供示例；test 集则是评测问题的来源。
auxiliary_training 数据可用于微调，这对不具备少样本能力的模型尤为重要。这些辅助训练数据来自其他 NLP 多项选择题数据集，例如 MCTest（Richardson et al., 2013）、RACE（Lai et al., 2017）、ARC（Clark et al., 2018, 2016）以及 OBQA（Mihaylov et al., 2018）。
除非另有说明，这些问题均以 2020 年 1 月 1 日的人类知识为参照。在更远的未来，可能有必要在提示中补充说明：该问题是面向 2020 年读者撰写的。

--

如果这项工作对您的研究有帮助，请考虑同时引用本评测以及其所借鉴的 ETHICS 数据集：

@article{hendryckstest2021,
  title={Measuring Massive Multitask Language Understanding},
  author={Dan Hendrycks and Collin Burns and Steven Basart and Andy Zou and Mantas Mazeika and Dawn Song and Jacob Steinhardt},
  journal={Proceedings of the International Conference on Learning Representations (ICLR)},
  year={2021}
}

@article{hendrycks2021ethics,
  title={Aligning AI With Shared Human Values},
  author={Dan Hendrycks and Collin Burns and Steven Basart and Andrew Critch and Jerry Li and Dawn Song and Jacob Steinhardt},
  journal={Proceedings of the International Conference on Learning Representations (ICLR)},
  year={2021}
}
