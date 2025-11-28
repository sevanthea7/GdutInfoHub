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
        "key_words": ["图书馆", "理论学习", "专题党课"],
        "label": "校园通知/学术活动/行政通知/社区公告",
        "department": "图书馆"
      },
      {
        "title": "2025年度学术讲座安排公示",
        "url": "https://academic.gdut.edu.cn/info/2025/lecture.htm",
        "date": "2025/11/12",
        "content": "...",
        "key_words": ["学术讲座", "专家", "报名"],
        "label": "学术活动",
        "department": "科研处"
      }
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
        "key_words": ["图书馆", "理论学习", "专题党课"],
        "department": "图书馆"
      },
      {
        "title": "2025年度学术讲座安排公示",
        "url": "https://academic.gdut.edu.cn/info/2025/lecture.htm",
        "date": "2025/11/12",
        "content": "...",
        "key_words": ["学术讲座", "专家", "报名"],
        "department": "科研处"
      }
    ]
  }
}
```


### 字段说明  
| 字段        | 说明                                                                 |
|-------------|----------------------------------------------------------------------|
| `title`     | 内容标题                                                             |
| `url`       | 内容详情链接                                                         |
| `date`      | 发布日期                                                             |
| `content`   | 内容详情                                                             |
| `key_words` | 关键词列表（部分场景未实际使用）                                     |
| `label`     | 内容标签（仅通知公告页面返回，其他页面无此字段）                     |
| `department`| 发布部门                                                             |
```

响应体

```json
// eg.通知公告
{
  "code": 200,
  "msg": "success",
  "data": {
    "items": [
      {
        "title": "图书馆召开党总支理论学习中心组学习会",
        "url": "https://library.gdut.edu.cn/info/1128/1917.htm",
        "date": "2025/11/13",
        "content": "xxx",
        "key_words": ["图书馆", "理论学习", "专题党课"],
        "label": "通知公告"
      },
      {
        "title": "xxx",
        "url": "xxx.htm",
        "date": "2025/11/13",
        "content": "xxx",
        "key_words": ["xxx", "xxx", "xxx"],
        "label": "通知公告"
      },
      ...
    ]
  }
}

```
