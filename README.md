# Celestial Decree of Triple Blessings - 销售站点

## 🎉 项目状态

✅ **基础框架已完成!** 页面正在运行: http://localhost:1314/

---

## 📂 项目结构

```
my-product-site/
├── content/
│   └── _index.md              # 主页内容 (你可以编辑文案)
├── layouts/
│   └── shortcodes/
│       ├── stripe_button.html # Stripe支付按钮组件
│       └── summary_box.html   # 黄色摘要框组件
├── assets/
│   └── css/
│       └── main.css          # 自定义样式
├── static/
│   └── images/               # 图片文件夹 (需要你添加图片)
├── hugo.toml                 # 网站配置
└── themes/hugo-product-launch/
```

---

## 🚀 当前功能

### ✅ 已完成
- [x] Hugo项目初始化
- [x] 销售页面基础结构
- [x] Stripe支付按钮shortcode
- [x] 黄色摘要框shortcode
- [x] 自定义CSS样式 (绿色CTA按钮)
- [x] 响应式设计
- [x] 联系表单

### 📝 页面内容包含
- Hero区域 (标题 + 价值主张)
- 摘要框
- Grace的故事案例
- 三官大帝介绍
- 产品功效
- 证言/评价
- FAQ
- 多个CTA按钮
- 联系表单

---

## 📋 下一步待办事项

### 1. 填充真实内容 (你来做)

编辑 `content/_index.md`:
- ✏️ 替换Grace的故事为真实案例
- ✏️ 添加更多用户评价
- ✏️ 完善产品详情描述
- ✏️ 更新FAQ内容

### 2. 添加图片

在 `static/images/` 目录添加:
```
static/images/
├── teaser.jpg          # Hero背景图 (1920x1080px)
├── product-1.jpg       # 产品特写
├── product-2.jpg       # 使用场景
├── favicon.png         # 网站图标 (32x32px)
└── share-image.png     # 社交分享图 (1200x630px)
```

### 3. 配置Stripe

#### 步骤 A: 获取Stripe API密钥

1. 访问 https://stripe.com 注册/登录
2. 进入 Dashboard > Developers > API keys
3. 复制 **Publishable key** (pk_test_... 或 pk_live_...)

#### 步骤 B: 创建产品和价格

1. 进入 Dashboard > Products
2. 点击 "Add Product"
3. 填写产品信息:
   - Name: Celestial Decree of Triple Blessings
   - Description: Sacred talisman for wealth and protection
   - Price: $XX.XX
4. 复制 **Price ID** (price_xxxxxxxxxxxxx)

#### 步骤 C: 配置到网站

编辑 `hugo.toml`,在 `[params]` 末尾添加:
```toml
[params.stripe]
  publishable_key = "pk_test_YOUR_KEY_HERE"
```

然后在 `content/_index.md` 中,找到所有:
```markdown
{{< stripe_button price_id="" label="..." >}}
```

替换为:
```markdown
{{< stripe_button price_id="price_YOUR_PRICE_ID" label="..." >}}
```

### 4. 配置表单处理

当前联系表单使用Netlify Forms。如果部署到Cloudflare,需要:

**选项 A: 使用 Web3Forms (最简单)**
1. 访问 https://web3forms.com
2. 获取 Access Key
3. 修改联系表单为Web3Forms格式

**选项 B: 使用 Cloudflare Workers**
参考 `DEPLOYMENT_GUIDE.md` 的表单处理方案

### 5. 创建成功/失败页面

创建以下文件:

`content/success.md`:
```markdown
---
title: "Payment Successful"
---

# 🎉 Thank You!

Your order has been confirmed. You will receive an email shortly.

[Return to Home](/)
```

`content/cancel.md`:
```markdown
---
title: "Payment Cancelled"
---

# Payment Cancelled

No charges were made.

[Try Again](/#pricing) | [Return Home](/)
```

---

## 🛠️ 开发命令

### 本地预览
```bash
cd /Users/ming/Documents/HUGO/my-product-site
hugo server --port 1314
```
访问: http://localhost:1314/

### 构建生产版本
```bash
hugo --minify
```
输出目录: `public/`

### 安装依赖
```bash
npm install
```

---

## 🎨 自定义样式

### 修改颜色

编辑 `assets/css/main.css` 中的颜色变量:
```css
:root {
  --color-primary: #3FA026;      /* 主绿色 */
  --color-primary-hover: #5ED54B; /* 悬停色 */
  --color-accent: #FEF5C4;       /* 黄色框 */
  --color-celestial: #4A90E2;    /* 蓝色链接 */
}
```

### 修改字体

在 `hugo.toml` 的 `<head>` 区域添加Google Fonts,然后更新CSS。

---

## 📦 使用Shortcodes

### Stripe支付按钮
```markdown
{{< stripe_button
    price_id="price_xxxxx"
    label="Buy Now - $29"
    size="large"
>}}
```

参数:
- `price_id`: Stripe价格ID (必填)
- `label`: 按钮文字 (默认: "Buy Now")
- `mode`: "payment"或"subscription" (默认: "payment")
- `size`: "normal"或"large" (默认: "normal")

### 摘要框
```markdown
{{< summary_box >}}
你的摘要内容...可以使用**粗体**和[链接](#)
{{< /summary_box >}}
```

### 联系表单
```markdown
{{< contact_form
    id="contact-form"
    placeholder_name="Your Name"
    placeholder_email="Your Email"
    placeholder_message="Your Message"
    button_label="Send"
>}}
```

---

## 🚀 部署到Cloudflare Pages

### 准备工作
1. 推送代码到GitHub:
```bash
git add .
git commit -m "Initial commit: Celestial Decree sales page"
git remote add origin https://github.com/YOUR_USERNAME/celestial-decree.git
git push -u origin main
```

2. 登录 Cloudflare Dashboard
3. 进入 **Workers & Pages** > **Create Application** > **Pages**
4. 连接GitHub仓库

### 构建配置
```
Framework preset: Hugo
Build command: hugo --minify
Build output directory: public
Root directory: (留空)
```

### 环境变量
```
HUGO_VERSION = 0.145.0
NODE_VERSION = 20
```

### 部署后配置
1. 添加自定义域名
2. 配置SSL (自动)
3. 设置Cloudflare缓存规则

详细步骤参考: `DEPLOYMENT_GUIDE.md`

---

## 📊 测试清单

部署前测试:
- [ ] 所有文案已替换为真实内容
- [ ] 所有图片已上传并正确显示
- [ ] Stripe按钮可点击 (测试模式)
- [ ] 联系表单可提交
- [ ] 移动端显示正常
- [ ] 所有链接正常工作
- [ ] SEO信息已配置 (title, description)

Stripe测试:
- [ ] 使用测试卡号: 4242 4242 4242 4242
- [ ] 测试成功支付流程
- [ ] 测试取消支付流程
- [ ] 验证成功/失败页面跳转

---

## 🔧 常见问题

### Q: 修改内容后页面没更新?
A: Hugo开发服务器支持热更新。检查终端是否有错误信息。

### Q: Stripe按钮点击没反应?
A: 检查:
1. `hugo.toml` 中是否配置了 `publishable_key`
2. shortcode中是否提供了 `price_id`
3. 浏览器控制台是否有错误

### Q: 图片不显示?
A: 确保图片路径正确:
- 放在 `static/images/xxx.jpg`
- Markdown中使用: `![描述](images/xxx.jpg)`

### Q: 如何修改CTA按钮颜色?
A: 编辑 `assets/css/main.css` 中的 `--color-primary` 变量。

---

## 📖 参考文档

- [Hugo文档](https://gohugo.io/documentation/)
- [Stripe文档](https://stripe.com/docs)
- [Cloudflare Pages文档](https://developers.cloudflare.com/pages/)
- [Tailwind CSS文档](https://tailwindcss.com/docs)

项目部署指南: `DEPLOYMENT_GUIDE.md`
FengShui页面分析: `reference-pages/FENGSHUI-PAGE-ANALYSIS.md`

---

## 🎯 当前可以做的事

1. **访问页面**: http://localhost:1314/
2. **编辑文案**: `content/_index.md`
3. **添加图片**: `static/images/`
4. **修改样式**: `assets/css/main.css`
5. **配置Stripe**: 按上述步骤操作

---

**祝你销售成功! 🎊**

_May the Three Officials smile upon you._ ✨
