"""
LLM服务模块
"""
import json
import time
from typing import List, Dict, Optional
from openai import OpenAI
from loguru import logger
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, SEARCH_DELAY
from .search_service import SearchService

class LLMService:
    """大语言模型服务类"""
    
    def __init__(self, api_key: str = DEEPSEEK_API_KEY, base_url: str = DEEPSEEK_BASE_URL):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = DEEPSEEK_MODEL
        self.search_service = SearchService()
        
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "execute_searches",
                    "description": "根据一个包含多个具体查询词的列表，逐一执行网络搜索来收集信息。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "queries": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "一个包含多个具体搜索查询词的列表，例如 ['中国氢能汽车补贴政策 2025', '德国绿氢项目最新进展']"
                            }
                        },
                        "required": ["queries"]
                    }
                }
            }
        ]
    
    def generate_report(self, initial_prompt: str) -> Optional[str]:
        """
        通过多轮、串行的聚焦搜索，生成氢能产业报告。

        Args:
            initial_prompt (str): 包含报告要求的初始提示。

        Returns:
            Optional[str]: 生成的Markdown格式报告，如果失败则返回None。
        """
        try:
            logger.info("开始生成氢能产业报告（稳定串行搜索策略）")
            messages = [{"role": "user", "content": initial_prompt}]
            
            # 步骤 1: 让LLM根据prompt生成多个搜索查询
            logger.info("第一步: 生成搜索查询列表...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice={"type": "function", "function": {"name": "execute_searches"}}
            )
            
            message = response.choices[0].message
            messages.append(message)
            
            # 步骤 2: 逐一执行搜索并将结果返回给LLM
            if not message.tool_calls:
                logger.warning("LLM未能生成搜索查询，将尝试直接生成报告。")
                return self.chat_completion(messages)

            logger.info("第二步: 开始逐一执行聚焦搜索...")
            all_search_results = []
            tool_call = message.tool_calls[0]
            if tool_call.function.name == "execute_searches":
                args = json.loads(tool_call.function.arguments)
                queries = args.get("queries", [])
                logger.info(f"LLM请求搜索以下查询: {queries}")
                
                for query in queries:
                    # 对每个查询调用串行搜索服务
                    search_results = self.search_service.search(query)
                    all_search_results.extend(search_results)
                    # 在不同查询词之间也加入延时，进一步确保稳定
                    time.sleep(SEARCH_DELAY)
            
            # 格式化并添加工具结果
            formatted_results = self.search_service.format_search_results(all_search_results)
            messages.append({
                "role": "tool",
                "name": "execute_searches",
                "content": formatted_results,
                "tool_call_id": tool_call.id
            })

            # 步骤 3: 基于所有搜索结果，生成最终报告
            logger.info("第三步: 汇总信息并生成最终报告...")
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            report_content = final_response.choices[0].message.content
            logger.success("报告生成成功！")
            return report_content
                
        except Exception as e:
            logger.error(f"生成报告过程中发生严重错误: {e}", exc_info=True)
            return None
    
    def chat_completion(self, messages: List[Dict]) -> Optional[str]:
        """
        通用聊天完成接口
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"聊天完成请求失败: {e}")
            return None
