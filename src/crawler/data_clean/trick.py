##################################
# 该程序用于管理员快速添加栏目信息
##################################
import os
import json
folder_path = 'src/crawler/news_data'
# 遍历文件夹里的所有 JSON 文件
for filename in os.listdir(folder_path):
    if filename.endswith('party_news_reprocessed.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)  # 读取文件
            except json.JSONDecodeError:
                print(f"文件 {filename} 不是有效 JSON，跳过")
                continue

        for item in data:
            item["department"] = "党建部"
            item["column"] = "党建快讯"
            item["label"] = "通知公告"

        new_filename = filename.replace('_reprocessed', '_database')
        new_file_path = os.path.join(folder_path, new_filename)

        # 写入新文件
        with open(new_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)  # 保存为格式化的 JSON

        print(f"已生成 {new_filename}")