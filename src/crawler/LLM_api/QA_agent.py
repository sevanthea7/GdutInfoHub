from src.crawler.LLM_api.create_api_client import client


def get_QA_reply(info, question):
    if question == '':
        input_text = f"你是一个智慧问答机器人，用户没有输入问题，请提示用户输入问题。"
    elif len(info) == []:
        input_text =  f"你是一个智慧问答机器人，熟悉广东工业大学的各类通知，请用你已知的真实数据回答用户问题{question}（如果没有相关信息直接告诉用户没有相关信息，需要保证回答真实）。"
    else:
        input_text = f"你是一个智慧问答机器人，你知道的信息有“{info}”（注意这些信息当作是你本身已知的，回答过程中不要透露从文本分析之类的内容），请回答用户问题{question}。"
    resp = client.chat.completions.create(
        model="doubao-1-5-lite-32k-250115",
        messages=[{"content":f"{input_text}.","role":"user"}],
        stream=True,
    )

    for chunk in resp:
        if chunk.choices:
            delta = chunk.choices[0].delta.content or ""
            yield delta   # 流式部分

    # return full
