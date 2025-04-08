const WebSocket = require('ws');
const express = require('express');
const storageManager = require('./frontend/public/js/storage');

const server = new WebSocket.Server({ port: 8080 });
const app = express();
const port = 3000;

// Base de conocimientos del sitio
const siteKnowledge = {
    programs: {
        'avast premium security': {
            category: 'Antivirus',
            size: '628 MB',
            description: 'Antivirus premium con protección completa',
            version: '21.1.2323'
        },
        'ccleaner professional': {
            category: 'Utilities',
            size: '25 MB',
            description: 'Optimizador y limpiador del sistema',
            version: '6.12.0'
        },
        'winrar': {
            category: 'File Tools',
            size: '3.5 MB',
            description: 'Compresor de archivos',
            version: '6.24'
        }
    },
    categories: ['Antivirus', 'Utilities', 'File Tools', 'Internet', 'Security', 'Office', 'Development'],
    features: ['búsqueda', 'modo oscuro', 'filtrado por categorías', 'ordenamiento']
};

function processQuery(query) {
    query = query.toLowerCase();

    // Búsqueda de programas
    if (query.includes('buscar') || query.includes('encontrar') || query.includes('donde')) {
        const programNames = Object.keys(siteKnowledge.programs)
            .map(name => `- ${name.toUpperCase()}`).join('\n');
        return `Estos son los programas disponibles:\n${programNames}`;
    }

    // Información sobre categorías
    if (query.includes('categoria') || query.includes('categorías')) {
        return `Las categorías disponibles son:\n${siteKnowledge.categories.map(c => `- ${c}`).join('\n')}`;
    }

    // Cambio de tema
    if (query.includes('tema') || query.includes('oscuro') || query.includes('claro')) {
        return "Puedes cambiar entre tema claro y oscuro usando el botón con el ícono de luna/sol en la esquina superior derecha.";
    }

    // Información sobre un programa específico
    for (const [name, info] of Object.entries(siteKnowledge.programs)) {
        if (query.includes(name)) {
            return `${name.toUpperCase()}:\n- Categoría: ${info.category}\n- Tamaño: ${info.size}\n- Versión: ${info.version}\n- Descripción: ${info.description}`;
        }
    }

    // Ayuda general
    return `Puedo ayudarte con:
- Búsqueda de programas
- Información sobre categorías
- Cambio de tema claro/oscuro
- Detalles de programas específicos
- Ordenamiento y filtrado

¿Qué te gustaría saber?`;
}

server.on('connection', (ws) => {
    console.log('Nueva conexión establecida');

    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message);
            
            if (data.type === 'query') {
                const response = processQuery(data.text);
                ws.send(JSON.stringify({
                    type: 'response',
                    text: response
                }));
            }
        } catch (error) {
            console.error('Error:', error);
            ws.send(JSON.stringify({
                type: 'response',
                text: 'Lo siento, ha ocurrido un error al procesar tu pregunta.'
            }));
        }
    });

    ws.on('error', (error) => {
        console.error('WebSocket error:', error);
    });
});

console.log('Servidor WebSocket iniciado en puerto 8080');

app.get('/download/:filename', async (req, res) => {
    try {
        const url = await storageManager.getSignedUrl(req.params.filename);
        res.json({ downloadUrl: url });
    } catch (error) {
        res.status(500).json({ error: 'Error al generar enlace de descarga' });
    }
});

app.listen(port, () => {
    console.log(`Servidor corriendo en puerto ${port}`);
});