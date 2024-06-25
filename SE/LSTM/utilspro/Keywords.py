import re
from collections import Counter

import jieba
import jieba.analyse
import pandas as pd


def Clean_text(text):
    """
    去掉文本中的标点符号、制表符和换行符，但保留中文字符、字母数字字符
    :param text: 输入文本
    :return: 干净文本
    """
    cleaned_text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)  # 保留中文字符、字母、数字和空格
    cleaned_text = re.sub(r'[\t\n\r]', '', cleaned_text)  # 移除制表符、换行符和回车符
    cleaned_text = re.sub(r'\s+', '', cleaned_text)  # 去掉所有空格

    return cleaned_text


def Drop_stopwords(contents):
    """
    清除停用词
    :param contents: 待处理的词列表
    :return: 清除停用词后的词列表
    """

    # 读取停用词表
    stopwords = pd.read_csv('LSTM_data/Stopwords.csv')

    # 将停用词表转换为列表
    stopwords = stopwords['Stopwords'].tolist()

    # 初始化一个空列表，用于存储清除停用词后的词
    content_clean = []

    for word in contents:
        # 如果词在停用词列表中，则跳过该词
        if word in stopwords:
            continue
        # 如果词中包含'的'或'x'，则跳过该词
        if word.find('的') != -1 or word.find('x') != -1:
            continue
        # 将不在停用词列表中且不包含'的'或'x'的词添加到content_clean列表中
        content_clean.append(word)

    return content_clean


def Get_keywords(text):
    """
    关键词分析、获取关键词
    :param text: 内容
    :return:   1. 文本有意义：词总数，关键词列表（关键词，词频）
               2. 文本无意义：0，提示信息
    """
    # 清洗文本
    text = Clean_text(text)
    # 使用jieba分词器进行分词
    text = jieba.lcut(text)
    # 清除停用词
    text = Drop_stopwords(text)
    if len(text) == 0:
        warning = "输入文本无效，请提供有意义的数据！"
        return 0, warning

    # 统计词频
    word_counts = Counter(text)

    # 将词频排序
    sorted_word_counts = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

    return len(text), sorted_word_counts
