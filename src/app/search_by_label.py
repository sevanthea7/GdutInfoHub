import json
import os
import re

def normalize_date(date_str):
    if not date_str:
        return ""

    parts = re.findall(r"\d+", date_str)
    if len(parts) >= 3:
        year, month, day = parts[:3]
        # 补零（保证两位数）
        month = month.zfill(2)
        day = day.zfill(2)
        return f"{year}/{month}/{day}"
    
    return date_str


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
                    # matched_contents.append(news)
                    cleaned_news = dict(news)   # 复制一份，避免直接修改原数据
                    # 删除字段
                    cleaned_news.pop("label", None)
                    cleaned_news.pop("keywords", None)
                    if label != "通知公告" and "column" in cleaned_news: 
                        cleaned_news.pop("column", None)
                    if "date" in cleaned_news:
                        cleaned_news["date"] = normalize_date(cleaned_news["date"])
                    matched_contents.append(cleaned_news)

    num_lb = len(matched_contents)
    print(f'查找到 {label} 内容共 {num_lb} 条！')
    # print(matched_contents[0])
    return matched_contents


# search_news_by_label('通知公告', 'src/crawler/news_data')