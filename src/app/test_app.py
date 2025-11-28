import requests

url = "http://127.0.0.1:5000/api/stream"

payload = {
    "question": "我们学校举办过哪些校友相关的活动？"
}

# stream=True 开启流式接收
with requests.post(url, json=payload, stream=True) as r:
    # 检查是否成功
    if r.status_code != 200:
        print("请求失败:", r.status_code, r.text)
    else:
        print("开始接收流式输出：\n")
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                print(chunk.decode("utf-8"), end="")  # 边接收边输出
