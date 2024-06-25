from SE.LSTM.history_search import history_append
from SE.LSTM.utilspro import Keywords, LSTM_predict, LSTM_predict_Email, LSTM_predict_PhoneNumber, spider
from SE import models

"""服务函数包装"""


# 文本分析
def text_analysis(text):
    """
    文本分析
    :param text: 待分析文本
    :return: 关键词、预测结果 (dict)
    """
    try:
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

        # 文本分析的历史记录追加到表中
        history_append(stype='text_analysis', text=text, Analysis_report=Analysis_report)

        return Analysis_report

    except Exception as e:
        Analysis_report = {
            'status': 0,
            'error': "诈骗信息库中未找到相应记录",
        }
        return Analysis_report


# 电话号码库查询
def phonenumber_query(text):
    """
    :param text: 待查询电话号码
    :return: 查询结果 (dict)
    """
    try:
        # 可能会引发异常的代码
        # 查询数据库中是否有电话号码与输入的电话号码相同
        # （这里用get获得的类型是可以直接用phone_number.id这样的方式直接获取字段）
        phone_number = models.phone_number.objects.get(电话号码=text)
        # 如果没有，则返回相应提示信息
        if not phone_number:
            phonenumber_query_result = {
                'status': 1,
                'error': "信息库中无对应信息"
            }
        # 如果有，则返回数据库表中对应的那一行
        else:
            phonenumber_query_result = {
                'status': 1,
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
        Query_report = {
            'phonenumber_query_result': {'status': 0,
                                         'error': "诈骗信息库中未找到相应记录", }
        }
        return Query_report


# 电话号码归属地查询
def phone_number_location(text):
    """
    电话号码归属地查询
    :param text: 待查询电话号码
    :return: 查询结果 (dict)
            'data': {'phone': '15728484768', 'province': '广东', 'city': '河源', 'isp': '中国移动', 'areacode': '0762'}}
    """
    try:
        # 可能会引发异常的代码
        # 通过网页自动脚本查询电话号码归属地
        location_result = spider.phone_number_spider(phone=text)
        if location_result['code'] == 0:
            Query_report = {
                'status': 0,
                'error': "归属地查询失败"
            }

            # 电话号码查询的历史记录追加到表中
            history_append(stype='phone', text=text, Analysis_report=Query_report)

            return Query_report
        print(location_result)
        Query_report = {
            'status': 1,
            '省份': location_result['province'],
            '城市': location_result['city'],
            '运营商': location_result['isp'],
            '区号': location_result['areacode'],
        }
        print(Query_report)

        # 电话号码查询的历史记录追加到表中
        history_append(stype='phone', text=text, Analysis_report=Query_report)

        return Query_report
    except Exception as e:
        print("An error occurred:", e)
        Query_report = {
            'status': 0,
            'error': "归属地查询失败"
        }
        return Query_report


# 电子邮箱库查询
def emails_query(text):
    """
    :param text: 待查询电子邮箱地址
    :return: 查询结果 (dict)
    """
    try:
        # 可能会引发异常的代码
        # 查询数据库中是否有电子邮箱地址与输入的电子邮箱地址相同
        # （这里用get获得的类型是可以直接用emails.id这样的方式直接获取字段）
        emails = models.email.objects.get(电子邮箱地址=text)
        # 如果没有，则返回相应提示信息
        if not emails:
            emails_query_result = {
                'status': 1,
                'error': "信息库中无对应信息"
            }
        # 如果有，则返回数据库表中对应的那一行
        else:
            emails_query_result = {
                'status': 1,
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
        Query_report = {
            'emails_query_result': {'status': 0,
                                    'error': "诈骗信息库中未找到相应记录", }
        }
        return Query_report


# IP地址库查询
def ip_query(text):
    """
    :param text: 待查询IP地址
    :return: 查询结果 (dict)
    """
    try:
        # 可能会引发异常的代码
        # 查询数据库中是否有IP地址与输入的IP地址相同
        # （这里用get获得的类型是可以直接用ip.id这样的方式直接获取字段）
        ip = models.website.objects.get(网站域名=text)
        # 如果没有，则返回相应提示信息
        if not ip:
            ip_query_result = {
                'status': 1,
                'error': "信息库中无对应信息"
            }
        # 如果有，则返回数据库表中对应的那一行
        else:
            ip_query_result = {
                'status': 1,
                'id': ip.id,
                'IP地址': ip.IP地址
            }
        # 将上面的结果归纳为一个查询报告
        Query_report = {
            'ip_query_result': ip_query_result
        }
        # 返回该查询报告，字典格式
        return Query_report

    except Exception as e:
        # 捕获所有异常，并在这里处理
        print("An error occurred:", e)
        Query_report = {
            'ip_query_result': {'status': 0,
                                'error': "诈骗信息库中未找到相应记录", }
        }
        return Query_report


# 预测电话号码是否为诈骗电话号码
def phone_number_predict(text):
    """
    预测电话号码是否为诈骗电话号码
    :param text: 预测电话号码
    :return: 1. 预测成功：True，预测标签，预测概率
             2. 电话号码无意义：False，提示信息，0
             3. 未知错误：0，错误信息
    """
    try:
        flag, label, probability = LSTM_predict_PhoneNumber.PhoneNumber_predict(text)
        if not flag:
            Phone_number_predict_report = {
                'status': 0,
                'error': label
            }
            return Phone_number_predict_report
        else:
            probability_arr = []
            for i in probability:
                probability_arr.append('%.3f' % i)
            print(probability_arr)
            Phone_number_predict_report = {
                'status': 1,
                'label': int(label),
                'probability': probability_arr,
            }
            return Phone_number_predict_report
    except Exception as e:
        Phone_number_predict_report = {
            'status': 0,
            'error': "诈骗信息库中未找到相应记录"
        }
        return Phone_number_predict_report


# 预测电子邮箱是否为诈骗电子邮箱
def email_predict(text):
    """
    预测电子邮箱是否为诈骗电子邮箱
    :param text: 预测电子邮箱
    :return: 1. 预测成功：True，预测标签，预测概率
             2. 电子邮箱无意义：False，提示信息，0
             3. 未知错误：0，错误信息
    """
    try:
        flag, label, probability = LSTM_predict_Email.Email_predict(text)
        if not flag:
            Email_predict_report = {
                'status': 0,
                'error': label
            }
            return Email_predict_report
        else:
            probability_arr = []
            for i in probability:
                probability_arr.append('%.3f' % i)
            print(probability_arr)
            Email_predict_report = {
                'status': 1,
                'label': int(label),
                'probability': probability_arr,
            }
            return Email_predict_report
    except Exception as e:
        Email_predict_report = {
            'status': 0,
            'error': "诈骗信息库中未找到相应记录"
        }
        return Email_predict_report
