/**
 * Cloudflare Worker for Stripe Webhook Handler
 *
 * Environment Variables Required:
 * - STRIPE_WEBHOOK_SECRET: Your Stripe webhook signing secret (whsec_...)
 * - RESEND_API_KEY: Your Resend API key (re_...)
 *
 * Optional: KV Namespace binding for storing orders
 * - ORDERS: KV namespace for order storage
 */

import { getEmailSubject, getEmailHtml, getEmailText } from './email-template.js';

export default {
  async fetch(request, env) {
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      // Get raw body and signature
      const payload = await request.text();
      const signature = request.headers.get('stripe-signature');

      if (!signature) {
        return new Response('No signature', { status: 400 });
      }

      // Verify webhook signature
      const event = await verifyWebhookSignature(
        payload,
        signature,
        env.STRIPE_WEBHOOK_SECRET
      );

      console.log('Webhook event:', event.type);

      // Handle different event types
      switch (event.type) {
        case 'checkout.session.completed':
          await handleCheckoutCompleted(event.data.object, env);
          break;

        case 'payment_intent.succeeded':
          await handlePaymentSucceeded(event.data.object, env);
          break;

        case 'payment_intent.payment_failed':
          await handlePaymentFailed(event.data.object, env);
          break;

        default:
          console.log(`Unhandled event type: ${event.type}`);
      }

      return new Response(JSON.stringify({ received: true }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });

    } catch (error) {
      console.error('Webhook error:', error);
      return new Response(JSON.stringify({ error: error.message }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }
};

/**
 * Verify Stripe webhook signature
 */
async function verifyWebhookSignature(payload, signature, secret) {
  // Parse signature header
  const parts = signature.split(',');
  const timestamp = parts.find(p => p.startsWith('t=')).substring(2);
  const expectedSignature = parts.find(p => p.startsWith('v1=')).substring(3);

  // Create signed payload
  const signedPayload = `${timestamp}.${payload}`;

  // Compute HMAC
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    encoder.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );

  const signature_bytes = await crypto.subtle.sign(
    'HMAC',
    key,
    encoder.encode(signedPayload)
  );

  // Convert to hex
  const computedSignature = Array.from(new Uint8Array(signature_bytes))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');

  // Compare signatures
  if (computedSignature !== expectedSignature) {
    throw new Error('Invalid signature');
  }

  // Check timestamp (prevent replay attacks)
  const currentTime = Math.floor(Date.now() / 1000);
  if (currentTime - parseInt(timestamp) > 300) { // 5 minutes tolerance
    throw new Error('Timestamp too old');
  }

  return JSON.parse(payload);
}

/**
 * Handle successful checkout
 */
async function handleCheckoutCompleted(session, env) {
  console.log('Checkout completed:', session.id);
  console.log('Customer email:', session.customer_details?.email);
  console.log('Amount:', session.amount_total / 100, session.currency.toUpperCase());

  // Store order in KV (if available)
  if (env.ORDERS) {
    const order = {
      sessionId: session.id,
      customerEmail: session.customer_details?.email,
      amount: session.amount_total,
      currency: session.currency,
      status: session.payment_status,
      metadata: session.metadata,
      createdAt: new Date().toISOString(),
    };

    await env.ORDERS.put(
      `order:${session.id}`,
      JSON.stringify(order),
      { expirationTtl: 60 * 60 * 24 * 90 } // 90 days
    );
  }

  // Send confirmation email
  if (session.customer_details?.email) {
    await sendOrderConfirmationEmail({
      customerEmail: session.customer_details.email,
      customerName: session.customer_details.name || 'Valued Customer',
      orderId: session.id,
      productName: 'Celestial Decree of Triple Blessings',
      amount: session.amount_total,
      currency: session.currency,
    }, env);
  }
}

/**
 * Handle successful payment
 */
async function handlePaymentSucceeded(paymentIntent, env) {
  console.log('Payment succeeded:', paymentIntent.id);
  console.log('Customer email:', paymentIntent.receipt_email);
  console.log('Amount:', paymentIntent.amount / 100, paymentIntent.currency.toUpperCase());

  // Send confirmation email
  if (paymentIntent.receipt_email) {
    // Extract customer name from billing details
    const customerName = paymentIntent.charges?.data?.[0]?.billing_details?.name || 'Valued Customer';

    await sendOrderConfirmationEmail({
      customerEmail: paymentIntent.receipt_email,
      customerName: customerName,
      orderId: paymentIntent.id,
      productName: paymentIntent.metadata?.product_name || 'Celestial Decree of Triple Blessings',
      amount: paymentIntent.amount,
      currency: paymentIntent.currency,
    }, env);
  }
}

/**
 * Handle failed payment
 */
async function handlePaymentFailed(paymentIntent, env) {
  console.log('Payment failed:', paymentIntent.id);
  // TODO: Send failure notification email (optional)
}

/**
 * Send order confirmation email via Resend
 */
async function sendOrderConfirmationEmail(orderData, env) {
  if (!env.RESEND_API_KEY) {
    console.error('RESEND_API_KEY not configured');
    return;
  }

  try {
    // Format order date
    const orderDate = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: 'UTC'
    });

    const emailData = {
      ...orderData,
      orderDate
    };

    // Prepare email
    const emailPayload = {
      from: 'Celestial Decree <orders@blessaura.com>',
      to: [orderData.customerEmail],
      subject: getEmailSubject(emailData),
      html: getEmailHtml(emailData),
      text: getEmailText(emailData),
    };

    console.log('Sending email to:', orderData.customerEmail);

    // Call Resend API
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(emailPayload),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Resend API error: ${error}`);
    }

    const result = await response.json();
    console.log('Email sent successfully:', result.id);

    return result;

  } catch (error) {
    console.error('Failed to send email:', error);
    // Don't throw - we don't want to fail the webhook if email fails
  }
}
