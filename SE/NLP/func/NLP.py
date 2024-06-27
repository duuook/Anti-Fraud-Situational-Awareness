# 示例用法
from SE.NLP.spider.get_txet_and_url import start_crawl, process_file
from SE.NLP.util.LSTM_predict_website import Text_predict
from SE.LSTM.utilspro import Keywords, LSTM_predict


def websit_analysis(url):
    """
    :param url: 预测网站
    :return: website_analysis_report(dict)
            1. 预测成功：status=1，预测标签，预测概率
            2. 预测失败：status=0，提示信息
    """
    try:
        # start_url = "https://www.processon.com/diagrams"
        start_url = url

        output_file = 'website_texts.txt'
        start_crawl(start_url, output_file)
        # 将爬取到的网站文本转变为字符串进行预测
        # 示例用法
        cleaned_text = process_file(output_file)

        # ---------------------------网页预测-------------------------------------
        # 使用处理的字符串进行预测
        flag, predict, prediction = Text_predict(cleaned_text)
        if flag:
            sub_prediction = []
            if predict:
                print('该网站有可能是诈骗网站')
            print(f'预测结果：\n非诈骗网站的概率：{prediction[0]:.3f}  诈骗网站的概率：{prediction[1]:.3f}')
            sub_prediction.append(f'{prediction[0]:.3f}')
            sub_prediction.append(f'{prediction[1]:.3f}')
            website_predict_report = {
                'status': 1,
                'predict': int(predict),
                'prediction': sub_prediction
            }
        else:
            website_predict_report = {
                'status': 0,
                'error': predict
            }

        # ---------------------------网页关键词提取-------------------------------------
        # 获取关键词
        size, ans = Keywords.Get_keywords(cleaned_text)
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
                fre = len(key[0]) / len(cleaned_text)
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

        website_analysis_report = {
            'status': 1,
            'website_predict_report': website_predict_report,
            'Get_keywords_report': Get_keywords_report,
        }

        # print(website_analysis_report)
        return website_analysis_report
    except Exception as e:
        website_analysis_report = {
            'status': 0,
            'error': "模型分析进程错误",
            'detail': e
        }
        return website_analysis_report
