from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib3.exceptions import InsecureRequestWarning
import urllib3
urllib3.disable_warnings(InsecureRequestWarning)

from src.crawler.crawler.tool_func import save_json, get_html, parse_detail_page

BASE_URL = 'https://tyb.gdut.edu.cn/info/'
START_PAGE = "https://tyb.gdut.edu.cn/index/tzgg.htm"   # 列表页地址

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}

NEWS_TYPE = 'sports_news'

def parse_list_page(url):
    resp_text = get_html(url, headers)
    if resp_text is None:
        return []
    soup = BeautifulSoup(resp_text, "html.parser")

    dds = soup.find_all("dd")

    results = []
    for dd in dds:
        a = dd.find("a")
        if not a:
            continue

        link = urljoin(url, a.get("href"))  # 自动补路径

        # 过滤明显不是文章的链接
        if not link.startswith(BASE_URL):
            continue

        title = a.get_text(strip=True)
        date_tag = dd.find("span", class_="fr gray")
        date = date_tag.get_text(strip=True) if date_tag else ""
        
        results.append({
            "title": title,
            "url": link,
            "date": date
        })

    return results


def crawl_all_pages(start_url):
    all_results = []
    next_page = start_url

    while next_page:
        print(f"\n抓取列表页: {next_page}")
        articles = parse_list_page(next_page)
        for article in articles:
            print(f"*抓取文章: {article['title']}")
            # 抓取内容页
            detail = parse_detail_page(article["url"], headers)
            article["content"] = detail["content"]

            all_results.append(article)

        # 解析下一页
        resp_text = get_html(next_page, headers)
        if resp_text is None:
            break

        soup = BeautifulSoup(resp_text, "lxml")
        next_link = soup.select_one("span.p_next a")

        if next_link:
            next_page = urljoin(next_page, next_link["href"])
        else:
            next_page = None
        # next_page = None

    return all_results


def crawl_sports_func(save_path):
    data = crawl_all_pages(START_PAGE)
    save_json(save_path, NEWS_TYPE, data)

# crawl_sports_func('src/crawler/news_data')