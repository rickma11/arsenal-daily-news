#!/usr/bin/env python3
"""
社交媒体数据源
从 Twitter/X、Instagram 获取阿森纳动态
"""

import os
import requests
from datetime import datetime, timedelta


class SocialMedia:
    name = "社交媒体"
    categories = ['match', 'transfer', 'club', 'player', 'interview']
    
    def __init__(self):
        self.twitter_api_key = os.getenv('TWITTER_API_KEY')
        self.twitter_api_secret = os.getenv('TWITTER_API_SECRET')
        self.twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.twitter_access_secret = os.getenv('TWITTER_ACCESS_SECRET')
    
    def collect(self, target_date):
        news_data = {
            'match': [],
            'transfer': [],
            'club': [],
            'player': [],
            'interview': []
        }
        images = []
        
        if self.twitter_api_key:
            try:
                print("  - 正在从 Twitter/X 获取数据...")
                tweets = self._get_twitter_tweets(target_date)
                
                for tweet in tweets:
                    category = self._categorize(tweet['text'])
                    if category in news_data:
                        news_data[category].append(tweet)
                    
                    if 'image' in tweet:
                        images.append(tweet['image'])
                
                print(f"  - ✓ Twitter/X 获取完成 ({len(tweets)} 条)")
                
            except Exception as e:
                print(f"  - ✗ Twitter/X 获取失败: {str(e)}")
        else:
            print("  - ⚠ Twitter API 未配置，跳过")
        
        return {
            **news_data,
'images': images
        }
    
    def _get_twitter_tweets(self, target_date):
        if not all([self.twitter_api_key, self.twitter_api_secret, 
                   self.twitter_access_token, self.twitter_access_secret]):
            return []
        
        tweets = []
        
        try:
            auth = requests.auth.OAuth1(
                self.twitter_api_key,
                self.twitter_api_secret,
                self.twitter_access_token,
                self.twitter_access_secret
            )
            
            search_url = "https://api.twitter.com/2/tweets/search/recent"
            params = {
                'query': '#Arsenal OR @Arsenal -is:retweet',
                'max_results': 100,
                'tweet.fields': 'created_at,entities,author_id'
            }
            
            response = requests.get(search_url, auth=auth, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data:
                for tweet_data in data['data']:
                    tweet_time = datetime.strptime(
                        tweet_data['created_at'], 
                        '%Y-%m-%dT%H:%M:%S.%fZ'
                    )
                    
                    if not self._is_same_day(tweet_time, target_date):
                        continue
                    
                    image = None
                    if 'entities' in tweet_data and 'media' in tweet_data['entities']:
                        media = tweet_data['entities']['media'][0]
                        image = media.get('url', '')
                    
                    category = self._categorize(tweet_data['text'])
                    
                    tweets.append({
                        'title': tweet_data['text'][:100],
                        'url': f"https://twitter.com/i/status/{tweet_data['id']}",
                        'description': tweet_data['text'],
                        'timestamp': tweet_time.isoformat(),
                        'source': 'Twitter/X',
                        'category': category
                    })
                    
                    if image:
                        tweets[-1]['image'] = image
        
        except Exception as e:
            print(f"Twitter API 调用失败: {str(e)}")
        
        return tweets
    
    def _is_same_day(self, date1, date2):
        return date1.date() == date2
    
    def _categorize(self, text):
        text_lower = text.lower()
        
        match_keywords = ['match', 'game', 'win', 'draw', 'loss', 'score', 'goal', 'premier league', 'fa cup', 'champions league']
        transfer_keywords = ['sign', 'contract', 'transfer', 'deal', 'loan', 'extend', 'renew']
        player_keywords = ['injury', 'fitness', 'training', 'squad', 'player']
        interview_keywords = ['interview', 'press conference', 'says', 'speaks', 'talks']
        
        for keyword in match_keywords:
            if keyword in text_lower:
                return 'match'
        
        for keyword in transfer_keywords:
            if keyword in text_lower:
                return 'transfer'
        
        for keyword in player_keywords:
            if keyword in text_lower:
                return 'player'
        
        for keyword in interview_keywords:
            if keyword in text_lower:
                return 'interview'
        
        return 'club'