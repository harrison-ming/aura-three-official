/**
 * Cloudflare Worker for Stripe Checkout Session Creation
 *
 * Environment Variables Required:
 * - STRIPE_SECRET_KEY: Your Stripe secret key (sk_live_...)
 */

export default {
  async fetch(request, env) {
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': 'https://new-vansky.com',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Only allow POST
    if (request.method !== 'POST') {
      return new Response('Method not allowed', {
        status: 405,
        headers: corsHeaders
      });
    }

    try {
      // Parse request body
      const { priceId, quantity = 1, customerEmail, metadata } = await request.json();

      if (!priceId) {
        return new Response(JSON.stringify({ error: 'Price ID is required' }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // Create Stripe Checkout Session
      const session = await createCheckoutSession(env.STRIPE_SECRET_KEY, {
        priceId,
        quantity,
        customerEmail,
        metadata,
        successUrl: 'https://new-vansky.com/success?session_id={CHECKOUT_SESSION_ID}',
        cancelUrl: 'https://new-vansky.com/cancel',
      });

      return new Response(JSON.stringify({ sessionId: session.id, url: session.url }), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });

    } catch (error) {
      console.error('Error creating checkout session:', error);
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};

/**
 * Create Stripe Checkout Session
 */
async function createCheckoutSession(secretKey, options) {
  const {
    priceId,
    quantity,
    customerEmail,
    metadata = {},
    successUrl,
    cancelUrl,
  } = options;

  // Prepare form data for Stripe API
  const formData = new URLSearchParams();
  formData.append('mode', 'payment');
  formData.append('line_items[0][price]', priceId);
  formData.append('line_items[0][quantity]', quantity.toString());
  formData.append('success_url', successUrl);
  formData.append('cancel_url', cancelUrl);

  if (customerEmail) {
    formData.append('customer_email', customerEmail);
  }

  // Add metadata
  Object.entries(metadata).forEach(([key, value]) => {
    formData.append(`metadata[${key}]`, value);
  });

  // Call Stripe API
  const response = await fetch('https://api.stripe.com/v1/checkout/sessions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${secretKey}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData.toString(),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Stripe API error: ${error}`);
  }

  return await response.json();
}
