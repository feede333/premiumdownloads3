async function logVisit() {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        
        const visitData = {
            timestamp: new Date().toISOString(),
            ip: data.ip,
            userAgent: navigator.userAgent,
            language: navigator.language,
            screenResolution: `${window.screen.width}x${window.screen.height}`,
            referrer: document.referrer,
            path: window.location.pathname
        };

        await fetch('/api/log-visit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(visitData)
        });

    } catch (error) {
        console.error('Error logging visit:', error);
    }
}

document.addEventListener('DOMContentLoaded', logVisit);