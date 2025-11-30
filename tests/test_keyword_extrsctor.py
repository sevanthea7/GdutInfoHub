import json
import os

def search_news_by_keywords(keywords, folder_path):
    matched_contents = []
    if not os.path.exists(folder_path):
        print(f"错误：文件夹不存在，请检查路径：{folder_path}")
        return matched_contents

    for filename in os.listdir(folder_path):
        if filename.endswith('_database.json'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                print(f"警告：文件 {filename} 不是有效 JSON，跳过")
                continue
            except Exception as e:
                print(f"警告：读取文件 {filename} 失败：{str(e)}，跳过")
                continue

            for news in data:
                news_keywords = news.get("keywords", [])
                if not isinstance(news_keywords, list):
                    continue
                common_keywords = set([kw.lower() for kw in keywords]) & set([kw.lower() for kw in news_keywords])
                if common_keywords:
                    content = news.get("content", "").strip()
                    if content:  # 只保留非空内容
                        matched_contents.append(content)

    kw = '、'.join(keywords)
    num_kw = len(matched_contents)
    print(f'\n✅ 查找到「{kw}」相关内容共 {num_kw} 条！')
    return matched_contents

TEST_FOLDER = '../src/crawler/news_data'


def test_search_keyword_skill():
    """测试关键词「技能」的搜索功能"""
    # 1. 执行搜索
    result = search_news_by_keywords(['技能'], TEST_FOLDER)

    # 2. 断言（验证结果符合预期）
    assert isinstance(result, list), "返回结果必须是列表"
    # 如果已知有匹配数据，可加：assert len(result) > 0, "未找到任何包含「技能」的新闻"


def test_search_nonexistent_keyword():
    """测试搜索不存在的关键词（比如「不存在的关键词123」）"""
    result = search_news_by_keywords(['不存在的关键词123'], TEST_FOLDER)
    assert isinstance(result, list), "返回结果必须是列表"
    assert len(result) == 0, "搜索不存在的关键词应返回空列表"


def test_search_empty_keywords():
    """测试搜索空关键词列表"""
    result = search_news_by_keywords([], TEST_FOLDER)
    assert len(result) == 0, "空关键词应返回空列表"


def test_invalid_folder_path():
    """测试无效的文件夹路径"""
    result = search_news_by_keywords(['技能'], '../invalid_folder')
    assert len(result) == 0, "无效路径应返回空列表"


if __name__ == '__main__':
    matched_result = search_news_by_keywords(['技能'], TEST_FOLDER)
    print("\n" + "=" * 50)
    print("匹配到的具体内容：")
    print("=" * 50)
    for idx, content in enumerate(matched_result, 1):
        print(f"\n【第{idx}条】")
        print(content[:200] + "..." if len(content) > 200 else content)