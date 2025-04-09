async function loadPrograms() {
    try {
        const response = await fetch('/premiumdownloads3/data/programs.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Datos cargados:', data);

        const programsGrid = document.getElementById('programsGrid');
        if (!programsGrid) {
            console.error('No se encontró el elemento programsGrid');
            return;
        }

        // Limpiar grid existente
        programsGrid.innerHTML = '';

        data.programs.forEach(program => {
            const programCard = document.createElement('div');
            programCard.className = 'download-card';
            programCard.innerHTML = `
                <div class="card-image">
                    <img src="${program.image}" alt="${program.title}">
                </div>
                <div class="card-content">
                    <h3 class="card-title">${program.title}</h3>
                    <span class="category-badge">${program.category}</span>
                    <div class="card-meta">
                        <span>${program.fileSize}</span>
                        <span>${program.version || ''}</span>
                    </div>
                    <a href="/premiumdownloads3/detail.html?id=${program.id}" class="download-button">Ver detalles</a>
                </div>
            `;
            programsGrid.appendChild(programCard);
        });
    } catch (error) {
        console.error('Error cargando programas:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadPrograms);