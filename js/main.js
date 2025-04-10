document.addEventListener('DOMContentLoaded', () => {
    // Elementos del DOM
    const searchInput = document.querySelector('.search-input');
    const searchButton = document.querySelector('.search-button');
    const downloadCards = document.querySelectorAll('.download-card');
    const downloadGrid = document.querySelector('.download-grid');

    // Actualizar la función de búsqueda
    function searchPrograms(searchTerm) {
        searchTerm = searchTerm.toLowerCase().trim();
        let hasResults = false;

        // Limpiar el grid antes de mostrar resultados
        downloadGrid.innerHTML = '';
        
        // Filtrar y mostrar las cards originales
        downloadCards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            const category = card.querySelector('.category-badge').textContent.toLowerCase();
            const meta = card.querySelector('.card-meta').textContent.toLowerCase();
            
            const matches = title.includes(searchTerm) || 
                          category.includes(searchTerm) || 
                          meta.includes(searchTerm);
            
            if (matches) {
                // Clonar la card para no modificar la original
                const clonedCard = card.cloneNode(true);
                downloadGrid.appendChild(clonedCard);
                hasResults = true;
            }
        });

        // Mostrar mensaje de no resultados
        showNoResultsMessage(!hasResults);

        // Importante: Resetear el índice del scroll infinito
        currentIndex = 0;
    }

    // Función para mensaje de no resultados
    function showNoResultsMessage(show) {
        let message = document.querySelector('.no-results-message');
        
        if (!message && show) {
            message = document.createElement('div');
            message.className = 'no-results-message';
            message.style.cssText = `
                text-align: center;
                padding: 2rem;
                color: var(--text-secondary);
                width: 100%;
                grid-column: 1/-1;
            `;
            message.textContent = 'No se encontraron resultados';
            downloadGrid.appendChild(message);
        }
        
        if (message) {
            message.style.display = show ? 'block' : 'none';
        }
    }

    // Event listeners
    if (searchInput && searchButton) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value;
            if (searchButton) searchButton.disabled = !searchTerm.trim();
            searchPrograms(searchTerm);
        });

        searchButton.addEventListener('click', () => {
            const searchTerm = searchInput.value;
            if (searchTerm.trim()) {
                searchPrograms(searchTerm);
            }
        });

        // Prevenir envío del formulario si existe
        const searchForm = searchInput.closest('form');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
            });
        }
    }

    // Filtrado por categorías
    const categoryLinks = document.querySelectorAll('.category-link');

    categoryLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault(); // Prevenir el scroll
            
            // Remover clase active de todos los links
            categoryLinks.forEach(cat => cat.classList.remove('active'));
            // Agregar clase active al link clickeado
            link.classList.add('active');

            const selectedCategory = link.getAttribute('data-category');

            downloadCards.forEach(card => {
                const cardCategory = card.querySelector('.category-badge')
                    .textContent.toLowerCase();
                
                if (selectedCategory === 'all') {
                    card.style.display = 'flex';
                } else {
                    card.style.display = cardCategory === selectedCategory.toLowerCase() 
                        ? 'flex' 
                        : 'none';
                }
            });

            // Ocultar mensaje de "no results" si estaba visible
            const noResults = document.querySelector('.no-results-message');
            if (noResults) {
                noResults.style.display = 'none';
            }
        });
    });

    // Modo nocturno
    const themeToggle = document.querySelector('.theme-toggle');
    const html = document.documentElement;
    
    // Cargar tema guardado
    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    themeToggle?.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        const icon = themeToggle.querySelector('i');
        if (icon) {
            icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }

    // Ordenamiento
    const sortSelect = document.querySelector('.sort-select');

    sortSelect?.addEventListener('change', () => {
        const cards = Array.from(document.querySelectorAll('.download-card'));
        const sortBy = sortSelect.value;

        cards.sort((a, b) => {
            switch(sortBy) {
                case 'recent':
                    const dateA = a.querySelector('.file-date')?.textContent || '';
                    const dateB = b.querySelector('.file-date')?.textContent || '';
                    return new Date(dateB) - new Date(dateA);
                
                case 'downloads':
                    const downloadsA = parseInt(a.querySelector('.card-meta')?.textContent.match(/\d+/)[0] || '0');
                    const downloadsB = parseInt(b.querySelector('.card-meta')?.textContent.match(/\d+/)[0] || '0');
                    return downloadsB - downloadsA;
                
                case 'name':
                    const nameA = a.querySelector('h3')?.textContent.toLowerCase() || '';
                    const nameB = b.querySelector('h3')?.textContent.toLowerCase() || '';
                    return nameA.localeCompare(nameB);
                
                default:
                    return 0;
            }
        });

        // Limpiar y reinsertar cards ordenadas
        downloadGrid.innerHTML = '';
        cards.forEach(card => downloadGrid.appendChild(card));
    });

    // Agregar scroll infinito
    let isLoading = false;
    let page = 1;

    // Desactivar el scroll infinito durante la búsqueda
    window.addEventListener('scroll', () => {
        const {scrollTop, scrollHeight, clientHeight} = document.documentElement;
        
        // Solo cargar más programas si no hay término de búsqueda activo
        if (scrollTop + clientHeight >= scrollHeight - 5 && !isLoading && 
            (!searchInput.value.trim() || searchInput.value.trim() === '')) {
            loadMorePrograms();
        }
    });

    // Array de programas predefinidos
    const additionalPrograms = [
        {
            image: 'images/photoshop.png',
            title: 'Adobe Photoshop 2024',
            category: 'Design',
            size: '2.8 GB',
            downloads: '2.3K'
        },
        {
            image: 'images/premiere.png',
            title: 'Adobe Premiere Pro 2024',
            category: 'Video',
            size: '3.5 GB',
            downloads: '1.8K'
        },
        {
            image: 'images/vegas.png',
            title: 'VEGAS Pro 21',
            category: 'Video',
            size: '1.2 GB',
            downloads: '950'
        }
        // Agrega más programas aquí
    ];

    let currentIndex = 0;

    async function loadMorePrograms() {
        if (currentIndex >= additionalPrograms.length) {
            // No hay más programas para cargar
            return;
        }

        isLoading = true;
        
        // Agregar indicador de carga
        const loadingIndicator = document.createElement('div');
        loadingIndicator.className = 'loading-indicator';
        loadingIndicator.innerHTML = `
            <div class="spinner"></div>
            <span>Cargando más programas...</span>
        `;
        document.querySelector('.download-grid').appendChild(loadingIndicator);

        try {
            // Simular carga
            await new Promise(resolve => setTimeout(resolve, 800));
            
            // Cargar los siguientes 3 programas (o menos si no hay suficientes)
            const programsToLoad = additionalPrograms.slice(currentIndex, currentIndex + 3);
            
            // Agregar los programas al grid
            programsToLoad.forEach(program => {
                const card = createProgramCard(program);
                document.querySelector('.download-grid').appendChild(card);
            });

            currentIndex += 3;

        } catch (error) {
            console.error('Error cargando más programas:', error);
        } finally {
            // Eliminar indicador de carga
            loadingIndicator.remove();
            isLoading = false;
        }
    }

    function createProgramCard(program) {
        const card = document.createElement('div');
        card.className = 'download-card';
        card.innerHTML = `
            <div class="card-image">
                <img src="${program.image}" alt="${program.title}">
            </div>
            <div class="card-content">
                <h3 class="card-title">${program.title}</h3>
                <span class="category-badge">${program.category}</span>
                <div class="card-meta">
                    <span>${program.size}</span>
                    <span>${program.downloads} descargas</span>
                </div>
                <a href="detail.html" class="download-button">Ver detalles</a>
            </div>
        `;
        return card;
    }

    // Agregar al archivo JavaScript existente
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.menu-overlay');

    menuToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    overlay.addEventListener('click', function() {
        menuToggle.classList.remove('active');
        sidebar.classList.remove('active');
        this.classList.remove('active');
    });
});

