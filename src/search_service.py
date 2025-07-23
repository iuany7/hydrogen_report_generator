
"""
搜索服务模块
"""
import requests
from typing import List, Dict, Optional
from loguru import logger
from config import SERPAPI_API_KEY, SEARCH_RESULTS_NUM, SEARCH_CACHE_ENABLED


class SearchService:
    """网络搜索服务类"""
    
    def __init__(self, api_key: str = SERPAPI_API_KEY):
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search.json"
        
    def search_web(self, query: str, num: int = SEARCH_RESULTS_NUM) -> List[Dict]:
        """
        使用SerpApi搜索网页内容
        
        Args:
            query: 搜索关键词
            num: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        try:
            logger.info(f"搜索关键词: {query}")
            
            params = {
                "q": query,
                "api_key": self.api_key,
                "num": num,
                "no_cache": not SEARCH_CACHE_ENABLED
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            organic_results = data.get("organic_results", [])
            
            results = []
            for item in organic_results[:num]:
                results.append({
                    "title": item.get("title", ""),
                    "date": item.get("date", ""),
                    "source": item.get("source") or item.get("displayed_link", ""),
                    "snippet": item.get("snippet", "")
                })
            
            logger.info(f"搜索完成，返回 {len(results)} 条结果")
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"搜索请求失败: {e}")
            return []
        except Exception as e:
            logger.error(f"搜索过程中发生错误: {e}")
            return []
    
    def format_search_results(self, results: List[Dict]) -> str:
        """
        格式化搜索结果为文本
        
        Args:
            results: 搜索结果列表
            
        Returns:
            格式化后的文本
        """
        if not results:
            return "未找到相关搜索结果"
        
        formatted_items = []
        for item in results:
            formatted_item = f"{item['date']} | {item['title']}\n{item['source']}\n{item['snippet']}"
            formatted_items.append(formatted_item)
        
        return "\n\n".join(formatted_items)
