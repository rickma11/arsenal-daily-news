#!/usr/bin/env python3
"""
体育新闻网站数据源
从 ESPN、BBC Sport、Sky Sports 获取阿森纳相关新闻
"""

import requests
from datetime import datetime
from bs4 import BeautifulSoup


class SportsNews:
    name = "体育新闻网站"
    categories = ['match', 'transfer', 'club', 'player', 'interview']
    
    def __init__(self):
        self.sources = {
            'ESPN': {
                'url': 'https://www.espn.com/soccer/team/_/id/359/arsenal/news',
                'parser': self._parse_espn
            },
            'BBC Sport': {
                'url': 'https://www.bbc.co.uk/sport/football/teams/arsenal',
                'parser': self._parse_bbc
            },
            'Sky Sports': {
                'url': 'https://www.skysports.com/football/teams/arsenal',
                'parser': self._parse_sky
            }
        }
    
    def collect(self, target_date):
        news_data = {
            'match': [],
            'transfer': [],
            'club': [],
            'player': [],
            'interview': []
        }
        images = []
        
        for source_name, source_info in self.sources.items():
            try:
                print(f"  - 正在从 {source_name} 获取数据...")
                response = requests.get(source_info['url'], timeout=10)
                response.raise_for_status()
                
                items = source_info['parser'](response.text, target_date)
                
                for item in items:
                    category = item.get('category', 'club')
                    if category in news_data:
                        news_data[category].append(item)
                    
                    if 'image' in item:
                        images.append(item['image'])
                
                print(f"  - ✓ {source_name} 获取完成 ({len(items)} 条)")
                
            except Exception as e:
                print(f"  - ✗ {source_name} 获取失败: {str(e)}")
        
        return {
            **news_data,
'images': images
        }
    
    def _parse_espn(self, html, target_date):
        soup = BeautifulSoup(html, 'html.parser')
        items = []
        
        articles = soup.find_all('article', class_='article-item')
        for article in articles:
            title_elem = article.find('h1')
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            link_elem = article.find('a')
            url = link_elem.get('href') if link_elem else ''
            
            time_elem = article.find('time')
            if time_elem:
                timestamp = self._parse_time(time_elem.get('datetime', ''))
                if not self._is_same_day(timestamp, target_date):
                    continue
            else:
                continue
            
            category = self._categorize(title)
            
            items.append({
                'title': title,
                'url': f"https://www.espn.com{url}" if url.startswith('/') else url,
                'description': self._extract_description(article),
                'timestamp': timestamp.isoformat(),
                'source': 'ESPN',
                'category': category
            })
        
        return items
    
    def _parse_bbc(self, html, target_date):
        soup = BeautifulSoup(html, 'html.parser')
        items = []
        
        articles = soup.find_all('div', class_='gs-c-promo')
        for article in articles:
            title_elem = article.find('h3')
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            link_elem = article.find('a')
            url = link_elem.get('href') if link_elem else ''
            
            time_elem = article.find('span', class_='gs-o-bullet__text')
            if time_elem:
                time_text = time_elem.get_text(strip=True)
                timestamp = self._parse_relative_time(time_text)
                if not self._is_same_day(timestamp, target_date):
                    continue
            else:
                continue
            
            category = self._categorize(title)
            
            items.append({
                'title': title,
                'url': f"https://www.bbc.co.uk{url}" if url.startswith('/') else url,
                'description': self._extract_description(article),
                'timestamp': timestamp.isoformat(),
                'source': 'BBC Sport',
                'category': category
            })
        
        return items
    
    def _parse_sky(self, html, target_date):
        soup = BeautifulSoup(html, 'html.parser')
        items = []
        
        articles = soup.find_all('div', class_='news-list__item')
        for article in articles:
            title_elem = article.find('h3')
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            link_elem = article.find('a')
            url = link_elem.get('href') if link_elem else ''
            
            time_elem = article.find('time')
            if time_elem:
                timestamp = self._parse_time(time_elem.get('datetime', ''))
                if not self._is_same_day(timestamp, target_date):
                    continue
            else:
                continue
            
            category = self._categorize(title)
            
            items.append({
                'title': title,
                'url': f"https://www.skysports.com{url}" if url.startswith('/') else url,
                'description': self._extract_description(article),
                'timestamp': timestamp.isoformat(),
                'source': 'Sky Sports',
                'category': category
            })
        
        return items
    
    def _parse_time(self, time_str):
        try:
            return datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
        except:
            return datetime.now()
    
    def _parse_relative_time(self, time_str):
        now = datetime.now()
        
        if 'hour' in time_str:
            hours = int(''.join(filter(str.isdigit, time_str)))
            return now - timedelta(hours=hours)
        elif 'minute' in time_str:
            minutes = int(''.join(filter(str.isdigit, time_str)))
            return now - timedelta(minutes=minutes)
        elif 'yesterday' in time_str.lower():
            return now - timedelta(days=1)
        
        return now
    
    def _is_same_day(self, date1, date2):
        return date1.date() == date2
    
    def _extract_description(self, element):
        desc_elem = element.find('p')
        if desc_elem:
            text = desc_elem.get_text(strip=True)
            return text[:200] + '...' if len(text) > 200 else text
        return ''
    
    def _categorize(self, title):
        title_lower = title.lower()
        
        match_keywords = ['match', 'game', 'win', 'draw', 'loss', 'score', 'goal', 'premier league', 'fa cup', 'champions league']
        transfer_keywords = ['sign', 'contract', 'transfer', 'deal', 'loan', 'extend', 'renew']
        player_keywords = ['injury', 'fitness', 'training', 'squad', 'player']
        interview_keywords = ['interview', 'press conference', 'says', 'speaks', 'talks']
        
        for keyword in match_keywords:
            if keyword in title_lower:
                return 'match'
        
        for keyword in transfer_keywords:
            if keyword in title_lower:
                return 'transfer'
        
        for keyword in player_keywords:
            if keyword in title_lower:
                return 'player'
        
        for keyword in interview_keywords:
            if keyword in title_lower:
                return 'interview'
        
        return 'club'