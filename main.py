"""
氢能产业简报生成系统 - 主程序入口
"""
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm

# 提前加载环境变量，确保所有模块都能访问
load_dotenv()

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from src.utils import setup_logging, validate_api_keys, check_dependencies, get_project_info
from src.llm_service import LLMService
from src.report_generator import ReportGenerator
from templates.prompts import get_hydrogen_report_prompt
from config import LOG_LEVEL


def main():
    """主函数"""
    # 设置日志
    setup_logging(LOG_LEVEL)
    
    # 显示项目信息
    info = get_project_info()
    logger.info(f"启动 {info['name']} v{info['version']}")
    
    # 检查依赖和API密钥
    if not check_dependencies():
        logger.error("依赖检查失败，程序退出")
        sys.exit(1)
    
    if not validate_api_keys():
        logger.error("API密钥验证失败，程序退出")
        sys.exit(1)
    
    try:
        # 初始化服务
        logger.info("初始化服务...")
        llm_service = LLMService()
        report_generator = ReportGenerator()
        
        # 生成报告
        logger.info("开始生成氢能产业简报...")
        with tqdm(total=3, desc="生成进度") as pbar:
            
            # 步骤1: 生成报告内容
            pbar.set_description("生成报告内容")
            report_prompt = get_hydrogen_report_prompt()
            markdown_content = llm_service.generate_report(report_prompt)
            
            if not markdown_content:
                logger.error("报告内容生成失败")
                return
            
            pbar.update(1)
            
            # 步骤2: 生成图片
            pbar.set_description("生成报告图片")
            image_paths, pdf_path = report_generator.generate_complete_report(markdown_content)
            pbar.update(1)
            
            # 步骤3: 完成
            pbar.set_description("完成")
            pbar.update(1)
        
        # 显示结果
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.success(f"报告生成完成! ({current_time})")
        
        if image_paths:
            logger.info(f"生成了 {len(image_paths)} 张图片")
            for i, path in enumerate(image_paths, 1):
                logger.info(f"  页面 {i}: {path}")
        
        if pdf_path:
            logger.info(f"PDF报告: {pdf_path}")
        
        # 显示文件大小
        if pdf_path and os.path.exists(pdf_path):
            size = os.path.getsize(pdf_path)
            from src.utils import format_file_size
            logger.info(f"PDF大小: {format_file_size(size)}")
        
    except KeyboardInterrupt:
        logger.warning("用户中断程序")
    except Exception as e:
        logger.error(f"程序执行过程中发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()