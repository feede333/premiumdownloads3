const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 3000;

// Basic middleware
app.use(express.json());
app.use(express.static(__dirname));

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

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});