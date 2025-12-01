import json
import os
import requests
import re
from bs4 import BeautifulSoup

def save_json(save_path, news_type, data):
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, news_type+"_raw.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("抓取完成，已保存为" + file_path)


def get_html(url, headers):
    try:
        resp = requests.get(url, headers=headers, timeout=10, verify=False)   # 关闭 SSL 验证
        resp.encoding = resp.apparent_encoding
        return resp.text
    except Exception as e:
        print(f"请求失败！")
        return None
    
def parse_detail_page(url, headers, get_date=False):
    resp_text = get_html(url, headers)
    if resp_text is None:
        return {"content": ""} if not get_date else {"content": "", "date": ""}

    soup = BeautifulSoup(resp_text, "html.parser")

    content_box = (
        soup.find("div", id="vsb_content") or
        soup.find("div", class_="v_news_content")
    )

    if not content_box:
        return {"content": ""}

    paragraphs = []
    for p in content_box.find_all("p"):
        text = p.get_text(" ", strip=True)
        if text:  # 避免空段落
            paragraphs.append(text)

    # 合并成多段内容，每段用换行分隔
    content = "\n".join(paragraphs)
    result = {
        "content": content
    }

    if get_date:
        result["date"] = extract_date_from_detail(soup)
        
    return result

def extract_date_from_detail(soup):
    # 尝试找到常见的日期所在 div
    date_div = soup.find("div", align="center")
    if not date_div:
        return ""

    # 获取 div 的纯文本，不包含 script
    text = date_div.get_text(" ", strip=True)

    # 如果没有时间，匹配 YYYY年MM月DD日
    match = re.search(r"(\d{4}年\d{2}月\d{2}日)", text)
    if match:
        return match.group(1)

    return ""
