from SE.LSTM.utilspro import Keywords, LSTM_predict
from SE import models

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
            'error': title
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


# 电话号码查询
def phonenumber_query(text):
    try:
        # 可能会引发异常的代码
        # 查询数据库中是否有电话号码与输入的电话号码相同
        # （这里用get获得的类型是可以直接用phone_number.id这样的方式直接获取字段）
        phone_number = models.phone_number.objects.get(电话号码=text)
        # 如果没有，则返回相应提示信息
        if not phone_number:
            phonenumber_query_result = {
                'error': "信息库中无对应信息"
            }
        # 如果有，则返回数据库表中对应的那一行
        else:
            phonenumber_query_result = {
                'id': phone_number.id,
                '电话号码': phone_number.电话号码,
                '电话类型': phone_number.电话类型,
                '标记次数': phone_number.标记次数
            }
        # 将上面的结果归纳为一个查询报告
        Query_report = {
            'phonenumber_query_result': phonenumber_query_result
        }
        # 返回该查询报告，字典格式
        return Query_report

    except Exception as e:
        # 捕获所有异常，并在这里处理
        print("An error occurred:", e)


# 电子邮箱查询
def emails_query(text):
    try:
        # 可能会引发异常的代码
        # 查询数据库中是否有电子邮箱地址与输入的电子邮箱地址相同
        # （这里用get获得的类型是可以直接用emails.id这样的方式直接获取字段）
        emails = models.phone_number.objects.get(电子邮箱地址=text)
        # 如果没有，则返回相应提示信息
        if not emails:
            emails_query_result = {
                'error': "信息库中无对应信息"
            }
        # 如果有，则返回数据库表中对应的那一行
        else:
            emails_query_result = {
                'id': emails.id,
                '电子邮箱地址': emails.电子邮箱地址
            }
        # 将上面的结果归纳为一个查询报告
        Query_report = {
            'emails_query_result': emails_query_result
        }
        # 返回该查询报告，字典格式
        return Query_report

    except Exception as e:
        # 捕获所有异常，并在这里处理
        print("An error occurred:", e)
