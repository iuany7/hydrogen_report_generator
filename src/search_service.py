
"""
搜索服务模块
"""
import requests
import time
from typing import List, Dict
from loguru import logger
from config import SERPAPI_API_KEY, SEARCH_RESULTS_NUM, SERPAPI_ENGINES, SEARCH_DELAY

class SearchService:
    """
    高质量、稳定的多引擎串行搜索服务。
    """
    def __init__(self, api_key: str = SERPAPI_API_KEY, engines: List[str] = SERPAPI_ENGINES):
        if not api_key:
            logger.warning("SerpApi API key 未配置。搜索功能将不可用。")
        if not engines:
            logger.warning("未指定任何搜索引擎。搜索功能将不可用。")
            
        self.api_key = api_key
        self.engines = [e.strip() for e in engines]
        self.base_url = "https://serpapi.com/search.json"

    def search(self, query: str, num_results: int = SEARCH_RESULTS_NUM) -> List[Dict]:
        """
        对单个查询词，串行查询多个搜索引擎，并汇总结果。

        Args:
            query (str): 单个搜索查询词。
            num_results (int): 每个搜索引擎期望返回的结果数量。

        Returns:
            List[Dict]: 从所有搜索引擎汇总的、去重后的搜索结果列表。
        """
        if not self.api_key or not self.engines:
            logger.error("搜索服务未正确配置，无法执行搜索。")
            return []

        logger.info(f"开始在 {self.engines} 上对 '{query}' 进行串行搜索...")
        
        all_results = []
        seen_links = set()

        for engine in self.engines:
            logger.info(f" -> 正在查询引擎: {engine}...")
            params = {
                "q": query,
                "api_key": self.api_key,
                "num": num_results,
                "engine": engine,
            }
            try:
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json().get("organic_results", [])
                
                count = 0
                for item in data:
                    link = item.get("link") or item.get("href")
                    if link and link not in seen_links:
                        all_results.append({
                            "title": item.get("title", ""),
                            "date": item.get("date", ""),
                            "source": item.get("source") or item.get("displayed_link", ""),
                            "snippet": item.get("snippet", ""),
                            "engine": engine
                        })
                        seen_links.add(link)
                        count += 1
                logger.info(f"    从 {engine} 获得 {count} 条新结果。")

            except requests.exceptions.RequestException as e:
                logger.error(f"    查询 {engine} 失败: {e}")
            except Exception as e:
                logger.error(f"    处理 {engine} 的结果时出错: {e}")
            
            # 在每次API调用后都暂停，这是避免速率限制的关键
            time.sleep(SEARCH_DELAY)

        logger.success(f"对 '{query}' 的搜索完成，共获得 {len(all_results)} 条独立结果。")
        return all_results

    def format_search_results(self, results: List[Dict]) -> str:
        """
        将搜索结果列表格式化为单个字符串。
        """
        if not results:
            return "未找到相关搜索结果。"
        
        formatted_items = []
        for item in results:
            date_str = f"{item.get('date', '无日期')} | " if item.get('date') else ""
            engine_str = f"[{item.get('engine', '未知引擎')}] "
            formatted_item = f"{engine_str}{date_str}{item['title']}\n来源: {item['source']}\n摘要: {item['snippet']}"
            formatted_items.append(formatted_item)
        
        return "\n\n---\n\n".join(formatted_items)

