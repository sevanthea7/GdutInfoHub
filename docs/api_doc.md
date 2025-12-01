# 接口文档

## 1. 对话页

请求方式：post

请求体 body 传参

```json
{
  "question": "xxx" // 用户输入的问题
}
```

响应体

```json
// 在这之前采用流式输出，最后的json用于标记结束
{
  "code": 200, // 400文件错误、500捕获错误
  "msg": "success",
  "data": {
    "anwser": "xxx" // 大模型回答完整内容
  }
}
```

## 2. 栏目页
### 接口请求说明
- **请求方式**：GET  
- **请求参数**：无需参数  


### 响应数据示例  

#### 1. 通知公告页面  
```json
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
```

#### 2. 其他三个页面  
```json
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


### 字段说明  
| 字段         | 说明                     |
| ------------ | ------------------------ |
| `title`      | 内容标题                 |
| `url`        | 内容详情链接             |
| `date`       | 发布日期                 |
| `content`    | 内容详情                 |
| `department` | 发布部门                 |
| `column`     | （仅通知公告类）不同栏目 |




## 3. 本地网络接口示例

- 问答模块
  - http://127.0.0.1:5000/api/stream

- 栏目模块
  - 通知公告：http://127.0.0.1:5000/api/notices
  - 教务信息：http://127.0.0.1:5000/api/teaching_notices
  - 水电服务：http://127.0.0.1:5000/api/service_notices
  - 水电服务：http://127.0.0.1:5000/api/maintainance_notices