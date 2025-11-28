from flask import Flask, Response, request, jsonify
from src.app.QA_main import QA_func

app = Flask(__name__)
    

@app.route("/api/stream", methods=["POST"])
def api_stream():
    try:
        # 1. 接收 JSON
        # req = request.get_json()

        # if not req or "data" not in req:
        #     return jsonify({"code": 400, "msg": "JSON不合法", "data": None})

        # data = req["data"]
        # question = data.get("question")

        # # 参数校验
        # if question is None:
        #     return jsonify({"code": 400, "msg": "消息为空", "data": None})

        prompt = request.json["prompt"]
        return Response(QA_func(prompt), mimetype="text/plain")

    except Exception as e:
        # 捕获错误
        return jsonify({"code": 500, "msg": str(e), "data": None})
    

@app.route("/api/notices", methods=["GET"])
def notices():
    # 规定请求体后完成
    # return jsonify({
    #     "code": 200,
    #     "msg": "success",
    #     "data": {"items": items}
    # })
    pass

if __name__ == "__main__":
    app.run(port=5000, debug=True)
