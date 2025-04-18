const express = require('express');
const axios = require('axios');
const dotenv = require('dotenv');
const path = require('path');
const fs = require('fs');

// Cargar variables de entorno
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middlewares
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// CORS headers
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    next();
});

// Add specific route for subpages
app.use('/subpages', express.static(path.join(__dirname, 'subpages')));

// Add specific route for data folder
app.use('/data', express.static(path.join(__dirname, 'data')));

// Modify versions.json route
app.get('/data/versions.json', (req, res) => {
    try {
        const versionsPath = path.join(__dirname, 'data', 'versions.json');
        console.log('Attempting to read versions from:', versionsPath);
        
        if (fs.existsSync(versionsPath)) {
            const data = fs.readFileSync(versionsPath, 'utf8');
            console.log('Successfully loaded versions:', data);
            res.json(JSON.parse(data));
        } else {
            console.warn('versions.json not found at:', versionsPath);
            res.json({ versions: [] });
        }
    } catch (error) {
        console.error('Error reading versions:', error);
        res.status(500).json({ error: 'Error reading versions' });
    }
});

// Create logs directory if it doesn't exist
const logsDir = path.join(__dirname, 'logs');
if (!fs.existsSync(logsDir)) {
    fs.mkdirSync(logsDir);
}

// Add logging endpoint
app.post('/api/log-visit', (req, res) => {
    try {
        const logData = {
            ...req.body,
            timestamp: new Date().toISOString()
        };

        const logPath = path.join(__dirname, 'logs', 'visits.log');
        fs.appendFileSync(logPath, JSON.stringify(logData) + '\n');

        res.status(200).send('Log recorded');
    } catch (error) {
        console.error('Error logging visit:', error);
        res.status(500).send('Error recording log');
    }
});

// Configuración segura de las credenciales de Paykassa
const PAYKASSA_API_CONFIG = {
    apiId: process.env.PAYKASSA_API_ID,
    apiPassword: process.env.PAYKASSA_API_PASSWORD,
    baseUrl: 'https://paykassa.pro/api/0.6/index.php'
};

// Endpoint para crear una solicitud de pago
app.post('/api/create-paykassa-payment', async (req, res) => {
    try {
        const {
            amount,
            currency,
            orderId,
            productId,
            productName,
            customerName,
            customerEmail
        } = req.body;

        // Crear solicitud a Paykassa
        const paymentRequest = {
            func: 'sci_create_order',
            sci_id: PAYKASSA_API_CONFIG.apiId,
            sci_key: PAYKASSA_API_CONFIG.apiPassword,
            amount: amount,
            currency: currency,
            order_id: orderId,
            comment: `Compra de ${productName}`,
            phone: '', // Opcional
            email: customerEmail,
            success_url: `${req.protocol}://${req.get('host')}/payment/success?id=${productId}`,
            fail_url: `${req.protocol}://${req.get('host')}/payment/cancel`
        };

        // Enviar solicitud a Paykassa
        const response = await axios.post(PAYKASSA_API_CONFIG.baseUrl, paymentRequest);
        
        if (response.data && response.data.error === false) {
            // Éxito - devolver URL de redirección
            res.json({
                success: true,
                redirectUrl: response.data.data.url,
                paymentId: response.data.data.transaction
            });
        } else {
            // Error desde Paykassa
            res.json({
                success: false,
                message: response.data?.message || 'Error al crear la solicitud de pago'
            });
        }
    } catch (error) {
        console.error('Error al procesar la solicitud de pago:', error);
        res.status(500).json({
            success: false,
            message: 'Error del servidor al procesar el pago'
        });
    }
});

// Página de éxito de pago
app.get('/payment/success', (req, res) => {
    const productId = req.query.id;
    res.sendFile(path.join(__dirname, 'success.html'));
});

// Página de cancelación de pago
app.get('/payment/cancel', (req, res) => {
    res.sendFile(path.join(__dirname, 'cancel.html'));
});

app.listen(PORT, () => {
    console.log(`Servidor corriendo en el puerto ${PORT}`);
});