import sys
import os
import pytest
import json
from urllib.parse import urlparse

# 把项目根目录加入Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# 导入notice.py中的函数
from src.crawler.crawler.notice import (
    parse_list_page,
    parse_detail_page,
    crawl_all_pages,
    crawl_notice_func,
    START_PAGE,
    BASE_URL
)

# 项目内临时测试目录
TEST_TEMP_DIR = os.path.join(os.path.dirname(__file__), "test_notice_temp")


# ---------------------- 测试列表页解析（parse_list_page） ----------------------
def test_parse_list_page():
    """测试能否从通知列表页获取文章信息"""
    articles = parse_list_page(START_PAGE)

    # 断言：至少能拿到1篇文章
    assert len(articles) > 0, "未能从通知列表页获取到任何文章"

    # 断言：每篇文章包含title、url、date字段，且url符合要求
    for article in articles:
        assert "title" in article, f"文章缺少title字段：{article}"
        assert "url" in article, f"文章缺少url字段：{article}"
        assert "date" in article, f"文章缺少date字段：{article}"

        # 断言：url是合法链接且以BASE_URL开头
        parsed_url = urlparse(article["url"])
        assert parsed_url.scheme in ["http", "https"], f"文章URL不合法：{article['url']}"
        assert article["url"].startswith(BASE_URL), f"文章URL不符合要求：{article['url']}"


# ---------------------- 测试详情页解析（parse_detail_page） ----------------------
def test_parse_detail_page():
    """测试能否从通知详情页获取正文内容"""
    # 先从列表页拿第一篇文章的URL
    articles = parse_list_page(START_PAGE)
    if not articles:
        pytest.skip("未获取到文章列表，跳过详情页测试")

    first_article_url = articles[0]["url"]
    detail_result = parse_detail_page(first_article_url)

    # 断言：返回结果是字典且包含content字段
    assert isinstance(detail_result, dict), "详情页返回结果不是字典"
    assert "content" in detail_result, "详情页返回结果缺少content字段"
    # 断言：content内容不为空
    assert len(detail_result["content"].strip()) > 0, f"文章{first_article_url}内容为空"


# ---------------------- 测试全页爬取（crawl_all_pages） ----------------------
def test_crawl_all_pages():
    """测试能否爬取多页通知"""
    crawl_results = crawl_all_pages(START_PAGE)

    # 断言：爬取结果不为空
    assert len(crawl_results) > 0, "全页爬取未获取到任何文章"

    # 断言：每篇文章包含完整字段
    for article in crawl_results:
        assert all(key in article for key in ["title", "url", "date", "content"]), \
            f"文章字段不完整：{article}"


# ---------------------- 测试完整爬取+保存（不写C盘） ----------------------
def test_crawl_notice_func():
    """测试完整爬取流程（文件保存到项目内临时目录）"""
    # 创建项目内临时目录（避免C盘写入）
    os.makedirs(TEST_TEMP_DIR, exist_ok=True)

    try:
        # 执行爬取+保存
        crawl_notice_func(TEST_TEMP_DIR)

        # 断言：生成了JSON文件
        json_files = [f for f in os.listdir(TEST_TEMP_DIR) if f.endswith(".json")]
        assert len(json_files) > 0, "爬取完成后未生成任何JSON文件"

        # 断言：JSON文件内容不为空
        json_path = os.path.join(TEST_TEMP_DIR, json_files[0])
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) > 0, "JSON文件内容为空"

    finally:
        # 测试结束后自动删除临时文件+目录（避免占用空间）
        for file in os.listdir(TEST_TEMP_DIR):
            os.remove(os.path.join(TEST_TEMP_DIR, file))
        os.rmdir(TEST_TEMP_DIR)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])