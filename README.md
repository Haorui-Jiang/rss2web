# Academic RSS Monitor 📚

**基于Python的学术期刊资讯聚合与智能展示系统 | 追踪最新研究成果**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

监控学术期刊动态，自动构建双语知识库的智能解决方案。

## 功能特点

- 自动根据 RSS 抓取并解析期刊论文信息
- 抓取信息时自动过滤已保存的期刊论文
- 文章标题中英文双语显示
- 可将生成的 Excel 文件作为知识库，导入 AI 大模型快速提取所需信息
- 在生成的网页中可根据标题、作者等信息进行实时搜索

## 技术栈

- **核心框架**: Python 3.8+
- **数据处理**: feedparser + Pandas + lxml etree
- **翻译引擎**: 智谱 AI glm-4-plus 模型
- **网页生成**: Jinja2 + Bootstrap 5

## 使用说明

### 文件结构

```python
project/
├── api_key.txt			# 大模型 API Key
├── requirements.txt	# Python 依赖模块
├── rss2excel.py		# rss 解析脚本
├── papers.xlsx       	# 解析脚本生成的 Excel 数据文件
├── template.html     	# 网页模板
├── generate_website.py # 生成网页脚本
└── index.html        	# 生成的网页
```

### Excel 数据结构

| 列名 | 说明 |
|-------------------|--------------------|
| title | 英文标题 |
| title_zh | 中文标题 |
| publication_date | 出版日期 |
| source | 期刊、卷号等信息 |
| author | 作者（逗号分隔） |
| link | 论文链接 |

### 运行流程

```python
# 1. 设置大模型 API Key
# 智谱 AI 开放平台 API Key 网址：https://bigmodel.cn/usercenter/proj-mgmt/apikeys
# 将创建的 API Key 复制粘贴至 api_key.txt 并保存文件
# 注意不要与他人共享 API Key，避免将其暴露在浏览器和其他客户端代码中。

# 2. 安装依赖
pip install -r requirements.txt

# 3. 解析 rss，翻译论文标题，整理论文信息，并将数据保存至 Excel 文件
python rss2excel.py

# 4. 生成网页
python generate_website.py

# 5. 打开生成的 index.html，查看期刊论文信息
```

### 注意事项

- 示例代码基于 [Journal of Historical Geography](https://www.sciencedirect.com/journal/journal-of-historical-geography) 官网中的 RSS 链接进行数据提取。如需获取其他期刊 RSS 链接，请自行去对应期刊官网查找。且不同期刊 RSS 格式可能有所差异，可自行调整 rss2excel 代码。
- 示例代码通过 OpenAI SDK 调用[智谱 AI 大模型](https://bigmodel.cn/)进行标题翻译，如需使用其他大模型请自行调整 rss2excel 代码。
- RSS 链接中仅包含过去的论文信息，配置完成后请定期运行代码更新数据库。

## 致谢

本程序初始灵感来自锐多宝（程锐）开源发布的 [rss2web](https://github.com/ruiduobao/rss2web) 项目，核心代码在继承其设计理念的基础上进行调整。通过他的公众号【锐多宝】收获了很多知识和方法，真诚感谢他多年来无私的技术分享。

本程序代码参考自[智谱](https://bigmodel.cn/)、[Kimi](https://kimi.moonshot.cn/)、[DeepSeek](https://www.deepseek.com/)（[腾讯元宝](https://yuanbao.tencent.com/)）等国产大模型，衷心感谢这些人工智能研究团队的技术支持。
