#!/usr/bin/env python3
"""
文章格式化工具
生成符合要求的微信公众号文章格式
"""

from datetime import datetime


class ArticleFormatter:
    def __init__(self):
        self.category_titles = {
            'match': '🏆 比赛信息',
            'transfer': '💰 转会信息',
            'club': '📢 俱乐部动态',
            'player': '🏃 球员动态',
            'interview': '🎤 采访言论'
        }
    
    def generate(self, date, news_data, images):
        article_lines = []
        
        article_lines.append(self._generate_header(date))
        article_lines.append('')
        
        for category in ['match', 'transfer', 'club', 'player', 'interview']:
            if news_data.get(category):
                article section = self._generate_category_section(
                    category, 
                    news_data[category]
                )
                article_lines.append(section)
                article_lines.append('')
        
        if images:
            article_lines.append(self._generate_images_section(images))
            article_lines.append('')
        
        article_lines.append(self._generate_footer())
        
        return '\n'.join(article_lines)
    
    def _generate_header(self, date):
        date_str = date.strftime('%Y年%m月%d日')
        return f"""【阿森纳每日动态】{date_str}

📅 日期：{date_str}
⚽ 阿森纳俱乐部今日动态汇总

---"""
    
    def _generate_category_section(self, category, items):
        title = self.category_titles.get(category, category.upper())
        
        section_lines = [title, '']
        
        for item in items:
            section_lines.append(self._format_item(item))
            section_lines.append('')
        
        return '\n'.join(section_lines)
    
    def _format_item(self, item):
        title = item.get('title', '无标题')
        description = item.get('description', '')
        source = item.get('source', '未知来源')
        url = item.get('url', '')
        timestamp = item.get('timestamp', '')
        
        formatted_lines = []
        
        formatted_lines.append(f"▸ {title}")
        
        if description:
            formatted_lines.append(f"  {description}")
        
        formatted_lines.append(f"  来源：{source}")
        
        if timestamp:
            time_str = self._format_timestamp(timestamp)
            formatted_lines.append(f"  时间：{time_str}")
        
        if url:
            formatted_lines.append(f"  链接：{url}")
        
        return '\n'.join(formatted_lines)
    
    def _format_timestamp(self, timestamp):
        try:
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime('%H:%M')
        except:
            return timestamp
    
    def _generate_images_section(self, images):
        section_lines = ['📸 相关图片', '']
        
        for i, image_url in enumerate(images[:10], 1):
            section_lines.append(f"{i}. {image_url}")
        
        if len(images) > 10:
            section_lines.append(f"\n... 还有 {len(images) - 10} 张图片")
        
        return '\n'.join(section_lines)
    
    def _generate_footer(self):
        return """---
本文章由 Arsenal Daily News 自动生成
如有任何问题或建议，请联系管理员

⚽ COYG (Come On You Gunners!)"""