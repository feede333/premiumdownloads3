async function loadPrograms() {
    try {
        console.log('Iniciando carga de programas...');
        const response = await fetch('./data/programs.json'); 
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Datos cargados:', data);

        const programsGrid = document.getElementById('dynamicProgramsGrid');
        if (!programsGrid) {
            console.error('No se encontró el elemento dynamicProgramsGrid');
            return;
        }

        // Empezar con Avast (que ya está en el HTML)
        programsGrid.innerHTML = ''; // Limpiar grid

        // Agregar los programas dinámicos
        data.programs.forEach(program => {
            const programCard = document.createElement('div');
            programCard.className = 'download-card';
            programCard.innerHTML = `
                <div class="card-image">
                    <img src="./images/${program.id}.png" alt="${program.title}">
                </div>
                <div class="card-content">
                    <h3 class="card-title">${program.title}</h3>
                    <span class="category-badge">${program.category}</span>
                    <div class="card-meta">
                        <span>${program.fileSize}</span>
                        <span>${program.version || ''}</span>
                    </div>
                    <p class="program-description">${program.description.substring(0, 100)}...</p>
                    <a href="./detail.html?id=${program.id}" class="download-button">Ver detalles</a>
                </div>
            `;
            programsGrid.appendChild(programCard);
        });

        console.log('Programas cargados exitosamente');
    } catch (error) {
        console.error('Error cargando programas:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadPrograms);