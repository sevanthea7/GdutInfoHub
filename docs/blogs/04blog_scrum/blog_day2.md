# Day2 Scrum冲刺博客

## 1. 团队会议

==todo补充会议照片==

### 1）昨天已完成的工作

- 前端
  - 前端项目初始化完成，实现了路由、菜单配置和登录页面
  - "关于我们"弹窗初步完成
- 后端
  - 完成了爬虫程序的初步实践
  - 产生了示例数据，用于后续的数据存储结构构建和数据清晰实践
- 测试
  - 完成了初步的测试计划，尝试部署了框架

### 2）今天计划完成的工作

- 前端
  - 实现个人设置弹窗以及问答模式静态页面，实现问答模式缓存
  - "关于我们"细节修正
- 后端
  - 完成爬虫数据的数据清洗
  - 增加爬虫程序适配的信息网站
- 测试
  - 检查各代码文件格式清晰性

### 3）工作中遇到的困难



## 2. 项目燃尽图

今日为第二天，已快于理想进度。

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202511252246614.png)



## 3.代码/文档签入记录

## 4. 运行截图

- 前端

  - 前端项目初始化完成

    

    ![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202511252257981.png)

- 后端

  - 数据爬取完成，存入JSON，JSON格式存在`docs\return_doc.md`

    - 爬虫模块更新代码

      ```python
      import requests
      from bs4 import BeautifulSoup
      from tool_func import save_json
      from urllib.parse import urljoin
      
      # 配置
      start_page = 'https://library.gdut.edu.cn/xwgg/xwdt.htm' 
      headers = {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
      }
      
      save_path = "src/crawler/news_data"
      news_type = 'library_news'
      
      def get_page_urls(page_url):    # 获取当前列表页的所有文章 URL、标题、日期
          resp = requests.get(page_url, headers=headers)
          resp.encoding = resp.apparent_encoding
          soup = BeautifulSoup(resp.text, "html.parser")
          
          articles = []
          for li in soup.select("div.lm_list ul li"):
              a_tag = li.find("a")
              span_tag = li.find("span")
              if a_tag and span_tag:
                  title = a_tag.text.strip()
                  href = urljoin(page_url, a_tag['href'])
                  date = span_tag.text.strip()
                  articles.append({
                      "title": title,
                      "url": href,
                      "date": date
                  })
          return articles
      
      def get_article_content(article_url):    # 获取文章正文内容
          resp = requests.get(article_url, headers=headers)
          resp.encoding = resp.apparent_encoding
          soup = BeautifulSoup(resp.text, "html.parser")
          
          content_div = soup.select_one("div.nr-info div.v_news_content")
          if content_div:
              paragraphs = [p.get_text(strip=True) for p in content_div.find_all("p")]
              content = "\n".join(paragraphs)
          else:
              content = ""
          return content
      
      def crawl_all_pages(start_url): # 抓取所有文章分页
          results = []
          next_page = start_url
          
          while next_page:
              print(f"抓取页面: {next_page}")
              articles = get_page_urls(next_page)
              for article in articles:
                  article["content"] = get_article_content(article["url"])
                  results.append(article)
              
              resp = requests.get(next_page, headers=headers)
              resp.encoding = resp.apparent_encoding
              soup = BeautifulSoup(resp.text, "html.parser")
              next_link = soup.select_one("span.p_next a")
              if next_link:
                  next_page = urljoin(next_page, next_link['href'])
              else:
                  next_page = None
          return results
      
      
      # test lines
      data = crawl_all_pages(start_page)
      save_json(save_path, news_type, data)
      
      ```

      

    ![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202511252257574.png)

  - 数据清洗完成，示例数据可见

    - 数据清洗更新代码

      ```python
      
      ```

      

  ![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202511252254952.png)

- 