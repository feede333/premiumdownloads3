// This file contains configuration settings for payment processing, such as API keys and endpoints for payment gateways.

const paymentConfig = {
    gateway: {
        name: 'YourPaymentGateway', // Replace with your payment gateway name
        apiKey: process.env.PAYMENT_GATEWAY_API_KEY, // API key for the payment gateway
        apiSecret: process.env.PAYMENT_GATEWAY_API_SECRET, // API secret for the payment gateway
        endpoint: 'https://api.yourpaymentgateway.com/v1/payments', // Replace with your payment gateway endpoint
    },
    currency: 'USD', // Default currency for transactions
    timeout: 30000, // Timeout for payment requests in milliseconds
};

module.exports = paymentConfig;