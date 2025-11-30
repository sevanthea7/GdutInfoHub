import json

from src.crawler.LLM_api.intention_agent import get_user_intension
from src.crawler.LLM_api.QA_agent import get_QA_reply
from src.crawler.data_clean.time_trans import extract_and_convert_time
from src.crawler.data_clean.keyword_extractor import search_news_by_keywords
from src.crawler.data_clean.reprocess import keyword_process

def QA_func(qtext, DATA_DIR):
    qlist = get_user_intension(qtext)
    full_reply = ''
    for q in qlist:
        q = extract_and_convert_time(q)                 # 将用户问题中的模糊时间转换成具体日期格式
        kw = keyword_process(q, is_path=False)          # 提取用户提问中的关键词
        info = search_news_by_keywords(kw, DATA_DIR)    # 根据关键词在数据中找到相关内容

        for delta in get_QA_reply(info, q):
            full_reply += delta
            yield delta

        yield "\n"  # 多问题之间

    # end_json = {
    #     "code": 200,
    #     "msg": "success",
    #     "data": {
    #         "anwser": full_reply  # 最后给出完整内容
    #     }
    # }
    # yield json.dumps(end_json)

# for chunk in QA_func('举办过哪些校友相关的活动？'):
#     print(chunk, end='')