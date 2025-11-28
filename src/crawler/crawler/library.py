import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from src.crawler.crawler.tool_func import save_json, get_html

# 配置
START_PAGE = 'https://library.gdut.edu.cn/xwgg/xwdt.htm' 
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}

NEWS_TYPE = 'library_news'

def get_page_urls(page_url):    # 获取当前列表页的所有文章 URL、标题、日期
    resp_text = get_html(page_url, headers)
    if resp_text is None:
        return []
    soup = BeautifulSoup(resp_text, "html.parser")
    
    articles = []
    for li in soup.select("div.lm_list ul li"):
        a_tag = li.find("a")
        span_tag = li.find("span")
        if a_tag and span_tag:
            title = a_tag.text.strip()
            href = urljoin(page_url, a_tag['href'])
            date = span_tag.text.strip()
            articles.append({
                "title": title,
                "url": href,
                "date": date
            })
    return articles

def get_article_content(article_url):    # 获取文章正文内容
    resp_text = get_html(article_url, headers)
    if resp_text is None:
        return {"content": ""}
    soup = BeautifulSoup(resp_text, "html.parser")

    content_div = soup.select_one("div.nr-info div.v_news_content")
    if content_div:
        paragraphs = [p.get_text(strip=True) for p in content_div.find_all("p")]
        content = "\n".join(paragraphs)
    else:
        content = ""
    return content

def crawl_all_pages(start_url): # 抓取所有文章分页
    results = []
    next_page = start_url
    
    while next_page:
        print(f"抓取页面: {next_page}")
        articles = get_page_urls(next_page)
        for article in articles:
            print(f"*抓取文章: {article['title']}")
            article["content"] = get_article_content(article["url"])
            results.append(article)
        
        resp_text = get_html(next_page, headers)
        if resp_text is None:
            break
        soup = BeautifulSoup(resp_text, "html.parser")
        next_link = soup.select_one("span.p_next a")
        if next_link:
            next_page = urljoin(next_page, next_link['href'])
        else:
            next_page = None
    return results


def crawl_library_func(save_path):
    data = crawl_all_pages(START_PAGE)
    save_json(save_path, NEWS_TYPE, data)
