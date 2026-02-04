# 阿森纳每日新闻收集工具

自动收集阿森纳俱乐部每日动态并生成微信公众号文章。

## 功能特性

- 多数据源收集：阿森纳官网、体育新闻网站、社交媒体
- 智能分类：自动识别比赛、转会、俱乐部动态、球员动态、采访言论
- 文章生成：生成符合微信公众号格式的纯文本文章
- 历史记录：保存每日数据，方便回顾
- 自动推送：支持推送到微信公众号草稿箱
- 定时执行：使用 GitHub Actions 每天自动运行

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置环境变量

创建 `.env` 文件：

```bash
# 微信公众号 API（可选）
WECHAT_APPID=your_appid
WECHAT_SECRET=123456

# Twitter API（可选）
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret

# 自定义 RSS 源（可选）
CUSTOM_RSS_URLS=https://example.com/feed1,https://example.com/feed2
```

## 使用方法

### 手动执行

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
```

### GitHub Actions 定时执行

1. Fork 或克隆此仓库到你的 GitHub
2. 在仓库设置中配置 Secrets：
   - `WECHAT_APPID`
   - `WECHAT_SECRET`
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_SECRET`
3. 启用 GitHub Actions
4. 每天早上北京时间 8 点自动执行

## 输出文件

- `output/daily_news_YYYYMMDD.txt` - 当日新闻文章
- `history/YYYYMMDD.json` - 历史记录（JSON 格式）
- `images/YYYYMMDD/` - 当日图片

## 文章格式示例

```
【阿森纳每日动态】2026年2月4日

📅 日期：2026年2月4日
⚽ 阿森纳俱乐部今日动态汇总

---

🏆 比赛信息
▸ 阿森纳 2-0 战胜对手
  阿森纳在主场以 2-0 的比分战胜了对手...
  来源：阿森纳官网
  时间：15:30
  链接：https://www.arsenal.com/news/...

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
1. https://www.arsenal.com/images/...
2. https://www.arsenal.com/images/...

---
本文章由 Arsenal Daily News 自动生成
如有任何问题或建议，请联系管理员

⚽ COYG (Come On You Gunners!)
```

## 扩展功能

### 添加新的数据源

1. 在 `scripts/sources/` 下创建新的源文件
2. 实现统一的接口（返回标准格式数据）
3. 在 `collect_news.py` 中注册新源
4. 更新文档说明

### 自定义文章格式

修改 `scripts/utils/formatter.py` 中的 `ArticleFormatter` 类。

## 注意事项

1. **内容真实性**：所有信息必须经过验证，确保准确无误
2. **版权问题**：使用图片和内容时注意版权，优先使用官方内容
3. **API 限制**：遵守各平台的 API 限制，避免被封禁
4. **网络稳定**：确保网络连接稳定，或配置代理
5. **时区问题**：注意时区转换，确保收集正确日期的内容

## 许可证

MIT License