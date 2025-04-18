// This file contains client-side JavaScript for handling payment interactions on the frontend.

document.addEventListener('DOMContentLoaded', function() {
    const paymentForm = document.getElementById('payment-form');
    const paymentButton = document.getElementById('payment-button');

    paymentButton.addEventListener('click', function(event) {
        event.preventDefault();
        processPayment();
    });

    function processPayment() {
        const formData = new FormData(paymentForm);
        const paymentData = {
            cardNumber: formData.get('cardNumber'),
            cardExpiry: formData.get('cardExpiry'),
            cardCVC: formData.get('cardCVC'),
            amount: formData.get('amount'),
        };

        fetch('/api/payment/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(paymentData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/confirmation.html';
            } else {
                alert('Payment failed: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error processing payment:', error);
            alert('An error occurred while processing your payment. Please try again.');
        });
    }
});