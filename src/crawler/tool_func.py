import json
import os

def save_json(save_path, data):
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, "library_news.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("抓取完成，已保存为" + save_path)