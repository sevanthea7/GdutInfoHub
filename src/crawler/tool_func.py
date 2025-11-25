import json
import os

def save_json(save_path, news_type, data):
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, news_type+"_raw.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("抓取完成，已保存为" + save_path)