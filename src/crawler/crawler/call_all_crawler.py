from src.crawler.crawler.library import crawl_library_func
from src.crawler.crawler.notice import crawl_notice_func
from src.crawler.crawler.sports import crawl_sports_func
from src.crawler.crawler.art import crawl_art_func
from src.crawler.crawler.party import crawl_party_func

def crawl_all_sources(save_path, target="all"):
    CRAWLER_MAP = {
        "library": crawl_library_func,
        "notice": crawl_notice_func,
        "sports": crawl_sports_func,
        "art": crawl_art_func,
        "party": crawl_party_func,
    }

    # results = {}

    # 调用全部
    if target == "all":
        for name, func in CRAWLER_MAP.items():
            print(f"\n开始爬取：{name}")
            try:
                func(save_path)
            except Exception as e:
                print(f"[错误] {name} 爬取失败：{e}")
        # return results

    # 调用指定模块
    if target in CRAWLER_MAP:
        print(f"\n开始爬取：{target}")
        try:
            CRAWLER_MAP[target](save_path)
        except Exception as e:
            print(f"[错误] {target} 爬取失败：{e}")
        # return results

    # 传入的 target 无效
    raise ValueError(f"未知的模块 '{target}'，可选：{list(CRAWLER_MAP.keys()) + ['all']}")