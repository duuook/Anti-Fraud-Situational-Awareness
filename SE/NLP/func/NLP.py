# 示例用法
from SE.NLP.spider.get_txet_and_url import start_crawl, process_file
from SE.NLP.util.LSTM_predict_website import Text_predict


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
        print(cleaned_text)

        # 使用处理的字符串进行预测
        flag, predict, prediction = Text_predict(cleaned_text)
        if flag:
            prediction = []
            if predict:
                print('该网站有可能是诈骗网站')
            print(f'预测结果：\n非诈骗网站的概率：{prediction[0]:.3f}  诈骗网站的概率：{prediction[1]:.3f}')
            prediction.append('prediction[0]:.3f')
            prediction.append('prediction[1]:.3f')
            website_analysis_report = {
                'status': 1,
                'predict': predict,
                'prediction': prediction
            }
        else:
            website_analysis_report = {
                'status': 0,
                'error': predict
            }

        return website_analysis_report
    except Exception as e:
        website_analysis_report = {
            'status': 0,
            'error': "模型分析进程错误",
        }
        return website_analysis_report
