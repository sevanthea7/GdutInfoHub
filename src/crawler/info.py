import requests
from bs4 import BeautifulSoup
import json
import re

# ---------------------
# Cookie & Headers
# ---------------------
cookies = {
    "JSESSIONID": "81F26CC7275A3C18D0A4AE547EDF89EF.SY189",
    "avatarImageUrl": "-6964000252392685202",
    "route": "bcdc66501e5374f95409364b7d34d476",
    "loginPageURL": ""
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": "https://oas.gdut.edu.cn/seeyon/newsData.do?method=newsIndex&boardId=2945931106835317958",
}

LIST_URL = "https://oas.gdut.edu.cn/seeyon/newsData.do?method=newsIndex&boardId=2945931106835317958"
DETAIL_URL = "https://oas.gdut.edu.cn/seeyon/newsData.do?method=newsView&newsId={}"

session = requests.Session()

# -------------------------
# 获取新闻列表
# -------------------------
def get_news_list(page_no=1, page_size=20):
    payload = [{
        "pageSize": str(page_size),
        "pageNo": page_no,
        "listType": "1",
        "spaceType": "",
        "spaceId": "",
        "typeId": "2945931106835317958",
        "condition": "publishDepartment",
        "textfield1": "",
        "textfield2": "",
        "myNews": ""
    }]

    resp = session.post(LIST_URL, headers=headers, cookies=cookies, data=json.dumps(payload))
    resp.encoding = resp.apparent_encoding

    soup = BeautifulSoup(resp.text, "html.parser")
    items = []

    # 找到每个 <td class="... articel_title">
    for td in soup.select("td.articel_title"):
        # 检查是否有 <span class="newTag">NEW</span>
        new_tag = td.find("span", class_="newTag")
        if new_tag:
            # 找标题 span
            title_span = td.find("span", class_="titleText")
            if title_span:
                title = title_span.get_text(strip=True)
                onclick = title_span.get("onclick", "")
                match = re.search(r"newsId=(\d+)&", onclick)
                if match:
                    news_id = match.group(1)
                    items.append((news_id, title))
    print(f"Page {page_no} 找到 {len(items)} 条带 NEW 的新闻")
    return items

# -------------------------
# 获取新闻详情
# -------------------------
def crawl_detail(news_id):
    url = DETAIL_URL.format(news_id)
    resp = session.get(url, headers=headers, cookies=cookies)
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, "html.parser")
    content_div = soup.find(id="contentTD")
    if content_div:
        content = content_div.get_text("\n", strip=True)
    else:
        content = soup.get_text("\n", strip=True)
    return content

# -------------------------
# 主函数
# -------------------------
def get_new_tag_news(save_path="news_new.json", pages=3):
    all_news = []

    for page in range(1, pages + 1):
        news_list = get_news_list(page_no=page)

        for news_id, title in news_list:
            print(f"爬取详情：{title} ({news_id})")
            content = crawl_detail(news_id)
            all_news.append({
                "news_id": news_id,
                "title": title,
                "content": content,
                "url": DETAIL_URL.format(news_id)
            })

        # 实时写入文件
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(all_news, f, ensure_ascii=False, indent=2)

    print(f"\n已成功写入：{save_path}")

# -------------------------
# 运行
# -------------------------
get_new_tag_news(save_path="news_new.json", pages=3)
