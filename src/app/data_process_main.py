from src.crawler.LLM_api.label_agent import create_database_JSON
from src.crawler.data_clean.reprocess import keyword_process
from src.crawler.library import crawl_library_func

SAVE_PATH = "src/crawler/news_data"

def data_process_func(save_path):
    crawl_library_func(save_path)
    keyword_process(save_path)
    create_database_JSON(save_path)
    print('知识库信息已更新')


data_process_func(SAVE_PATH)