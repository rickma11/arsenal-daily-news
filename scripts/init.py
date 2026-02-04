#!/usr/bin/env python3
"""
初始化脚本
创建必要的目录和配置文件
"""

import os
from pathlib import Path


def create_directories():
    directories = [
        'output',
        'history',
        'images'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ 创建目录: {directory}")


def create_env_file():
    env_file = Path('.env')
    
    if env_file.exists():
        print("⚠ .env 文件已存在，跳过创建")
        return
    
    env_content = """# 微信公众号 API（可选）
WECHAT_APPID=your_appid
WECHAT_SECRET=your_secret

# Twitter API（可选）
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret

# 自定义 RSS 源（可选）
CUSTOM_RSS_URLS=https://example.com/feed1,https://example.com/feed2
"""
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✓ 创建 .env 文件")
    print("  请根据需要配置 API 密钥")


def create_gitignore():
    gitignore_file = Path('.gitignore')
    
    if gitignore_file.exists():
        print("⚠ .gitignore 文件已存在，跳过创建")
        return
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# Environment variables
.env

# Output files
output/
history/
images/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
"""
    
    with open(gitignore_file, 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("✓ 创建 .gitignore 文件")


def main():
    print("阿森纳每日新闻收集工具 - 初始化")
    print("=" * 50)
    
    create_directories()
    print()
    create_env_file()
    print()
    create_gitignore()
    print()
    
    print("=" * 50)
    print("✓ 初始化完成！")
    print()
    print("下一步：")
    print("1. 安装依赖: pip install -r requirements.txt")
    print("2. 配置 .env 文件（可选）")
    print("3. 运行脚本: python scripts/collect_news.py")
    print()
    print("详细使用说明请查看 USAGE.md")


if __name__ == '__main__':
    main()