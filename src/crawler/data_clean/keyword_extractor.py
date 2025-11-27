import json
import os


def search_news_by_keywords(keywords: list[str]) -> list[str]:

    # JSON 文件路径
    json_file_path = os.path.join("src", "crawler", "news_data", "library_news_reprocessed.json")

    # 读取 JSON 文件内容
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            news_data = json.load(f)  # 解析为 Python 列表（包含多个新闻字典）
    except FileNotFoundError:
        print(f"错误：文件未找到，请检查路径是否正确：{json_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"错误：JSON 文件格式异常，无法解析")
        return []

    # 筛选匹配关键词的新闻，并提取 content
    matched_contents = []
    for news in news_data:
        # 检查新闻是否包含 keywords 字段，且为列表类型
        news_keywords = news.get("keywords", [])
        if not isinstance(news_keywords, list):
            continue

        # 计算输入关键词和新闻关键词的交集（判断是否有共同关键词）
        common_keywords = set(keywords) & set(news_keywords)
        if common_keywords:  # 有共同关键词则视为匹配
            # 提取 content 字段
            content = news.get("content", "")
            if isinstance(content, str):
                matched_contents.append(content)

    return matched_contents