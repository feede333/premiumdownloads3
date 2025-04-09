const fs = require('fs');
const path = require('path');

const [,, version, date, size, torrentLink, magnetLink, seeds, peers] = process.argv;

const jsonPath = path.join(__dirname, 'data', 'versions.json');

// Leer el archivo JSON existente
let versionsData = { versions: [] };
if (fs.existsSync(jsonPath)) {
    const fileContent = fs.readFileSync(jsonPath, 'utf8');
    versionsData = JSON.parse(fileContent);
}

// Agregar nueva versión
const newVersion = {
    version,
    date,
    size,
    torrentLink,
    magnetLink,
    seeds,
    peers
};

versionsData.versions.unshift(newVersion); // Agregar al inicio del array

// Guardar el archivo JSON
fs.writeFileSync(jsonPath, JSON.stringify(versionsData, null, 2));