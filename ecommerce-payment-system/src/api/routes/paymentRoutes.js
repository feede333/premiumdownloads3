import express from 'express';
import PaymentController from '../controllers/paymentController';
import { authenticate } from '../middlewares/auth';
import { validatePayment } from '../middlewares/validation';

const router = express.Router();
const paymentController = new PaymentController();

export const setPaymentRoutes = (app) => {
    router.post('/process', authenticate, validatePayment, paymentController.processPayment);
    router.get('/status/:paymentId', authenticate, paymentController.getPaymentStatus);

    app.use('/api/payments', router);
};