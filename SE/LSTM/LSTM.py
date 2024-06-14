from SE.LSTM.utilspro import Keywords, LSTM_predict

"""服务函数包装"""


def text_analysis(text):
    """
    文本分析
    :param text: 待分析文本
    :return: 关键词、预测结果 (dict)
    """
    # 获取关键词
    size, ans = Keywords.Get_keywords(text)
    if size == 0:
        Get_keywords_report = {
            'status': 0,
            'error': ans,
        }

    elif size > 0:
        Keywords_n_Fre = []
        for index, key in enumerate(ans):
            fre = len(key[0]) / len(text)
            fre = '{:.0%}'.format(fre)
            Keywords_n_Fre.append((key[1], fre))
        Get_keywords_report = {
            'status': 1,
            'Keywords_n_Num': ans,
            'Keywords_n_Fre': Keywords_n_Fre,
        }

    else:
        Get_keywords_report = {
            'status': 0,
            'error': '未知错误',
        }

    # 获取预测结果
    flag, title, probability = LSTM_predict.Text_predict(text)
    if not flag:
        Text_predict_report = {
            'status': 0,
            'error': title,
        }
    else:
        Text_predict_report = {
            'status': 1,
            'title': title,
            'probability': probability,
        }

    # 返回分析报告
    Analysis_report = {
        'Get_keywords_report': Get_keywords_report,
        'Text_predict_report': Text_predict_report,
    }

    return Analysis_report
