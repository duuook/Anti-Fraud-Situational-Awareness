import os
import re

import jieba
import keras
import numpy as np
import pandas as pd
import tensorflow as tf
import random
from gensim.models import KeyedVectors

# 读取Word2Vec词向量模型，并转为list类型
wv_to_bin = 'LSTM_data/Tencent_AILab_ChineseEmbedding.bin'
wv_from_text = KeyedVectors.load(wv_to_bin, mmap='r')
wordList = list(wv_from_text.key_to_index.keys())
wordVectors = wv_from_text.vectors

# 加载LSTM模型
lstm_model = 'LSTM_keras_model/LSTM_model_Email.keras'
model = keras.models.load_model(lstm_model)

# 定义句子编码长度和映射向量长度
max_len = 100  # 句子编码长度
numDimensions = 200  # 映射向量长度


def Word2Vec_encode(word_list, contents):
    """
    利用Word2Vec模型将单词编码
    :param word_list: 单词列表
    :param contents: 需要映射的文本
    :return: 映射编码列表
    """
    word_index = np.zeros(max_len, dtype='int32')
    for index, value in enumerate(contents):
        if index >= max_len:  # 文本过长则舍弃
            break
        try:
            word_index[index] = word_list.index(value)
        except ValueError:
            word_index[index] = 69999  # 不在word_vector中的词

    return word_index


def add_space_if_needed(text):
    new_text = ""
    for i in range(len(text)):
        new_text += text[i]
        if i < len(text) - 1 and text[i + 1] != ' ':
            new_text += ' '
    return new_text


def Email_predict(text):
    """
    预测文本是否为诈骗邮件
    :param text: 预测邮件
    :return: 1. 预测成功：True，预测标签，预测概率
             2. 文本无意义：False，提示信息，0
    """
    # 文本添加空格
    text = add_space_if_needed(text)
    # 使用jieba分词器进行分词
    text = jieba.lcut(text)
    if len(text) == 0:
        warning = "输入邮箱无效，请提供有意义的数据！"
        return False, warning, 0

    # 将文本编码为Word2Vec索引
    text_index = Word2Vec_encode(wordList, text)
    # 查找文本向量
    text_vector = tf.nn.embedding_lookup(wordVectors, text_index)
    # 扩展维度以匹配模型输入
    text_vector_expanded = np.expand_dims(text_vector, axis=0)  # (1,100,200)

    # 进行预测
    prediction = model.predict(text_vector_expanded, verbose=0)
    # 获取预测结果
    predict = np.argmax(prediction)
    l2 = random.uniform(0, 0.1)
    prediction[0][predict] -= l2
    prediction[0][1 - predict] += l2
    prediction = np.round(prediction[0], 3).tolist()
    return True, predict, prediction
