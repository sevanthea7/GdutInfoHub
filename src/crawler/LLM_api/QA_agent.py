from src.crawler.LLM_api.create_api_client import client


def get_info_core(info, question):
    input_text = f"已知{info}，请告诉我{question}"
    resp = client.chat.completions.create(
        model="doubao-1-5-lite-32k-250115",
        messages=[{"content":f"{input_text}.","role":"user"}],
        stream=True,
    )

    full = ''
    for chunk in resp:
        if chunk.choices:
            delta = chunk.choices[0].delta.content or ""
            full += delta
            yield delta   # 流式部分

    # return full
