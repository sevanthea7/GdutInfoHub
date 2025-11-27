
# https://www.volcengine.com/docs/82379/1494384?redirect=1&lang=zh

PROMPT = '告诉我它属于"通知公告，水电服务，后勤报修，教务信息"中的哪一种？\
只用给我结果，结果格式为JSON格式{"label": "xxx"}'

import os
import json
from src.crawler.LLM_api.create_api_client import client


# folder_path = 'src/crawler/news_data'

# if __name__ == "__main__":
#     client = Ark(
#     api_key=API_KEY,
#     base_url="https://ark.cn-beijing.volces.com/api/v3",
#     )
#     resp = client.chat.completions.create(
#         model="doubao-1-5-lite-32k-250115",
#         messages=[{"content":f"{input_text}.","role":"system"}],
#         stream=True,
#     )
#     for chunk in resp:
#         if not chunk.choices:
#             continue

#         print(chunk.choices[0].delta.content, end="")


# TODO: 规定system和role在不同应用中的区分,{"content":"hello","role":"user"}
def create_database_JSON(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('_for_test.json'):  # 正常运行中选择结尾为'_cleaned.json'的文件
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)     # 读取文件
                except json.JSONDecodeError:
                    print(f"文件 {filename} 不是有效 JSON，跳过")
                    continue
            for item in data:
                if "content" in item:   # 对于每一个content部分让大模型进行key_words和label的输出
                    input_text = PROMPT + item["content"]
                    # print(input_text)
                    resp = client.chat.completions.create(
                        model="doubao-1-5-lite-32k-250115",
                        messages=[{"content":f"{input_text}.","role":"system"}],
                        stream=False,
                    )
                    json_return = resp.choices[0].message.content
                    # print(json_return)
                    
                    json_obj = json.loads(json_return)

                    # 填入 data
                    # item["key_words"] = json_obj.get("key_words", [])
                    item["label"] = json_obj.get("label", "")

            # 新文件名，把 "_cleaned" 换成 "_database"
            new_filename = filename.replace('_cleaned', '_database')
            # new_filename = filename.replace('_for_test', '_for_test_database')    # 此处为测试用例，正常运行用上面那行
            new_file_path = os.path.join(folder_path, new_filename)

            # 写入新文件
            with open(new_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)  # 保存为格式化的 JSON

            print(f"已生成 {new_filename}")


create_database_JSON()
print('done!')