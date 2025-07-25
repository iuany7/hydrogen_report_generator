"""
邮件服务模块
"""
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from typing import List
from loguru import logger
from PIL import Image
import io

class EmailService:
    """用于发送带附件邮件的服务"""

    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def _compress_image(self, file_path: str, quality: int = 75) -> bytes:
        """压缩图片并返回其字节流"""
        try:
            img = Image.open(file_path)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format, quality=quality, optimize=True)
            return img_byte_arr.getvalue()
        except Exception as e:
            logger.error(f"压缩图片 {file_path} 失败: {e}")
            return None

    def send_email_with_attachments(self, recipients: List[str], subject: str, body: str, attachments: List[str]) -> bool:
        """
        发送一封包含附件的邮件。图片将被压缩。

        Args:
            recipients (List[str]): 收件人邮箱地址列表。
            subject (str): 邮件主题。
            body (str): 邮件正文 (纯文本格式)。
            attachments (List[str]): 附件的文件路径列表。

        Returns:
            bool: 如果邮件发送成功则返回 True，否则返回 False。
        """
        if not all([self.host, self.port, self.user, self.password]):
            logger.warning("邮件服务配置不完整，跳过发送。请检查 .env 文件中的配置。")
            return False
        
        if not recipients or not recipients[0]:
            logger.warning("未指定收件人，跳过发送。")
            return False

        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject

        # 创建更详细的邮件正文
        body_parts = [body, "\n\n--- 附件列表 ---"]
        for file_path in attachments:
            body_parts.append(f"- {os.path.basename(file_path)}")
        final_body = "\n".join(body_parts)
        msg.attach(MIMEText(final_body, 'plain'))

        # 添加附件
        for file_path in attachments:
            try:
                filename = os.path.basename(file_path)
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    compressed_data = self._compress_image(file_path)
                    if compressed_data:
                        part = MIMEImage(compressed_data, name=filename)
                        logger.info(f"成功压缩并附加图片: {file_path}")
                    else:
                        continue
                else:
                    with open(file_path, 'rb') as f:
                        part = MIMEApplication(f.read(), Name=filename)
                    logger.info(f"成功附加文件: {file_path}")
                
                part['Content-Disposition'] = f'attachment; filename="{filename}"'
                msg.attach(part)

            except FileNotFoundError:
                logger.error(f"找不到附件文件: {file_path}，已跳过。")
            except Exception as e:
                logger.error(f"附加文件 {file_path} 时发生错误: {e}")

        # 发送邮件的健壮性处理
        server = None
        try:
            server = smtplib.SMTP_SSL(self.host, self.port)
            server.set_debuglevel(1)
            server.login(self.user, self.password)
            server.send_message(msg)
            logger.success(f"邮件数据已成功发送至: {', '.join(recipients)}")
            return True
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP认证失败！请检查您的邮箱地址和授权码。")
            return False
        except Exception as e:
            logger.error(f"发送邮件过程中发生错误: {e}", exc_info=True)
            return False
        finally:
            if server:
                try:
                    server.quit()
                except smtplib.SMTPServerDisconnected:
                    logger.warning("服务器提前关闭了连接，但这通常意味着邮件已发送成功。")
                except Exception as e:
                    logger.warning(f"关闭SMTP连接时发生了一个小问题: {e}")