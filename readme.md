# 氢能产业简报生成系统

一个基于大型语言模型（LLM）和网络搜索的自动化工具，用于搜集、整理并生成结构化的氢能产业简报。  
可以调整templates.prompts/html_templates后用于生成各种内容/类型的结构化简报。

## 核心功能

-  **智能搜索**: 利用SerpApi进行多维度的实时信息检索。
-  **AI分析与整合**: 使用DeepSeek大语言模型对信息进行深度分析、去重和结构化整理。
-  **结构化报告**: 自动生成包含政策、行业动态、热点聚焦、前沿理论和关键数据五个部分的专业简报。
-  **自定义输出**: 将生成的报告与图片以附件形式传输给指定邮箱。
-  **精美可视化**: 将生成的报告自动化渲染为高质量的PNG图片序列和完整的PDF文档。
-  **自定义模板**: 报告的视觉样式（CSS）和内容提示（Prompt）均可通过模板文件轻松定制。

## 环境要求

- Python 3.8 或更高版本（不要3.13，不兼容）
- Google Chrome 浏览器（用于`html2image`库在后台进行截图）

## 安装与配置

**1. 克隆仓库**

```bash
git clone https://github.com/iuany7/hydrogen_report_generator.git
cd hydrogen_report_generator
```

**2. 创建并激活虚拟环境**

我们强烈建议在虚拟环境中使用此项目。

- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows**:
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

**3. 安装依赖**

```bash
pip install -r requirements.txt
```

**4. 配置API密钥**

项目需要`DeepSeek`和`SerpApi`的API密钥才能正常工作。

```bash
# 复制环境变量模板文件
cp .env.example .env
```

然后，编辑新创建的`.env`文件，填入您自己的API密钥：

```dotenv
# .env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here
```

- **DeepSeek API Key**: 从 [platform.deepseek.com](https://platform.deepseek.com) 获取。
- **SerpApi API Key**: 从 [serpapi.com](https://serpapi.com) 获取。

## 使用方法

完成安装和配置后，直接运行`main.py`即可开始生成报告。

```bash
python main.py
```

生成的报告图片和PDF文件将保存在`output/`目录下。

## 项目结构

```
/
├── main.py                 # 主程序入口
├── config.py               # 全局配置文件（报告样式、字体、尺寸等）
├── requirements.txt        # Python依赖列表
├── .env.example            # 环境变量模板
├── readme.md               # 本说明文件
├── LICENSE                 # MIT许可证
├── src/                    # 核心源代码
│   ├── email_service.py    # 邮箱发送服务             
│   ├── llm_service.py      # LLM服务交互
│   ├── search_service.py   # 搜索引擎服务
│   └── report_generator.py # 报告生成与可视化
├── templates/              # 模板文件
│   ├── prompts.py          # LLM提示词模板
│   └── html_template.py    # 报告HTML与CSS样式模板
├── assets/                 # 静态资源
│   └── logo.png            # 报告中使用的Logo（自行选择加入）
└── output/                 # **（自动生成）**报告输出目录
```

## 自定义

- **报告样式**: 修改 `templates/html_template.py` 中的 `BASE_CSS_STYLES` 变量。
- **报告内容与结构**: 修改 `templates/prompts.py` 中的 `get_hydrogen_report_prompt` 函数。
- **页面与字体**: 修改 `config.py` 中的相关配置项。

## 技术栈

- **LLM**: DeepSeek Chat API
- **搜索**: SerpApi
- **文档处理**: markdown2
- **图像生成**: html2image, Pillow
- **日志**: Loguru
- **进度条**: tqdm

## 许可证

本项目基于 [MIT License](LICENSE) 开源。
