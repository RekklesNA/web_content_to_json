import json

# 指定文件的完整路径
file_path = 'D:\\PycharmProject\\web_content_to_json\\cleaned_merged_results.txt'

# 读取输入的文本文件
with open(file_path, 'r', encoding='utf-8') as infile:
    data = infile.read().strip().split('\n')

# 准备输出数据的列表
output_data = []

# 处理每个JSON内容
for line in data:
    item = json.loads(line)

    url = item['url']
    title = item['title']
    paragraphs = item['paragraphs']

    # 拼接所有段落内容，剔除乱码
    content = ' '.join(paragraphs).replace('\u201d', '"').replace('\u2013', '-').replace('\u2026', '...')

    # 创建新的格式，将URL保留在instruction中，将title添加到output的开始
    new_item = {
        "instruction": url,
        "input": "",
        "output": f"{title}\n\n{content}"
    }

    # 添加到输出数据列表
    output_data.append(new_item)

# 将输出数据写入新的JSON文件
output_file_path = 'D:\\PycharmProject\\web_content_to_json\\output.json'
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, indent=4, ensure_ascii=False)

print("处理完成，结果已写入output.json")

