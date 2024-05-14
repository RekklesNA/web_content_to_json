import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from bs4 import BeautifulSoup
import json
import time


def fetch_and_parse(url):
    browser = webdriver.Firefox()
    try:
        browser.get(url)
        time.sleep(5)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').text if soup.find('title') else 'No title'
        paragraphs = [p.text for p in soup.find_all('p')]
        data = {
            'url': url,
            'title': title,
            'paragraphs': paragraphs
        }
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
    except NoSuchWindowException:
        print(f"Window was closed unexpectedly for URL: {url}")
        json_data = json.dumps({
            'error': 'Window was closed unexpectedly',
            'url': url,
        }, ensure_ascii=False, indent=4)
    finally:
        try:
            browser.quit()
        except NoSuchWindowException:
            pass
    return json_data


def main():
    # Open the file containing URLs
    with open('urls.txt', 'r') as file:
        urls = file.readlines()

    # Process each URL
    for i, url in enumerate(urls):
        url = url.strip()  # Remove any trailing newline or spaces
        print(f"Processing URL {i + 1}/{len(urls)}: {url}")
        data = fetch_and_parse(url)

        # Write the result to a new file in the 'results' folder
        with open(os.path.join('results', f'result{i + 1}.txt'), 'w', encoding='utf-8') as out_file:
            out_file.write(data)


if __name__ == "__main__":
    main()
