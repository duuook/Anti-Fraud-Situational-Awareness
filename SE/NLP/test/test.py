# 示例用法
from spider.get_txet_and_url import start_crawl, process_file
from util.LSTM_predict_website import Text_predict

# 在此输入预测网站
# start_url = "https://www.processon.com/diagrams"
start_url = "https://blog.csdn.net/u010244992/article/details/105039778"

output_file = 'website_texts.txt'
start_crawl(start_url, output_file)
# 将爬取到的网站文本转变为字符串进行预测
# 示例用法
cleaned_text = process_file(output_file)
print(cleaned_text)

# 使用处理的字符串进行预测
flag, predict, prediction = Text_predict(cleaned_text)
if flag:
    if predict:
        print('该网站有可能是诈骗网站')
    print(f'预测结果：\n非诈骗网站的概率：{prediction[0]:.3f}  诈骗网站的概率：{prediction[1]:.3f}')
else:
    print("0")
