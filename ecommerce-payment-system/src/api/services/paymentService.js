class PaymentService {
    constructor(paymentGateway) {
        this.paymentGateway = paymentGateway; // Payment gateway instance
    }

    async initiatePayment(paymentDetails) {
        try {
            // Logic to initiate payment with the payment gateway
            const response = await this.paymentGateway.processPayment(paymentDetails);
            return response; // Return the response from the payment gateway
        } catch (error) {
            throw new Error('Payment initiation failed: ' + error.message);
        }
    }

    async verifyPayment(paymentId) {
        try {
            // Logic to verify payment status with the payment gateway
            const response = await this.paymentGateway.checkPaymentStatus(paymentId);
            return response; // Return the payment status
        } catch (error) {
            throw new Error('Payment verification failed: ' + error.message);
        }
    }
}

export default PaymentService;