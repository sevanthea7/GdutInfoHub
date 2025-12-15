# Day5 Scrum冲刺博客

## 1. 团队会议

因为各成员有不同的课程与实习安排，难以找到大家都在的线下时间，所以采用线上会议代替站立式会议。

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512031043184.png)

### 1）昨天已完成的工作

- 前端
  - 初步完成了四个通知栏目页的搭建
- 后端
  - 完成了数据库建立的完整流程
  - 完成了时间信息的提取函数
  - 规定了部分接口格式
- 测试
  - 检查新加入各代码文件格式清晰性
  - 准备开始测试

### 2）今天计划完成的工作

- 前端
  - 完成请求体与接口规定
  - 前后端初步尝试对接联调
- 后端
  - 完成了适配更多网站的爬虫程序
  - 完成了问答接口的本地调试
- 测试
  - 初步完成多个功能的测试代码

### 3）工作中遇到的困难

- 前端
  - 联调过程中统一对接的json格式。
- 后端
  - 不同网站页面结构差异较大，爬虫在适配新站点时需要针对每个网站单独处理。
- 测试
  - 在编写测试代码时发现部分功能的输入输出规范尚未完全固定，需要调整测试用例。

## 2. 项目燃尽图

今日为第五天，已快于理想进度。

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202511281838482.png)

## 3.代码/文档签入记录

- 今日签入记录

  ![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202511282157846.png)

- 签入记录链接：https://github.com/sevanthea7/GdutInfoHub/commits/main/

- 相关联issue见commit记录中`#`后链接内容

  - 相关任务链接：

    https://github.com/sevanthea7/GdutInfoHub/issues/4

    https://github.com/sevanthea7/GdutInfoHub/issues/5

    https://github.com/sevanthea7/GdutInfoHub/issues/6

    https://github.com/sevanthea7/GdutInfoHub/issues/13

    https://github.com/sevanthea7/GdutInfoHub/issues/16

    https://github.com/sevanthea7/GdutInfoHub/issues/26

- 接口文档与返回格式文档见 `docs/api_doc.md` 与 `docs/return_doc.md`

  更新：确定了问答&表单模式接口格式

  ```json
  // 1. 问答模式
  // 请求体 body 传参
  
  {
    "question": "xxx" // 用户输入的问题
  }
  
  // 响应体
  
  // 在这之前采用流式输出，最后的json用于标记结束
  {
    "code": 200, // 400文件错误、500捕获错误
    "msg": "success",
    "data": {
      "anwser": "xxx" // 大模型回答完整内容
    }
  }
  
  // 2.表单模式
  //1) 通知公告页面
  
  {
    "code": 200,
    "msg": "success",
    "data": {
      "items": [
        {
          "title": "图书馆召开党总支理论学习中心组学习会",
          "url": "https://library.gdut.edu.cn/info/1128/1917.htm",
          "date": "2025/11/13",
          "content": "11月10日，图书馆召开党总支理论学习中心组学习会，深入学习贯彻习近平新时代中国特色社会主义思想，聚焦高质量发展主题，全体中心组成员参加会议，会议由党总支书记主持。会上，大家围绕学习内容结合工作实际进行了交流研讨，明确了下一步工作方向。",
          "department": "图书馆",
          "column": "图书馆讯/体育馆讯/通识公告/党建快讯"
        },
        ...
      ]
    }
  }
  
  //2) 其他三个页面
  
  {
    "code": 200,
    "msg": "success",
    "data": {
      "items": [
        {
          "title": "图书馆召开党总支理论学习中心组学习会",
          "url": "https://library.gdut.edu.cn/info/1128/1917.htm",
          "date": "2025/11/13",
          "content": "...",
          "department": "图书馆"
        },
        ...
      ]
    }
  }
  ```

  

## 4. 运行截图

- 前端

  - 规定前后端交互方式，尝试对接

    - 相关规定见上方api_doc内容

  - 表单模式模拟后台输入，以教务信息为例
  
    ```javascript
    import academicInfoMock from "./mockAcademicData";
    //模拟API请求函数
    export const noticeApi = {
    // 获取教务信息通知
    getAcademicInfo: () => {
    		// 实际项目中这里会是真实的API请求
    	    // return axios.get('/api/academic-info');
    		return new Promise((resolve) => {
    		setTimeout(() => {
    		resolve(academicInfoMock);
    		}, 500); // 模拟网络延迟
    	});
    	},
    };
    ```
  
    
  
- 后端

  - 实现了关键词与数据库中关键词的匹配算法

    ```python
import json
    import os
    
    
    def search_news_by_keywords(keywords, folder_path):
        matched_contents = []
        for filename in os.listdir(folder_path):
            if filename.endswith('_database.json'):     # 读取所有结尾是_database的文件
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)  # 读取文件
                    except json.JSONDecodeError:
                        print(f"文件 {filename} 不是有效 JSON，跳过")
                        continue
    
                # 筛选匹配关键词的新闻，并提取 content
                for news in data:
                    # 检查新闻是否包含 keywords 字段，且为列表类型
                    news_keywords = news.get("keywords", [])
                    if not isinstance(news_keywords, list):
                        continue
    
                    # 计算输入关键词和新闻关键词的交集（判断是否有共同关键词）
                    common_keywords = set(keywords) & set(news_keywords)
                    if common_keywords:  # 有共同关键词则视为匹配
                        # 提取 content 字段
                        content = news.get("content", "")
                        if isinstance(content, str):
                            matched_contents.append(content)
        kw = '、'.join(keywords)
        num_kw = len(matched_contents)
        print(f'查找到 {kw} 相关内容共 {num_kw} 条！')
        return matched_contents
    ```
    
    
    
    ![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202511281639069.png)
    
  - 问答接口的本地调试
  
    ```python
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
    ```
    
  
  ![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202511282207365.png)
  
  

## 5. 每人每日总结

- 前端
  - 张洁：今天完成了请求体结构与接口规范的整理与编写，进一步明确了字段命名和数据格式要求。同时对现有页面请求逻辑进行了梳理，为后续联调阶段减少通信歧义提供了保障。
  - 吴佳童：参与前后端初步联调，对多个接口的请求与返回进行了验证。在调试过程中发现部分参数类型与后端定义不一致，并主动协助沟通修正，推动了联调流程的顺利进行。
  - 李恺凝：协助完成前后端联调，对页面与接口的整体调用链进行了测试验证。过程中排查了初次数据不通的问题，并对相关前端逻辑进行了小幅优化，使接口调用流程更加稳定。
- 后端
  - 王韵清：完善了爬虫程序对更多网站的适配规则，包括页面结构分析、字段提取和异常情况处理。针对部分结构复杂的站点进行了额外调试，提升了爬虫的通用性和数据抓取成功率。
  - 曾钰仪：完成了问答接口的本地调试工作，重点检查了提示词处理、参数构造及返回格式。在调试过程中修复了若干输入校验问题，使接口整体逻辑更加严谨。
  - 徐伊彤：协助调试问答接口，对请求流程、数据传输、错误响应等环节进行了细致检查。对可能导致异常的字段缺失问题进行了补充处理，使接口输出表现更加稳定可靠。
- 测试
  - 戴军霞：编写了多个功能模块的初步测试代码，覆盖了核心功能、接口调用及常见边界情况。整理了测试数据与预期输出，为后续更系统化的集成测试奠定基础。

