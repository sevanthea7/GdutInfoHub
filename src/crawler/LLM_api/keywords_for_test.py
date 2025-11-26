
import json
import os

# 为了避免不必要的大模型token消耗，用该文件进行key_words和label的计算的模拟
folder_path = 'src/crawler/news_data'

for filename in os.listdir(folder_path):
    if filename.endswith('_for_test.json'):  # 正常运行中选择结尾为‘_cleaned.json'的文件
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)     # 读取文件
            except json.JSONDecodeError:
                print(f"文件 {filename} 不是有效 JSON，跳过")
                continue

        if 'content' in data:   # 对于每一个content部分让大模型进行key_words和label的输出
            # api调用
            json_return = '{ \
                "key_words": ["示例关键词1", "示例关键词2", "示例关键词3"], \
                "label": "示例标签" \
            }'
            
            json_obj = json.loads(json_return)

            # 填入 data
            data["key_words"] = json_obj.get("key_words", [])
            data["label"] = json_obj.get("label", "")

        # 新文件名，把 "_cleaned" 换成 "_database"
        new_filename = filename.replace('_cleaned', '_database')
        new_file_path = os.path.join(folder_path, new_filename)

        # 写入新文件
        with open(new_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)  # 保存为格式化的 JSON

        print(f"已生成 {new_filename}")
