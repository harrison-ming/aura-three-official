# 快速开始指南

## 🚀 5分钟上手

### 场景：分析一个新的营销页面

#### 步骤1: 准备环境（30秒）

```bash
# 进入工具目录
cd /path/to/fengshui-bracelet-case

# 创建新项目
mkdir ../new-product-case
cd ../new-product-case

# 复制工具
cp -r ../fengshui-bracelet-case/reusable-tools ./
mkdir -p product-specific/{content,images} analysis backups
```

#### 步骤2: 下载页面（1分钟）

```bash
# 方法1: 使用curl（快速）
curl -L 'https://target-url.com' -o product-specific/content/index.html

# 方法2: 使用wget（更完整）
wget --mirror --page-requisites 'https://target-url.com' -P product-specific/content/
```

#### 步骤3: 运行工具（2分钟）

```bash
cd reusable-tools

# 1. 下载所有资源
python3 download_assets.py

# 2. 修复链接
python3 fix_links.py

# 3. 嵌入图片（可选，如果需要单文件）
python3 embed_images.py
python3 embed_avatars.py
python3 embed_css_js.py
```

#### 步骤4: 开始分析（1分钟）

```bash
# 在浏览器中打开
open ../product-specific/content/index.html

# 或者在编辑器中分析
code ../product-specific/content/index.html
```

---

## 📝 工具配置清单

### 每个工具需要修改的地方

#### 1. download_assets.py

```python
# 第 7-10 行
base_dir = Path('/Users/ming/Documents/HUGO/aura-three-official/reference-pages')  # 改成你的路径
html_file = base_dir / 'index.html'
base_url = 'https://offer.fengshuibracelets.co'  # 改成目标网站域名
```

#### 2. fix_links.py

```python
# 第 6-7 行
base_dir = Path('/path/to/your/project')
html_file = base_dir / 'index.html'

# 第 17-25 行 - 根据目标网站调整
replacements = [
    (r'href="/core\.min\.css"', 'href="css/core.min.css"'),
    (r'src="/core\.min\.js"', 'src="js/core.min.js"'),
    (r'//img\.target-cdn\.com/', 'images/'),  # 修改为目标CDN
]
```

#### 3. embed_images.py / embed_avatars.py / embed_css_js.py

```python
# 所有文件的 main 函数中
base_dir = Path('/path/to/your/project')
html_file = base_dir / 'index.html'
```

---

## 🎯 常用命令速查

### 文件操作

```bash
# 查看项目结构
tree -L 3

# 查看文件大小
du -sh *

# 统计图片数量
find images -type f | wc -l

# 查找特定类型文件
find . -name "*.png" -o -name "*.jpg"
```

### Python 脚本

```bash
# 运行单个脚本
python3 reusable-tools/download_assets.py

# 批量运行（创建 run_all.sh）
for script in reusable-tools/*.py; do
    echo "Running $script..."
    python3 "$script"
done
```

### HTML 分析

```bash
# 提取所有链接
grep -o 'href="[^"]*"' index.html

# 查找所有图片标签
grep -o '<img[^>]*>' index.html

# 统计字数
wc -w index.html
```

---

## 🔧 故障排除

### 问题1: 图片下载失败

**症状**: `✗ Failed to download https://...`

**解决方案**:
```python
# 在 download_assets.py 中增加超时时间
with urllib.request.urlopen(req, timeout=60) as response:  # 从30改为60
```

### 问题2: 链接替换不生效

**症状**: HTML中的链接还是远程URL

**解决方案**:
1. 查看实际的URL格式
```bash
grep "img.example.com" index.html | head -5
```

2. 调整正则表达式
```python
# 如果是 //img.example.com，不要加 https:
(r'//img\.example\.com/', 'images/')
```

### 问题3: Python 脚本报错

**症状**: `ModuleNotFoundError: No module named 'bs4'`

**解决方案**:
```bash
# 安装依赖
pip3 install beautifulsoup4

# 如果需要其他依赖
pip3 install requests lxml
```

### 问题4: 文件太大无法打开

**症状**: 嵌入后的HTML文件超过50MB，编辑器打不开

**解决方案**:
1. 使用浏览器直接打开（浏览器能处理大文件）
2. 压缩图片后重新嵌入
3. 只嵌入关键图片，其他保持外部引用

---

## 💡 使用技巧

### 技巧1: 快速预览

```bash
# macOS
open product-specific/content/index.html

# Linux
xdg-open product-specific/content/index.html

# Windows
start product-specific/content/index.html
```

### 技巧2: 对比版本

```bash
# 对比原始版本和修改后的版本
diff backups/index.html.backup product-specific/content/index.html > changes.diff
```

### 技巧3: 批量处理图片

```bash
# 压缩所有PNG图片（需要pngquant）
find images -name "*.png" -exec pngquant --force --ext .png {} \;

# 转换为WebP格式
for img in images/**/*.{jpg,png}; do
    cwebp "$img" -o "${img%.*}.webp"
done
```

### 技巧4: 提取文本内容

```bash
# 使用Python提取所有文本
python3 << 'EOF'
from bs4 import BeautifulSoup

with open('product-specific/content/index.html', 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')
    text = soup.get_text(separator='\n', strip=True)
    
with open('analysis/extracted-text.txt', 'w') as f:
    f.write(text)
EOF
```

---

## 📊 分析检查清单

### 内容分析 ✓

- [ ] 标题/副标题结构
- [ ] 故事叙事（如果有）
- [ ] 产品卖点
- [ ] 社会证明（评论、案例）
- [ ] 紧迫感元素
- [ ] CTA按钮位置和文案

### 视觉分析 ✓

- [ ] 首屏视觉冲击
- [ ] 图片类型和数量
- [ ] 色彩方案
- [ ] 排版层级
- [ ] 动画效果

### 技术分析 ✓

- [ ] 页面加载速度
- [ ] 移动端适配
- [ ] 图片优化
- [ ] SEO优化
- [ ] 跟踪代码

### 心理学分析 ✓

- [ ] 目标受众
- [ ] 痛点识别
- [ ] 情感触发
- [ ] 信任建立
- [ ] 异议处理

---

## 🎨 分析模板

### 基础模板（适合快速分析）

```markdown
# [产品名] 营销页面分析

## 第一印象
- 主色调：
- 核心信息：
- 情感基调：

## 内容结构
1. 开场：
2. 主体：
3. 结尾：

## 关键要素
- 最强卖点：
- 社会证明：
- 紧迫感：
- CTA文案：

## 学习要点
1.
2.
3.

## 可改进之处
1.
2.
3.
```

### 标准模板（适合完整分析）

参考 `fengshui-bracelet-case/analysis/marketing-analysis.md`

---

## 🔄 工作流程图

```
┌─────────────┐
│  发现页面    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 下载HTML    │ → curl / wget
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 下载资源    │ → download_assets.py
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 修复链接    │ → fix_links.py
└──────┬──────┘
       │
       ├─────────────┐
       ▼             ▼
┌─────────────┐  ┌─────────────┐
│ 本地浏览    │  │ 嵌入资源    │ → embed_*.py
└─────────────┘  └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │ 单文件版本  │
                 └──────┬──────┘
                        │
       ┌────────────────┴────────────────┐
       ▼                                 ▼
┌─────────────┐                  ┌─────────────┐
│ 内容分析    │                  │ 视觉分析    │
└──────┬──────┘                  └──────┬──────┘
       │                                │
       └────────────┬───────────────────┘
                    ▼
            ┌─────────────┐
            │ 输出报告    │
            └─────────────┘
```

---

## 📦 项目打包

### 分享给他人

```bash
# 创建压缩包（不包含大文件）
tar -czf project-analysis.tar.gz \
  --exclude='*.html' \
  --exclude='images' \
  reusable-tools/ \
  analysis/ \
  README.md

# 只分享工具和文档
tar -czf tools-only.tar.gz \
  reusable-tools/ \
  README.md \
  QUICK_START.md
```

### 创建Git仓库

```bash
git init
git add reusable-tools/ *.md
git commit -m "Initial commit: Web scraping and analysis tools"

# .gitignore 示例
echo "*.html" >> .gitignore
echo "images/" >> .gitignore
echo "backups/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

---

## 🎓 学习路径

### 初级（1-2小时）

1. ✅ 运行一次完整流程
2. ✅ 理解每个工具的作用
3. ✅ 修改配置参数
4. ✅ 完成一个简单的分析

### 中级（1周）

1. ✅ 处理3-5个不同的页面
2. ✅ 自定义工具脚本
3. ✅ 编写详细的分析报告
4. ✅ 总结常见模式

### 高级（持续）

1. ✅ 开发自动化工具
2. ✅ 建立分析框架
3. ✅ 创建案例库
4. ✅ 指导他人使用

---

*创建日期: 2025年10月8日*  
*适用版本: v1.0*
