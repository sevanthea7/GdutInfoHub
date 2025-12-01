from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib3.exceptions import InsecureRequestWarning
import urllib3
urllib3.disable_warnings(InsecureRequestWarning)

from src.crawler.crawler.tool_func import save_json, get_html, parse_detail_page

BASE_URL = 'https://zzb.gdut.edu.cn/info/'
START_PAGE = "https://zzb.gdut.edu.cn/tzgg.htm"   # 列表页地址

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}

NEWS_TYPE = 'party_news'

def parse_list_page(url):
    resp_text = get_html(url, headers)
    if resp_text is None:
        return []
    soup = BeautifulSoup(resp_text, "html.parser")

    rows = soup.find_all("tr")

    results = []
    for tr in rows:
        a = tr.find("a")
        if not a:
            continue

        link = urljoin(url, a.get("href"))

        # 过滤非本站链接
        if not link.startswith(BASE_URL):
            continue

        title = a.get_text(strip=True)

        # 日期在第二个 td 的 <span> 中
        # date_td = tr.find_all("td")
        # date = ""
        # if len(date_td) >= 3:  # 通常日期在第 3 列
        #     date_span = date_td[2].find("span")
        #     if date_span:
        #         date = date_span.get_text(strip=True)

        results.append({
            "title": title,
            "url": link
            # "date": date
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
            detail = parse_detail_page(article["url"], headers, True)
            article["content"] = detail["content"]
            article["date"] = detail["date"]

            all_results.append(article)

        # 解析下一页
        resp_text = get_html(next_page, headers)
        if resp_text is None:
            break

        soup = BeautifulSoup(resp_text, "lxml")
        next_link = soup.find("a", class_="Next", string=lambda x: x and "下页" in x)

        if next_link:
            next_page = urljoin(next_page, next_link["href"])
        else:
            next_page = None
        # next_page = None

    return all_results


def crawl_party_func(save_path):
    data = crawl_all_pages(START_PAGE)
    save_json(save_path, NEWS_TYPE, data)

# crawl_party_func('src/crawler/news_data')