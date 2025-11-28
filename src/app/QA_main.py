import json

from src.crawler.LLM_api.intention_agent import get_user_intension
from src.crawler.data_clean.time_trans import extract_and_convert_time
from src.crawler.LLM_api.QA_agent import get_info_core


def QA_func(qtext):
    qlist = get_user_intension(qtext)
    full_reply = ''
    for q in qlist:
        q = extract_and_convert_time(q)
        info = get_related_info() # TODO

        for delta in get_info_core(info, q):
            full_reply += delta
            yield delta

        yield "\n"  # 多问题之间

    end_json = {
        "code": 200,
        "msg": "success",
        "data": {
            "anwser": full_reply  # 最后给出完整内容
        }
    }
    yield json.dumps(end_json)