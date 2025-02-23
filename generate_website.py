# -*- encoding: utf-8 -*-
"""
    @ 程序名称: generate_website.py
    @ 程序功能: 基于 Excel 创建网页
"""

import pandas as pd
from jinja2 import Template


def read_excel(file_path):
    df = pd.read_excel(file_path, engine="openpyxl")

    # 强制类型转换和空值处理
    df["author"] = df["author"].fillna("").astype(str)

    # 验证链接格式
    df["link"] = df["link"].apply(lambda x: x if str(x).startswith("http") else "#")

    return df.to_dict(orient="records")


def render_template(template_path, papers):  # 修改参数名称
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(papers=papers)  # 保持参数名称一致


if __name__ == "__main__":
    papers_data = read_excel("papers.xlsx")
    html = render_template("template.html", papers=papers_data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
