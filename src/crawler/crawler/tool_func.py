import json
import os
import requests

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