import requests
import json

# 设置API Key
key = '8434af033cf9ce2224fc92cbbefeddfc'


# phone = input("请输入要查询的电话号码：")

# 电话号码归属地查询
def phone_number_spider(phone):
    # 构造请求的URL
    url = 'https://api.tanshuapi.com/api/attribution_phone/v1/index?key={}&phone={}'.format(key, phone)

    # 发送请求
    response = requests.get(url)

    # 解析返回结果
    result = response.json()

    # 输出查询结果
    print(result)

    # 返回字典形式的查询结果
    return json.loads(result)
