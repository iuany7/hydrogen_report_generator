"""
HTML模板模块
"""

BASE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {styles}
    </style>
</head>
<body>
    <div class="header">{header}</div>
    <div class="footer">{footer}</div>
    <div class="content">
        {content}
    </div>
</body>
</html>
"""

BASE_CSS_STYLES = """
body {
    font-family: "Microsoft YaHei", "LXGW WenKai", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
    background: white;
    padding: 140px 50px 60px 50px;
    line-height: 1.8;
    max-width: 960px;
    margin: auto;
    font-size: 16px;
    color: #333;
}

h1, h2, h3, h4, h5, h6 {
    color: #003366;
    margin-top: 20px;
    margin-bottom: 10px;
    font-weight: 600;
}

h1 {
    font-size: 28px;
    border-bottom: 2px solid #003366;
    padding-bottom: 10px;
}

h2 {
    font-size: 24px;
    margin-top: 30px;
}

h3 {
    font-size: 20px;
    margin-top: 25px;
}

h4 {
    font-size: 18px;
    color: #004080;
    margin-top: 20px;
}

p {
    margin-bottom: 12px;
    text-align: justify;
}

ul, ol {
    margin-bottom: 16px;
    padding-left: 20px;
}

li {
    margin-bottom: 8px;
    line-height: 1.6;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 14px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

th {
    background-color: #f0f8ff;
    color: #003366;
    font-weight: 600;
    padding: 12px;
    text-align: center;
    border: 1px solid #ddd;
}

td {
    padding: 10px;
    text-align: center;
    border: 1px solid #ddd;
    background-color: #fafafa;
}

tr:nth-child(even) td {
    background-color: #f9f9f9;
}

tr:hover td {
    background-color: #e6f3ff;
}

code {
    background: #f4f4f4;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: "Courier New", monospace;
    font-size: 14px;
    color: #d63384;
}

pre {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 6px;
    overflow-x: auto;
    border-left: 4px solid #003366;
    margin: 16px 0;
}

pre code {
    background: none;
    padding: 0;
    color: #333;
}

blockquote {
    background: #f0f8ff;
    border-left: 4px solid #003366;
    padding: 15px 20px;
    margin: 16px 0;
    font-style: italic;
    color: #555;
}

.header {
    position: fixed;
    top: 40px;
    left: 50px;
    right: 50px;
    font-weight: bold;
    color: #004080;
    font-size: 30px;
    text-align: center;
    z-index: 1000;
    background: white;
    padding: 10px 0;
    border-bottom: 2px solid #e6f3ff;
}

.footer {
    position: fixed;
    bottom: 10px;
    left: 50px;
    right: 50px;
    font-size: 14px;
    color: #999;
    text-align: center;
    z-index: 1000;
    background: white;
    padding: 10px 0;
    border-top: 1px solid #e6f3ff;
}

.content {
    position: relative;
    z-index: 1;
}

.highlight {
    background-color: #fff3cd;
    padding: 2px 4px;
    border-radius: 3px;
    font-weight: 500;
}

.date-tag {
    background-color: #e6f3ff;
    color: #003366;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
    margin-right: 8px;
}

.source-tag {
    background-color: #f0f8ff;
    color: #666;
    padding: 2px 6px;
    border-radius: 8px;
    font-size: 11px;
    margin-left: 8px;
}

.section-divider {
    height: 2px;
    background: linear-gradient(to right, #003366, #e6f3ff, #003366);
    margin: 30px 0;
    border-radius: 1px;
}

.logo-container {
    position: fixed;
    top: 40px;
    right: 50px;
    z-index: 1001;
}

.logo-container img {
    width: 80px;
    height: 80px;
    object-fit: contain;
}

@media print {
    body {
        padding: 120px 40px 40px 40px;
    }
    
    .header, .footer {
        position: static;
        margin: 0;
        padding: 10px 0;
    }
    
    .logo-container {
        position: static;
        float: right;
        margin-bottom: 20px;
    }
}
"""

REPORT_SECTIONS_TEMPLATE = """
<div class="section-divider"></div>
<h2>{section_title}</h2>
<div class="section-content">
    {section_content}
</div>
"""

TABLE_TEMPLATE = """
<table>
    <thead>
        <tr>
            {table_headers}
        </tr>
    </thead>
    <tbody>
        {table_rows}
    </tbody>
</table>
"""

NEWS_ITEM_TEMPLATE = """
<div class="news-item">
    <span class="date-tag">{date}</span>
    <strong>{title}</strong>
    <span class="source-tag">{source}</span>
    <p>{content}</p>
</div>
"""