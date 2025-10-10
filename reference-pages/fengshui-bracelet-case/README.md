# 网页抓取与分析工具集

## 📁 项目结构

```
fengshui-bracelet-case/
├── product-specific/          # 产品特定内容（每个产品都不同）
│   ├── content/               # 网页内容
│   │   ├── index.html        # 完整的独立网页（已嵌入所有资源）
│   │   ├── css/              # CSS文件
│   │   └── js/               # JavaScript文件
│   └── images/               # 原始图片资源
│       ├── 4081/             # 产品图片
│       ├── 19578/            # 图标
│       ├── 3986/             # 其他资源
│       └── api/              # 用户头像
│
├── reusable-tools/           # 可复用工具（适用于所有项目）
│   ├── download_assets.py    # 下载网页资源
│   ├── fix_links.py          # 修复本地链接
│   ├── embed_images.py       # 嵌入图片到HTML
│   ├── embed_avatars.py      # 嵌入用户头像
│   ├── embed_css_js.py       # 嵌入CSS和JS
│   └── analyze_images.py     # 分析图片资源
│
├── analysis/                 # 分析文档
│   ├── marketing-analysis.md # 营销策略深度分析
│   └── README.md             # 项目总结报告
│
└── backups/                  # 备份文件
    ├── index.html.backup     # 原始HTML
    ├── index_before_embed.html
    └── index_before_css_js_embed.html
```

---

## 🔧 工具使用说明

### 1. download_assets.py - 资源下载器

**功能**: 解析HTML并下载所有图片、CSS、JS资源

**使用方法**:
```python
# 修改以下参数
base_dir = Path('/your/output/directory')
html_file = base_dir / 'index.html'
base_url = 'https://target-website.com'
```

**输出**: 
- `images/` 文件夹（所有图片）
- `css/` 文件夹（样式表）
- `js/` 文件夹（脚本）

---

### 2. fix_links.py - 链接修复器

**功能**: 将HTML中的远程URL替换为本地路径

**适用场景**: 下载资源后，需要让HTML引用本地文件

**使用方法**:
```python
# 配置路径
base_dir = Path('/your/project/directory')
html_file = base_dir / 'index.html'
```

**替换规则**:
```python
replacements = [
    (r'href="/core\.min\.css"', 'href="css/core.min.css"'),
    (r'src="/core\.min\.js"', 'src="js/core.min.js"'),
    (r'//img\.domain\.com/', 'images/'),
]
```

---

### 3. embed_images.py - 图片嵌入器

**功能**: 将本地图片转换为base64编码，直接嵌入HTML

**优点**:
- ✅ 单文件，易于分享
- ✅ 离线可用
- ✅ 无需管理图片路径

**缺点**:
- ⚠️ 文件体积大
- ⚠️ 不利于SEO

**使用方法**:
```python
base_dir = Path('/your/project/directory')
html_file = base_dir / 'index.html'
```

---

### 4. embed_avatars.py - 头像嵌入器

**功能**: 专门处理评论区或用户头像的嵌入

**使用场景**: 当主图片嵌入后，还有零散的用户头像需要处理

---

### 5. embed_css_js.py - 样式脚本嵌入器

**功能**: 将外部CSS和JS文件内联到HTML中

**最终效果**: 完全独立的单HTML文件

---

### 6. analyze_images.py - 图片分析器

**功能**: 统计和分类图片资源

**输出信息**:
- 图片总数
- 图片分类（产品图、场景图、头像、图标）
- 文件大小
- 动画GIF识别

---

## 🎯 完整工作流程

### 步骤1: 下载网页

```bash
# 1. 下载HTML
curl -L 'https://target-url.com' -o index.html

# 2. 运行资源下载器
python3 download_assets.py
```

### 步骤2: 修复链接

```bash
python3 fix_links.py
```

### 步骤3: 嵌入资源

```bash
# 嵌入图片
python3 embed_images.py

# 嵌入头像（如果有）
python3 embed_avatars.py

# 嵌入CSS和JS
python3 embed_css_js.py
```

### 步骤4: 分析内容

```bash
# 分析图片资源
python3 analyze_images.py

# 人工分析文案和设计
# 输出到 marketing-analysis.md
```

---

## 🔄 如何应用到新产品

### 准备工作

1. 创建新项目文件夹：
```bash
mkdir new-product-case
cd new-product-case
```

2. 复制可复用工具：
```bash
cp -r ../fengshui-bracelet-case/reusable-tools ./
```

3. 创建必要的文件夹：
```bash
mkdir -p product-specific/{content,images}
mkdir -p analysis
mkdir -p backups
```

---

### 配置参数

每个Python脚本需要修改的参数：

#### download_assets.py
```python
base_dir = Path('/path/to/new-product-case/product-specific')
base_url = 'https://new-target-website.com'
```

#### fix_links.py
```python
base_dir = Path('/path/to/new-product-case/product-specific')

# 根据目标网站调整替换规则
replacements = [
    (r'//cdn\.example\.com/', 'images/'),
    # 添加其他替换规则
]
```

#### embed_*.py 系列
```python
base_dir = Path('/path/to/new-product-case/product-specific')
```

---

## 📊 分析模板

### 营销分析框架

对于任何营销页面，按以下结构分析：

#### 1. 文案结构
- 开场钩子（Hook）
- 故事叙事（Story）
- 产品解释（Mechanism）
- 社会证明（Social Proof）
- 行动号召（CTA）

#### 2. 情感调动
- 痛点识别
- 情感弧线
- 共鸣点
- 希望构建

#### 3. 转化策略
- 心理触发器
- 紧迫感制造
- 稀缺性暗示
- 异议处理

#### 4. 视觉设计
- 图片功能分析
- 色彩心理学
- 排版逻辑
- 视觉层级

#### 5. 目标受众
- 人口统计
- 心理特征
- 痛点需求
- 购买动机

---

## 📝 配置文件模板

### config.json（建议创建）

```json
{
  "project_name": "FengShui Bracelet Case Study",
  "target_url": "https://offer.fengshuibracelets.co/fengshui/news",
  "base_domain": "offer.fengshuibracelets.co",
  "download_date": "2025-10-08",
  
  "paths": {
    "output_dir": "/Users/ming/Documents/HUGO/aura-three-official/reference-pages",
    "content_dir": "product-specific/content",
    "images_dir": "product-specific/images",
    "tools_dir": "reusable-tools",
    "analysis_dir": "analysis"
  },
  
  "url_replacements": [
    {"pattern": "//img.funnelish.com/", "replace": "images/"},
    {"pattern": "https://randomuser.me/api/", "replace": "images/api/"}
  ],
  
  "analysis_template": "marketing-analysis-template.md"
}
```

---

## 🚀 进阶使用

### 批量处理

创建主控脚本 `master.py`：

```python
import subprocess
import sys

scripts = [
    'download_assets.py',
    'fix_links.py',
    'embed_images.py',
    'embed_avatars.py',
    'embed_css_js.py'
]

for script in scripts:
    print(f"\n{'='*60}")
    print(f"Running: {script}")
    print('='*60)
    result = subprocess.run(['python3', script])
    if result.returncode != 0:
        print(f"❌ Error in {script}")
        sys.exit(1)

print("\n✅ All tasks completed!")
```

---

### 自动化分析

创建分析脚本 `auto_analyze.py`：

```python
import re
from pathlib import Path
from bs4 import BeautifulSoup

def analyze_page_structure(html_file):
    """分析页面结构"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    analysis = {
        'headings': len(soup.find_all(['h1', 'h2', 'h3'])),
        'paragraphs': len(soup.find_all('p')),
        'images': len(soup.find_all('img')),
        'buttons': len(soup.find_all(class_='btn')),
        'word_count': len(soup.get_text().split())
    }
    
    return analysis
```

---

## 💡 最佳实践

### 1. 文件命名规范

```
产品名-case/
├── product-specific/
│   ├── content/
│   │   └── index-{date}.html
│   └── images/
│       └── {category}/{filename}
├── reusable-tools/
│   └── {function}_v{version}.py
└── analysis/
    └── {product}-analysis-{date}.md
```

### 2. 版本控制

- 每次重要修改创建备份
- 使用Git管理代码
- 在文件中添加版本注释

### 3. 文档维护

- 每个工具添加详细注释
- 更新README记录使用心得
- 记录遇到的问题和解决方案

---

## 🔍 常见问题

### Q1: 下载的图片路径不对怎么办？

**A**: 检查并修改 `fix_links.py` 中的替换规则，确保匹配目标网站的URL模式。

### Q2: 嵌入后HTML文件太大怎么办？

**A**: 
- 压缩图片（使用tinypng等工具）
- 只嵌入关键图片
- 考虑使用懒加载

### Q3: 如何处理动态加载的内容？

**A**: 
- 使用浏览器开发者工具查看实际加载的内容
- 考虑使用Selenium等工具模拟浏览器
- 分析AJAX请求，直接获取数据

### Q4: 分析文档写多详细？

**A**: 
- 基础版：结构+策略概述（2-3页）
- 标准版：详细分析+案例（10-15页）
- 专业版：完整分析+模板+建议（20+页）

---

## 📚 相关资源

### 学习资料

- **文案写作**: "The Copywriter's Handbook" by Robert Bly
- **营销心理学**: "Influence" by Robert Cialdini
- **故事营销**: "Building a StoryBrand" by Donald Miller
- **登陆页优化**: "Landing Page Optimization" by Tim Ash

### 工具推荐

- **抓取工具**: wget, HTTrack, SingleFile（浏览器插件）
- **图片优化**: TinyPNG, ImageOptim
- **分析工具**: Google Analytics, Hotjar
- **A/B测试**: Optimizely, VWO

---

## 📞 维护日志

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2025-10-08 | 1.0 | 初始版本，完成FengShui Bracelet案例 |
| | | 创建工具集和分析框架 |

---

## 🎯 下一步计划

- [ ] 添加命令行参数支持
- [ ] 创建Web界面
- [ ] 集成AI分析功能
- [ ] 支持批量处理多个页面
- [ ] 添加数据可视化

---

*最后更新: 2025年10月8日*  
*维护者: Ming*
