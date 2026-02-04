#!/usr/bin/env python3
"""
阿森纳每日新闻收集脚本
收集指定日期的阿森纳俱乐部动态并生成文章
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sources.arsenal_official import ArsenalOfficial
from sources.sports_news import SportsNews
from sources.social_media import SocialMedia
from sources.other_sources import OtherSources
from utils.formatter import ArticleFormatter
from utils.image_handler import ImageHandler
from utils.wechat_push import WeChatPush


class ArsenalNewsCollector:
    def __init__(self, target_date=None):
        self.target_date = target_date or datetime.now().date()
        self.news_data = {
            'match': [],
            'transfer': [],
            'club': [],
            'player': [],
            'interview': []
        }
        self.images = []
        
        self.sources = [
            ArsenalOfficial(),
            SportsNews(),
            SocialMedia(),
            OtherSources()
        ]
        
        self.formatter = ArticleFormatter()
        self.image_handler = ImageHandler()
        self.wechat_push = WeChatPush()

    def collect_from_all_sources(self):
        for source in self.sources:
            try:
                print(f"正在从 {source.name} 收集数据...")
                data = source.collect(self.target_date)
                self.merge_data(data)
                print(f"✓ {source.name} 收集完成")
            except Exception as e:
                print(f"✗ {source.name} 收集失败: {str(e)}")

    def merge_data(self, data):
        for category in self.news_data:
            if category in data:
                self.news_data[category].extend(data[category])
        
        if 'images' in data:
            self.images.extend(data['images'])

    def deduplicate(self):
        seen = set()
        for category in self.news_data:
            unique_items = []
            for item in self.news_data[category]:
                key = f"{item.get('title', '')}{item.get('url', '')}"
                if key not in seen:
                    seen.add(key)
                    unique_items.append(item)
            self.news_data[category] = unique_items

    def sort_by_time(self):
        for category in self.news_data:
            self.news_data[category].sort(
                key=lambda x: x.get('timestamp', ''), 
                reverse=True
            )

    def generate_article(self):
        article = self.formatter.generate(
            date=self.target_date,
            news_data=self.news_data,
            images=self.images
        )
        return article

    def save_article(self, article):
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        
        filename = f"daily_news_{self.target_date.strftime('%Y%m%d')}.txt"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(article)
        
        print(f"✓ 文章已保存: {filepath}")
        return filepath

    def save_history(self):
        history_dir = Path('history')
        history_dir.mkdir(exist_ok=True)
        
        filename = f"{self.target_date.strftime('%Y%m%d')}.json"
        filepath = history_dir / filename
        
        history_data = {
            'date': self.target_date.isoformat(),
            'news': self.news_data,
            'images': self.images
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 历史记录已保存: {filepath}")

    def save_images(self):
        if not self.images:
            return
        
        image_dir = Path('images') / self.target_date.strftime('%Y%m%d')
        image_dir.mkdir(parents=True, exist_ok=True)
        
        for i, image_url in enumerate(self.images):
            try:
                image_path = self.image_handler.download(
                    image_url, 
                    image_dir / f"image_{i}.jpg"
                )
                print(f"✓ 图片已保存: {image_path}")
            except Exception as e:
                print(f"✗ 图片下载失败: {str(e)}")

    def push_to_wechat(self, article):
        try:
            self.wechat_push.push(article, self.target_date)
            print("✓ 已推送到微信公众号草稿箱")
        except Exception as e:
            print(f"✗ 推送失败: {str(e)}")

    def run(self, push_wechat=False, save_images=False):
        print(f"\n开始收集阿森纳 {self.target_date} 的新闻...")
        print("=" * 50)
        
        self.collect_from_all_sources()
        self.deduplicate()
        self.sort_by_time()
        
        print("\n生成文章...")
        article = self.generate_article()
        
        print("\n保存文件...")
        self.save_article(article)
        self.save_history()
        
        if save_images:
            print("\n下载图片...")
            self.save_images()
        
        if push_wechat:
            print("\n推送到微信公众号...")
            self.push_to_wechat(article)
        
        print("\n" + "=" * 50)
        print("✓ 所有任务完成！")


def main():
    parser = argparse.ArgumentParser(description='阿森纳每日新闻收集工具')
    parser.add_argument('--date', type=str, help='目标日期 (YYYY-MM-DD)')
    parser.add_argument('--type', type=str, help='只收集特定类型 (match/transfer/club/player/interview)')
    parser.add_argument('--push-wechat', action='store_true', help='推送到微信公众号')
    parser.add_argument('--save-images', action='store_true', help='下载图片')
    
    args = parser.parse_args()
    
    target_date = None
    if args.date:
        target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
    
    collector = ArsenalNewsCollector(target_date)
    
    if args.type:
        collector.sources = [source for source in collector.sources if args.type in source.categories]
    
    collector.run(push_wechat=args.push_wechat, save_images=args.save_images)


if __name__ == '__main__':
    main()