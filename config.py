# 配置文件

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "output"
ASSETS_DIR = PROJECT_ROOT / "assets"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# 创建必要的目录
OUTPUT_DIR.mkdir(exist_ok=True)
(OUTPUT_DIR / "pages").mkdir(exist_ok=True)
(OUTPUT_DIR / "reports").mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

# API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")   # llm配置
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")   # 搜索引擎配置
# 要使用的搜索引擎列表，用逗号分隔，例如 "google,bing,baidu"
SERPAPI_ENGINES = os.getenv("SERPAPI_ENGINES", "google,bing,baidu").split(',')
# 搜索引擎轮询之间的时间间隔（秒），以避免速率限制
SEARCH_DELAY = 1.5

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# 邮件服务配置
EMAIL_HOST = os.getenv("EMAIL_HOST")  
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))  # 465 (SSL)
EMAIL_USER = os.getenv("EMAIL_USER")  # 发件人邮箱
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # 发件人邮箱的SMTP授权码
EMAIL_RECIPIENTS = [email.strip() for email in os.getenv("EMAIL_RECIPIENTS", "").split(",") if email.strip()]  # 收件人列表，用逗号分隔   


# 搜索配置
SEARCH_RESULTS_NUM = 30
SEARCH_CACHE_ENABLED = False

# 报告配置
REPORT_CONFIG = {
    "chars_per_page": 1800,
    "image_size": (1080, 1600),
    "logo_size": (80, 80),
    "logo_margin": (40, 40),
    "font_family": "Microsoft YaHei, LXGW WenKai, sans-serif",
    "font_size": 16,
}

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

