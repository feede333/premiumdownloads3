async function loadPrograms() {
    try {
        console.log('Intentando cargar programas...'); // Debug
        
        // Usar ruta relativa
        const response = await fetch('./data/programs.json');
        console.log('Response status:', response.status); // Debug
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Datos cargados:', data); // Debug

        const programsGrid = document.getElementById('programsGrid');
        if (!programsGrid) {
            throw new Error('No se encontró el elemento programsGrid');
        }

        // Limpiar el grid
        programsGrid.innerHTML = '';

        data.programs.forEach(program => {
            const programCard = document.createElement('div');
            programCard.className = 'program-card';
            
            programCard.innerHTML = `
                <a href="detail.html?id=${program.id}">
                    <img src="${program.image}" alt="${program.title}">
                    <div class="program-info">
                        <h3>${program.title}</h3>
                        <span class="category">${program.category}</span>
                        <div class="meta">
                            <span class="size">${program.fileSize}</span>
                            <span class="date">${program.date}</span>
                        </div>
                    </div>
                </a>
            `;
            programsGrid.appendChild(programCard);
        });
    } catch (error) {
        console.error('Error cargando programas:', error);
        const programsGrid = document.getElementById('programsGrid');
        if (programsGrid) {
            programsGrid.innerHTML = `<p class="error">Error cargando programas: ${error.message}</p>`;
        }
    }
}

// Cargar programas cuando el documento esté listo
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM cargado, iniciando carga de programas...'); // Debug
    loadPrograms();
});