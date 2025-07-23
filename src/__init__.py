"""
包初始化系统
"""

__version__ = "1.0.0"
__author__ = "iuany7"
__email__ = "nuozhixia123@gmail.com"
__description__ = "基于LLM和搜索引擎的氢能产业简报自动生成系统"

from .llm_service import LLMService
from .search_service import SearchService
from .report_generator import ReportGenerator
from .utils import (
    setup_logging,
    validate_api_keys,
    check_dependencies,
    get_project_info,
    ensure_dir,
    format_file_size,
    clean_output_directory
)

__all__ = [
    "LLMService",
    "SearchService", 
    "ReportGenerator",
    "setup_logging",
    "validate_api_keys",
    "check_dependencies",
    "get_project_info",
    "ensure_dir",
    "format_file_size",
    "clean_output_directory"
]