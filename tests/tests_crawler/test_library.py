import sys
import os
import pytest
import json
from urllib.parse import urlparse

# 把项目根目录加入Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# 导入library.py中的函数
from src.crawler.crawler.library import (
    get_page_urls,
    get_article_content,
    crawl_library_func,
    START_PAGE
)

# 项目内临时测试目录
TEST_TEMP_DIR = os.path.join(os.path.dirname(__file__), "test_temp_output")


# ---------------------- 测试文章列表获取（get_page_urls） ----------------------
def test_get_page_urls():
    """测试能否从图书馆首页获取文章列表"""
    articles = get_page_urls(START_PAGE)

    # 断言：至少能拿到1篇文章
    assert len(articles) > 0, "未能从图书馆首页获取到任何文章列表"

    # 断言：每篇文章都包含title、url、date字段
    for article in articles:
        assert "title" in article, f"文章缺少title字段：{article}"
        assert "url" in article, f"文章缺少url字段：{article}"
        assert "date" in article, f"文章缺少date字段：{article}"

        # 断言：url是合法的链接
        parsed_url = urlparse(article["url"])
        assert parsed_url.scheme in ["http", "https"], f"文章URL不合法：{article['url']}"


# ---------------------- 测试文章内容获取（get_article_content） ----------------------
def test_get_article_content():
    """测试能否从文章详情页获取正文内容（适配原代码返回值类型不一致问题）"""
    # 先获取第一篇文章的URL
    articles = get_page_urls(START_PAGE)
    if not articles:
        pytest.skip("未获取到文章列表，跳过内容测试")  # 列表为空时跳过

    first_article_url = articles[0]["url"]
    content_result = get_article_content(first_article_url)

    # 适配原代码：可能返回字符串（正常情况）或字典（异常情况）
    if isinstance(content_result, dict):
        # 原代码异常时返回 {"content": ""}
        assert "content" in content_result, "文章内容返回结果缺少content字段"
        actual_content = content_result["content"].strip()
    else:
        # 原代码正常时返回纯字符串
        actual_content = content_result.strip()

    # 断言：内容不为空
    assert len(actual_content) > 0, f"文章{first_article_url}的内容为空"


# ---------------------- 测试完整爬取流程 ----------------------
def test_crawl_library_func():
    """测试完整爬取流程（文件保存到项目内临时目录，不在C盘）"""
    # 创建项目内临时目录（避免C盘写入）
    os.makedirs(TEST_TEMP_DIR, exist_ok=True)

    try:
        # 执行爬取+保存（保存到项目内临时目录）
        crawl_library_func(TEST_TEMP_DIR)

        # 断言：生成了至少1个JSON文件
        json_files = [f for f in os.listdir(TEST_TEMP_DIR) if f.endswith(".json")]
        assert len(json_files) > 0, "爬取完成后未生成任何JSON文件"

        # 断言：JSON文件内容不为空
        json_file_path = os.path.join(TEST_TEMP_DIR, json_files[0])
        with open(json_file_path, "r", encoding="utf-8") as f:
            crawled_data = json.load(f)
        assert len(crawled_data) > 0, "❌ JSON文件内容为空"

    finally:
        for f in os.listdir(TEST_TEMP_DIR):
            os.remove(os.path.join(TEST_TEMP_DIR, f))
        os.rmdir(TEST_TEMP_DIR)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])