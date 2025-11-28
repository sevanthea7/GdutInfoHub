from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib3.exceptions import InsecureRequestWarning
import urllib3
urllib3.disable_warnings(InsecureRequestWarning)

from src.crawler.crawler.tool_func import save_json, get_html

BASE_URL = 'https://www.gdut.edu.cn/info/'
START_PAGE = "https://www.gdut.edu.cn/index/tzgg.htm"   # 列表页地址

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}

NEWS_TYPE = 'notice_news'

def parse_list_page(url):
    resp_text = get_html(url, headers)
    if resp_text is None:
        return []
    soup = BeautifulSoup(resp_text, "html.parser")

    lis = soup.find_all("li")

    results = []
    for li in lis:
        a = li.find("a")
        if not a:
            continue

        link = urljoin(url, a.get("href"))  # 自动补路径

        # 过滤明显不是文章的链接
        if not link.startswith(BASE_URL):
            continue

        title = a.get_text(strip=True)
        date_tag = a.find("i")
        date = date_tag.get_text(strip=True) if date_tag else ""

        results.append({
            "title": title,
            "url": link,
            "date": date
        })

    return results


def parse_detail_page(url):
    resp_text = get_html(url, headers)
    if resp_text is None:
        return {"content": ""}
    soup = BeautifulSoup(resp_text, "html.parser")

    content_box = (
        soup.find("div", id="vsb_content") or
        soup.find("div", class_="v_news_content")
    )

    content = content_box.get_text("\n", strip=True) if content_box else ""

    return {
        "content": content
    }


def crawl_all_pages(start_url):
    all_results = []
    next_page = start_url

    while next_page:
        print(f"\n抓取列表页: {next_page}")
        articles = parse_list_page(next_page)
        for article in articles:
            print(f"*抓取文章: {article['title']}")
            # 抓取内容页
            detail = parse_detail_page(article["url"])
            article["content"] = detail["content"]

            all_results.append(article)

        # 解析下一页
        resp_text = get_html(next_page, headers)
        if resp_text is None:
            break

        soup = BeautifulSoup(resp_text, "lxml")
        next_link = soup.find("a", class_="Next")

        if next_link:
            next_page = urljoin(next_page, next_link["href"])
        else:
            next_page = None
        # next_page = None

    return all_results


def crawl_notice_func(save_path):
    data = crawl_all_pages(START_PAGE)
    save_json(save_path, NEWS_TYPE, data)

# crawl_notice_func('src/crawler/news_data')