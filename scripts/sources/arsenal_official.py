#!/usr/bin/env python3
"""
阿森纳官网数据源
从 arsenal.com 获取官方新闻
"""

import feedparser
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


class ArsenalOfficial:
    name = "阿森纳官网"
    categories = ['match', 'transfer', 'club', 'player', 'interview']
    
    def __init__(self):
        self.rss_url = "https://www.arsenal.com/news/feed"
        self.base_url = "https://www.arsenal.com"
    
    def collect(self, target_date):
        news_data = {
            'match': [],
            'transfer': [],
            'club': [],
            'player': [],
            'interview': []
        }
        images = []
        
        try:
            feed = feedparser.parse(self.rss_url)
            
            for entry in feed.entries:
                entry_date = self._parse_date(entry.published)
                
                if not self._is_same_day(entry_date, target_date):
                    continue
                
                category = self._categorize(entry.title, entry.description)
                if category not in self.categories:
                    continue
                
                news_item = {
                    'title': entry.title,
                    'url': entry.link,
                    'description': self._extract_description(entry.description),
                    'timestamp': entry_date.isoformat(),
                    'source': '阿森纳官网'
                }
                
                image_url = self._extract_image(entry.description)
                if image_url:
                    images.append(image_url)
                    news_item['image'] = image_url
                
                news_data[category].append(news_item)
        
        except Exception as e:
            print(f"获取阿森纳官网数据失败: {str(e)}")
        
        return {
            **news_data,
'images': images
        }
    
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
        soup = BeautifulSoup(description, 'html.parser')
        text = soup.get_text(strip=True)
        return text[:200] + '...' if len(text) > 200 else text
    
    def _extract_image(self, description):
        soup = BeautifulSoup(description, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            return img.get('src')
        return None
    
    def _categorize(self, title, description):
        title_lower = title.lower()
        desc_lower = description.lower()
        
        match_keywords = ['match', 'game', 'win', 'draw', 'loss', 'score', 'goal', 'premier league', 'fa cup', 'champions league']
        transfer_keywords = ['sign', 'contract', 'transfer', 'deal', 'loan', 'extend', 'renew']
        player_keywords = ['injury', 'fitness', 'training', 'squad', 'player']
        interview_keywords = ['interview', 'press conference', 'says', 'speaks', 'talks']
        
        for keyword in match_keywords:
            if keyword in title_lower or keyword in desc_lower:
                return 'match'
        
        for keyword in transfer_keywords:
            if keyword in title_lower or keyword in desc_lower:
                return 'transfer'
        
        for keyword in player_keywords:
            if keyword in title_lower or keyword in desc_lower:
                return 'player'
        
        for keyword in interview_keywords:
            if keyword in title_lower or keyword in desc_lower:
                return 'interview'
        
        return 'club'