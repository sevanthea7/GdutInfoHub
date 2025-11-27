# 接口文档

## 1. 登录页

## 2. 首页

## 3. 对话页


响应体
```json
// 在这之前采用流式输出，最后的json用于标记结束
{
  "code": 200,  // 400文件错误、500捕获错误
  "msg": "success",
  "data": {
    "anwser": "xxx",    // 大模型回答完整内容
  }
}
```

## 4. 栏目页


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
