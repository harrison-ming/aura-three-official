/**
 * Email Template for Order Confirmation
 *
 * HOW TO CUSTOMIZE THIS TEMPLATE:
 * ================================
 *
 * 1. SUBJECT LINE (line 17):
 *    - Change the emoji or text
 *    - Modify the wording
 *
 * 2. COLORS (lines 30-34):
 *    - primaryColor: Main brand color (buttons, headers)
 *    - accentColor: Accent color for highlights
 *    - textColor: Main text color
 *    - backgroundColor: Email background
 *
 * 3. CONTENT SECTIONS:
 *    - Hero section (line 50): Main greeting and thank you message
 *    - Order details (line 70): Product info and pricing
 *    - Next steps (line 90): What happens after purchase
 *    - Footer (line 120): Contact info and legal
 *
 * 4. IMAGES:
 *    - Add your logo URL at line 45
 *    - Add product image at line 75
 *
 * 5. LINKS:
 *    - Update website URL (line 130)
 *    - Update support email (line 125)
 */

export function getEmailSubject(orderData) {
  return `🎉 Your Celestial Blessing is Confirmed - Order #${orderData.orderId.slice(-8)}`;
}

export function getEmailHtml(orderData) {
  const {
    customerName,
    customerEmail,
    orderId,
    productName,
    amount,
    currency,
    orderDate
  } = orderData;

  // Brand colors - CUSTOMIZE THESE
  const colors = {
    primaryColor: '#3FA026',
    accentColor: '#5ED54B',
    textColor: '#1f2937',
    backgroundColor: '#f9fafb',
    goldColor: '#facc15'
  };

  return `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Order Confirmation</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: ${colors.backgroundColor};">

  <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: ${colors.backgroundColor};">
    <tr>
      <td style="padding: 40px 20px;">

        <!-- Main Container -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">

          <!-- Header -->
          <tr>
            <td style="padding: 40px 40px 20px; text-align: center; background: linear-gradient(135deg, ${colors.primaryColor} 0%, ${colors.accentColor} 100%); border-radius: 8px 8px 0 0;">
              <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: bold;">
                ✨ Thank You for Your Order
              </h1>
            </td>
          </tr>

          <!-- Greeting -->
          <tr>
            <td style="padding: 30px 40px;">
              <p style="margin: 0 0 20px; font-size: 16px; color: ${colors.textColor}; line-height: 1.6;">
                Dear <strong>${customerName}</strong>,
              </p>
              <p style="margin: 0 0 20px; font-size: 16px; color: ${colors.textColor}; line-height: 1.6;">
                Your order for the <strong>Celestial Decree of Triple Blessings</strong> has been confirmed! The Three Officials have heard your prayers.
              </p>
            </td>
          </tr>

          <!-- Order Summary Box -->
          <tr>
            <td style="padding: 0 40px 30px;">
              <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: ${colors.backgroundColor}; border-radius: 8px; border: 2px solid ${colors.goldColor};">
                <tr>
                  <td style="padding: 20px;">
                    <h2 style="margin: 0 0 15px; font-size: 18px; color: ${colors.textColor};">
                      📦 Order Details
                    </h2>
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="font-size: 14px; color: ${colors.textColor};">
                      <tr>
                        <td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">Product:</td>
                        <td style="padding: 8px 0; text-align: right; border-bottom: 1px solid #e5e7eb; font-weight: 600;">
                          ${productName}
                        </td>
                      </tr>
                      <tr>
                        <td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">Amount:</td>
                        <td style="padding: 8px 0; text-align: right; border-bottom: 1px solid #e5e7eb; font-weight: 600;">
                          $${(amount / 100).toFixed(2)} ${currency.toUpperCase()}
                        </td>
                      </tr>
                      <tr>
                        <td style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">Order ID:</td>
                        <td style="padding: 8px 0; text-align: right; border-bottom: 1px solid #e5e7eb; font-family: monospace; font-size: 12px;">
                          ${orderId}
                        </td>
                      </tr>
                      <tr>
                        <td style="padding: 8px 0;">Order Date:</td>
                        <td style="padding: 8px 0; text-align: right;">
                          ${orderDate}
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- What's Next Section -->
          <tr>
            <td style="padding: 0 40px 30px;">
              <h2 style="margin: 0 0 15px; font-size: 18px; color: ${colors.textColor};">
                🚚 What Happens Next?
              </h2>
              <div style="background-color: #fef5c4; padding: 15px; border-radius: 6px; border-left: 4px solid ${colors.goldColor};">
                <p style="margin: 0 0 10px; font-size: 14px; color: ${colors.textColor}; line-height: 1.6;">
                  <strong>1. Sacred Preparation:</strong> Your Celestial Decree will be carefully prepared and blessed during the next auspicious celestial date.
                </p>
                <p style="margin: 0 0 10px; font-size: 14px; color: ${colors.textColor}; line-height: 1.6;">
                  <strong>2. Shipping Confirmation:</strong> You will receive tracking information within 3-5 business days.
                </p>
                <p style="margin: 0; font-size: 14px; color: ${colors.textColor}; line-height: 1.6;">
                  <strong>3. Delivery:</strong> Free worldwide shipping. Estimated delivery: 7-14 business days.
                </p>
              </div>
            </td>
          </tr>

          <!-- Spiritual Guidance -->
          <tr>
            <td style="padding: 0 40px 30px;">
              <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, rgba(63,160,38,0.1) 0%, rgba(94,213,75,0.1) 100%); border-radius: 8px;">
                <p style="margin: 0 0 10px; font-size: 16px; color: ${colors.textColor}; font-weight: 600;">
                  🙏 In the Meantime
                </p>
                <p style="margin: 0; font-size: 14px; color: ${colors.textColor}; line-height: 1.6; font-style: italic;">
                  Take a moment to set your intentions. The celestial Three Officials hear sincere prayers and respond to pure hearts.
                </p>
              </div>
            </td>
          </tr>

          <!-- CTA Button -->
          <tr>
            <td style="padding: 0 40px 30px; text-align: center;">
              <a href="https://blessaura.com" style="display: inline-block; padding: 14px 32px; background-color: ${colors.primaryColor}; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px;">
                Visit Our Website
              </a>
            </td>
          </tr>

          <!-- Support Section -->
          <tr>
            <td style="padding: 0 40px 30px;">
              <p style="margin: 0; font-size: 14px; color: #6b7280; text-align: center; line-height: 1.6;">
                Questions or concerns? Reply to this email or contact us at<br>
                <a href="mailto:support@blessaura.com" style="color: ${colors.primaryColor}; text-decoration: none;">support@blessaura.com</a>
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding: 20px 40px; background-color: ${colors.backgroundColor}; border-radius: 0 0 8px 8px; border-top: 1px solid #e5e7eb;">
              <p style="margin: 0 0 10px; font-size: 14px; color: #6b7280; text-align: center; font-style: italic;">
                May the celestial blessings flow to you.
              </p>
              <p style="margin: 0; font-size: 12px; color: #9ca3af; text-align: center;">
                © ${new Date().getFullYear()} Celestial Decree. All rights reserved.<br>
                <a href="https://blessaura.com/privacy" style="color: #9ca3af; text-decoration: none;">Privacy Policy</a> |
                <a href="https://blessaura.com/terms" style="color: #9ca3af; text-decoration: none;">Terms of Service</a> |
                <a href="https://blessaura.com/refund" style="color: #9ca3af; text-decoration: none;">Refund Policy</a>
              </p>
            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>
  `.trim();
}

export function getEmailText(orderData) {
  const {
    customerName,
    orderId,
    productName,
    amount,
    currency,
    orderDate
  } = orderData;

  return `
✨ Thank You for Your Order

Dear ${customerName},

Your order for the Celestial Decree of Triple Blessings has been confirmed!

📦 ORDER DETAILS:
- Product: ${productName}
- Amount: $${(amount / 100).toFixed(2)} ${currency.toUpperCase()}
- Order ID: ${orderId}
- Date: ${orderDate}

🚚 WHAT HAPPENS NEXT?

1. Sacred Preparation: Your Celestial Decree will be carefully prepared and blessed during the next auspicious celestial date.

2. Shipping Confirmation: You will receive tracking information within 3-5 business days.

3. Delivery: Free worldwide shipping. Estimated delivery: 7-14 business days.

🙏 IN THE MEANTIME:
Take a moment to set your intentions. The celestial Three Officials hear sincere prayers and respond to pure hearts.

Questions? Reply to this email or contact us at support@blessaura.com

May the celestial blessings flow to you.

---
© ${new Date().getFullYear()} Celestial Decree. All rights reserved.
https://blessaura.com
  `.trim();
}
