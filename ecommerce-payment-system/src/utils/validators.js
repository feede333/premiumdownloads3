// This file contains utility functions for validating various data inputs, ensuring they meet specific criteria.

function validateCardNumber(cardNumber) {
    const regex = /^\d{16}$/;
    return regex.test(cardNumber);
}

function validateExpiryDate(expiryDate) {
    const regex = /^(0[1-9]|1[0-2])\/?([0-9]{4}|[0-9]{2})$/;
    return regex.test(expiryDate);
}

function validateCVV(cvv) {
    const regex = /^\d{3}$/;
    return regex.test(cvv);
}

function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function validateAmount(amount) {
    return typeof amount === 'number' && amount > 0;
}

module.exports = {
    validateCardNumber,
    validateExpiryDate,
    validateCVV,
    validateEmail,
    validateAmount
};