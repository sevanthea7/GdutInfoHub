import re
from datetime import datetime, timedelta

def extract_and_convert_time(input_sentences):
    """
    提取句子中的时间关键词，并转换为具体日期（mm月dd日格式）
    
    参数：
        input_sentences: list，输入的句子列表（如["明天图书馆有什么活动", "最近宿舍的热水供应时间"]）
    
    返回：
        list，每个元素为字典，包含句子、提取的时间关键词、转换后的具体日期
    """
    # 1. 定义时间关键词正则模式（覆盖直接日期、相对时间、模糊时间）
    # 直接日期：支持“11月13日”“十二月十号”“12-05”“2025年3月20日”等格式
    direct_date_pattern = r"""
    (?:\d{4}年)?                # 可选的年份（如2025年）
    (?:\d{1,2}月|十二|十一|十|九|八|七|六|五|四|三|二|一)  # 月份（数字或中文）
    (?:\d{1,2}日|\d{1,2}号|十|十一|十二|十三|十四|十五|十六|十七|十八|十九|二十|二十一|二十二|二十三|二十四|二十五|二十六|二十七|二十八|二十九|三十|三十一)  # 日期（数字或中文）
    |(?:\d{1,2}-\d{1,2})        # 短横线格式（如12-05）
    """
    
    # 相对时间关键词（映射为天数偏移）
    relative_time_map = {
        "今天": 0, "明天": 1, "后天": 2, "大后天": 3,
        "昨天": -1, "前天": -2, "大前天": -3,
        "本周": 0, "本周一": 0 - datetime.now().weekday(), "本周二": 1 - datetime.now().weekday(),
        "本周三": 2 - datetime.now().weekday(), "本周四": 3 - datetime.now().weekday(),
        "本周五": 4 - datetime.now().weekday(), "本周六": 5 - datetime.now().weekday(),
        "本周日": 6 - datetime.now().weekday()
    }
    
    # 模糊时间关键词（映射为日期范围）
    fuzzy_time_map = {
        "最近": (0, 7),    # 今天到7天后
        "近期": (0, 14),   # 今天到14天后
        "近几天": (0, 3),  # 今天到3天后
        "近一周": (0, 7),  # 今天到7天后
        "近两周": (0, 14), # 今天到14天后
        "近一个月": (0, 30)# 今天到30天后
    }
    
    # 合并所有时间关键词模式（忽略空格，使用VERBOSE模式）
    time_pattern = re.compile(
        rf"""
        ({direct_date_pattern}|{"|".join(re.escape(k) for k in relative_time_map.keys())}|{"|".join(re.escape(k) for k in fuzzy_time_map.keys())})
        """,
        re.VERBOSE | re.IGNORECASE
    )
    
    # 中文数字转阿拉伯数字（用于月份/日期转换）
    chinese_num_map = {
        "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
        "十": 10, "十一": 11, "十二": 12, "十三": 13, "十四": 14, "十五": 15,
        "十六": 16, "十七": 17, "十八": 18, "十九": 19, "二十": 20,
        "二十一": 21, "二十二": 22, "二十三": 23, "二十四": 24, "二十五": 25,
        "二十六": 26, "二十七": 27, "二十八": 28, "二十九": 29, "三十": 30, "三十一": 31
    }
    
    # 2. 处理每个句子
    result = []
    today = datetime.now().date()  # 当前日期（仅日期部分，忽略时间）
    
    for sentence in input_sentences:
        # 提取所有时间关键词（去重）
        time_keywords = list(set(time_pattern.findall(sentence)))
        converted_times = []
        
        for keyword in time_keywords:
            keyword = keyword.strip()
            
            # 3. 处理相对时间（如“明天”“昨天”）
            if keyword in relative_time_map:
                offset_days = relative_time_map[keyword]
                target_date = today + timedelta(days=offset_days)
                converted_times.append(target_date.strftime("%m月%d日"))
            
            # 4. 处理模糊时间（如“最近”“近一周”）
            elif keyword in fuzzy_time_map:
                start_offset, end_offset = fuzzy_time_map[keyword]
                start_date = today + timedelta(days=start_offset)
                end_date = today + timedelta(days=end_offset)
                converted_times.append(f"{start_date.strftime('%m月%d日')}-{end_date.strftime('%m月%d日')}")
            
            # 5. 处理直接日期（如“11月13日”“十二月十号”“12-05”）
            else:
                try:
                    # 处理短横线格式（如12-05）
                    if "-" in keyword:
                        month, day = map(int, keyword.split("-"))
                    # 处理点格式（如12.05）
                    if "." in keyword:
                        month, day = map(int, keyword.split("."))
                    else:
                        # 处理中文/数字混合格式（如“十二月十号”“11月13日”）
                        # 提取月份（替换“月”为分隔符）
                        month_part = re.search(r"(.*?)[月]", keyword).group(1) if "月" in keyword else ""
                        # 提取日期（替换“日”“号”为分隔符）
                        day_part = re.search(r"[月](.*?)[日号]", keyword).group(1) if any(c in keyword for c in ["日", "号"]) else ""
                        
                        # 中文数字转阿拉伯数字
                        month = chinese_num_map.get(month_part, int(month_part) if month_part.isdigit() else 1)
                        day = chinese_num_map.get(day_part, int(day_part) if day_part.isdigit() else 1)
                    
                    # 构造日期（年份默认为当前年）
                    target_date = datetime(today.year, month, day).date()
                    # 若日期已过（如当前12月，输入“1月5日”，自动视为明年）
                    if target_date < today and month < today.month:
                        target_date = datetime(today.year + 1, month, day).date()
                    converted_times.append(target_date.strftime("%m月%d日"))
                except (ValueError, AttributeError):
                    # 日期格式错误时，保留原关键词
                    converted_times.append(f"无法识别：{keyword}")
        
        # 整理结果
        # 包含原句对比，方便测试
        # result.append({
        #     "句子": sentence,
        #     "时间关键词": time_keywords,
        #     "具体时间": converted_times if converted_times else ["未提取到时间"]
        # })
            # 输入大模型
            result.append(converted_times)
    
    return result

# ------------------------------ 测试示例 ------------------------------
if __name__ == "__main__":
    # 测试输入句子列表
    test_sentences = [
        "明天图书馆有什么活动？",
        "最近宿舍的热水供应时间是几点？",
        "11月13日的讲座取消了吗？",
        "十二月十号有没有社团招新？",
        "昨天忘记去取快递了，后天能补取吗？",
        "近一周的食堂菜单会更新吗？",
        "2025年3月20日的会议地点在哪里？",
        "12-05的考试安排出来了吗？",
        "本周五下午有体育课吗？",
        "近一个月的天气预报怎么样？"
    ]
    
    # 执行时间提取与转换
    output = extract_and_convert_time(test_sentences)
    
    # 打印结果
    # for item in output:
    #     print("-" * 50)
    #     print(f"句子：{item['句子']}")
    #     print(f"时间关键词：{item['时间关键词']}")
    #     print(f"具体时间：{item['具体时间']}")
    print(output)

# 本周五识别结果为本周，待改进