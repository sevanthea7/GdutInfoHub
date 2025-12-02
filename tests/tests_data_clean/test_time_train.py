import sys
import os
from datetime import datetime, timedelta
import pytest

# 把项目根目录加入Python路径，确保能导入src里的time_trans.py
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# 导入你原代码中的函数（路径对应图1的time_trans.py）
from src.crawler.data_clean.time_trans import extract_and_convert_time


# ---------------------- 测试用例（覆盖你提到的场景） ----------------------
def test_relative_time_friday():
    """测试“本周五”的转换（你提到的待改进场景）"""
    input_sent = "本周五下午有体育课吗？"
    # 调用你的函数
    result = extract_and_convert_time(input_sent)
    # 预期结果（基于当前日期2025-12-01，本周五是12月05日）
    expected = "12月05日下午有体育课吗？"
    print(f"\n原句：{input_sent}")
    print(f"你的代码输出：{result}")
    print(f"预期输出：{expected}")
    # 断言（即使失败，也会显示对比）
    assert result == expected


def test_direct_date_chinese():
    """测试“十二月十号”的转换"""
    input_sent = "十二月十号有没有社团招新？"
    result = extract_and_convert_time(input_sent)
    expected = "12月10号有没有社团招新？"
    print(f"\n原句：{input_sent}")
    print(f"你的代码输出：{result}")
    print(f"预期输出：{expected}")
    assert result == expected


def test_relative_time_tomorrow():
    """测试“明天”的转换（预期能正常工作）"""
    input_sent = "明天图书馆有什么活动？"
    tomorrow_date = (datetime.now().date() + timedelta(days=1)).strftime("%m月%d日")
    result = extract_and_convert_time(input_sent)
    expected = f"{tomorrow_date}图书馆有什么活动？"
    print(f"\n原句：{input_sent}")
    print(f"你的代码输出：{result}")
    print(f"预期输出：{expected}")
    assert result == expected


def test_fuzzy_time_recent():
    """测试“最近”的转换（预期能正常工作）"""
    input_sent = "最近宿舍的热水供应时间是几点？"
    today = datetime.now().date().strftime("%m月%d日")
    next_7 = (datetime.now().date() + timedelta(days=7)).strftime("%m月%d日")
    expected = f"{today}-{next_7}宿舍的热水供应时间是几点？"
    result = extract_and_convert_time(input_sent)
    print(f"\n原句：{input_sent}")
    print(f"你的代码输出：{result}")
    print(f"预期输出：{expected}")
    assert result == expected


