# 用于爬取指定电话库，并且格式化输出csv文件
import random

import requests  # 导入 requests 库，用于发送 HTTP 请求
from bs4 import BeautifulSoup  # 导入 BeautifulSoup 库，用于解析 HTML 和 XML 文档
import time  # 导入 time 库，用于暂停执行
import os  # 导入 os 库，用于文件和操作系统相关操作
import csv  # 导入 csv 库，用于处理 CSV 文件
import chardet  # 导入 chardet 库，用于检测文件编码

def fetch_website_info(url, visited, output_file):
    # 设置 HTTP 请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # 发送 HTTP GET 请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是 200，抛出 HTTPError 异常

        # 检测网页内容的编码
        encoding = chardet.detect(response.content)['encoding']
        # 将内容解码为检测到的编码
        content = response.content.decode(encoding, errors='ignore')

        # 使用 BeautifulSoup 解析 HTML 内容
        soup = BeautifulSoup(content, 'html.parser')

        # 提取包含诈骗电话信息的 div
        searchnr_div = soup.find('div', class_='searchnr')
        if searchnr_div:
            # 提取所有包含电话信息的 div
            bj_divs = searchnr_div.find_all('div', class_='bj')
            # 打开 CSV 文件，准备追加写入
            with open(output_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for bj_div in bj_divs:
                    # 获取电话号文本，去除首尾空格，如果没有找到则设为 'N/A'
                    phone = bj_div.a.get_text().strip() if bj_div.a else 'N/A'
                    # 获取标记次数文本，去除首尾空格，如果没有找到则设为 'N/A'
                    mark_text = bj_div.span.get_text().strip() if bj_div.span else 'N/A'

                    # 拆分电话类型和标记次数
                    if '标记' in mark_text:
                        phone_type, mark_count = mark_text.split('标记')
                        phone_type = phone_type.strip()
                        mark_count = mark_count.strip()
                    else:
                        phone_type = mark_text
                        mark_count = 'N/A'

                    # 将信息写入 CSV 文件
                    writer.writerow([phone, phone_type, mark_count])

        # 将当前 URL 添加到已访问集合中
        visited.add(url)
        # 获取页面中的所有链接
        links = [a['href'] for a in soup.find_all('a', href=True)]
        i = 0
        for link in links:
            i += 1
            if i == 20:  # 限制爬取链接的数量，避免过多请求
                break
            if link.startswith('/'):  # 处理相对路径链接
                link = url + link
            if link not in visited and link.startswith(url):
                # 递归爬取新的链接
                fetch_website_info(link, visited, output_file)
                time.sleep(1)  # 防止请求过于频繁

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")  # 捕捉异常并输出错误信息

def start_crawl(start_url, output_file):
    visited = set()  # 创建一个集合用于存储已访问的 URL
    if os.path.exists(output_file):
        os.remove(output_file)  # 如果输出文件已存在，则删除
    # 创建并打开 CSV 文件，准备写入
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["诈骗电话", "电话类型", "标记次数"])  # 写入 CSV 文件头
    fetch_website_info(start_url, visited, output_file)  # 开始爬取

# 示例用法
start_url = 'https://www.00cha.com/biaoji.asp'  # 设置起始 URL
output_file = 'scam_phones.csv'  # 设置输出文件名
start_crawl(start_url, output_file)  # 开始爬取

#——————————————————————————————————————————————————————————————————————————————————————————————————————————
# 数据库中电话号码表的定期更新
import csv
import pymysql

# 连接到MySQL数据库
connection = pymysql.connect(
    host='gz-cynosdbmysql-grp-ey0itk0t.sql.tencentcdb.com',
    user='root',
    password='!A123456',
    port=20269,
    database='SE_db',
    cursorclass=pymysql.cursors.DictCursor
)

# 读取CSV文件并将数据插入或更新到数据库
with open('scam_phones.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    cursor = connection.cursor()
    # 获取表中最后一行的id
    cursor.execute("SELECT * FROM SE_phone_number ORDER BY id DESC LIMIT 1")
    last_row = cursor.fetchone()
    last_row_id=last_row['id']
    print(last_row_id)


    for row in csv_reader:
        # 检查数据库中是否已存在该数据（根据需要进行更新或插入操作）
        cursor.execute("SELECT * FROM SE_phone_number WHERE 电话号码 = %s", (row['诈骗电话'],))
        existing_data = cursor.fetchone()
        rand_int = random.randint(1, 5)
        if existing_data:
            existing_data_id = existing_data['id']
            # 如果数据已存在，则更新数据
            cursor.execute("UPDATE SE_phone_number SET 电话号码 = %s, 电话类型 = %s, 标记次数 = %s WHERE id = %s",
                           (row['诈骗电话'], '诈骗电话', rand_int, existing_data_id))
        else:
            # 如果数据不存在，则插入新数据
            cursor.execute("INSERT INTO SE_phone_number (电话号码, 电话类型, 标记次数) VALUES (%s, %s, %s)",
                           (row['诈骗电话'], '诈骗电话', rand_int))

    connection.commit()

# 关闭数据库连接
connection.close()