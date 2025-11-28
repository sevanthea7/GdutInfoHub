from src.crawler.LLM_api.create_api_client import client


def get_QA_reply(info, question):
    input_text = f"你是一个智慧问答机器人，你知道的信息有“{info}”，请回答用户{question}。"
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
