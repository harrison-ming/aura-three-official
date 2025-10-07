/**
 * Cloudflare Worker for Stripe Checkout Session Creation
 *
 * Environment Variables Required:
 * - STRIPE_SECRET_KEY: Your Stripe secret key (sk_live_...)
 */

export default {
  async fetch(request, env) {
    // Get origin from request
    const origin = request.headers.get('Origin');

    // Allow both production and local development origins
    const allowedOrigins = [
      'https://blessaura.com',
      'http://localhost:1313',
      'http://localhost:1314'
    ];

    const corsOrigin = allowedOrigins.includes(origin) ? origin : 'https://blessaura.com';

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': corsOrigin,
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
      const { amount, currency = 'usd', customerEmail, metadata } = await request.json();

      if (!amount) {
        return new Response(JSON.stringify({ error: 'Amount is required' }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // Check if secret key exists
      if (!env.STRIPE_SECRET_KEY) {
        console.error('STRIPE_SECRET_KEY not found in environment');
        return new Response(JSON.stringify({ error: 'Stripe configuration error' }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      console.log('Creating payment intent with amount:', amount, currency);

      // Create Stripe PaymentIntent
      const paymentIntent = await createPaymentIntent(env.STRIPE_SECRET_KEY, {
        amount,
        currency,
        customerEmail,
        metadata,
      });

      return new Response(JSON.stringify({
        clientSecret: paymentIntent.client_secret,
        paymentIntentId: paymentIntent.id
      }), {
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
 * Create Stripe PaymentIntent
 */
async function createPaymentIntent(secretKey, options) {
  const {
    amount,
    currency,
    customerEmail,
    metadata = {},
  } = options;

  // Prepare form data for Stripe API
  const formData = new URLSearchParams();
  formData.append('amount', amount.toString());
  formData.append('currency', currency);
  formData.append('automatic_payment_methods[enabled]', 'true');

  if (customerEmail) {
    formData.append('receipt_email', customerEmail);
  }

  // Add metadata
  Object.entries(metadata).forEach(([key, value]) => {
    formData.append(`metadata[${key}]`, value);
  });

  // Call Stripe API
  const response = await fetch('https://api.stripe.com/v1/payment_intents', {
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
