import json
import re
import codecs

# 加载 JSON 数据
with open('output.json', 'r') as file:
    data = json.load(file)


# 清洗文本函数
def clean_text(text):
    text = text.replace('\n', ' ').replace('\r', '').replace('â\x80\x99', '').strip()  # 删除 'â\x80\x99'
    text = re.sub(' +', ' ', text)  # 将多个空格替换为一个空格
    try:
        text = codecs.getdecoder("unicode_escape")(text)[0]  # 解码 Unicode 转义序列
    except ValueError:  # 网络抓取的 raw strings 可能会抛出 'ValueError: invalid \x escape'
        text = text.encode('utf-8').decode('unicode_escape')  # 尝试再次解码
    return text



# 验证 URL 函数
def validate_url(url):
    # 简单的 URL 验证正则表达式
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost…
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...或 ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # 是 ipv6 
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


# 清洗和验证数据
for entry in data:
    if 'instruction' in entry:
        entry['instruction'] = clean_text(entry['instruction'])
        if not validate_url(entry['instruction']):
            print(f"无效的 URL: {entry['instruction']}")
    if 'input' in entry:
        entry['input'] = clean_text(entry['input'])
    if 'output' in entry:
        entry['output'] = clean_text(entry['output'])

# 保存清洗后的数据
with open('cleaned_output.json', 'w') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("数据清洗完成。清洗过的数据已保存到 'cleaned_output.json'。")
