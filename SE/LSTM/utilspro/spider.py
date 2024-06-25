import requests
import json

# 设置API Key
key = '8434af033cf9ce2224fc92cbbefeddfc'


# phone = input("请输入要查询的电话号码：")

# 电话号码归属地查询
def phone_number_spider(phone):
    """
    :param phone: 待查询的电话号码
    :return: 查询结果 (dict)
    """
    try:
        # 构造请求的URL
        url = 'https://api.tanshuapi.com/api/attribution_phone/v1/index?key={}&phone={}'.format(key, phone)

        # 发送请求
        response = requests.get(url)

        # 解析返回结果
        # {'code': 1, 'msg': '操作成功',
        # 'data': {'phone': '15728484768', 'province': '广东', 'city': '河源', 'isp': '中国移动', 'areacode': '0762'}}
        result = response.json()

        # 输出查询结果
        # print(result)

        if result['code']:
            query = result['data']
            query['code'] = 1
            # 返回字典形式的查询结果
            return query
    except Exception as e:
        return {'code': 0, 'error': '查询失败'}
