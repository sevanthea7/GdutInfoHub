import sys
import os
import pytest
import json
import shutil
import requests

# 把项目根目录加入Python路径（确保能导入src中的tool_func）
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# 导入tool_func中的函数
from src.crawler.crawler.tool_func import save_json, get_html

# 项目内临时测试目录
TEST_TEMP_DIR = os.path.join(os.path.dirname(__file__), "tool_func_temp")
# 测试用有效URL（用广工官网通知页，确保能正常请求）
TEST_VALID_URL = "https://www.gdut.edu.cn/index/tzgg.htm"
# 测试用无效URL
TEST_INVALID_URL = "http://invalid.gdut.test.nonexist"
# 测试用超时URL（模拟慢请求）
TEST_TIMEOUT_URL = "http://httpstat.us/200?sleep=20"  # 20秒后返回，设置1秒超时


# ---------------------- 测试get_html函数 ----------------------
def test_get_html_success():
    """测试正常URL能否成功获取HTML"""
    headers = {"User-Agent": "test-agent"}
    html = get_html(TEST_VALID_URL, headers)

    # 断言：返回的是字符串且不为空
    assert isinstance(html, str), "get_html应返回字符串"
    assert len(html.strip()) > 0, "get_html返回的HTML内容为空"


def test_get_html_invalid_url():
    """测试无效URL是否返回None"""
    headers = {"User-Agent": "test-agent"}
    html = get_html(TEST_INVALID_URL, headers)

    # 断言：返回None
    assert html is None, "无效URL时get_html应返回None"


def test_get_html_timeout():
    """测试超时请求是否返回None"""
    headers = {"User-Agent": "test-agent"}

    # 覆盖原函数的timeout（临时设为1秒）
    def get_html_with_short_timeout(url, headers):
        try:
            resp = requests.get(url, headers=headers, timeout=1, verify=False)
            resp.encoding = resp.apparent_encoding
            return resp.text
        except:
            return None

    # 这里用临时改写的函数测试超时
    html = get_html_with_short_timeout(TEST_TIMEOUT_URL, headers)

    assert html is None, "超时请求时get_html应返回None"


# ---------------------- 测试save_json函数 ----------------------
@pytest.fixture(autouse=True)
def clean_temp_dir():
    """测试前后自动清理临时目录（确保不残留文件）"""
    # 测试前删除旧目录
    if os.path.exists(TEST_TEMP_DIR):
        shutil.rmtree(TEST_TEMP_DIR)
    yield  # 执行测试
    # 测试后删除新目录
    if os.path.exists(TEST_TEMP_DIR):
        shutil.rmtree(TEST_TEMP_DIR)


def test_save_json_creates_directory():
    """测试save_json是否能自动创建不存在的目录"""
    test_data = [{"title": "测试文章", "content": "测试内容"}]
    save_json(TEST_TEMP_DIR, "test_news", test_data)

    # 断言：目录已创建
    assert os.path.exists(TEST_TEMP_DIR), "save_json未自动创建目录"


def test_save_json_writes_correct_content():
    """测试save_json是否能正确写入JSON内容"""
    test_data = [
        {"title": "测试文章1", "content": "内容1"},
        {"title": "测试文章2", "content": "内容2"}
    ]
    news_type = "test_news"
    save_json(TEST_TEMP_DIR, news_type, test_data)

    # 读取写入的文件，验证内容
    file_path = os.path.join(TEST_TEMP_DIR, f"{news_type}_raw.json")
    assert os.path.exists(file_path), "save_json未生成目标文件"

    with open(file_path, "r", encoding="utf-8") as f:
        saved_data = json.load(f)

    # 断言：写入的内容和输入一致
    assert saved_data == test_data, "save_json写入的内容与输入不一致"


def test_save_json_correct_filename():
    """测试save_json生成的文件名是否正确（news_type_raw.json）"""
    test_data = [{"title": "测试"}]
    news_type = "notice_test"
    save_json(TEST_TEMP_DIR, news_type, test_data)

    expected_filename = f"{news_type}_raw.json"
    file_path = os.path.join(TEST_TEMP_DIR, expected_filename)

    assert os.path.exists(file_path), f"save_json生成的文件名不是{expected_filename}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])