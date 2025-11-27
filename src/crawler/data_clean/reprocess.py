import json
import re
import os
import jieba.analyse
from src.crawler.data_clean.clean_pro import advanced_clean


def keywords_extract(TEXT):
    keywords = jieba.analyse.extract_tags(
        sentence=TEXT,
        topK=6,  # 提取的关键词数量
        allowPOS=['n', 'nz', 'ns'],  # 允许的关键词的词性
        withWeight=False,  # 是否附带词语权重
        withFlag=False,  # 是否附带词语词性
    )
    return keywords

# 用于保存所有整理后的内容
all_contents = []
# TODO: 增加处理不成功的处理方法&返回
def keyword_process(input_path):
    if isinstance(input_path, str):
        folder_path = input_path
        # 遍历文件夹里的所有 JSON 文件
        for filename in os.listdir(folder_path):
            if filename.endswith('_raw.json'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)  # 读取文件
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
                        # TEXT = item['content']
                        TEXT = advanced_clean(item['content'])
                        TEXT = re.sub(r'[\s\u2028\u2029]+', ' ', TEXT).strip()

                        # 从处理后的文本中应用 TF-IDF 算法提取关键词
                        keywords = keywords_extract(TEXT)
                        # 为data添加关键词字段
                        item['keywords'] = keywords

                    if 'title' in item:
                        item['title'] = advanced_clean(item['title'])

                # 新文件名，把 "_raw" 换成 "_cleaned"，如果没有 "_raw" 就直接加 "_cleaned"
                new_filename = filename.replace('_raw', '_reprocessed')
                new_file_path = os.path.join(folder_path, new_filename)

                # 写入新文件
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)  # 保存为格式化的 JSON

                print(f"已生成 {new_filename}")
        return True # success

    elif isinstance(input_path, list):
        que_list = input_path
        kw_list = []
        for que in que_list:
            kw = keywords_extract(que)
            print(kw)
            kw_list.append(kw)
        return kw_list
        


# folder_path = 'src/crawler/news_data'
folder_path= ['图书馆明天会举办的活动', '最近宿舍的热水供应时间']
keyword_process(folder_path)    # test line