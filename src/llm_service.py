"""
LLM服务模块
"""
import json
from typing import List, Dict, Optional
from openai import OpenAI
from loguru import logger
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL
from .search_service import SearchService


class LLMService:
    """大语言模型服务类"""
    
    def __init__(self, api_key: str = DEEPSEEK_API_KEY, base_url: str = DEEPSEEK_BASE_URL):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = DEEPSEEK_MODEL
        self.search_service = SearchService()
        
        # 工具定义
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "搜索信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "num": {"type": "integer"}
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
    
    def generate_report(self, initial_prompt: str) -> Optional[str]:
        """
        生成氢能产业报告
        
        Args:
            initial_prompt: 初始提示词
            
        Returns:
            生成的报告内容
        """
        try:
            logger.info("开始生成氢能产业报告")
            
            messages = [{"role": "user", "content": initial_prompt}]
            
            # 第一次调用LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools
            )
            
            message = response.choices[0].message
            dump = message.model_dump() if hasattr(message, "model_dump") else message.dict()
            messages.append(dump)
            
            # 处理工具调用
            if message.tool_calls:
                logger.info(f"LLM请求调用 {len(message.tool_calls)} 个工具")
                
                for tool_call in message.tool_calls:
                    if tool_call.function.name == "search_web":
                        args = json.loads(tool_call.function.arguments)
                        query = args.get("query")
                        num = args.get("num", 30)
                        
                        logger.info(f"执行搜索: {query}")
                        search_results = self.search_service.search_web(query, num)
                        formatted_results = self.search_service.format_search_results(search_results)
                        
                        # 添加工具调用结果
                        messages.append({
                            "role": "tool",
                            "name": tool_call.function.name,
                            "content": formatted_results,
                            "tool_call_id": tool_call.id
                        })
                
                # 第二次调用LLM获取最终结果
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                
                report_content = final_response.choices[0].message.content
                logger.info("报告生成完成")
                return report_content
            
            else:
                logger.warning("LLM没有调用搜索工具")
                return message.content
                
        except Exception as e:
            logger.error(f"生成报告时发生错误: {e}")
            return None
    
    def chat_completion(self, messages: List[Dict], use_tools: bool = False) -> Optional[str]:
        """
        通用聊天完成接口
        
        Args:
            messages: 消息列表
            use_tools: 是否使用工具
            
        Returns:
            LLM回复内容
        """
        try:
            kwargs = {
                "model": self.model,
                "messages": messages
            }
            
            if use_tools:
                kwargs["tools"] = self.tools
            
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"聊天完成请求失败: {e}")
            return None