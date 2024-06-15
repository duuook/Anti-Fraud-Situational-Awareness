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
        Fre = []
        Num = []
        keywords = []
        for index, key in enumerate(ans):
            keywords.append(key[0])
            fre = len(key[0]) / len(text)
            # fre = '{:.0%}'.format(fre)
            Fre.append(fre)
            Num.append(int(key[1]))

        Get_keywords_report = {
            'status': 1,
            'Keywords': keywords,
            'Keywords_Num': Num,
            'Keywords_Frequency': Fre,
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
            'error': int(title)
        }
    else:
        probability_arr = []
        for i in probability:
            probability_arr.append('%.3f' % i)
        print(probability_arr)
        Text_predict_report = {
            'status': 1,
            'title': int(title),
            'probability': probability_arr,
        }

    # 返回分析报告
    Analysis_report = {
        'Get_keywords_report': Get_keywords_report,
        'Text_predict_report': Text_predict_report,
    }

    return Analysis_report
