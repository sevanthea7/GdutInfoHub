# 改进后的clean.py
import json
import re
import os

folder_path = 'src/crawler/news_data'
all_contents = []


def advanced_clean(text):
    """增强版文本正则化处理"""
    if not text:
        return ""

    # 1. 去除HTML标签残留
    text = re.sub(r'<[^>]+>', '', text)
    # 2. 去除特殊符号（保留基本标点）
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9,.?!，。？！；;：: ]', '', text)
    # 3. 处理空白字符（包括全角空格）
    text = re.sub(r'[\s\u3000\u2028\u2029]+', ' ', text).strip()
    # 4. 标准化日期格式（示例：2023年12月3日 → 2023-12-03）
    text = re.sub(r'(\d{4})年(\d{1,2})月(\d{1,2})日', r'\1-\2-\3', text)
    text = re.sub(r'(\d{4})-(\d{1})(?=-)', r'\1-0\2', text)  # 补全月份
    text = re.sub(r'(\d{4}-\d{2})-(\d{1})\b', r'\1-0\2', text)  # 补全日期
    return text


for filename in os.listdir(folder_path):
    if filename.endswith('_raw.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"文件 {filename} 不是有效 JSON，跳过")
                continue

        # 对内容和标题都进行清洗
        if 'content' in data:
            data['content'] = advanced_clean(data['content'])
        if 'title' in data:
            data['title'] = advanced_clean(data['title'])

        new_filename = filename.replace('_raw', '_cleaned')
        new_file_path = os.path.join(folder_path, new_filename)

        with open(new_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"已生成 {new_filename}")