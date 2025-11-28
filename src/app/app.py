from flask import Flask, Response, request, jsonify
from src.app.QA_main import QA_func
from src.app.search_by_label import search_news_by_label

app = Flask(__name__)

DATA_DIR = 'src/crawler/news_data'

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


@app.route("/api/notices", methods=["GET"])
def api_notices():
    items = search_news_by_label('通知公告', DATA_DIR)
    return jsonify({"code": 200,
                    "msg": "success", 
                    "data": {
                        "items": items
                        }
                    })

@app.route("/api/teaching_notices", methods=["GET"])
def api_teaching_notices():
    items = search_news_by_label('教务信息', DATA_DIR)
    return jsonify({"code": 200,
                    "msg": "success", 
                    "data": {
                        "items": items
                        }
                    })

@app.route("/api/service_notices", methods=["GET"])
def api_service_notices():
    items = search_news_by_label('水电服务', DATA_DIR)
    return jsonify({"code": 200,
                    "msg": "success", 
                    "data": {
                        "items": items
                        }
                    })

@app.route("/api/maintainance_notices", methods=["GET"])
def api_maintainance_notices():
    items = search_news_by_label('后勤报修', DATA_DIR)
    return jsonify({"code": 200,
                    "msg": "success", 
                    "data": {
                        "items": items
                        }
                    })
    

if __name__ == "__main__":
    print("Flask starting...")
    app.run(port=5000, debug=True)

