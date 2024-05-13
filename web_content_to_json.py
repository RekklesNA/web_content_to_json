from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time

def fetch_and_parse(url):
    # 创建一个新的Selenium浏览器实例
    browser = webdriver.Firefox()  # 或者使用其他的浏览器，例如Chrome

    # 使用Selenium获取网页内容
    browser.get(url)

    # 等待一段时间，让JavaScript有足够的时间加载内容
    time.sleep(5)

    # 获取网页的源代码
    html = browser.page_source

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html, 'html.parser')

    # 提取网页的标题和所有段落
    title = soup.find('title').text if soup.find('title') else 'No title'
    paragraphs = [p.text for p in soup.find_all('p')]

    # 创建一个字典来存储提取的数据
    data = {
        'title': title,
        'paragraphs': paragraphs
    }

    # 将字典转换为JSON字符串
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # 关闭浏览器
    browser.quit()

    return json_data

def get_url_from_user():
    url = input("请输入要获取的网址：")
    return url


def main():
    url = get_url_from_user()
    data = fetch_and_parse(url)
    print(data)


if __name__ == "__main__":
    main()
