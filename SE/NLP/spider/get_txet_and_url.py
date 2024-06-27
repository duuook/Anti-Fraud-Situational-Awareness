from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
from urllib.parse import urljoin, urlsplit
import re
def fetch_website_info(url, driver):
    try:
        print(f"Fetching {url}")
        driver.get(url)
        time.sleep(3)  # 等待页面加载

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        title = soup.title.string if soup.title else 'No title found'
        links = [a['href'] for a in soup.find_all('a', href=True)]
        texts = soup.stripped_strings
        page_text = ' '.join(texts)

        print(f"Fetched {url} successfully")
        return title, page_text, links

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None, []

def start_crawl(start_url, output_file):
    if os.path.exists(output_file):
        os.remove(output_file)

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-block-third-party-cookies')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(), options=options)

    try:
        base_url = "{0.scheme}://{0.netloc}".format(urlsplit(start_url))

        # 只爬取首页内容
        title, page_text, links = fetch_website_info(start_url, driver)
        if title and page_text:
            with open(output_file, 'a', encoding='utf-8') as file:
                file.write(f"URL: {start_url}\n")
                file.write(f"Title: {title}\n")
                file.write("Page Text:\n")
                file.write(page_text)
                file.write("\n\n" + "=" * 80 + "\n\n")

        # 将首页的所有链接写入到另一个文件中
        links_file = 'links.txt'
        with open(links_file, 'w', encoding='utf-8') as file:
            for link in links:
                full_link = urljoin(base_url, link)
                file.write(full_link + '\n')

        print(f"Saved links to {links_file}")

    finally:
        driver.quit()

def clean_text(text):
    # 去除空白行
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    # 去除开头的 URL 和 Title 行
    if cleaned_lines and cleaned_lines[0].startswith('URL:'):
        cleaned_lines.pop(0)
    if cleaned_lines and cleaned_lines[0].startswith('Title:'):
        cleaned_lines.pop(0)

    # 将多行文本合并为一个字符串
    combined_text = ' '.join(cleaned_lines)

    # 去掉URL
    cleaned_text = re.sub(r'http\S+|www\S+|https\S+', '', combined_text)

    # 去掉不是常用符号，只保留中文、英文、数字和常用标点符号
    cleaned_text = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff,.，。?!？！：:;；\'"“”]', ' ', cleaned_text)

    # 多个空格替换为单个空格
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

    return cleaned_text


def process_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    cleaned_text = clean_text(text)

    return cleaned_text



if __name__ == '__main__':
    # 示例用法
    #爬虫
    start_url = "https://www.processon.com/diagrams"
    output_file = 'website_texts.txt'
    start_crawl(start_url, output_file)

    # 将爬取到的网站文本转变为字符串进行预测
    # 示例用法
    cleaned_text = process_file(output_file)
    print(cleaned_text)