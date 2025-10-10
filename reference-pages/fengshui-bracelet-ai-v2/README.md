# FengShui Bracelet AI版本 v2.0

基于原版网页，使用AI生成新版本落地页。

## 📁 项目结构

```
fengshui-bracelet-ai-v2/
├── prompts/                 # 所有AI图片生成prompts
│   ├── main-images-prompts.json
│   ├── avatar-prompts.json
│   └── ALL-PROMPTS.md      # 可读的Markdown格式
├── images/                  # 生成的图片（待生成）
├── content/                 # 页面文本内容
│   ├── page-content.json
│   └── page-content.md     # 可读预览
├── scripts/                 # 生成脚本
│   ├── 01_extract_original_structure.py
│   ├── 02_generate_content_and_prompts.py
│   └── 03_generate_images.py
├── analysis/                # 原网页分析结果
└── index.html              # 最终网页（待生成）
```

## 👥 新版人物角色

- **女主角**: Emma (原版: Lisa)
- **男主角**: James (原版: David)
- **地点**: Seattle, Boston

## 📊 内容统计

- **主要图片**: 18 张
- **用户头像**: 12 个
- **内容模块**: 15 个

## 🚀 使用流程

### 步骤1: 生成内容和Prompts

```bash
cd scripts
python3 02_generate_content_and_prompts.py
```

### 步骤2: 生成AI图片

```bash
python3 03_generate_images.py
```

这将调用 StellarView 的图片生成服务（MiniMax），自动生成所有图片。

### 步骤3: 生成HTML网页

```bash
python3 04_generate_html.py
```

将内容和图片组合成最终的HTML文件。

## 🎨 图片生成说明

所有图片使用 **MiniMax Image Service** 生成：
- 宽高比根据位置优化（hero: 16:9, 产品: 1:1, 人物: 3:4）
- 高质量photorealistic风格
- 自动保存到 `images/` 目录

## 📝 内容特点

完全复制原网页的：
- ✅ 故事结构（两个主角的转变故事）
- ✅ 情感节奏（痛点→希望→证明→行动）
- ✅ 说服技巧（社会证明、稀缺性、权威性）
- ✅ CTA位置和文案

仅修改：
- 人物名字
- 地理位置

## 🔗 原版参考

原网页: https://offer.fengshuibracelets.co/fengshui/news

分析文档: `../fengshui-bracelet-case/analysis/marketing-analysis.md`

---

*生成日期: 2025-10-09*
