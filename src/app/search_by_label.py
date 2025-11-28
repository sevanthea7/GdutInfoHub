import json
import os

def search_news_by_label(label, folder_path):
    matched_contents = []
    for filename in os.listdir(folder_path):
        if filename.endswith('_database.json'):     # 读取所有结尾是_database的文件
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)  # 读取文件
                except json.JSONDecodeError:
                    print(f"文件 {filename} 不是有效 JSON，跳过")
                    continue
            for news in data:
                news_label = news.get("label")
                if not isinstance(news_label, str):
                    continue
                if label == news_label:
                    matched_contents.append(news)
    num_lb = len(matched_contents)
    print(f'查找到 {label} 内容共 {num_lb} 条！')
    return matched_contents


# search_news_by_label('水电服务', 'src/crawler/news_data')