import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from collections import deque


def is_valid(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def fetch_all_links(url, visited):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"获取 {url} 时出错: {e}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    links = deque()
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(url, href)
        if is_valid(full_url) and full_url not in visited:
            links.append(full_url)
    return links


def crawl(url, file_path):
    visited = set()
    # 使用队列实现广度优先搜索
    queue = deque([url])
    while queue:
        url = queue.popleft()  # deque.popleft() 能快速取出
        visited.add(url)
        # 一旦网址被访问，就写入文件
        with open(file_path, 'a') as file:
            file.write(url + '\n')
        links = fetch_all_links(url, visited)
        # 将所有新的网址添加到队列的末尾
        queue.extend(link for link in links if link not in visited)


def main():
    url = 'https://www.hyperscalers.com.au/index.php'
    if not is_valid(url):
        print(f"非有效网址: {url}")
        return
    # 将网址保存到文件的名称
    file_path = 'urls.txt'
    crawl(url, file_path)


if __name__ == "__main__":
    main()
