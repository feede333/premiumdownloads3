import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class VersionManager:
    def __init__(self):
        self.base_path = r"c:\Users\Federico\Downloads\downloads site\premiumdownloads2"
        self.programs_path = os.path.join(self.base_path, "programs")
        self.subpages_path = os.path.join(self.base_path, "subpages")
        
        # Crear directorios base si no existen
        os.makedirs(self.programs_path, exist_ok=True)
        os.makedirs(self.subpages_path, exist_ok=True)

    def validate_program_name(self, program_name):
        """Valida que el nombre del programa no tenga caracteres especiales"""
        import re
        if not program_name or not program_name.strip():
            messagebox.showerror("Error", "El nombre del programa no puede estar vacío")
            return False
        
        if not re.match("^[a-zA-Z0-9\s-]+$", program_name):
            messagebox.showerror("Error", "El nombre del programa solo puede contener letras, números, espacios y guiones")
            return False
        return True

    def create_program_structure(self, program_name):
        """Crea la estructura inicial para un nuevo programa"""
        # Validar nombre del programa
        if not self.validate_program_name(program_name):
            return False

        # Normalizar el nombre del programa para usarlo en rutas
        program_id = program_name.lower().replace(' ', '-')
        
        try:
            # 1. Crear carpeta específica del programa en subpages
            program_subpages = os.path.join(self.subpages_path, program_id)
            os.makedirs(program_subpages, exist_ok=True)
            
            # 2. Crear archivo details específico del programa
            details_path = os.path.join(self.programs_path, f"{program_id}-details.html")
            self.create_details_file(program_name, program_id)
            
            print(f"\n✅ Estructura creada para {program_name}:")
            print(f"  📁 Carpeta: {program_subpages}")
            print(f"  📄 Details: {details_path}\n")
            
            return program_id
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la estructura: {str(e)}")
            return False

    def create_details_file(self, program_name, program_id):
        """Crea el archivo details.html específico para el programa"""
        details_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{program_name} - Detalles | PremiumDownloads</title>
    <link rel="stylesheet" href="../css/csscomun.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
    <header>
        <div class="container header-content">
            <a href="../index.html" class="logo">
                <span>⬇️</span>
                <span>PremiumDownloads</span>
            </a>
            <nav>
                <ul>
                    <li><a href="../index.html">Inicio</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <div class="container">
        <div class="download-versions">
            <h3 class="versions-title">Versiones de {program_name}</h3>
            <ul class="version-years">
                <!-- AÑOS-START -->
                <!-- Las versiones se insertarán aquí -->
                <!-- AÑOS-END -->
            </ul>
        </div>
    </div>

    <footer>
        <div class="container">
            <div class="footer-links">
                <a href="#">Términos de uso</a>
                <a href="#">Política de privacidad</a>
                <a href="#">DMCA</a>
                <a href="#">Contacto</a>
            </div>
            <p>© {datetime.now().year} PremiumDownloads. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>"""
        
        details_path = os.path.join(self.programs_path, f"{program_id}-details.html")
        with open(details_path, "w", encoding="utf-8") as file:
            file.write(details_content)

    def create_html_file(self, program_name, year):
        """Crea un archivo HTML de versiones para el año especificado"""
        program_id = program_name.lower().replace(' ', '-')
        program_path = os.path.join(self.subpages_path, program_id)
        file_name = f"{year}.html"
        file_path = os.path.join(program_path, file_name)

        if os.path.exists(file_path):
            return False

        base_html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{program_name} {year} - Versiones</title>
    <link rel="stylesheet" href="../../css/csscomun.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
    <header>
        <div class="container header-content">
            <a href="../../index.html" class="logo">
                <span>⬇️</span>
                <span>PremiumDownloads</span>
            </a>
            <nav>
                <ul>
                    <li><a href="../../index.html">Inicio</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <div class="container">
        <a href="../../programs/{program_id}-details.html" class="back-link">
            <i class="fa fa-arrow-left"></i> Volver a detalles
        </a>

        <div class="download-detail">
            <h2>Versiones de {year}</h2>
            
            <div class="version-list">
                <!-- Las versiones se cargarán dinámicamente -->
            </div>

            <div class="torrent-note">
                <p><i class="fas fa-info-circle"></i> Para usar estos enlaces necesitas:</p>
                <ul>
                    <li>• qBittorrent (Recomendado)</li>
                    <li>• uTorrent</li>
                    <li>• BitTorrent</li>
                </ul>
            </div>
        </div>
    </div>

    <footer>
        <div class="container">
            <div class="footer-links">
                <a href="#">Términos de uso</a>
                <a href="#">Política de privacidad</a>
                <a href="#">DMCA</a>
                <a href="#">Contacto</a>
            </div>
            <p>© {year} PremiumDownloads. Todos los derechos reservados.</p>
        </div>
    </footer>

    <script>
    document.addEventListener('DOMContentLoaded', () => {{
        const data = {{
            "versions": []
        }};
        const versionList = document.querySelector('.version-list');
        versionList.innerHTML = data.versions.map(version => `
            <div class="version-item">
                <div class="version-info">
                    <h3 class="version-name">${{version.version}}</h3>
                    <span class="version-date">${{version.date}}</span>
                    <span class="file-size">${{version.size}}</span>
                </div>
                <div class="download-container">
                    <div class="download-options">
                        <a href="${{version.magnetLink}}" class="magnet-button">
                            <i class="fas fa-magnet"></i>
                            <span>Magnet</span>
                        </a>
                        <a href="${{version.torrentLink}}" class="torrent-button" target="_blank">
                            <i class="fas fa-download"></i>
                            <span>Torrent</span>
                        </a>
                    </div>
                    <div class="torrent-stats">
                        <div class="peer-info">
                            <span class="seeds-indicator"></span>
                            <span>Seeds: ${{version.seeds}}</span>
                        </div>
                        <div class="peer-info">
                            <span class="peers-indicator"></span>
                            <span>Peers: ${{version.peers}}</span>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }});
    </script>
</body>
</html>"""

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(base_html_content)

        # Actualizar el archivo details del programa
        self.update_program_details(program_id)
        return True

    def list_html_files(self, program_id):
        program_path = os.path.join(self.subpages_path, program_id)
        files = [f for f in os.listdir(program_path) if f.endswith(".html")]
        return files

    def read_versions_from_html(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                
            # Buscar el array de versiones en el contenido
            start = content.find('"versions": [') + len('"versions": [')
            end = content.find(']', start)
            versions_json = content[start:end].strip()
            
            if not versions_json:
                return []  # Retorna lista vacía si no hay versiones
                
            try:
                return json.loads(f"[{versions_json}]")
            except json.JSONDecodeError:
                return []  # Retorna lista vacía si hay error al decodificar JSON
                
        except Exception as e:
            # Solo mostrar error si no es un archivo recién creado
            if os.path.getsize(file_path) > 0:
                messagebox.showerror("Error", f"Error al leer las versiones: {str(e)}")
            return []

    def save_versions_to_html(self, file_path, versions):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            start = content.find('"versions": [') + len('"versions": [')
            end = content.find(']', start)
            
            new_content = (
                content[:start] + 
                "\n    " + 
                json.dumps(versions, indent=4)[1:-1] + 
                "\n" + 
                content[end:]
            )
            
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(new_content)
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar las versiones: {str(e)}")
            return False

    def delete_html_file(self, file_path, filename):
        try:
            os.remove(file_path)
            # Actualizar el archivo details del programa después de eliminar
            program_id = filename.split('-')[0]
            self.update_program_details(program_id)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el archivo: {str(e)}")
            return False

    def delete_program(self, program_id):
        """Elimina un programa completo (carpeta y details)"""
        try:
            # Eliminar carpeta en subpages
            program_path = os.path.join(self.subpages_path, program_id)
            if os.path.exists(program_path):
                import shutil
                shutil.rmtree(program_path)

            # Eliminar archivo details
            details_path = os.path.join(self.programs_path, f"{program_id}-details.html")
            if os.path.exists(details_path):
                os.remove(details_path)

            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el programa: {str(e)}")
            return False

    def update_program_details(self, program_id):
        """Actualiza el archivo details.html del programa con los enlaces a los archivos de años disponibles"""
        details_path = os.path.join(self.programs_path, f"{program_id}-details.html")
        program_path = os.path.join(self.subpages_path, program_id)
        
        try:
            # Obtener lista de años ordenados de manera descendente
            years = sorted([f.replace('.html', '') for f in os.listdir(program_path) 
                           if f.endswith('.html')], key=int, reverse=True)
            
            # Leer el contenido actual del archivo details.html
            with open(details_path, "r", encoding="utf-8") as file:
                content = file.read()
                
            # Encontrar la sección donde se insertan los años
            start_marker = '<!-- AÑOS-START -->'
            end_marker = '<!-- AÑOS-END -->'
            start = content.find(start_marker)
            end = content.find(end_marker)
            
            if start == -1 or end == -1:
                messagebox.showerror("Error", "No se encontraron los marcadores en el archivo details.html")
                return False
            
            # Generar el nuevo contenido HTML para los años
            years_html = []
            for year in years:
                # Contar versiones para este año
                file_path = os.path.join(program_path, f"{year}.html")
                versions = self.read_versions_from_html(file_path)
                version_count = len(versions)
                
                years_html.append(f'''
                            <li class="year-item">
                                <a href="./{program_id}/{year}.html" class="year-link">
                                    <span class="year">{year}</span>
                                    <span class="version-count">({version_count} versiones)</span>
                                    <i class="fas fa-chevron-right"></i>
                                </a>
                            </li>''')
            
            # Insertar el nuevo contenido
            new_content = (
                content[:start + len(start_marker)] + 
                '\n' + 
                ''.join(years_html) + 
                '\n                        ' +
                content[end:]
            )
            
            # Guardar los cambios
            with open(details_path, "w", encoding="utf-8") as file:
                file.write(new_content)
                
            return True
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el archivo details.html: {str(e)}")
            return False

    def log_change(self, action, details):
        """Registra cambios en un archivo de log"""
        log_path = os.path.join(self.base_path, "changes.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_path, "a", encoding="utf-8") as log:
            log.write(f"[{timestamp}] {action}: {details}\n")

class VersionManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Versiones")
        self.root.geometry("800x600")
        
        self.manager = VersionManager()
        
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        header = ttk.Label(self.root, text="Gestor de Versiones", style='Header.TLabel')
        header.pack(pady=20)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        ttk.Button(main_frame, text="Crear Nuevo Programa", 
                  command=self.show_create_program_dialog).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Seleccionar Programa Existente", 
                  command=self.show_select_program_dialog).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Salir", 
                  command=self.root.quit).pack(fill='x', pady=5)

    def show_create_program_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Crear Nuevo Programa")
        dialog.geometry("400x200")
        dialog.grab_set()

        ttk.Label(dialog, text="Ingresa el nombre del programa:").pack(pady=20)
        program_entry = ttk.Entry(dialog)
        program_entry.pack(pady=5)

        def create_program():
            program_name = program_entry.get()
            if not self.manager.validate_program_name(program_name):
                return
            program_id = self.manager.create_program_structure(program_name)
            messagebox.showinfo("Éxito", f"Programa {program_name} creado correctamente.")
            dialog.destroy()
            self.show_program_management(program_id)

        ttk.Button(dialog, text="Crear", command=create_program).pack(pady=20)

    def show_select_program_dialog(self):
        programs = [f.replace('-details.html', '') for f in os.listdir(self.manager.programs_path) if f.endswith("-details.html")]
        if not programs:
            messagebox.showwarning("Aviso", "No se encontraron programas.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Seleccionar Programa Existente")
        dialog.geometry("500x400")
        dialog.grab_set()

        ttk.Label(dialog, text="Selecciona un programa:", style='Header.TLabel').pack(pady=20)
        
        listbox = tk.Listbox(dialog)
        listbox.pack(fill='both', expand=True, padx=20)
        
        for program in sorted(programs):
            listbox.insert('end', program)

        def select_program():
            if not listbox.curselection():
                messagebox.showwarning("Aviso", "Por favor selecciona un programa.")
                return
                
            program_id = listbox.get(listbox.curselection()[0])
            dialog.destroy()
            self.show_program_management(program_id)

        ttk.Button(dialog, text="Seleccionar", command=select_program).pack(pady=20)

    def show_program_management(self, program_id):
        for widget in self.root.winfo_children():
            widget.destroy()

        header = ttk.Label(self.root, text=f"Gestión de Programa - {program_id}", 
                          style='Header.TLabel')
        header.pack(pady=20)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        ttk.Button(main_frame, text="Agregar Año", 
                  command=lambda: self.show_add_year_dialog(program_id)).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Eliminar Año", 
                  command=lambda: self.show_remove_year_dialog(program_id)).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Listar Años", 
                  command=lambda: self.show_list_years(program_id)).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Vista Previa Details", 
                  command=lambda: self.show_details_preview(program_id.replace('-', ' ').title(), program_id)).pack(fill='x', pady=5)
        ttk.Button(main_frame, text="Eliminar Programa", 
                  command=lambda: self.delete_program_dialog(program_id)).pack(fill='x', pady=5)
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        ttk.Button(main_frame, text="Volver al menú principal", 
                  command=self.create_main_menu).pack(fill='x', pady=5)

    def show_add_year_dialog(self, program_id):
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Nuevo Año")
        dialog.geometry("400x200")
        dialog.grab_set()

        ttk.Label(dialog, text="Ingresa el año para el nuevo archivo:").pack(pady=20)
        year_entry = ttk.Entry(dialog)
        year_entry.pack(pady=5)

        def add_year():
            year = year_entry.get()
            program_name = program_id.replace('-', ' ').title()
            if self.manager.create_html_file(program_name, year):
                messagebox.showinfo("Éxito", f"Año {year} agregado correctamente.")
                dialog.destroy()

        ttk.Button(dialog, text="Agregar", command=add_year).pack(pady=20)

    def show_remove_year_dialog(self, program_id):
        years = self.manager.list_html_files(program_id)
        if not years:
            messagebox.showinfo("Info", "No hay años para eliminar")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Eliminar Año")
        dialog.geometry("400x300")
        dialog.grab_set()

        ttk.Label(dialog, text="Selecciona el año a eliminar:").pack(pady=20)
        
        listbox = tk.Listbox(dialog)
        listbox.pack(fill='both', expand=True, padx=20)
        
        for year in years:
            listbox.insert('end', year.replace('.html', ''))

        def remove_year():
            if not listbox.curselection():
                messagebox.showwarning("Aviso", "Por favor selecciona un año")
                return
                
            year = listbox.get(listbox.curselection()[0])
            file_path = os.path.join(self.manager.subpages_path, program_id, f"{year}.html")
            if self.manager.delete_html_file(file_path, f"{year}.html"):
                messagebox.showinfo("Éxito", f"Año {year} eliminado correctamente")
                dialog.destroy()

        ttk.Button(dialog, text="Eliminar", command=remove_year).pack(pady=20)

    def show_list_years(self, program_id):
        dialog = tk.Toplevel(self.root)
        dialog.title("Lista de Años")
        dialog.geometry("400x300")

        listbox = tk.Listbox(dialog)
        listbox.pack(fill='both', expand=True, padx=20, pady=20)

        years = self.manager.list_html_files(program_id)
        for year in years:
            listbox.insert('end', year.replace('.html', ''))

        ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)

    def delete_program_dialog(self, program_id):
        confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el programa {program_id}?")
        if confirm:
            if self.manager.delete_program(program_id):
                messagebox.showinfo("Éxito", f"Programa {program_id} eliminado correctamente.")
                self.create_main_menu()

    def show_details_preview(self, program_name, program_id):
        """Muestra una vista previa del archivo details"""
        preview = tk.Toplevel()
        preview.title("Vista Previa Details")
        preview.geometry("600x400")

        text = tk.Text(preview, wrap=tk.WORD)
        text.pack(fill='both', expand=True)

        # Insertar contenido
        details_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{program_name} - Detalles</title>
</head>
<body>
    <h1>{program_name}</h1>
    <div class="versions">
        <!-- AÑOS-START -->
        <!-- Las versiones aparecerán aquí -->
        <!-- AÑOS-END -->
    </div>
</body>
</html>"""

        text.insert('1.0', details_content)
        text.config(state='disabled')

        ttk.Button(preview, text="Cerrar", command=preview.destroy).pack(pady=10)

def main():
    root = tk.Tk()
    app = VersionManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()