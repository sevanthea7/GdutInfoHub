from flask import Flask, Response, request, jsonify
from src.app.QA_main import QA_func

app = Flask(__name__)

@app.route("/api/stream", methods=["POST"])
def api_stream():
    try:
        # 检查是否能解析成 JSON
        req_json = request.get_json(silent=True)
        if req_json is None:
            return jsonify({"code": 400, "msg": "请求体不是合法JSON！", "data": None})

        # 检查字段是否存在
        if "question" not in req_json:
            return jsonify({"code": 400, "msg": "缺少字段 'question'", "data": None})

        # 检查question是否为空
        question = req_json["question"]
        if not isinstance(question, str) or question.strip() == "":
            return jsonify({"code": 400, "msg": "字段 'question' 必须是非空字符串", "data": None})

        return Response(QA_func(question), mimetype="text/plain")

    except Exception as e:
        # 捕获所有错误
        return jsonify({"code": 500, "msg": f"传输错误: {str(e)}", "data": None})


@app.route("/api/notices", methods=["POST"])
def notices():
    # 规定请求体后完成
    # return jsonify({
    #     "code": 200,
    #     "msg": "success",
    #     "data": {"items": items}
    # })
    pass

if __name__ == "__main__":
    print("Flask starting...")
    app.run(port=5000, debug=True)

