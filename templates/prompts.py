"""
提示词模板模块
"""
from datetime import datetime, timedelta

def get_hydrogen_report_prompt() -> str:
    """
    生成包含动态日期范围的氢能产业报告Prompt。
    """
    today = datetime.now()
    two_weeks_ago = today - timedelta(weeks=2)
    
    start_date = two_weeks_ago.strftime("%Y年%m月%d日")
    end_date = today.strftime("%Y年%m月%d日")

    return f"""
【第一步指令】
你的第一个任务是，根据下方【报告要求】中提到的所有主题（政策、行业动态、技术、数据等），生成一个高度浓缩的、不超过10个的综合性查询词列表。这些查询词应该具有代表性，能够覆盖报告的核心领域。请调用 `execute_searches` 工具来执行搜索。

【报告要求】

【数据时间范围】
请搜索 **{start_date} 至 {end_date}** 之间的信息。

【地域范围】
中国与国际（如德国、日本、美国、澳大利亚、韩国等）。

【信息结构】按以下五个部分分类整理：

### Part 1: 核心政策与事件
- 汇总中外氢能领域最重要的政策发布、法规变化、及重大行业事件。

### Part 2: 关键行业动态
- 整理最具代表性的企业动态、新项目、投融资等。

### Part 3: 市场热点
- 汇总行业内的热点新闻或重要企业动态。

### Part 4: 技术前沿
- 收录最新的关键技术突破或重要学术成果。

### Part 5: 重点数据
- 展示中外氢能行业关键数据，如新增产能、装机量、汽车销量等。

【最终报告输出要求】
- 在你接收到搜索结果后，请根据【报告要求】的结构，生成最终的行业简报。
- 内容必须真实、权威，拒绝虚构和旧闻。
"""
