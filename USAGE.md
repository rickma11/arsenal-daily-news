# 阿森纳每日新闻收集工具 - 使用说明

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）

创建 `.env` 文件：

```bash
# 微信公众号 API
WECHAT_APPID=your_appid
WECHAT_SECRET=your_secret

# Twitter API
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret

# 自定义 RSS 源
CUSTOM_RSS_URLS=https://example.com/feed1,https://example.com/feed2
```

### 3. 运行脚本

```bash
# 收集当天新闻
python scripts/collect_news.py

# 收集指定日期新闻
python scripts/collect_news.py --date 2026-02-04

# 只收集特定类型
python scripts/collect_news.py --type match

# 下载图片
python scripts/collect_news.py --save-images

# 推送到微信公众号
python scripts/collect_news.py --push-wechat

# 组合使用
python scripts/collect_news.py --date 2026-02-04 --save-images --push-wechat
```

## 输出文件说明

### output/daily_news_YYYYMMDD.txt

生成的微信公众号文章，纯文本格式。

### history/YYYYMMDD.json

历史记录，JSON 格式，包含所有收集到的原始数据。

### images/YYYYMMDD/

下载的图片文件。

## GitHub Actions 部署

### 1. 推送到 GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/arsenal-daily-news.git
git push -u origin main
```

### 2. 配置 GitHub Secrets

在 GitHub 仓库设置中添加以下 Secrets：

- `WECHAT_APPID`
- `WECHAT_SECRET`
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`

### 3. 启用 GitHub Actions

1. 进入仓库的 "Actions" 标签
2. 启用 Actions
3. 每天凌晨（UTC 时间）自动执行
4. 也可以手动触发

## 数据源说明

### 阿森纳官网

- URL: https://www.arsenal.com/news
- 类型: RSS
- 包含: 官方新闻、比赛信息、转会公告

### 体育新闻网站

- ESPN: https://www.espn.com/soccer/team/_/id/359/arsenal
- BBC Sport: https://www.bbc.co.uk/sport/football/teams/arsenal
- Sky Sports: https://www.skysports.com/football/teams/arsenal

### 社交媒体

- Twitter/X: 搜索 #Arsenal、@Arsenal
- 需要 Twitter API 密钥

### 其他来源

- 自定义 RSS 源
- 通过环境变量 `CUSTOM_RSS_URLS` 配置

## 文章格式

生成的文章包含以下部分：

1. 标题：日期和主题
2. 比赛信息
3. 转会信息
4. 俱乐部动态
5. 球员动态
6. 采访言论
7. 相关图片
8. 页脚

## 常见问题

### Q: 如何只收集特定类型？

使用 `--type` 参数：

```bash
python scripts/collect_news.py --type match
python scripts/collect_news.py --type transfer
python scripts/collect_news.py --type club
python scripts/collect_news.py --type player
python scripts/collect_news.py --type interview
```

### Q: 如何添加新的数据源？

1. 在 `scripts/sources/` 下创建新文件
2. 实现统一的接口
3. 在 `collect_news.py` 中注册新源

### Q: 如何自定义文章格式？

修改 `scripts/utils/formatter.py` 中的 `ArticleFormatter` 类。

### Q: 如何处理时区问题？

脚本使用 UTC 时间，如需使用其他时区，修改 `_parse_date` 方法。

### Q: 如何避免重复内容？

脚本会自动去重，基于标题和 URL 的组合。

## 注意事项

1. **API 限制**：遵守各平台的 API 限制
2. **网络稳定**：确保网络连接稳定
3. **版权问题**：使用图片和内容时注意版权
4. **内容验证**：确保信息准确性
5. **时区转换**：注意时区问题

## 技术支持

如有问题，请查看：
- README.md
- SKILL.md
- GitHub Issues