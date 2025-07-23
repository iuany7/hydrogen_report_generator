"""
工具函数模块
"""
import os
from pathlib import Path
from typing import Union
from loguru import logger


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        path: 目录路径
        
    Returns:
        Path对象
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_api_keys() -> bool:
    """
    验证API密钥是否设置
    
    Returns:
        是否所有必需的API密钥都已设置
    """
    required_keys = ["DEEPSEEK_API_KEY", "SERPAPI_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        logger.error(f"缺少必需的API密钥: {', '.join(missing_keys)}")
        logger.info("请在.env文件中设置以下环境变量:")
        for key in missing_keys:
            logger.info(f"  {key}=your_api_key_here")
        return False
    
    return True


def setup_logging(level: str = "INFO"):
    """
    设置日志配置
    
    Args:
        level: 日志级别
    """
    from config import LOG_FORMAT
    
    logger.remove()  # 移除默认处理器
    logger.add(
        sink=lambda msg: print(msg, end=""),
        format=LOG_FORMAT,
        level=level,
        colorize=True
    )
    
    # 添加文件日志
    log_file = Path("logs") / "hydrogen_report.log"
    ensure_dir(log_file.parent)
    
    logger.add(
        sink=str(log_file),
        format=LOG_FORMAT,
        level=level,
        rotation="1 day",
        retention="7 days"
    )


def get_project_info() -> dict:
    """
    获取项目信息
    
    Returns:
        项目信息字典
    """
    return {
        "name": "氢能产业简报生成系统",
        "version": "1.0.0",
        "description": "基于LLM和搜索引擎的氢能产业简报自动生成系统",
        "author": "您的名字",
        "email": "your.email@example.com"
    }


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 字节数
        
    Returns:
        格式化后的文件大小字符串
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def clean_output_directory(keep_latest: int = 5):
    """
    清理输出目录，保留最新的几个文件
    
    Args:
        keep_latest: 保留最新文件的数量
    """
    from config import OUTPUT_DIR
    
    try:
        pages_dir = OUTPUT_DIR / "pages"
        reports_dir = OUTPUT_DIR / "reports"
        
        for directory in [pages_dir, reports_dir]:
            if directory.exists():
                files = list(directory.glob("*"))
                files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                # 删除旧文件
                for file in files[keep_latest:]:
                    file.unlink()
                    logger.info(f"删除旧文件: {file}")
                    
        logger.info(f"清理完成，每个目录保留最新 {keep_latest} 个文件")
        
    except Exception as e:
        logger.error(f"清理输出目录时发生错误: {e}")


def check_dependencies():
    """
    检查项目依赖是否安装
    
    Returns:
        是否所有依赖都已安装
    """
    required_packages = [
        "openai", "requests", "markdown2", "html2image", 
        "Pillow", "python-dotenv", "tqdm", "loguru"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"缺少必需的依赖包: {', '.join(missing_packages)}")
        logger.info("请运行以下命令安装依赖:")
        logger.info("pip install -r requirements.txt")
        return False
    
    return True
