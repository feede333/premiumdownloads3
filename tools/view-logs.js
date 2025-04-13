const fs = require('fs');
const path = require('path');

const logPath = path.join(__dirname, '..', 'logs', 'visits.log');

function analyzeLogs() {
    if (!fs.existsSync(logPath)) {
        console.log('No logs found. The file will be created when visits are logged.');
        return;
    }

    const logs = fs.readFileSync(logPath, 'utf8')
        .split('\n')
        .filter(line => line.trim())
        .map(line => JSON.parse(line));

    console.log('Total visits:', logs.length);
    
    // Análisis por IP
    const ipCounts = {};
    logs.forEach(log => {
        ipCounts[log.ip] = (ipCounts[log.ip] || 0) + 1;
    });
    
    console.log('\nVisits by IP:');
    Object.entries(ipCounts)
        .sort(([,a], [,b]) => b - a)
        .forEach(([ip, count]) => {
            console.log(`${ip}: ${count} visits`);
        });
}

analyzeLogs();