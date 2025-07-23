"""
报告生成器模块
"""
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image
import markdown2
from html2image import Html2Image
from loguru import logger
from config import OUTPUT_DIR, ASSETS_DIR, REPORT_CONFIG
from templates.html_template import BASE_CSS_STYLES
from .utils import ensure_dir


class ReportGenerator:
    """报告生成器类"""
    
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.assets_dir = ASSETS_DIR
        self.config = REPORT_CONFIG
        
        # 统一使用html_template中的样式，并为表格添加强制换行
        self.base_style = BASE_CSS_STYLES.replace(
            "tr:hover td {",
            "td { word-break: break-all; } tr:hover td {"
        )
    
    def generate_report_images(self, markdown_text: str, output_subdir: str = "pages") -> List[str]:
        """
        将Markdown文本转换为图片
        
        Args:
            markdown_text: Markdown格式的报告内容
            output_subdir: 输出子目录
            
        Returns:
            生成的图片路径列表
        """
        try:
            current_time = datetime.now().strftime("%Y年%m月%d日")
            header_text = f"氢能产业双周简报 {current_time}"
            footer_text = "来源：国家能源局、IEA、等"
            
            output_path = self.output_dir / output_subdir
            ensure_dir(output_path)
            
            # 分页处理
            pages = self._split_markdown_pages(markdown_text)
            total_pages = len(pages)
            
            hti = Html2Image(
                output_path=str(output_path),
                size=self.config["image_size"],
                browser="chrome"
            )
            
            image_paths = []
            
            for i, page_content in enumerate(pages):
                page_num = i + 1
                html_content = self._create_html_page(
                    page_content, header_text, footer_text, page_num, total_pages
                )
                
                image_filename = f"hydrogen_report_page_{page_num}.png"
                hti.screenshot(html_str=html_content, save_as=image_filename)
                
                image_path = output_path / image_filename
                image_paths.append(str(image_path))
                
                logger.info(f"生成第 {page_num} 页图片: {image_filename}")
                
                # 添加Logo
                logo_path = self.assets_dir / "logo.png"
                if logo_path.exists():
                    self._add_logo_to_image(str(image_path), str(logo_path))
            
            return image_paths
            
        except Exception as e:
            logger.error(f"生成报告图片时发生错误: {e}")
            return []
    
    def generate_pdf(self, image_paths: List[str], output_filename: str = "hydrogen_report.pdf") -> Optional[str]:
        """
        将图片合并为PDF
        
        Args:
            image_paths: 图片路径列表
            output_filename: 输出PDF文件名
            
        Returns:
            生成的PDF文件路径
        """
        try:
            if not image_paths:
                logger.warning("没有图片可以转换为PDF")
                return None
            
            pdf_path = self.output_dir / "reports" / output_filename
            ensure_dir(pdf_path.parent)
            
            images = []
            for img_path in image_paths:
                img = Image.open(img_path).convert("RGB")
                images.append(img)
            
            if images:
                images[0].save(str(pdf_path), save_all=True, append_images=images[1:])
                logger.info(f"PDF生成成功: {pdf_path}")
                return str(pdf_path)
            
        except Exception as e:
            logger.error(f"生成PDF时发生错误: {e}")
            return None
    
    def _split_markdown_pages(self, markdown_text: str) -> List[str]:
        """
        将报告分割为两页：Part 1-4 在第一页，Part 5 单独在第二页。
        能兼容 "### Part 5" 和 "### **Part 5**" 等格式。
        
        Args:
            markdown_text: 原始Markdown文本
            
        Returns:
            分页后的内容列表
        """
        pages = []
        # 使用更灵活的正则表达式查找Part 5的开头，兼容空格和加粗标记
        part5_match = re.search(r'(###\s*\**\s*Part 5\s*\**\s*[:：]?.+)', markdown_text, re.DOTALL)
        
        if part5_match:
            # 获取Part 5开始的位置
            split_index = part5_match.start()
            
            # 第一页是Part 5之前的所有内容
            page1_content = markdown_text[:split_index].strip()
            if page1_content:
                pages.append(page1_content)
            
            # 第二页是Part 5的全部内容
            page2_content = part5_match.group(1).strip()
            if page2_content:
                pages.append(page2_content)
            
            logger.info(f"报告已按Part 5分割为 {len(pages)} 页。")
        else:
            # 如果没有找到Part 5，则将所有内容放在一页
            pages.append(markdown_text)
            logger.warning("未找到 'Part 5'，报告将不会被特殊分页。")
            
        return pages
    
    def _create_html_page(self, content: str, header: str, footer: str, 
                         page_num: int, total_pages: int) -> str:
        """
        创建HTML页面
        
        Args:
            content: 页面内容
            header: 页眉文本
            footer: 页脚文本
            page_num: 当前页码
            total_pages: 总页数
            
        Returns:
            完整的HTML内容
        """
        html_body = markdown2.markdown(content, extras=["tables"])
        
        return f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>{self.base_style}</style>
        </head>
        <body>
            <div class="header">{header}</div>
            <div class="footer">第 {page_num} 页 / 共 {total_pages} 页 · {footer}</div>
            {html_body}
        </body>
        </html>
        """
    
    def _add_logo_to_image(self, image_path: str, logo_path: str):
        """
        为图片添加Logo
        
        Args:
            image_path: 图片路径
            logo_path: Logo路径
        """
        try:
            img = Image.open(image_path).convert("RGBA")
            logo = Image.open(logo_path).convert("RGBA")
            
            # 调整Logo大小
            logo = logo.resize(self.config["logo_size"])
            
            # 计算Logo位置（右上角）
            logo_x = img.width - self.config["logo_size"][0] - self.config["logo_margin"][0]
            logo_y = self.config["logo_margin"][1]
            
            # 粘贴Logo
            img.paste(logo, (logo_x, logo_y), mask=logo)
            img.save(image_path)
            
            logger.debug(f"成功添加Logo到图片: {image_path}")
            
        except Exception as e:
            logger.error(f"添加Logo失败: {e}")
    
    def generate_complete_report(self, markdown_content: str) -> Tuple[List[str], Optional[str]]:
        """
        生成完整报告（图片和PDF）
        
        Args:
            markdown_content: Markdown格式的报告内容
            
        Returns:
            图片路径列表和PDF路径
        """
        logger.info("开始生成完整报告")
        
        # 生成图片
        image_paths = self.generate_report_images(markdown_content)
        
        # 生成PDF
        pdf_path = None
        if image_paths:
            pdf_path = self.generate_pdf(image_paths)
        
        logger.info("完整报告生成完成")
        return image_paths, pdf_path