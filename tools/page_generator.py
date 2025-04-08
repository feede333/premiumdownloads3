import json
import os
from datetime import datetime

class PageGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, "data")
        self.subpages_dir = os.path.join(self.base_dir, "subpages")
        
        # Crear directorio de subpáginas si no existe
        os.makedirs(self.subpages_dir, exist_ok=True)

    def load_programs(self):
        json_path = os.path.join(self.data_dir, "programs.json")
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate_program_card(self, program):
        return f"""
        <div class="program-card">
            <img src="{program['image']}" alt="{program['title']}">
            <h3>{program['title']}</h3>
            <p class="category">{program['category']}</p>
            <p class="description">{program['description']}</p>
            <div class="requirements">
                <p><strong>OS:</strong> {program['requirements']['os']}</p>
                <p><strong>RAM:</strong> {program['requirements']['ram']}</p>
                <p><strong>Size:</strong> {program['fileSize']}</p>
            </div>
            <p class="date">Added: {program['date']}</p>
        </div>
        """

    def generate_year_page(self, year, programs):
        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Downloads {year}</title>
    <link rel="stylesheet" href="{year}.css">
</head>
<body>
    <header>
        <h1>Premium Downloads {year}</h1>
        <nav>
            <a href="../index.html">Home</a>
            <a href="2023.html">2023</a>
            <a href="2024.html">2024</a>
            <a href="2025.html">2025</a>
        </nav>
    </header>
    
    <main class="programs-grid">
        {''.join(self.generate_program_card(program) for program in programs)}
    </main>

    <footer>
        <p>&copy; {year} Premium Downloads. All rights reserved.</p>
    </footer>
</body>
</html>
        """
        
        # Guardar archivo HTML
        with open(os.path.join(self.subpages_dir, f"{year}.html"), 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Generar CSS si no existe
        css_path = os.path.join(self.subpages_dir, f"{year}.css")
        if not os.path.exists(css_path):
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(self.get_default_css())

    def get_default_css(self):
        return """
/* Estilos generales */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f0f0f0;
}

header {
    background-color: #333;
    color: white;
    padding: 1rem;
    text-align: center;
}

nav {
    margin-top: 1rem;
}

nav a {
    color: white;
    text-decoration: none;
    margin: 0 1rem;
}

/* Grid de programas */
.programs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
    padding: 2rem;
}

/* Tarjetas de programa */
.program-card {
    background: white;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.program-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 4px;
}

.program-card h3 {
    margin: 1rem 0;
    color: #333;
}

.category {
    color: #666;
    font-style: italic;
}

.requirements {
    background: #f9f9f9;
    padding: 1rem;
    border-radius: 4px;
    margin: 1rem 0;
}

.date {
    color: #999;
    font-size: 0.9rem;
    text-align: right;
}

/* Footer */
footer {
    background: #333;
    color: white;
    text-align: center;
    padding: 1rem;
    margin-top: 2rem;
}
        """

    def update_pages(self):
        # Cargar programas
        data = self.load_programs()
        programs = data.get('programs', [])

        # Organizar programas por año
        programs_by_year = {}
        for program in programs:
            year = datetime.strptime(program['date'], '%d.%m.%Y').year
            if year not in programs_by_year:
                programs_by_year[year] = []
            programs_by_year[year].append(program)

        # Generar páginas para cada año
        for year, year_programs in programs_by_year.items():
            self.generate_year_page(year, year_programs)

if __name__ == "__main__":
    generator = PageGenerator()
    generator.update_pages()
    print("✅ Páginas actualizadas correctamente")