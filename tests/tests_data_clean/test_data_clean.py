import json
import re
import os

# 从tests文件夹，先回到GdutInfoHub根目录，再进入src/crawler/news_data
folder_path = '../src/crawler/news_data'  # 关键：适配tests的路径

# 测试逻辑（和原clean.py功能一致，也可以加额外校验）
def test_clean_json():
    for filename in os.listdir(folder_path):
        if filename.endswith('_raw.json'):
            file_path = os.path.join(folder_path, filename)
            # 读取原文件
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f" {filename} 不是有效JSON，跳过")
                    continue

            # 执行清洗
            if 'content' in data:
                original_content = data['content']
                cleaned_content = re.sub(r'[\s\u2028\u2029]+', ' ', original_content).strip()
                data['content'] = cleaned_content
                # 额外校验：清洗是否生效
                assert len(cleaned_content) > 0 and '\n' not in cleaned_content, f"❌ {filename} 清洗失败"

            # 生成cleaned文件
            new_filename = filename.replace('_raw', '_cleaned')
            new_file_path = os.path.join(folder_path, new_filename)
            with open(new_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f" 已生成 {new_filename}（清洗完成）")

# 运行测试
if __name__ == '__main__':
    test_clean_json()