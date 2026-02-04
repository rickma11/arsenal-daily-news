#!/usr/bin/env python3
"""
图片处理工具
下载和处理图片
"""

import requests
from pathlib import Path
from urllib.parse import urlparse


class ImageHandler:
    def __init__(self):
        self.timeout = 10
        self.max_size = 5 * 1024 * 1024  # 5MB
    
    def download(self, url, save_path):
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        response = requests.get(url, timeout=self.timeout, stream=True)
        response.raise_for_status()
        
        content_length = int(response.headers.get('content-length', 0))
        if content_length > self.max_size:
            raise ValueError(f"图片过大: {content_length} bytes")
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return save_path
    
    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def get_extension(self, url):
        path = urlparse(url).path
        return Path(path).suffix.lower() or '.jpg'