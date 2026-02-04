---
name: arsenal-daily-news
description: 收集阿森纳俱乐部每日动态并生成微信公众号文章。当用户提到阿森纳、Arsenal、每日新闻、球队动态时使用。
---

# 当用户提到阿森纳每日新闻时使用此 Skill

## 功能概述

这个 Skill 帮助用户收集阿森纳俱乐部在指定日期内发生的所有动态，包括：
- 比赛信息（赛程、结果、比分）
- 转会信息（签约、续约、离队）
- 俱乐部动态（公告、管理层变动）
- 球员动态（伤病、复出、训练）
- 采访言论（教练采访、球员采访）

## 使用流程

### 1. 确定收集日期

首先询问用户要收集哪一天的新闻：
- 默认：当天
- 可选：指定具体日期

### 2. 收集数据

从以下来源收集信息：
- 阿森纳官网（arsenal.com）
- 体育新闻网站（ESPN、BBC Sport、Sky Sports）
- 社交媒体（Twitter/X、Instagram）
- 其他相关来源

### 3. 数据处理

- 去重：避免重复内容
- 验证：确保信息真实性
- 分类：按类型整理信息
- 排序：按时间顺序排列

### 4. 生成文章

使用纯文本格式生成文章，风格要求：
- 球迷风格：轻松、有趣
- 言辞严谨：确保准确性
- 内容完整：包含所有重要信息
- 包含图片：相关事件配图

### 5. 输出和推送

- 保存为纯文本文件
- 保存历史记录
- 推送到微信公众号草稿箱（如已配置）

## 数据收集方法

### 阿森纳官网

访问 https://www.arsenal.com/news 获取官方新闻：
- 使用 RSS 订阅获取最新新闻
- 提取标题、时间、内容、图片
- 筛选指定日期的新闻

### 体育新闻网站

从以下网站搜索阿森纳相关新闻：
- ESPN: https://www.espn.com/soccer/team/_/id/359/arsenal
- BBC Sport: https://www.bbc.co.uk/sport/football/teams/arsenal
- Sky Sports: https://www.skysports.com/football/teams/arsenal

使用 API 或爬虫获取相关报道。

### 社交媒体

从以下平台获取动态：
- Twitter/X: 搜索 #Arsenal、@Arsenal
- Instagram: @Arsenal 官方账号

使用各平台 API 获取内容。

## 文章格式

### 标题格式

```
【阿森纳每日动态】2026年2月4日
```

### 内容结构

```
📅 日期：2026年2月4日
⚽ 阿森纳俱乐部今日动态汇总

---

🏆 比赛信息
[比赛详情]

💰 转会信息
[转会详情]

📢 俱乐部动态
[俱乐部公告]

🏃 球员动态
[球员状态]

🎤 采访言论
[采访内容]

---

📸 相关图片
[图片链接列表]

---
本文章由 Arsenal Daily News 自动生成
```

## 配置要求

### 环境变量

需要配置以下环境变量（可选）：

```bash
# 微信公众号 API
WECHAT_APPID=your_appid
WECHAT_SECRET=your_secret

# Twitter API
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret

# 其他 API 密钥
```

### GitHub Actions 配置

使用 GitHub Actions 定时执行：

```yaml
name: Arsenal Daily News
on:
  schedule: 
    - cron: '0 0 * * *'  # 每天凌晨执行
  workflow_dispatch:  # 支持手动触发
jobs:
  collect-news:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Collect news
        env:
          WECHAT_APPID: ${{ secrets.WECHAT_APPID }}
          WECHAT_SECRET: ${{ secrets.WECHAT_SECRET }}
        run: |
          python scripts/collect_news.py
```

## 脚本使用

### 手动执行

```bash
# 收集当天新闻
python scripts/collect_news.py

# 收集指定日期新闻
python scripts/collect_news.py --date 2026-02-04

# 只收集特定类型
python scripts/collect_news.py --type match
```

### 输出文件

- `daily_news_YYYYMMDD.txt` - 当日新闻文章
- `history/YYYYMMDD.json` - 历史记录（JSON 格式）
- `images/YYYYMMDD/` - 当日图片

## 注意事项

1. **内容真实性**：所有信息必须经过验证，确保准确无误
2. **版权问题**：使用图片和内容时注意版权，优先使用官方内容
3. **时效性**：确保收集的是指定日期的内容
4. **去重处理**：避免重复内容
5. **图片处理**：保存图片链接，不直接下载（除非必要）
6. **历史记录**：保存每日数据，方便回顾和分析

## 错误处理

- 网络错误：重试 3 次，记录失败日志
- API 限制：遵守各平台的 API 限制
- 数据缺失：记录缺失的来源，不影响整体流程
- 格式错误：记录错误，跳过该条数据

## 扩展功能

如需添加新的数据来源：

1. 在 `scripts/sources/` 下创建新的源文件
2. 实现统一的接口（返回标准格式数据）
3. 在 `collect_news.py` 中注册新源
4. 更新文档说明