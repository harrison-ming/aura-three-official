# Cloudflare Workers 部署指南

这个目录包含处理 Stripe 支付的 Cloudflare Workers。

## 文件说明

- `checkout.js` - 创建 Stripe Checkout Session 的 Worker
- `webhook.js` - 接收 Stripe Webhook 事件的 Worker
- `wrangler.toml` - Workers 配置文件

## 部署步骤

### 1. 安装 Wrangler CLI

```bash
npm install -g wrangler
```

### 2. 登录 Cloudflare

```bash
wrangler login
```

### 3. 配置环境变量

#### 3.1 配置 Stripe Secret Key (Checkout Worker)

```bash
cd workers
wrangler secret put STRIPE_SECRET_KEY
# 输入你的 Stripe Secret Key: sk_live_...
```

#### 3.2 配置 Webhook Secret (Webhook Worker)

首先在 Stripe Dashboard 创建 Webhook:
1. 访问 https://dashboard.stripe.com/webhooks
2. 点击 "Add endpoint"
3. URL: `https://aura-webhook.YOUR-SUBDOMAIN.workers.dev`
4. 选择事件: `checkout.session.completed`
5. 复制 "Signing secret" (whsec_...)

然后配置:
```bash
wrangler secret put STRIPE_WEBHOOK_SECRET --name aura-webhook
# 输入你的 Webhook Secret: whsec_...
```

### 4. 部署 Workers

```bash
# 部署 Checkout Worker
wrangler deploy checkout.js --name aura-checkout

# 部署 Webhook Worker
wrangler deploy webhook.js --name aura-webhook
```

### 5. 获取 Worker URL

部署成功后会显示 URL，例如:
- Checkout: `https://aura-checkout.YOUR-SUBDOMAIN.workers.dev`
- Webhook: `https://aura-webhook.YOUR-SUBDOMAIN.workers.dev`

### 6. 更新 Hugo 配置

编辑 `hugo.toml`:

```toml
[params.stripe]
    publishable_key = "pk_live_..."
    worker_url = "https://aura-checkout.YOUR-SUBDOMAIN.workers.dev"
```

### 7. 配置 Stripe Webhook

1. 访问 https://dashboard.stripe.com/webhooks
2. 添加 endpoint URL: `https://aura-webhook.YOUR-SUBDOMAIN.workers.dev`
3. 选择事件: `checkout.session.completed`, `payment_intent.succeeded`

## 测试

### 本地测试 (可选)

```bash
# 启动本地开发服务器
wrangler dev checkout.js

# 测试 Checkout API
curl -X POST http://localhost:8787 \
  -H "Content-Type: application/json" \
  -d '{"priceId":"price_1SEvD0Icuszw748DmM64CZnQ","quantity":1}'
```

### 生产测试

1. 部署 Hugo 站点到 Cloudflare Pages
2. 访问站点并点击支付按钮
3. 完成支付测试

## 可选: 启用 KV 存储订单数据

### 1. 创建 KV Namespace

```bash
wrangler kv:namespace create "ORDERS"
```

### 2. 更新 wrangler.toml

将返回的 ID 添加到配置:

```toml
[[kv_namespaces]]
binding = "ORDERS"
id = "your_kv_namespace_id_here"
```

### 3. 重新部署

```bash
wrangler deploy webhook.js --name aura-webhook
```

## 查看日志

```bash
# 查看 Checkout Worker 日志
wrangler tail aura-checkout

# 查看 Webhook Worker 日志
wrangler tail aura-webhook
```

## 常见问题

### Q: Worker 部署后返回 CORS 错误?

A: 检查 `checkout.js` 中的 CORS 允许域名是否正确:
```javascript
'Access-Control-Allow-Origin': 'https://aura-three-official.pages.dev'
```

### Q: Webhook 签名验证失败?

A: 确保正确配置了 `STRIPE_WEBHOOK_SECRET`，并且使用的是正确的 endpoint。

### Q: 如何查看订单数据?

A: 如果启用了 KV 存储:
```bash
wrangler kv:key list --namespace-id=your_kv_namespace_id
wrangler kv:key get "order:cs_xxx" --namespace-id=your_kv_namespace_id
```

或者直接在 Stripe Dashboard 查看: https://dashboard.stripe.com/payments
