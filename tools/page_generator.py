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
        print(f"Loading programs from: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Loaded {len(data.get('programs', []))} programs")
            return data

    def generate_program_card(self, program):
        return f"""
        <div class="program-card">
            <img src="{program['image']}" alt="{program['title']}">
            <h3>{program['title']}</h3>
            <p class="category">{program['category']}</p>
            <p class="description">{program.get('description', '')}</p>
            <div class="requirements">
                <p><strong>OS:</strong> {program.get('requirements', {}).get('os', '')}</p>
                <p><strong>RAM:</strong> {program.get('requirements', {}).get('ram', '')}</p>
                <p><strong>Size:</strong> {program.get('fileSize', '')}</p>
            </div>
            <p class="date">Added: {program.get('date', '')}</p>
        </div>
        """

    def generate_year_page(self, year, programs):
        print(f"Generating page for year {year} with {len(programs)} programs")
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
        html_path = os.path.join(self.subpages_dir, f"{year}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Generated HTML file: {html_path}")

        # Generar CSS si no existe
        css_path = os.path.join(self.subpages_dir, f"{year}.css")
        if not os.path.exists(css_path):
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(self.get_default_css())
            print(f"Generated CSS file: {css_path}")

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

    def generate_index_page(self):
        print("Generating index page")
        html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Downloads</title>
    <link rel="stylesheet" href="subpages/2025.css">
</head>
<body>
    <header>
        <h1>Premium Downloads</h1>
        <nav>
            <a href="subpages/2023.html">2023</a>
            <a href="subpages/2024.html">2024</a>
            <a href="subpages/2025.html">2025</a>
        </nav>
    </header>
    
    <main>
        <h2>Bienvenido a Premium Downloads</h2>
        <p>Selecciona un año para ver los programas disponibles.</p>
    </main>

    <footer>
        <p>&copy; 2025 Premium Downloads. All rights reserved.</p>
    </footer>
</body>
</html>
        """
        
        # Guardar archivo HTML
        index_path = os.path.join(self.base_dir, "index.html")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Generated index file: {index_path}")

    def update_pages(self):
        try:
            # Cargar programas
            data = self.load_programs()
            programs = data.get('programs', [])

            # Organizar programas por año
            programs_by_year = {}
            for program in programs:
                try:
                    year = datetime.strptime(program['date'], '%d.%m.%Y').year
                    if year not in programs_by_year:
                        programs_by_year[year] = []
                    programs_by_year[year].append(program)
                except (ValueError, KeyError) as e:
                    print(f"Error processing program {program.get('title', 'unknown')}: {str(e)}")

            # Generar páginas para cada año
            for year, year_programs in programs_by_year.items():
                self.generate_year_page(year, year_programs)

            # Generar página de índice
            self.generate_index_page()

            print("✅ All pages generated successfully")
            return True
        except Exception as e:
            print(f"❌ Error generating pages: {str(e)}")
            return False

if __name__ == "__main__":
    generator = PageGenerator()
    generator.update_pages()