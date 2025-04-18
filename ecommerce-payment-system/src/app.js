const express = require('express');
const bodyParser = require('body-parser');
const paymentRoutes = require('./api/routes/paymentRoutes');
const { connectToDatabase } = require('./config/database');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Connect to the database
connectToDatabase();

// Set up routes
app.use('/api/payments', paymentRoutes);

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});