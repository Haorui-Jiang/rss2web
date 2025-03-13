# -*- encoding: utf-8 -*-
"""
    @ 程序名称: rss2excel_jhg.py
    @ 程序功能: 从 RSS 网站获取最新论文信息，并将其保存到 Excel 文件中
    @ 示例数据: Journal of Historical Geography
"""

import feedparser
from lxml import etree
import pandas as pd
from openai import OpenAI
import os
from datetime import datetime


# 读取 API 密钥
def read_api_key(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        api_key = file.readline().strip()
    return api_key


# RSS 链接 (Journal of Historical Geography)
rss_url = "https://rss.sciencedirect.com/publication/science/03057488"

# 文件名
excel_file = "papers.xlsx"

# 检测 Excel 文件是否存在
if os.path.exists(excel_file):
    # 如果 Excel 文件存在，则读取该文件
    df_existing = pd.read_excel(excel_file)
else:
    # 如果不存在，则创建一个空的 DataFrame
    df_existing = pd.DataFrame(
        columns=["title", "title_zh", "publication_date", "source", "author", "link", "created_time"]
    )

# 解析RSS
feed = feedparser.parse(rss_url)

# 用于存储新论文数据
new_data = []

# 遍历所有文章，并输出每篇文章的标题、出版日期、来源、作者及文章链接
for entry in feed.entries:
    title = entry.title
    summary = entry.summary
    link = entry.id

    # 检查标题是否已存在
    if not df_existing[df_existing["title"] == title].empty:
        print(f"论文 {title} 已存在，跳过该文章")
        continue

    # 通过 OpenAI SDK 调用智谱 AI 大模型，翻译标题
    client = OpenAI(
        api_key=read_api_key("api_key.txt"),
        base_url="https://open.bigmodel.cn/api/paas/v4/",
    )

    completion = client.chat.completions.create(
        model="glm-4-plus",
        messages=[
            {
                "role": "system",
                "content": f"请使用学术翻译模型将英文标题{title}翻译成中文",
            },
            {
                "role": "system",
                "content": "如词汇翻译存在问题，请自行根据上下文选择一个最合适的翻译",
            },
            {
                "role": "system",
                "content": "请直接输出不包含书名号的翻译结果，无需对翻译结果进行任何补充说明",
            },
            {"role": "user", "content": "中文翻译结果"},
        ],
        top_p=0.7,
        temperature=0.9,
    )

    title_zh = completion.choices[0].message.content

    # 通过 XPath 提取出版日期、来源、作者等信息
    e = etree.HTML(summary)
    publication_date_text = e.xpath('//p[contains(text(), "Publication date:")]/text()')
    publication_date = publication_date_text[0].split("Publication date: ")[1].strip()

    source_text = e.xpath('//p/b[contains(text(), "Source:")]/parent::p/text()')
    source = source_text[0].strip()

    author_text = e.xpath('//p[contains(text(), "Author(s):")]/text()')
    author = author_text[0].split("Author(s): ")[1].strip()

    # 获取当前时间并格式化
    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("论文标题:", title)
    print("中文标题:", title_zh)
    print("出版日期:", publication_date)
    print("来源:", source)
    print("作者:", author)
    print("文章链接:", link)
    print("创建时间:", created_time)
    print()  # 在不同文章之间添加空行

    # 将新论文的数据添加到列表
    new_data.append([title, title_zh, publication_date, source, author, link, created_time])


# 如果有新数据，将其添加到 DataFrame 并保存
if new_data:
    df_new = pd.DataFrame(
        new_data,
        columns=["title", "title_zh", "publication_date", "source", "author", "link", "created_time"]
    )
    df_combined = pd.concat([df_new, df_existing], ignore_index=True)
    df_combined.to_excel(excel_file, index=False)
