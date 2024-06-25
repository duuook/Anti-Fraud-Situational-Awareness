import random
from SE import models
from datetime import datetime
import pytz

from SE.LSTM import LSTM


# 历史查询/分析表（向数据库的表中增加查询/分析记录）
def history_append(stype,text,Analysis_report):
    try:
        # 设置时区为北京时间
        tz = pytz.timezone('Asia/Shanghai')
        # 获取当前时间并转换为北京时间
        beijing_time = datetime.now(tz)
        # 将整型的北京时间转换为字符串并进行去除杠号、空格和冒号的处理,并只截取到秒的部分，毫秒和时区都不需要
        beijing_time = str(beijing_time).replace("-","").replace(" ","").replace(":","")[0:14]

        # 生成一个0-1000的随机整数
        rand_int = random.randint(1, 999)

        # 往历史分析表中添加记录，分四种类型情况讨论
        if stype=='text_analysis':
            if Analysis_report['Text_predict_report']['status'] and Analysis_report['Get_keywords_report']['status']:
                models.history.objects.create(
                    时间戳id=f"{beijing_time}{rand_int:03d}",  # 时间戳id：北京时间+随机数
                    查询类型=stype,  # 将views.py中的stype当作参数传入进来判断查询/分析的类型
                    查询内容=text,
                    预测标签=Analysis_report['Text_predict_report']['title'],
                    预测概率=Analysis_report['Text_predict_report']['probability'][1],
                    文本长度=len(text),
                    关键词=str(Analysis_report['Get_keywords_report']['Keywords']),
                    关键词词数=str(Analysis_report['Get_keywords_report']['Keywords_Num'])
                )
            else:
                models.history.objects.create(
                    时间戳id=f"{beijing_time}{rand_int:03d}",  # 时间戳id：北京时间+随机数
                    查询类型=stype,  # 将views.py中的stype当作参数传入进来判断查询/分析的类型
                    查询内容=text
                )

        elif stype=='phone':
            models.history.objects.create(
                时间戳id=f"{beijing_time}{rand_int:03d}",  # 时间戳id：北京时间+随机数
                查询类型=stype,  # 将views.py中的stype当作参数传入进来判断查询/分析的类型
                查询内容=text
            )
        elif stype=='ip':
            models.history.objects.create(
                时间戳id=f"{beijing_time}{rand_int:03d}",  # 时间戳id：北京时间+随机数
                查询类型=stype,  # 将views.py中的stype当作参数传入进来判断查询/分析的类型
                查询内容=text
            )
        elif stype=='email':
            models.history.objects.create(
                时间戳id=f"{beijing_time}{rand_int:03d}",  # 时间戳id：北京时间+随机数
                查询类型=stype,  # 将views.py中的stype当作参数传入进来判断查询/分析的类型
                查询内容=text
            )

    except Exception as e:
        print("An error occurred:", e)


# 历史查询/分析表（用于显示查询/分析记录）
def history_query():  # 查询整表不需要参数
    try:
        # 因为是历史分析，所以在未采用筛选的情况下，数据库中的历史分析记录全部显示
        # 这里all()获取到的类型是列表类型
        history=models.history.objects.all()

        history_query_result = {
            'status': 1,
            # 这里后续需要用循环的形式取列表里的内容
            # 如for query in history_query:
            #     print(query.时间戳id,query.查询类型,query.查询内容………………)
            '整表记录的列表':history
        }

        Query_report = {
            'history_query_result': history_query_result
        }

        return Query_report

    except Exception as e:
        print("An error occurred:", e)
        Query_report = {
            'phonenumber_query_result': {'status': 0,
                                         'error': "历史查询/分析存在异常", }
        }
        return Query_report