import json
import os
from datetime import datetime
from bs4 import BeautifulSoup

class PageGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.frontend_dir = os.path.join(self.base_dir, 'frontend', 'public')
        self.data_dir = os.path.join(self.frontend_dir, 'data')

    def load_programs(self):
        json_path = os.path.join(self.data_dir, "programs.json")
        print(f"Loading programs from: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Loaded {len(data.get('programs', []))} programs")
            return data

    def generate_program_card(self, program):
        return f"""
        <div class="download-card">
            <div class="card-image">
                <img src="{program['image']}" alt="{program['title']}">
            </div>
            <div class="card-content">
                <h3 class="card-title">{program['title']}</h3>
                <span class="category-badge">{program['category']}</span>
                <div class="card-meta">
                    <span>{program.get('fileSize', '')}</span>
                    <span>{program.get('version', '')}</span>
                </div>
                <a href="detail.html?id={program['id']}" class="download-button">Ver detalles</a>
            </div>
        </div>
        """

    def update_index_page(self, programs):
        index_path = os.path.join(self.frontend_dir, 'index.html')
        print(f"Updating programs in: {index_path}")

        # Leer el archivo HTML existente
        with open(index_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Encontrar el contenedor de programas
        programs_grid = soup.find(id='programsGrid')
        if not programs_grid:
            print("❌ Error: No se encontró el contenedor #programsGrid")
            return False

        # Limpiar el contenedor existente
        programs_grid.clear()

        # Agregar las nuevas tarjetas de programa
        for program in programs:
            card_html = self.generate_program_card(program)
            card_soup = BeautifulSoup(card_html, 'html.parser')
            programs_grid.append(card_soup)

        # Guardar el archivo actualizado
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print("✅ Index page updated successfully")
        return True

    def update_pages(self):
        try:
            # Cargar programas
            data = self.load_programs()
            programs = data.get('programs', [])

            # Actualizar index.html
            if not self.update_index_page(programs):
                return False

            print("✅ All pages updated successfully")
            return True

        except Exception as e:
            print(f"❌ Error updating pages: {str(e)}")
            return False

if __name__ == "__main__":
    generator = PageGenerator()
    generator.update_pages()