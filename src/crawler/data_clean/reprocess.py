import json
import re
import os
import jieba.analyse

# 指定文件夹路径
# folder_path = 'src/crawler/news_data'
folder_path = 'news_data'

# 用于保存所有整理后的内容
all_contents = []

# 遍历文件夹里的所有 JSON 文件
for filename in os.listdir(folder_path):
    if filename.endswith('_raw.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)     # 读取文件
            except json.JSONDecodeError:
                print(f"文件 {filename} 不是有效 JSON，跳过")
                continue

        # 处理 json 文件中的每个字典  
        for item in data:
            # 正则化处理：
            # 1. 去掉开头结尾空白
            # 2. 将连续换行或空白替换为一个空格
            # 3. 去掉多余空格
            if 'content' in item:
                TEXT = item['content']
                TEXT = re.sub(r'[\s\u2028\u2029]+', ' ', TEXT).strip()

                # 从处理后的文本中应用 TF-IDF 算法提取关键词
                keywords = jieba.analyse.extract_tags(
                    sentence=TEXT,
                    topK=6,          # 提取的关键词数量
                    allowPOS=['n','nz', 'ns'],  # 允许的关键词的词性
                    withWeight=False,  # 是否附带词语权重
                    withFlag=False,    # 是否附带词语词性
                )
                # 为data添加关键词字段
                item['keywords'] = keywords

        # 新文件名，把 "_raw" 换成 "_cleaned"，如果没有 "_raw" 就直接加 "_cleaned"
        new_filename = filename.replace('_raw', '_reprocessed')
        new_file_path = os.path.join(folder_path, new_filename)

        # 写入新文件
        with open(new_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)  # 保存为格式化的 JSON

        print(f"已生成 {new_filename}")

