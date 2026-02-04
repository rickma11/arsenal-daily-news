#!/usr/bin/env python3
"""
其他数据源
可以从自定义的 RSS 或 API 获取数据
"""

import os
import feedparser
import requests
from datetime import datetime


class OtherSources:
    name = "其他来源"
    categories = ['match', 'transfer', 'club', 'player', 'interview']
    
    def __init__(self):
        self.custom_rss_urls = os.getenv('CUSTOM_RSS_URLS', '').split(',')
        self.custom_api_urls = os.getenv('CUSTOM_API_URLS', '').split(',')
    
    def collect(self, target_date):
        news_data = {
            'match': [],
            'transfer': [],
            'club': [],
            'player': [],
            'interview': []
        }
        images = []
        
        for rss_url in self.custom_rss_urls:
            if not rss_url.strip():
                continue
            
            try:
                print(f"  - 正在从 RSS 获取数据: {rss_url[:50]}...")
                items = self._parse_rss(rss_url, target_date)
                
                for item in items:
                    category = item.get('category', 'club')
                    if category in news_data:
                        news_data[category].append(item)
                    
                    if 'image' in item:
                        images.append(item['image'])
                
                print(f"  - ✓ RSS 获取完成 ({len(items)} 条)")
                
            except Exception as e:
                print(f"  - ✗ RSS 获取失败: {str(e)}")
        
        return {
            **news_data,
'images': images
        }
    
    def _parse_rss(self, rss_url, target_date):
        items = []
        
        try:
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries:
                entry_date = self._parse_date(entry.published)
                
                if not self._is_same_day(entry_date, target_date):
                    continue
                
                category = self._categorize(entry.title, entry.description)
                
                item = {
                    'title': entry.title,
                    'url': entry.link,
                    'description': self._extract_description(entry.description),
                    'timestamp': entry_date.isoformat(),
                    'source': feed.feed.get('title', '自定义来源'),
                    'category': category
                }
                
                image_url = self._extract_image(entry.description)
                if image_url:
                    item['image'] = image_url
                
                items.append(item)
        
        except Exception as e:
            print(f"解析 RSS 失败: {str(e)}")
        
        return items
    
    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        except:
            try:
                return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            except:
                return datetime.now()
    
    def _is_same_day(self, date1, date2):
        return date1.date() == date2
    
    def _extract_description(self, description):
        if not description:
            return ''
        
        text = description.strip()
        return text[:200] + '...' if len(text) > 200 else text
    
    def _extract_image(self, description):
        if not description:
            return None
        
        if '<img' in description:
            import re
            img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', description)
            if img_match:
                return img_match.group(1)
        
        return None
    
    def _categorize(self, title, description):
        text = f"{title} {description}".lower()
        
        match_keywords = ['match', 'game', 'win', 'draw', 'loss', 'score', 'goal', 'premier league', 'fa cup', 'champions league']
        transfer_keywords = ['sign', 'contract', 'transfer', 'deal', 'loan', 'extend', 'renew']
        player_keywords = ['injury', 'fitness', 'training', 'squad', 'player']
        interview_keywords = ['interview', 'press conference', 'says', 'speaks', 'talks']
        
        for keyword in match_keywords:
            if keyword in text:
                return 'match'
        
        for keyword in transfer_keywords:
            if keyword in text:
                return 'transfer'
        
        for keyword in player_keywords:
            if keyword in text:
                return 'player'
        
        for keyword in interview_keywords:
            if keyword in text:
                return 'interview'
        
        return 'club'