# -*- coding: utf-8 -*-
"""
AI 行业日报 - 主程序
流程：Serper 搜昨日新闻 → 豆包筛选核验时间 → 生成 HTML → 发邮件
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

from config.settings    import CATEGORIES
from src.news_fetcher   import fetch_all
from src.ai_summarizer  import summarize_all
from src.html_generator import generate_html
from src.email_sender   import send_report

Path("logs").mkdir(exist_ok=True)
Path("cache").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/daily.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)
CACHE_FILE = Path("cache/last_daily.json")


def main(dry_run=False, no_fetch=False):
    start = datetime.now()
    logger.info("=" * 50)
    logger.info("开始生成 AI 日报 [%s]", start.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("=" * 50)

    if no_fetch and CACHE_FILE.exists():
        logger.info("使用缓存数据")
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
        summarized = cache["summarized"]
    else:
        # Step 1: 抓取昨日新闻
        logger.info("Step 1/3: Serper 抓取昨日新闻...")
        raw_news = fetch_all(CATEGORIES)

        # Step 2: 豆包筛选 + 核验时间
        logger.info("Step 2/3: 豆包筛选核验时间...")
        summarized = summarize_all(CATEGORIES, raw_news)

        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({"summarized": summarized}, f, ensure_ascii=False, indent=2)

    total = sum(len(v) for v in summarized.values())
    logger.info("共保留 %d 条新闻", total)

    if total == 0:
        logger.warning("没有有效新闻，跳过生成")
        return

    # Step 3: 生成 HTML
    logger.info("Step 3/3: 生成 HTML...")
    html_path = generate_html(CATEGORIES, summarized)
    logger.info("已保存: %s", html_path)

    # 发送邮件
    if dry_run:
        logger.info("dry-run，跳过邮件发送，HTML 文件在: %s", html_path)
    else:
        logger.info("发送邮件...")
        send_report(html_path)

    logger.info("完成！耗时 %d 秒", (datetime.now() - start).seconds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run",  action="store_true", help="不发邮件，只生成 HTML")
    parser.add_argument("--no-fetch", action="store_true", help="用缓存数据，不重新抓取")
    args = parser.parse_args()
    main(dry_run=args.dry_run, no_fetch=args.no_fetch)
