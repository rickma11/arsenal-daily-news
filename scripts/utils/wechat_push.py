#!/usr/bin/env python3
"""
微信公众号推送工具
将文章推送到微信公众号草稿箱
"""

import os
import requests
import json


class WeChatPush:
    def __init__(self):
        self.appid = os.getenv('WECHAT_APPID')
        self.secret = os.getenv('WECHAT_SECRET')
        self.access_token = None
    
    def push(self, article, date):
        if not all([self.appid, self.secret]):
            print("微信公众号 API 未配置，跳过推送")
            return False
        
        try:
            self._get_access_token()
            self._create_draft(article, date)
            return True
        except Exception as e:
            print(f"推送到微信公众号失败: {str(e)}")
            return False
    
    def _get_access_token(self):
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.secret}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'access_token' in data:
            self.access_token = data['access_token']
        else:
            raise ValueError(f"获取 access_token 失败: {data}")
    
    def _create_draft(self, article, date):
        if not self.access_token:
            raise ValueError("未获取到 access_token")
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.access_token}"
        
        title = f"【阿森纳每日动态】{date.strftime('%Y年%m月%d日')}"
        
        payload = {
            "articles": [{
                "title": title,
                "content": article,
                "digest": article[:100],
                "author": "Arsenal Daily News",
                "show_cover_pic": 0
            }]
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('errcode') != 0:
            raise ValueError(f"创建草稿失败: {data}")
        
        print(f"草稿创建成功，media_id: {data.get('media_id')}")