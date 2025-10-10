# Hugo Product Launch - Cloudflare + Stripe 部署指南

本指南详细说明如何将 Hugo Product Launch 主题改造为基于 Cloudflare Pages 部署的单页面销售站点，并集成 Stripe 支付功能。

---

## 📋 完整任务清单

### 阶段一: 项目初始化与本地设置

#### 1.1 创建新项目（推荐方式）

**选项 A: 使用 Git Submodule（推荐 - 便于主题更新）**

```bash
# 1. 创建新项目目录
mkdir ~/Documents/HUGO/my-product-site
cd ~/Documents/HUGO/my-product-site

# 2. 初始化Hugo站点
hugo new site . --force

# 3. 将主题作为submodule添加
git init
git submodule add https://github.com/janraasch/hugo-product-launch.git themes/hugo-product-launch

# 4. 复制示例配置
cp themes/hugo-product-launch/exampleSite/hugo.toml .
cp themes/hugo-product-launch/exampleSite/netlify.toml .
cp -r themes/hugo-product-launch/exampleSite/content .
cp -r themes/hugo-product-launch/exampleSite/static .

# 5. 复制必要的构建文件
cp themes/hugo-product-launch/package.json .
cp themes/hugo-product-launch/package-lock.json .
```

**选项 B: 直接复制主题（适合深度定制）**

```bash
# 1. 创建新项目
mkdir ~/Documents/HUGO/my-product-site
cd ~/Documents/HUGO/my-product-site

# 2. 复制整个exampleSite
cp -r /path/to/hugo-product-launch/exampleSite/* .

# 3. 直接复制主题文件到项目中
mkdir -p themes/hugo-product-launch
cp -r /path/to/hugo-product-launch/{layouts,assets,archetypes,theme.toml} themes/hugo-product-launch/

# 4. 复制package.json
cp /path/to/hugo-product-launch/package.json .
cp /path/to/hugo-product-launch/package-lock.json .

# 5. 初始化git
git init
git add .
git commit -m "Initial commit: Hugo product launch site"
```

**为什么不直接 Fork？**

- ✅ 保持主题代码独立，便于将来更新主题
- ✅ 你的定制内容与主题分离
- ✅ Git 历史清晰，只追踪你的改动
- ✅ 可以随时切换或升级主题

#### 1.2 配置 Tailwind CSS

```bash
# 安装 npm 依赖
npm install

# 测试本地运行
hugo server
```

访问 `http://localhost:1313` 确认站点正常运行。

---

## 阶段二: Stripe 支付集成

### 2.1 创建 Stripe 账户并获取 API 密钥

1. 访问 [https://stripe.com](https://stripe.com) 注册账户
2. 进入 Dashboard > Developers > API keys
3. 获取以下密钥：
   - **可发布密钥** (Publishable Key): `pk_test_...` (测试模式) / `pk_live_...` (生产模式)
   - **密钥** (Secret Key): `sk_test_...` (测试模式) / `sk_live_...` (生产模式)

### 2.2 在 Stripe 中创建产品

1. 进入 Dashboard > Products
2. 点击 "Add Product"
3. 填写产品信息：
   - 名称
   - 描述
   - 价格（一次性或订阅）
4. 记录 **Price ID**: `price_xxxxx`

### 2.3 集成方案选择

#### 方案 A: Stripe Payment Links（最简单 - 推荐 MVP）

**优点:**
- 无需编写后端代码
- Stripe 托管整个支付流程
- 5分钟即可上线

**步骤:**

1. 在 Stripe Dashboard > Payment Links 创建支付链接
2. 在 Hugo 页面中添加购买按钮：

```markdown
[立即购买](https://buy.stripe.com/your-payment-link)
```

或使用 HTML 按钮：

```html
<a href="https://buy.stripe.com/your-payment-link"
   class="bg-blue-600 text-white px-6 py-3 rounded-lg">
  立即购买 - $29
</a>
```

#### 方案 B: Stripe Checkout（更灵活）

**优点:**
- 可编程控制
- 支持动态定价
- 可自定义成功页面

**前端实现:**

1. 在 `layouts/partials/custom_head.html` 添加 Stripe.js：

```html
<script src="https://js.stripe.com/v3/"></script>
```

2. 创建 `layouts/shortcodes/stripe_button.html`：

```html
<button id="checkout-button-{{ .Get "price_id" }}"
        class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
  {{ .Get "label" | default "立即购买" }}
</button>

<script>
  (function() {
    var stripe = Stripe('{{ site.Params.stripe.publishable_key }}');
    var checkoutButton = document.getElementById('checkout-button-{{ .Get "price_id" }}');

    checkoutButton.addEventListener('click', function() {
      stripe.redirectToCheckout({
        lineItems: [{price: '{{ .Get "price_id" }}', quantity: 1}],
        mode: '{{ .Get "mode" | default "payment" }}',
        successUrl: '{{ site.BaseURL }}success',
        cancelUrl: '{{ site.BaseURL }}cancel',
      }).then(function (result) {
        if (result.error) {
          alert(result.error.message);
        }
      });
    });
  })();
</script>
```

3. 在 `hugo.toml` 中添加配置：

```toml
[params.stripe]
  publishable_key = "pk_test_your_key_here"
```

4. 在 `content/_index.md` 中使用：

```markdown
{{< stripe_button price_id="price_xxxxx" label="立即购买 - $29" mode="payment" >}}
```

#### 方案 C: 完整后端（Cloudflare Workers）

**适用场景:**
- 需要 webhook 处理
- 需要存储订单数据
- 需要自定义业务逻辑

**步骤:**

1. 创建 `workers/payment.js`：

```javascript
export default {
  async fetch(request, env) {
    const stripe = require('stripe')(env.STRIPE_SECRET_KEY);

    if (request.method === 'POST' && new URL(request.url).pathname === '/create-checkout-session') {
      const session = await stripe.checkout.sessions.create({
        line_items: [{
          price: 'price_xxxxx',
          quantity: 1,
        }],
        mode: 'payment',
        success_url: 'https://yourdomain.com/success',
        cancel_url: 'https://yourdomain.com/cancel',
      });

      return Response.redirect(session.url, 303);
    }

    // Webhook 处理
    if (request.method === 'POST' && new URL(request.url).pathname === '/webhook') {
      const sig = request.headers.get('stripe-signature');
      const body = await request.text();

      try {
        const event = stripe.webhooks.constructEvent(body, sig, env.STRIPE_WEBHOOK_SECRET);

        switch (event.type) {
          case 'checkout.session.completed':
            // 处理成功支付
            const session = event.data.object;
            // 存储订单到 D1 或发送邮件
            break;
        }

        return new Response(JSON.stringify({received: true}), {status: 200});
      } catch (err) {
        return new Response(`Webhook Error: ${err.message}`, {status: 400});
      }
    }

    return new Response('Not Found', {status: 404});
  }
};
```

2. 创建 `wrangler.toml`：

```toml
name = "my-product-payment"
main = "workers/payment.js"
compatibility_date = "2024-01-01"

[vars]
# 可发布密钥可以公开
STRIPE_PUBLISHABLE_KEY = "pk_test_..."

# 敏感信息使用 secrets
# 运行: wrangler secret put STRIPE_SECRET_KEY
# 运行: wrangler secret put STRIPE_WEBHOOK_SECRET
```

3. 部署 Worker：

```bash
npm install wrangler -g
wrangler login
wrangler secret put STRIPE_SECRET_KEY
wrangler secret put STRIPE_WEBHOOK_SECRET
wrangler deploy
```

---

## 阶段三: 内容定制

### 3.1 修改页面内容

编辑 `content/_index.md`：

```markdown
---
header_brand: "您的产品名称"
header_tagline_paragraph: "一句话描述您的产品价值主张"
header_button_cta:
  url: "#pricing"
  title: "立即购买"
header_button_more:
  url: "#features"
  title: "了解更多"
teaser_image: "images/product-hero.jpg"
---

# 产品特性

## 🚀 核心功能

- **特性 1**: 描述
- **特性 2**: 描述
- **特性 3**: 描述

![产品截图](images/feature-1.png)

---

# 定价方案 {#pricing}

## 限时优惠 - 仅需 $29

原价 ~~$49~~，立即节省 $20！

{{< stripe_button price_id="price_xxxxx" label="立即购买 - $29" >}}

✓ 功能 1
✓ 功能 2
✓ 功能 3
✓ 终身更新

---

# 常见问题

**Q: 支持退款吗？**
A: 支持 30 天无理由退款。

**Q: 购买后多久可以使用？**
A: 立即可用，购买成功后会收到邮件。

---

# 联系我们

{{< contact_form id="contact-form" placeholder_name="姓名" placeholder_email="邮箱" placeholder_message="留言" button_label="发送">}}
```

### 3.2 准备图片素材

```bash
# 替换以下图片到 static/images/
static/images/
├── favicon.png          # 网站图标 (32x32px 以上)
├── share-image.png      # 社交分享图 (1200x630px)
├── product-hero.jpg     # 首页大图
├── feature-1.png        # 功能截图
├── feature-2.png
└── testimonial.jpg      # 客户评价照片（可选）
```

**图片优化建议:**
- 使用 [TinyPNG](https://tinypng.com) 压缩图片
- 使用 WebP 格式（Hugo 支持自动转换）
- 保持单个图片 < 200KB

### 3.3 设计调整

编辑 `assets/css/main.css`（如果不存在，从主题复制）：

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* 自定义品牌颜色 */
@layer base {
  :root {
    --color-primary: #3b82f6;      /* 主色调 */
    --color-secondary: #8b5cf6;    /* 辅助色 */
    --color-accent: #10b981;       /* 强调色 */
  }
}

/* 自定义按钮样式 */
@layer components {
  .btn-primary {
    @apply bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-all;
  }

  .btn-secondary {
    @apply bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-3 px-6 rounded-lg transition-all;
  }
}

/* 自定义字体（可选） */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
}
```

---

## 阶段四: Cloudflare 部署

### 4.1 准备部署配置

#### 修改 `hugo.toml`

```toml
baseURL = "https://yourdomain.com"  # 替换为你的域名

# 其他配置保持不变...

[params]
  # 添加 Stripe 配置
  [params.stripe]
    publishable_key = "pk_live_your_key"  # 生产环境使用 live key
```

#### 创建 `cloudflare-pages.toml`（可选）

```toml
[build]
  command = "hugo --minify"
  publish = "public"

[build.environment]
  HUGO_VERSION = "0.140.0"
  NODE_VERSION = "20"

[[redirects]]
  from = "/success"
  to = "/success.html"
  status = 200

[[redirects]]
  from = "/cancel"
  to = "/cancel.html"
  status = 200
```

#### 创建成功/失败页面

创建 `content/success.md`：

```markdown
---
title: "支付成功"
layout: "single"
---

# 🎉 支付成功！

感谢您的购买！您将在 5 分钟内收到包含产品访问信息的邮件。

如有任何问题，请联系我们：support@yourdomain.com

[返回首页](/)
```

创建 `content/cancel.md`：

```markdown
---
title: "支付取消"
layout: "single"
---

# 支付已取消

您的支付已取消，没有产生任何费用。

[重新购买](/#pricing) | [返回首页](/)
```

### 4.2 推送到 Git 仓库

```bash
# 初始化仓库（如果还没有）
git init
git add .
git commit -m "Initial commit: Product launch site"

# 创建 GitHub 仓库并推送
# 在 GitHub 创建新仓库后：
git remote add origin https://github.com/yourusername/your-product-site.git
git branch -M main
git push -u origin main
```

### 4.3 在 Cloudflare Pages 创建项目

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 进入 **Workers & Pages** > **Create Application** > **Pages** > **Connect to Git**
3. 选择你的 Git 仓库
4. 配置构建设置：

```
Framework preset: Hugo
Build command: hugo --minify
Build output directory: public
Root directory: / (或留空)
```

5. 环境变量设置：

```
HUGO_VERSION = 0.140.0
NODE_VERSION = 20
```

6. 点击 **Save and Deploy**

### 4.4 配置自定义域名

1. 在 Cloudflare Pages 项目中，进入 **Custom domains**
2. 点击 **Set up a custom domain**
3. 输入你的域名（如 `yourdomain.com`）
4. 按提示配置 DNS：
   - 类型: CNAME
   - 名称: @ (或 www)
   - 目标: your-project.pages.dev
5. 等待 DNS 生效（通常 5-10 分钟）
6. SSL 证书会自动配置

---

## 阶段五: 表单处理替换

原主题使用 Netlify Forms，需要替换为 Cloudflare 兼容方案。

### 方案 A: Cloudflare Workers + Email Workers（推荐）

#### 1. 创建 Email Worker

创建 `workers/contact-form.js`：

```javascript
export default {
  async fetch(request, env) {
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    const formData = await request.formData();
    const name = formData.get('name');
    const email = formData.get('email');
    const message = formData.get('message');

    // 发送邮件（需要配置 Email Routing）
    await fetch('https://api.mailchannels.net/tx/v1/send', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        personalizations: [{
          to: [{ email: 'your-email@yourdomain.com', name: 'Your Name' }],
        }],
        from: {
          email: 'noreply@yourdomain.com',
          name: 'Contact Form',
        },
        subject: `New Contact from ${name}`,
        content: [{
          type: 'text/plain',
          value: `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`,
        }],
      }),
    });

    return Response.redirect('https://yourdomain.com/#thank-you', 303);
  }
};
```

#### 2. 更新表单 HTML

修改 `layouts/shortcodes/contact_form.html`：

```html
<form action="https://your-worker.yourusername.workers.dev/contact"
      method="POST"
      id="{{ .Get "id" }}"
      class="space-y-4">
  <input type="text"
         name="name"
         placeholder="{{ .Get "placeholder_name" }}"
         required
         class="w-full px-4 py-2 border rounded">
  <input type="email"
         name="email"
         placeholder="{{ .Get "placeholder_email" }}"
         required
         class="w-full px-4 py-2 border rounded">
  <textarea name="message"
            placeholder="{{ .Get "placeholder_message" }}"
            required
            rows="5"
            class="w-full px-4 py-2 border rounded"></textarea>
  <button type="submit"
          class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
    {{ .Get "button_label" }}
  </button>
</form>
```

### 方案 B: 使用第三方服务（最简单）

#### 选项 1: Web3Forms（免费，无后端）

1. 访问 [web3forms.com](https://web3forms.com) 获取 Access Key
2. 修改表单：

```html
<form action="https://api.web3forms.com/submit" method="POST">
  <input type="hidden" name="access_key" value="YOUR_ACCESS_KEY_HERE">
  <input type="text" name="name" placeholder="姓名" required>
  <input type="email" name="email" placeholder="邮箱" required>
  <textarea name="message" placeholder="留言" required></textarea>
  <button type="submit">发送</button>
</form>
```

#### 选项 2: Formspree（免费 50 次/月）

1. 访问 [formspree.io](https://formspree.io) 注册
2. 创建新表单，获取 endpoint
3. 修改表单 action：

```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
  <!-- 表单字段 -->
</form>
```

---

## 阶段六: 测试与优化

### 6.1 功能测试清单

- [ ] **支付流程测试**
  - [ ] 使用 Stripe 测试卡号: `4242 4242 4242 4242`
  - [ ] 测试成功支付跳转
  - [ ] 测试取消支付跳转
  - [ ] 测试 webhook 接收（如果有）

- [ ] **表单测试**
  - [ ] 提交联系表单
  - [ ] 验证邮件接收
  - [ ] 测试字段验证

- [ ] **响应式测试**
  - [ ] 桌面端（1920px）
  - [ ] 平板端（768px）
  - [ ] 手机端（375px）

- [ ] **链接测试**
  - [ ] 所有内部链接正常
  - [ ] CTA 按钮跳转正确
  - [ ] 锚点链接工作

### 6.2 Stripe 测试卡号

```
成功支付: 4242 4242 4242 4242
需要验证: 4000 0025 0000 3155
被拒绝: 4000 0000 0000 9995

使用任意：
- 未来日期（如 12/34）
- 任意 3 位 CVC
- 任意 5 位邮编
```

### 6.3 性能优化

#### 图片优化

```bash
# 安装 Hugo 扩展版（支持 WebP 转换）
# macOS
brew install hugo

# 在 hugo.toml 中配置图片处理
[imaging]
  quality = 85
  resampleFilter = "Lanczos"

[imaging.exif]
  disableDate = false
  disableLatLong = true
```

#### Cloudflare 优化设置

1. 进入 Cloudflare Dashboard > Speed > Optimization
2. 启用以下功能：
   - ✅ Auto Minify (HTML, CSS, JS)
   - ✅ Brotli 压缩
   - ✅ Early Hints
   - ✅ Rocket Loader（谨慎，可能影响 Stripe.js）

3. 缓存规则：
   - Cache Level: Standard
   - Browser Cache TTL: 4 hours
   - Edge Cache TTL: 2 hours (for static assets)

#### 页面加载速度测试

使用以下工具测试：
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [GTmetrix](https://gtmetrix.com/)
- [WebPageTest](https://www.webpagetest.org/)

目标指标：
- First Contentful Paint (FCP): < 1.8s
- Largest Contentful Paint (LCP): < 2.5s
- Cumulative Layout Shift (CLS): < 0.1
- Time to Interactive (TTI): < 3.8s

### 6.4 SEO 配置

#### 更新 `hugo.toml` SEO 设置

```toml
[params]
  description = "简洁有力的产品描述，不超过 160 字符"

  [params.meta]
    keywords = "产品关键词1, 关键词2, 关键词3"
    author = "您的公司名称"

  # Open Graph / Facebook
  [params.og]
    title = "产品名称 - 一句话价值主张"
    description = "吸引人的产品描述"
    image = "https://yourdomain.com/images/share-image.png"

  # Twitter Card
  [params.twitter]
    card = "summary_large_image"
    site = "@yourtwitter"
    creator = "@yourtwitter"
```

#### 创建 `layouts/partials/seo.html`（如果需要自定义）

```html
{{ if .IsHome }}
<title>{{ site.Title }} - {{ site.Params.description }}</title>
{{ else }}
<title>{{ .Title }} - {{ site.Title }}</title>
{{ end }}

<meta name="description" content="{{ .Params.description | default site.Params.description }}">
<meta name="keywords" content="{{ .Params.keywords | default site.Params.meta.keywords }}">

<!-- Open Graph -->
<meta property="og:title" content="{{ .Title | default site.Title }}">
<meta property="og:description" content="{{ .Description | default site.Params.description }}">
<meta property="og:image" content="{{ .Params.image | default site.Params.og.image }}">
<meta property="og:url" content="{{ .Permalink }}">
<meta property="og:type" content="website">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ .Title | default site.Title }}">
<meta name="twitter:description" content="{{ .Description | default site.Params.description }}">
<meta name="twitter:image" content="{{ .Params.image | default site.Params.og.image }}">

<!-- Canonical -->
<link rel="canonical" href="{{ .Permalink }}">
```

#### Google Analytics（可选）

在 `layouts/partials/custom_head.html` 添加：

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 阶段七: 上线准备

### 7.1 法律合规页面

#### 创建隐私政策 `content/privacy.md`

```markdown
---
title: "隐私政策"
---

# 隐私政策

**生效日期**: 2024-01-01

## 我们收集的信息

- 姓名和电子邮件地址（通过联系表单）
- 支付信息（通过 Stripe 处理，我们不存储）
- 网站使用数据（通过 Cloudflare Analytics）

## 信息使用方式

- 处理您的订单
- 回复您的咨询
- 改进我们的服务

## Cookie 使用

本网站使用最少的 Cookie 来保证功能正常。我们不使用第三方追踪 Cookie。

## 您的权利

您有权：
- 访问您的个人数据
- 要求删除您的数据
- 拒绝营销邮件

联系我们: privacy@yourdomain.com

## 第三方服务

- **Stripe**: 支付处理（[Stripe 隐私政策](https://stripe.com/privacy)）
- **Cloudflare**: 托管服务（[Cloudflare 隐私政策](https://www.cloudflare.com/privacypolicy/)）
```

#### 创建服务条款 `content/terms.md`

```markdown
---
title: "服务条款"
---

# 服务条款

**生效日期**: 2024-01-01

## 1. 接受条款

使用本网站即表示您接受这些条款。

## 2. 产品描述

我们努力准确描述我们的产品，但不保证所有信息完全准确。

## 3. 定价和支付

- 所有价格以美元计价
- 支付通过 Stripe 处理
- 价格可能变动，恕不另行通知

## 4. 退款政策

- 30 天无理由退款
- 联系 refunds@yourdomain.com 申请退款
- 退款将在 5-10 个工作日内处理

## 5. 知识产权

所有内容归 [您的公司] 所有。

## 6. 责任限制

在法律允许的最大范围内，我们不对任何间接损失负责。

## 7. 联系方式

如有问题，请联系: legal@yourdomain.com
```

#### 创建退款政策 `content/refund.md`

```markdown
---
title: "退款政策"
---

# 退款政策

## 30 天无理由退款保证

我们对我们的产品充满信心。如果您不满意，我们提供 30 天无理由退款。

### 如何申请退款

1. 发送邮件至 refunds@yourdomain.com
2. 提供您的订单号或购买时使用的邮箱
3. 简要说明退款理由（可选）

### 退款处理时间

- **审批**: 24-48 小时内
- **退款到账**: 5-10 个工作日（取决于您的银行）

### 例外情况

以下情况不适用退款：
- 购买超过 30 天
- 滥用退款政策

有疑问？联系我们: support@yourdomain.com
```

#### 在页面底部添加链接

修改 `layouts/partials/footer.html` 或在 `content/_index.md` 底部添加：

```markdown
---

[隐私政策](/privacy) | [服务条款](/terms) | [退款政策](/refund)
```

### 7.2 GDPR Cookie 同意（如有需要）

如果目标用户包含欧盟用户，添加 Cookie 同意横幅：

```html
<!-- 在 layouts/partials/custom_head.html 添加 -->
<script src="https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.css">
<script>
window.addEventListener("load", function(){
  window.cookieconsent.initialise({
    "palette": {
      "popup": {"background": "#1e293b"},
      "button": {"background": "#3b82f6"}
    },
    "content": {
      "message": "本网站使用 Cookie 以提供更好的体验。",
      "dismiss": "同意",
      "link": "了解更多",
      "href": "/privacy"
    }
  })
});
</script>
```

### 7.3 配置 Stripe Webhook

如果使用后端处理，需要配置 webhook：

1. 进入 Stripe Dashboard > Developers > Webhooks
2. 点击 "Add endpoint"
3. 填写信息：
   - **Endpoint URL**: `https://your-worker.yourusername.workers.dev/webhook`
   - **Events to send**:
     - `checkout.session.completed`
     - `payment_intent.succeeded`
     - `payment_intent.payment_failed`
4. 复制 **Signing secret**: `whsec_...`
5. 添加到 Cloudflare Worker secrets：

```bash
wrangler secret put STRIPE_WEBHOOK_SECRET
# 粘贴 whsec_... 密钥
```

### 7.4 监控设置

#### Cloudflare Analytics

1. 在 Cloudflare Dashboard > Analytics 查看：
   - 访问量
   - 带宽使用
   - 请求统计
   - 国家/地区分布

#### Stripe Dashboard

监控以下指标：
- 总收入
- 成功/失败支付率
- 平均订单金额
- 客户来源

#### 错误监控（可选 - Sentry）

```html
<!-- 在 layouts/partials/custom_head.html 添加 -->
<script src="https://browser.sentry-cdn.com/7.x.x/bundle.min.js"></script>
<script>
  Sentry.init({
    dsn: 'https://your-dsn@sentry.io/project-id',
    environment: '{{ hugo.Environment }}'
  });
</script>
```

---

## 🔧 关键技术决策建议

### 表单处理方案对比

| 方案 | 优点 | 缺点 | 推荐指数 |
|------|------|------|----------|
| **Web3Forms** | 免费、无后端、易集成 | 依赖第三方 | ⭐⭐⭐⭐⭐ |
| **Cloudflare Workers** | 完全控制、无限量 | 需要编码 | ⭐⭐⭐⭐ |
| **Formspree** | 功能丰富 | 免费版限 50/月 | ⭐⭐⭐ |

### 支付处理架构对比

| 方案 | 适用场景 | 开发难度 | 推荐指数 |
|------|----------|----------|----------|
| **Stripe Payment Links** | MVP、快速上线 | ⭐ | ⭐⭐⭐⭐⭐ |
| **Stripe Checkout** | 需要定制化 | ⭐⭐ | ⭐⭐⭐⭐ |
| **完整后端 (Workers)** | 复杂业务逻辑 | ⭐⭐⭐⭐ | ⭐⭐⭐ |

### 最简 MVP 方案（1 天上线）

1. ✅ 使用 Stripe Payment Links
2. ✅ 使用 Web3Forms 处理联系表单
3. ✅ 直接部署到 Cloudflare Pages
4. ✅ 使用主题默认样式

### 标准方案（3-5 天）

1. ✅ Stripe Checkout + 自定义按钮
2. ✅ Cloudflare Workers 处理表单
3. ✅ 定制设计和内容
4. ✅ 配置 SEO 和分析

### 高级方案（1-2 周）

1. ✅ 完整 Stripe 集成 + Webhook
2. ✅ 使用 Cloudflare D1 存储订单
3. ✅ 自动发送订单邮件
4. ✅ 用户 dashboard（可选）
5. ✅ A/B 测试（Cloudflare Workers）

---

## 💡 成本估算

### 完全免费方案（0 元/月）

- **托管**: Cloudflare Pages（免费）
- **支付**: Stripe（仅按交易收费）
- **表单**: Web3Forms（免费）
- **域名**: 需购买（约 $10-15/年）

### 按需付费

- **Stripe 费用**: 2.9% + $0.30 每笔交易
  - 例：销售 $29 产品 → 手续费 $1.14
  - 实际到账: $27.86
- **Cloudflare Workers**:
  - 免费: 100,000 请求/天
  - 付费: $5/月 起（1000万请求）

### 月收入 $1000 示例

- 销售额: $1000
- Stripe 费用: ~$34
- Cloudflare 费用: $0（免费额度内）
- **净利润**: ~$966

---

## 📚 常见问题 (FAQ)

### Q: 一定要用 Cloudflare 吗？可以用 Netlify 或 Vercel 吗？

A: 可以！主题原本就支持 Netlify。但 Cloudflare Pages 的优势是：
- 更好的全球 CDN（中国大陆访问更快）
- Workers 集成更方便
- 免费额度更慷慨

### Q: Stripe 支持哪些国家？

A: Stripe 支持 40+ 个国家，包括美国、加拿大、欧盟、新加坡、香港等。中国大陆暂不支持。

替代方案：
- **PayPal**: 全球支持
- **LemonSqueezy**: 专为数字产品设计
- **Paddle**: 处理税务和支付

### Q: 如何处理增值税（VAT）？

A: 使用 Stripe Tax 自动计算（需付费）或集成 LemonSqueezy/Paddle（内置税务处理）。

### Q: 怎么发送产品下载链接给客户？

A: 方案：
1. **手动**: 收到 Stripe 邮件通知后手动发送
2. **半自动**: 使用 Zapier 连接 Stripe + Gmail
3. **全自动**: Cloudflare Worker 监听 webhook，自动发送邮件

### Q: 可以添加折扣码吗？

A: 可以！
- Stripe Checkout 原生支持
- 在 Stripe Dashboard > Products > Coupons 创建
- 在 checkout 配置中启用 `allow_promotion_codes: true`

### Q: 如何追踪转化率？

A: 使用以下工具：
- **Google Analytics**: 设置目标转化
- **Stripe Dashboard**: 查看支付成功率
- **Cloudflare Web Analytics**: 隐私友好的访问统计

### Q: 支持订阅模式吗？

A: 完全支持！
1. 在 Stripe 创建订阅价格
2. 将 `mode: 'payment'` 改为 `mode: 'subscription'`
3. 配置 webhook 处理订阅事件

---

## 🚀 快速启动检查清单

### 开发阶段
- [ ] 创建新 Hugo 项目
- [ ] 复制主题文件
- [ ] 安装 npm 依赖
- [ ] 本地测试运行
- [ ] 修改内容和设计

### Stripe 配置
- [ ] 注册 Stripe 账户
- [ ] 创建产品和价格
- [ ] 获取 API 密钥
- [ ] 选择集成方案
- [ ] 测试支付流程

### 部署阶段
- [ ] 推送代码到 Git
- [ ] 连接 Cloudflare Pages
- [ ] 配置构建设置
- [ ] 添加环境变量
- [ ] 首次部署成功

### 域名和 DNS
- [ ] 购买域名
- [ ] 配置 DNS 记录
- [ ] 等待 SSL 证书生效
- [ ] 验证 HTTPS 正常

### 上线前检查
- [ ] 所有链接测试通过
- [ ] 支付流程完整测试
- [ ] 表单提交正常
- [ ] 移动端显示正常
- [ ] 页面加载速度 < 3s
- [ ] SEO 标签完整
- [ ] 法律页面齐全

### 上线后
- [ ] 切换 Stripe 到生产模式
- [ ] 配置 webhook（如果需要）
- [ ] 监控首笔订单
- [ ] 设置分析工具
- [ ] 准备营销推广

---

## 📖 参考资源

### 官方文档
- [Hugo 文档](https://gohugo.io/documentation/)
- [Stripe 文档](https://stripe.com/docs)
- [Cloudflare Pages 文档](https://developers.cloudflare.com/pages/)
- [Cloudflare Workers 文档](https://developers.cloudflare.com/workers/)

### 有用工具
- [Stripe 测试卡号](https://stripe.com/docs/testing)
- [Hugo Themes](https://themes.gohugo.io/)
- [Tailwind CSS 文档](https://tailwindcss.com/docs)
- [MailChannels (免费邮件发送)](https://blog.cloudflare.com/sending-email-from-workers-with-mailchannels/)

### 社区支持
- [Hugo Discourse](https://discourse.gohugo.io/)
- [Cloudflare Community](https://community.cloudflare.com/)
- [Stripe Discord](https://discord.gg/stripe)

---

## 🎯 下一步行动

选择适合你的起步方案：

### 方案 1: 最快上线（推荐新手）
```bash
# 1. 创建项目
hugo new site my-product && cd my-product

# 2. 添加主题
git submodule add https://github.com/janraasch/hugo-product-launch.git themes/hugo-product-launch

# 3. 使用示例配置
cp themes/hugo-product-launch/exampleSite/* . -r

# 4. 开始编辑
code content/_index.md
```

### 方案 2: 从头开始（推荐自定义）

按照本文档的阶段一到阶段七依次执行。

### 方案 3: 先试用主题

```bash
cd /Users/ming/Documents/HUGO/hugo-product-launch/exampleSite
hugo server
# 访问 http://localhost:1313 预览
```

---

**最后更新**: 2024-10-05
**文档版本**: 1.0
**适用 Hugo 版本**: 0.140.0+

如有问题，请参考各阶段的详细说明或查阅官方文档。祝您的产品大卖！🚀
