def check_answer(response, ground_truth):
    """
    检查模型生成的答案是否正确。
    :param response: 模型生成的答案（字符串）。
    :param ground_truth: 正确答案（字符串）。
    :return: 布尔值，表示模型答案是否正确。
    """
    # 清理生成的答案和正确答案，比较是否相同
    if response is None or ground_truth is None:
        return False
    return str(response).strip().upper() == str(ground_truth).strip().upper()


def sort_answer(question, correct_answer, gold_choice):
    """
    根据选项将问题和答案重新排序。
    :param question: 原始问题（字符串）。
    :param correct_answer: 正确答案（字符串）。
    :param gold_choice: 用户指定的答案选项（"A", "B", "C", 或 "D"）。
    :return: 重新排序后的问题字符串。
    """
    # 将问题和答案结合，重新排序为指定的 gold_choice
    if gold_choice.upper() == correct_answer.upper():
        return question
    else:
        # 逻辑可根据具体需求改写，例如重新排列答案选项
        return f"{question} (Gold choice: {gold_choice})"
