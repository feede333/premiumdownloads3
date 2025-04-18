// This file contains middleware functions that validate incoming requests, ensuring that the data meets the required format before processing.

const { body, validationResult } = require('express-validator');

const validatePayment = [
    body('amount')
        .isNumeric()
        .withMessage('Amount must be a number')
        .notEmpty()
        .withMessage('Amount is required'),
    body('paymentMethod')
        .isString()
        .withMessage('Payment method must be a string')
        .notEmpty()
        .withMessage('Payment method is required'),
    body('currency')
        .isString()
        .withMessage('Currency must be a string')
        .notEmpty()
        .withMessage('Currency is required'),
    (req, res, next) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }
        next();
    }
];

module.exports = {
    validatePayment,
};