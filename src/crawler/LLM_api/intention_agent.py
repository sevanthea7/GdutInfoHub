
import json
from src.crawler.LLM_api.create_api_client import client

PROMPT = '解析用户的意图，把他的问题拆分为点，返回结果为JSON格式，形如{"1":"q1", "2": "q2",...}: '
def get_user_intension(user_text):
    input_text = PROMPT + user_text
    resp = client.chat.completions.create(
        model="doubao-1-5-lite-32k-250115",
        messages=[{"content":f"{input_text}.","role":"system"}],
        stream=False,
    )
    json_return = resp.choices[0].message.content
    # print(json_return)
    json_obj = json.loads(json_return)
    obj_lst = list(json_obj.values())
    # print(obj_lst)
    return obj_lst


test_text = "我想知道图书馆明天会举办的活动，以及最近宿舍的热水供应时间"
get_user_intension(test_text)