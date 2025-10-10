# 图片占位符说明文档

## 📸 需要的图片列表

### 1. HERO-PRODUCT-IMAGE (首屏主图)
**位置**: 页面顶部，第一个故事之前
**用途**: 产品主视觉，吸引注意力
**建议**:
- 使用你提供的 `/product/001.png` (三官赐福宝钞)
- 建议尺寸: 800px × 600px 或更大
- 处理建议:
  - 添加戏剧性lighting效果
  - 黑色背景或金色光晕背景
  - 3D悬浮效果(阴影)
  - 可以考虑做成GIF动画(旋转或发光效果)

**示例markdown**:
```markdown
![Celestial Decree of Triple Blessings](images/hero-product.jpg)
```

---

### 2. SARAH-STORY-IMAGE (Sarah的故事配图)
**位置**: Sarah故事结束后
**用途**: 视觉化故事人物，增加真实感
**建议**:
- AI生成: 专业女性,30-40岁,微笑/放松的表情
- 场景: 在家中或办公室，看起来如释重负
- 风格: 真实感,不要太过精致
- 尺寸: 600px × 400px

**AI Prompt 建议**:
```
"Professional woman in her 30s, relieved and happy expression,
sitting at home with warm lighting, realistic photo style,
natural smile, casual but neat appearance"
```

**示例markdown**:
```markdown
![Sarah's transformation story](images/sarah-story.jpg)
```

---

### 3. MICHAEL-STORY-IMAGE (Michael的故事配图)
**位置**: Michael故事结束后
**用途**: 视觉化成功商人形象
**建议**:
- AI生成: 专业男性,35-45岁,自信的表情
- 场景: 户外工作场景或办公室
- 可能有团队成员在背景
- 风格: 成功但接地气
- 尺寸: 600px × 400px

**AI Prompt 建议**:
```
"Successful businessman in his 40s, confident smile,
outdoor work setting or office, professional but approachable,
realistic photo style, natural lighting"
```

**示例markdown**:
```markdown
![Michael's business success story](images/michael-story.jpg)
```

---

### 4. THREE-OFFICIALS-DIAGRAM (三官大帝图示)
**位置**: "Why Does This Decree Work?" 章节
**用途**: 解释产品机制,视觉化三官概念
**建议**:
- 选项A: 传统道教三官画像(艺术风格)
- 选项B: 现代简化图示(3个icon + 说明)
- 选项C: 神秘东方氛围图(光、能量、符号)
- 尺寸: 800px × 500px

**AI Prompt 建议**:
```
"Three divine Chinese officials in traditional robes,
celestial background with golden light, mystical atmosphere,
one for heaven, one for earth, one for water,
artistic style, spiritual energy"
```

或简化版:
```
"Three golden symbols representing heaven, earth, and water,
minimal modern design, Chinese cultural elements,
spiritual energy flow visualization"
```

**示例markdown**:
```markdown
![The Three Officials - Heaven, Earth, Water](images/three-officials.jpg)
```

---

### 5. DECREE-DETAIL-CLOSEUP (宝钞细节特写)
**位置**: "The Sacred Inscription" 章节
**用途**: 展示宝钞上的文字细节
**建议**:
- 使用 `/product/001.png` 的特写裁剪
- 聚焦在"壹万貫"或其他关键文字
- 可以添加软光晕效果
- 尺寸: 700px × 500px

**示例markdown**:
```markdown
![Sacred inscriptions detail - "One Thousand Strings of Gold"](images/decree-detail.jpg)
```

---

### 6. TESTIMONIAL-AVATARS (用户头像网格)
**位置**: 用户评价区域
**用途**: 增加社交证明的真实感
**建议**:
- 8个不同的头像
- 可以使用 AI 生成或 https://randomuser.me/api/
- 多样化: 不同年龄、性别、族裔
- 尺寸: 每个 100px × 100px (圆形)

**获取方式**:
```bash
# 使用 RandomUser API
for i in {1..8}; do
  curl "https://randomuser.me/api/?results=1" > avatar_$i.json
done
```

**示例markdown**:
```markdown
<div class="testimonial-avatars">
  <img src="images/avatars/jennifer.jpg" alt="Jennifer H.">
  <img src="images/avatars/david.jpg" alt="David K.">
  <img src="images/avatars/lisa.jpg" alt="Lisa W.">
  <img src="images/avatars/robert.jpg" alt="Robert M.">
  <img src="images/avatars/amanda.jpg" alt="Amanda S.">
  <img src="images/avatars/james.jpg" alt="James L.">
  <img src="images/avatars/patricia.jpg" alt="Patricia G.">
  <img src="images/avatars/rachel.jpg" alt="Rachel T.">
</div>
```

---

## 🎨 可选增强图片

### 7. WARNING-BOX-ICON (警告图标)
**位置**: 顶部警告框
**建议**: ⚠️ emoji 或图标
**尺寸**: 32px × 32px

### 8. CERTIFICATE/GUARANTEE-BADGE (保证徽章)
**位置**: 30天退款保证区域
**建议**:
- "30-Day Guarantee" 徽章
- 金色或绿色
- 圆形或盾牌形状
**尺寸**: 150px × 150px

### 9. BACKGROUND-TEXTURE (背景纹理)
**建议**:
- 微妙的金色云纹
- 中国风图案(龙、云、水波)
- 半透明,不影响文字阅读
- 可作为某些section的背景

---

## 📐 图片规格建议

### 文件格式
- **产品图**: PNG (保留透明度) 或 JPG
- **故事配图**: JPG (压缩后更小)
- **图标**: SVG 或 PNG
- **动画**: GIF 或 MP4

### 文件大小
- 单张图片: < 500KB (优化后)
- GIF动画: < 3MB
- 总页面大小目标: < 5MB

### 优化工具
- TinyPNG: https://tinypng.com/
- ImageOptim (Mac)
- Squoosh: https://squoosh.app/

---

## 🎯 快速实施方案

### 方案A: 最小可行版本 (MVP)
只使用必需图片:
1. ✅ HERO-PRODUCT-IMAGE (你的001.png)
2. ✅ DECREE-DETAIL-CLOSEUP (001.png裁剪)
3. ✅ TESTIMONIAL-AVATARS (RandomUser API)

**时间**: 30分钟

### 方案B: 完整版
包含所有建议图片:
1. ✅ 所有6个主要图片
2. ✅ AI生成故事配图
3. ✅ 自定义图标和徽章

**时间**: 2-3小时

---

## 🤖 AI 图片生成工具推荐

### 免费工具:
1. **Leonardo.ai** - 每天150免费credits
2. **Bing Image Creator** - 完全免费
3. **Playground AI** - 每天500免费images

### 付费工具:
1. **Midjourney** - $10/月
2. **DALL-E 3** - 按使用付费
3. **Stable Diffusion** - 开源,可本地运行

---

## 📝 文件命名规范

```
images/
├── products/
│   ├── hero-decree.png          # 主产品图
│   └── decree-detail.png        # 细节特写
├── stories/
│   ├── sarah-transformation.jpg # Sarah配图
│   └── michael-success.jpg      # Michael配图
├── concepts/
│   └── three-officials.jpg      # 三官图示
├── avatars/
│   ├── jennifer-h.jpg
│   ├── david-k.jpg
│   ├── lisa-w.jpg
│   ├── robert-m.jpg
│   ├── amanda-s.jpg
│   ├── james-l.jpg
│   ├── patricia-g.jpg
│   └── rachel-t.jpg
└── icons/
    ├── warning.svg
    └── guarantee-badge.png
```

---

## ✅ 检查清单

在更新网站之前,确保:

- [ ] 所有图片已优化(< 500KB/张)
- [ ] 图片尺寸适配响应式设计
- [ ] Alt text 已添加(SEO优化)
- [ ] 文件名使用小写和连字符
- [ ] 图片已测试在不同设备上的显示
- [ ] 加载速度可接受(< 3秒)

---

## 🚀 下一步行动

1. **立即可做**:
   - 复制 `/product/001.png` 到 `/static/images/products/hero-decree.png`
   - 裁剪一个细节版本为 `decree-detail.png`

2. **今天完成**:
   - 下载8个用户头像(RandomUser API)
   - 使用AI生成Sarah和Michael的配图

3. **可选增强**:
   - 创建GIF动画版本的产品图
   - 设计三官大帝的视觉图示
   - 添加保证徽章和图标

---

**需要帮助?** 我可以帮你:
- 生成AI图片的详细prompt
- 批量下载和处理图片
- 优化图片大小
- 更新Hugo模板以显示这些图片
